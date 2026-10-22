def solve(expr):
    def tokenize(s):
        tokens = []
        i = 0
        while i < len(s):
            c = s[i]
            if c.isspace():
                i += 1
            elif c in "+-*/()":
                tokens.append(c)
                i += 1
            elif c.isdigit():
                start = i
                while i < len(s) and s[i].isdigit():
                    i += 1
                tokens.append(int(s[start:i]))
            else:
                i += 1
        return tokens

    tokens = tokenize(expr)
    
    def parse_expr(tokens, i):
        node, i = parse_term(tokens, i)
        while i < len(tokens) and tokens[i] in ('+', '-'):
            op = tokens[i]
            next_node, i = parse_term(tokens, i + 1)
            if op == '+':
                node += next_node
            else:
                node -= next_node
        return node, i

    def parse_term(tokens, i):
        node, i = parse_factor(tokens, i)
        while i < len(tokens) and tokens[i] == '*':
            next_node, i = parse_factor(tokens, i + 1)
            node *= next_node
        return node, i

    def parse_factor(tokens, i):
        if i < len(tokens) and tokens[i] == '-':
            val, i = parse_factor(tokens, i + 1)
            return -val, i
        elif i < len(tokens) and tokens[i] == '+':
            return parse_factor(tokens, i + 1)
        elif i < len(tokens) and tokens[i] == '(':
            val, i = parse_expr(tokens, i + 1)
            if i < len(tokens) and tokens[i] == ')':
                i += 1
            return val, i
        elif i < len(tokens) and isinstance(tokens[i], int):
            return tokens[i], i + 1
        return 0, i

    val, _ = parse_expr(tokens, 0)
    return val