def solve(expr):
    expr = expr.replace("(", "").replace(")", "")
    pos = 0

    def skip():
        nonlocal pos
        while pos < len(expr) and expr[pos].isspace():
            pos += 1

    def peek():
        skip()
        return expr[pos] if pos < len(expr) else ""

    def parse_expr():
        nonlocal pos
        value = parse_term()
        while peek() in ("+", "-"):
            op = expr[pos]
            pos += 1
            right = parse_term()
            value = value + right if op == "+" else value - right
        return value

    def parse_term():
        nonlocal pos
        value = parse_factor()
        while peek() == "*":
            pos += 1
            value *= parse_factor()
        return value

    def parse_factor():
        nonlocal pos
        if peek() == "-":
            pos += 1
            return -parse_factor()
        return parse_primary()

    def parse_primary():
        nonlocal pos
        token = peek()
        if token.isdigit():
            start = pos
            while pos < len(expr) and expr[pos].isdigit():
                pos += 1
            return int(expr[start:pos])
        raise ValueError("unexpected token")

    result = parse_expr()
    skip()
    if pos != len(expr):
        raise ValueError("trailing input")
    return result
