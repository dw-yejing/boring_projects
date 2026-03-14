from lark import Lark, Transformer
import json


grammar = r"""
?start: expr

?expr: expr OR term   -> or_expr
     | term

?term: term AND factor -> and_expr
     | factor

?factor: NOT factor   -> not_expr
       | atom

?atom: field
     | range
     | WORD           -> word
     | PHRASE         -> phrase
     | "(" expr ")"   -> group

# ---------- 字段 ----------
field: FIELD ":" atom

# ---------- 范围 ----------
range: FIELD ":" "[" WORD TO WORD "]"

# ---------- 运算符 ----------
AND: /(?i:and)/
OR: /(?i:or)/
NOT: /(?i:not)/
TO: /(?i:to)/

# ---------- token ----------
#
# FIELD 只在“后面紧跟冒号”时才匹配为字段名，
# 避免把 IPC:(H01M8) 里的 H01M8 错误识别为 FIELD。

FIELD: /[A-Za-z_][A-Za-z0-9_]*(?=\s*:)/ 

WORD: /[^\s()":\[\]]+/

PHRASE: /"[^"]+"/

%import common.WS
%ignore WS
"""

class QueryTransformer(Transformer):

    def __init__(self, default_fields):
        self.default_fields = default_fields

    # -------- 基础词 --------

    def word(self, items):
        text = items[0].value
        return self._multi_match(text)

    def phrase(self, items):
        text = items[0].value.strip('"')
        return self._phrase_match(text)

    def group(self, items):
        return items[0]

    # -------- 字段 --------

    def field(self, items):

        field = items[0].value
        query = items[1]

        return self._apply_field(query, field)

    # -------- range --------

    def range(self, items):

        field = items[0].value
        start = items[1].value
        end = items[3].value

        return {
            "range": {
                field: {
                    "gte": start,
                    "lte": end
                }
            }
        }

    # -------- 逻辑 --------

    def _is_simple_bool_should(self, node):
        if not isinstance(node, dict) or "bool" not in node:
            return False
        b = node["bool"]
        if not isinstance(b, dict):
            return False
        if "should" not in b:
            return False
        # 只合并“纯 should”节点，避免改变更复杂 bool 语义
        for k in b.keys():
            if k not in {"should", "minimum_should_match"}:
                return False
        return b.get("minimum_should_match", 1) == 1 and isinstance(b["should"], list)

    def _is_simple_bool_must(self, node):
        if not isinstance(node, dict) or "bool" not in node:
            return False
        b = node["bool"]
        if not isinstance(b, dict):
            return False
        if "must" not in b:
            return False
        for k in b.keys():
            if k != "must":
                return False
        return isinstance(b["must"], list)

    def and_expr(self, items):

        left = items[0]
        right = items[2]

        must = []
        if self._is_simple_bool_must(left):
            must.extend(left["bool"]["must"])
        else:
            must.append(left)

        if self._is_simple_bool_must(right):
            must.extend(right["bool"]["must"])
        else:
            must.append(right)

        return {"bool": {"must": must}}

    def or_expr(self, items):

        left = items[0]
        right = items[2]

        should = []
        if self._is_simple_bool_should(left):
            should.extend(left["bool"]["should"])
        else:
            should.append(left)

        if self._is_simple_bool_should(right):
            should.extend(right["bool"]["should"])
        else:
            should.append(right)

        return {"bool": {"should": should, "minimum_should_match": 1}}

    def not_expr(self, items):

        expr = items[1]

        return {
            "bool": {
                "must_not": [expr]
            }
        }

    # -------- DSL --------

    def _multi_match(self, text):

        return {
            "multi_match": {
                "query": text,
                "fields": self.default_fields
            }
        }

    def _phrase_match(self, text):

        return {
            "multi_match": {
                "query": text,
                "type": "phrase",
                "fields": self.default_fields
            }
        }

    # -------- 字段递归 --------

    def _apply_field(self, query, field):

        if "multi_match" in query:
            query["multi_match"]["fields"] = [field]

        elif "bool" in query:

            for k in ["must", "should", "must_not"]:

                if k in query["bool"]:

                    query["bool"][k] = [
                        self._apply_field(x, field)
                        for x in query["bool"][k]
                    ]

        return query


class QueryParser:

    def __init__(self, default_fields=None):

        if default_fields is None:
            default_fields = ["title", "keywords"]

        self.default_fields = default_fields

        self.parser = Lark(grammar, parser="lalr")

    def parse(self, query):

        tree = self.parser.parse(query)

        transformer = QueryTransformer(self.default_fields)

        return {
            "query": transformer.transform(tree)
        }


if __name__ == "__main__":

    parser = QueryParser(["title", "keywords", "abstract"])

    q = """
    (("协同过滤" AND "推荐算法")
    OR
    ("协同过滤" AND "推荐系统" AND 算法)
    OR
    ("协同过滤算法"))
    """

    # q="""(( "氢气浓度" OR "氢浓度" OR "浓度衰减" OR "衰减模型"  AND "膜湿度" OR "湿度" OR "加湿" OR "水含量"  AND "泄露率" OR "泄漏率" OR "渗透率" OR "实测"  AND "电堆" OR "燃料电池" OR "电堆寿命" OR "使用寿命"  AND  (IPC:(H01M8) OR IPC:(H01M4)) ) AND ( APD:[20200101 TO 20251231] )) AND (燃料电池)"""

    dsl = parser.parse(q)

    with open("dsl.json", "w", encoding="utf-8") as f:
        json.dump(dsl, f, ensure_ascii=False, indent=2) 
    print("done")