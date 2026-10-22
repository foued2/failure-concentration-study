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
    
    def parse_expr(tokens):
        # We can use Shunting-yard or recursive descent.
        # Let's do recursive descent for E = T ((+|-) T)*
        # T = F ((*|/) F)*
        # F = (E) | -F | +F | number
        
        idx = 0
        
        def peek():
            nonlocal idx
            if idx < len(tokens):
                return tokens[idx]
            return None

        def consume():
            nonlocal idx
            if idx < len(tokens):
                tok = tokens[idx]
                idx += 1
                return tok
            return None

        def parse_factor():
            tok = peek()
            if tok == '(':
                consume()
                val = parse_expression()
                consume() # ')'
                return val
            elif tok == '-':
                consume()
                return -parse_factor()
            elif tok == '+':
                consume()
                return parse_factor()
            elif isinstance(tok, int):
                consume()
                return tok
            return 0

        def parse_term():
            val = parse_factor()
            while True:
                tok = peek()
                if tok == '*':
                    consume()
                    val *= parse_factor()
                else:
                    break
            return val

        def parse_expression():
            val = parse_term()
            while True:
                tok = peek()
                if tok == '+':
                    consume()
                    val += parse_term()
                elif tok == '-':
                    consume()
                    val -= parse_term()
                else:
                    break
            return val

        return parse_expression()

    return parse_expr(tokens)