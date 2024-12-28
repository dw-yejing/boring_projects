from parser import SearchParser
# 使用示例
# parser = SearchParser("(ti,abst=car and date>2020) not origin=korea")
parser = SearchParser("ti,abst=car and date>2020")
result = parser.parse()
print(result) 