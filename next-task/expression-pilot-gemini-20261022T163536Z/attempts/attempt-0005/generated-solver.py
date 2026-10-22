```python
def solve(expr: str) -> int:
    def tokenize(s):
        tokens = []
        i = 0
        n = len(s)
        while i < n:
            c = s[i]
            if c.isspace():
                i += 1
            elif c in "+-*/()":
                tokens.append(c)
                i += 1
            elif c.isdigit():
                start = i
                while i < n and s[i].isdigit():
                    i += 1
                tokens.append(s[start:i])
            else:
                raise ValueError(f"Unknown character {c}")
        return tokens

    tokens = tokenize(expr)
    
    # Handle unary minus by replacing or processing during parsing
    # Actually, let's parse with a standard Pratt parser or recursive descent.
    
    pos = 0
    
    def peek():
        if pos < len(tokens):
            return tokens[pos]
        return None

    def consume(expected=None):
        nonlocal pos
        if pos < len(tokens):
            t = tokens[pos]
            if expected and t != expected:
                raise ValueError(f"Expected {expected}, got {t}")
            pos += 1
            return t
        if expected:
            raise ValueError(f"Expected {expected}, got EOF")
        return None

    def parse_primary():
        t = peek()
        if t == '+':
            consume('+')
            return parse_primary()
        if t == '-':
            consume('-')
            return -parse_primary()
        if t == '(':
            consume('(')
            node = parse_expr()
            consume(')')
            return node
        if t is not None and t.isdigit():
            consume()
            return int(t)
        raise ValueError(f"Unexpected token {t}")

    def parse_term():
        node = parse_primary()
        while peek() == '*':
            consume('*')
            node = node * parse_primary()
        return node

    def parse_expr():
        node = parse_term()
        while True:
            t = peek()
            if t == '+':
                consume('+')
                node = node + parse_term()
            elif t == '-':
                consume('-')
                node = node - parse_term()
            else:
                break
        return node

    result = parse_expr()
    if pos < len(tokens):
        raise ValueError("Trailing tokens")
    return result
```