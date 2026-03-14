# Queric (Java)

与 Python 版等价的查询解析器：将查询字符串编译为 Elasticsearch Query DSL。

## 语法

- **逻辑**：`AND`、`OR`、`NOT`（NOT 优先级最高，其次 AND，最后 OR）
- **词**：裸词、`"短语"`
- **字段**：`字段名:(词)` 或 `字段名:("短语")`，例如 `IPC:(H01M8)`
- **范围**：`字段名:[起始 TO 结束]`，例如 `APD:[20200101 TO 20251231]`

## 构建与运行

```bash
cd java
mvn compile
mvn exec:java -q
```

需 **JDK 8+**。输出与 Python 版一致（拍平连续 OR/AND，生成 `bool.should` / `bool.must`），并写入项目根目录的 `dsl.json`。

## 使用示例

```java
QueryParser parser = new QueryParser(Arrays.asList("title", "keywords", "abstract"));
Map<String, Object> dsl = parser.parse("(\"协同过滤\" AND \"推荐算法\") OR IPC:(H01M8)");
// dsl = { "query": { "bool": { "should": [...], "minimum_should_match": 1 } } }
```
