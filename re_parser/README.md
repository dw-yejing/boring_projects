# Introduction

The re_parser (short for retrieve expression parser) is a small tool designed to parse strings into Elasticsearch DSL. Here is an example of input and output:

Input:

```text
( ti,abst=car and date>2020 ) not origin=korea
```

Output:

```json
{
  "query": {
    "bool": {
      "must": [
        {
          "bool": {
            "should": [
              {
                "match": {
                  "ti": "car"
                }
              },
              {
                "match": {
                  "abst": "car"
                }
              }
            ],
            "filter": [
              {
                "range": {
                  "date": {
                    "gt": 2020
                  }
                }
              }
            ]
          }
        }
      ],
      "must_not": [
        {
          "term": {
            "origin": "korea"
          }
        }
      ]
    }
  }
}
```

# Features

1. Supports basic logical operators: and, or, not
2. Support parenthesis nesting to indicate priority
3. Support multi-field queries (separated by commas)
4. Support comparison operators: =, >, <
5. Automatically handle values of number and string types

# Usage

```python
from parser import SearchParser
parser = SearchParser("(ti,abst=car and date>2020) not origin=korea")
result = parser.parse()
print(result) 
```
