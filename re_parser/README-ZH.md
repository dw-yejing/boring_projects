# Introduction
这个小工具实现一个将字符串解析为 elasticsearch dsl的功能，以下是一个输入输出的示例：

Input: 
``` text
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
1. 支持基本的逻辑运算符：and、or、not
2. 支持括号嵌套来表示优先级
3. 支持多字段查询（使用逗号分隔）
4. 支持比较运算符：=、>、<
5. 自动处理数字和字符串类型的值

# Usage
```python
from parser import SearchParser
parser = SearchParser("(ti,abst=car and date>2020) not origin=korea")
result = parser.parse()
print(result) 
```

