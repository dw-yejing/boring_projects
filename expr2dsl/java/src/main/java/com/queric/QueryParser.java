package com.queric;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

import static com.queric.Token.Type.*;

/**
 * Recursive descent parser: query string → Elasticsearch DSL (Map).
 * Grammar: expr (OR term)* ; term (AND factor)* ; factor = NOT? atom ; atom = field | range | WORD | PHRASE | ( expr ).
 * Flattens consecutive OR into one bool.should, consecutive AND into one bool.must.
 */
public final class QueryParser {

    private final List<String> defaultFields;
    private List<Token> tokens;
    private int index;

    public QueryParser(List<String> defaultFields) {
        this.defaultFields = defaultFields != null && !defaultFields.isEmpty()
            ? defaultFields
            : Arrays.<String>asList("title", "keywords");
    }

    /**
     * Parse query string and return wrapper {@code { "query": <dsl> }}.
     */
    public Map<String, Object> parse(String query) {
        Lexer lexer = new Lexer(query);
        this.tokens = lexer.tokenize();
        this.index = 0;
        Map<String, Object> queryNode = parseExpr();
        if (current().type() != EOF) {
            throw new IllegalArgumentException("Unexpected token at end: " + current());
        }
        Map<String, Object> result = new LinkedHashMap<>();
        result.put("query", queryNode);
        return result;
    }

    private Token current() {
        return index < tokens.size() ? tokens.get(index) : new Token(EOF, "");
    }

    private Token consume(Token.Type expected) {
        Token t = current();
        if (t.type() != expected) {
            throw new IllegalArgumentException("Expected " + expected + ", got " + t);
        }
        index++;
        return t;
    }

    private boolean is(Token.Type type) {
        return current().type() == type;
    }

    // expr : term ( OR term )*
    private Map<String, Object> parseExpr() {
        Map<String, Object> left = parseTerm();
        while (is(OR)) {
            consume(OR);
            Map<String, Object> right = parseTerm();
            left = or(left, right);
        }
        return left;
    }

    // term : factor ( AND factor )*
    private Map<String, Object> parseTerm() {
        Map<String, Object> left = parseFactor();
        while (is(AND)) {
            consume(AND);
            Map<String, Object> right = parseFactor();
            left = and(left, right);
        }
        return left;
    }

    // factor : NOT? atom
    private Map<String, Object> parseFactor() {
        if (is(NOT)) {
            consume(NOT);
            Map<String, Object> child = parseFactor();
            return mustNot(child);
        }
        return parseAtom();
    }

    // atom : field | range | WORD | PHRASE | ( expr )
    private Map<String, Object> parseAtom() {
        if (is(FIELD) && index + 1 < tokens.size()) {
            Token next = tokens.get(index + 1);
            if (next.type() == COLON) {
                if (index + 2 < tokens.size() && tokens.get(index + 2).type() == LBRACK) {
                    return parseRange();
                }
                return parseField();
            }
        }
        if (is(WORD)) {
            String w = consume(WORD).value();
            return multiMatch(w, false);
        }
        if (is(PHRASE)) {
            String p = consume(PHRASE).value();
            return multiMatch(p, true);
        }
        if (is(LPAR)) {
            consume(LPAR);
            Map<String, Object> e = parseExpr();
            consume(RPAR);
            return e;
        }
        throw new IllegalArgumentException("Unexpected atom at: " + current());
    }

    // field : FIELD : atom
    private Map<String, Object> parseField() {
        String field = consume(FIELD).value();
        consume(COLON);
        Map<String, Object> inner = parseAtom();
        return applyField(inner, field);
    }

    // range : FIELD : [ WORD TO WORD ]
    private Map<String, Object> parseRange() {
        String field = consume(FIELD).value();
        consume(COLON);
        consume(LBRACK);
        String start = consume(WORD).value();
        consume(TO);
        String end = consume(WORD).value();
        consume(RBRACK);
        Map<String, Object> rangeInner = new LinkedHashMap<>();
        rangeInner.put("gte", start);
        rangeInner.put("lte", end);
        Map<String, Object> range = new LinkedHashMap<>();
        range.put(field, rangeInner);
        Map<String, Object> result = new LinkedHashMap<>();
        result.put("range", range);
        return result;
    }

    // --- DSL builders (match Python semantics, with flattening) ---

    private Map<String, Object> multiMatch(String text, boolean phrase) {
        Map<String, Object> mm = new LinkedHashMap<>();
        mm.put("query", text);
        mm.put("fields", new ArrayList<>(defaultFields));
        if (phrase) {
            mm.put("type", "phrase");
        }
        Map<String, Object> result = new LinkedHashMap<>();
        result.put("multi_match", mm);
        return result;
    }

