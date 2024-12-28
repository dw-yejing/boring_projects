from typing import Dict, Any
import re

class SearchParser:
    def __init__(self, query_string: str):
        self.query = query_string.strip()
        self.pos = 0
        self.parentheses_count = 0  # 添加括号计数器
        
    def parse(self) -> Dict[str, Any]:
        result = self._parse_expression()
        # 检查是否所有括号都已匹配
        if self.parentheses_count > 0:
            raise ValueError("Unmatched opening parenthesis")
        return {"query": result}
    
    def _parse_expression(self) -> Dict[str, Any]:
        """ 解析表达式，处理逻辑运算符 not and or
        """
        left = self._parse_term()
        
        while self.pos < len(self.query):
            self._skip_whitespace()
            if self.pos >= len(self.query):
                break
                
            if self._peek().lower() == 'and':
                self._consume('and')
                right = self._parse_term()
                left = {
                    "bool": {
                        "must": [left, right]
                    }
                }
            elif self._peek().lower() == 'not':
                self._consume('not')
                right = self._parse_term()
                left = {
                    "bool": {
                        "must": [left],
                        "must_not": [right]
                    }
                }
            elif self._peek().lower() == 'or':
                self._consume('or')
                right = self._parse_term()
                left = {
                    "bool": {
                        "should": [left, right]
                    }
                }
            else:
                break
                
        return left
    
    def _parse_term(self) -> Dict[str, Any]:
        """ 解析单个条件，包括字段比较和括号内的子表达式 > < =
        """
        self._skip_whitespace()
        
        if self.pos >= len(self.query):
            if self.parentheses_count > 0:
                raise ValueError(f"Unclosed parenthesis: missing {self.parentheses_count} closing parenthesis")
            raise ValueError("Unexpected end of input")
            
        if self.query[self.pos] == '(':
            self.parentheses_count += 1
            self.pos += 1  # consume '('
            result = self._parse_expression()
            self._skip_whitespace()
            
            if self.pos >= len(self.query):
                raise ValueError(f"Unclosed parenthesis: missing closing parenthesis at position {self.pos}")
            
            if self.query[self.pos] != ')':
                raise ValueError(f"Expected closing parenthesis at position {self.pos}, found '{self.query[self.pos]}'")
                
            self.parentheses_count -= 1
            self.pos += 1  # consume ')'
            return result
            
        # Parse field conditions like "field=value" or "field>value"
        match = re.match(r'([^=<>]+)(=|>|<)([^=<>\s\)]+)', self.query[self.pos:])
        if match:
            field, op, value = match.groups()
            self.pos += len(match.group())
            
            # Handle multiple fields with comma
            fields = [f.strip() for f in field.split(',')]
            
            if op == '=':
                if len(fields) == 1:
                    return {
                        "term": {
                            fields[0]: value
                        }
                    }
                else:
                    return {
                        "bool": {
                            "should": [
                                {"match": {f: value}} for f in fields
                            ]
                        }
                    }
            elif op in ['>', '<']:
                range_op = 'gt' if op == '>' else 'lt'
                try:
                    value = int(value)
                except ValueError:
                    pass
                
                return {
                    "range": {
                        fields[0]: {
                            range_op: value
                        }
                    }
                }
                
        raise ValueError(f"Invalid syntax at position {self.pos}")
    
    def _peek(self) -> str:
        self._skip_whitespace()
        if self.pos >= len(self.query):
            return ''
        
        # Look ahead for keywords
        for keyword in ['and', 'or', 'not']:
            if self.query[self.pos:].lower().startswith(keyword):
                return keyword
        return self.query[self.pos]
    
    def _consume(self, expected: str):
        self._skip_whitespace()
        if not self.query[self.pos:].lower().startswith(expected.lower()):
            raise ValueError(f"Expected '{expected}' at position {self.pos}")
        self.pos += len(expected)
    
    def _skip_whitespace(self):
        while self.pos < len(self.query) and self.query[self.pos].isspace():
            self.pos += 1 