    @SuppressWarnings("unchecked")
    private Map<String, Object> applyField(Map<String, Object> query, String field) {
        if (query.containsKey("multi_match")) {
            ((List<String>) ((Map<?, ?>) query.get("multi_match")).get("fields")).clear();
            ((List<String>) ((Map<?, ?>) query.get("multi_match")).get("fields")).add(field);
            return query;
        }
        if (query.containsKey("bool")) {
            Map<String, Object> b = (Map<String, Object>) query.get("bool");
            for (String k : Arrays.asList("must", "should", "must_not")) {
                if (b.containsKey(k)) {
                    List<Map<String, Object>> list = (List<Map<String, Object>>) b.get(k);
                    List<Map<String, Object>> replaced = new ArrayList<>();
                    for (Map<String, Object> x : list) {
                        replaced.add(applyField(copy(x), field));
                    }
                    b.put(k, replaced);
                }
            }
            return query;
        }
        return query;
    }

    private Map<String, Object> copy(Map<String, Object> m) {
        Map<String, Object> out = new LinkedHashMap<>();
        for (Map.Entry<String, Object> e : m.entrySet()) {
            Object v = e.getValue();
            if (v instanceof Map) {
                out.put(e.getKey(), copy((Map<String, Object>) v));
            } else if (v instanceof List) {
                List<?> list = (List<?>) v;
                List<Object> newList = new ArrayList<>();
                for (Object item : list) {
                    if (item instanceof Map) {
                        newList.add(copy((Map<String, Object>) item));
                    } else {
                        newList.add(item);
                    }
                }
                out.put(e.getKey(), newList);
            } else {
                out.put(e.getKey(), v);
            }
        }
        return out;
    }

    private static boolean isSimpleBoolShould(Map<String, Object> node) {
        if (node == null || !node.containsKey("bool")) return false;
        Map<String, Object> b = (Map<String, Object>) node.get("bool");
        if (!b.containsKey("should")) return false;
        for (String k : b.keySet()) {
            if (!k.equals("should") && !k.equals("minimum_should_match")) return false;
        }
        Object msm = b.get("minimum_should_match");
        if (msm instanceof Number && ((Number) msm).intValue() != 1) return false;
        return b.get("should") instanceof List;
    }

    private static boolean isSimpleBoolMust(Map<String, Object> node) {
        if (node == null || !node.containsKey("bool")) return false;
        Map<String, Object> b = (Map<String, Object>) node.get("bool");
        if (!b.containsKey("must")) return false;
        if (b.size() != 1) return false;
        return b.get("must") instanceof List;
    }

    @SuppressWarnings("unchecked")
    private Map<String, Object> or(Map<String, Object> left, Map<String, Object> right) {
        List<Map<String, Object>> should = new ArrayList<>();
        if (isSimpleBoolShould(left)) {
            should.addAll((List<Map<String, Object>>) ((Map<?, ?>) left.get("bool")).get("should"));
        } else {
            should.add(left);
        }
        if (isSimpleBoolShould(right)) {
            should.addAll((List<Map<String, Object>>) ((Map<?, ?>) right.get("bool")).get("should"));
        } else {
            should.add(right);
        }
        Map<String, Object> bool = new LinkedHashMap<>();
        bool.put("should", should);
        bool.put("minimum_should_match", 1);
        Map<String, Object> result = new LinkedHashMap<>();
        result.put("bool", bool);
        return result;
    }

    @SuppressWarnings("unchecked")
    private Map<String, Object> and(Map<String, Object> left, Map<String, Object> right) {
        List<Map<String, Object>> must = new ArrayList<>();
        if (isSimpleBoolMust(left)) {
            must.addAll((List<Map<String, Object>>) ((Map<?, ?>) left.get("bool")).get("must"));
        } else {
            must.add(left);
        }
        if (isSimpleBoolMust(right)) {
            must.addAll((List<Map<String, Object>>) ((Map<?, ?>) right.get("bool")).get("must"));
        } else {
            must.add(right);
        }
        Map<String, Object> bool = new LinkedHashMap<>();
        bool.put("must", must);
        Map<String, Object> result = new LinkedHashMap<>();
        result.put("bool", bool);
        return result;
    }

    private Map<String, Object> mustNot(Map<String, Object> expr) {
        List<Map<String, Object>> mustNot = new ArrayList<>();
        mustNot.add(expr);
        Map<String, Object> bool = new LinkedHashMap<>();
        bool.put("must_not", mustNot);
        Map<String, Object> result = new LinkedHashMap<>();
        result.put("bool", bool);
        return result;
    }
}
