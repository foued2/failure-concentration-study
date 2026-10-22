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
    
    # Preprocess unary minus
    processed = []
    expect_unary = True
    for i, tok in enumerate(tokens):
        if tok == '(':
            processed.append(tok)
            expect_unary = True
        elif tok == ')':
            processed.append(tok)
            expect_unary = False
        elif tok in '+-':
            if expect_unary:
                if tok == '-':
                    processed.append('UNARY_MINUS')
                # Ignore unary plus
            else:
                processed.append(tok)
                expect_unary = True
        else:
            processed.append(tok)
            expect_unary = False

    # Convert to postfix using Shunting-yard
    output = []
    stack = []
    precedence = {'+': 1, '-': 1, '*': 2, 'UNARY_MINUS': 3}

    for tok in processed:
        if isinstance(tok, int):
            output.append(tok)
        elif tok in precedence:
            while (stack and stack[-1] in precedence and 
                   precedence[stack[-1]] >= precedence[tok] and 
                   tok != 'UNARY_MINUS'):
                output.append(stack.pop())
            stack.append(tok)
        elif tok == '(':
            stack.append(tok)
        elif tok == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            if stack and stack[-1] == '(':
                stack.pop()

    while stack:
        output.append(stack.pop())

    # Evaluate postfix
    eval_stack = []
    for tok in output:
        if isinstance(tok, int):
            eval_stack.append(tok)
        elif tok == 'UNARY_MINUS':
            val = eval_stack.pop()
            eval_stack.append(-val)
        else:
            b = eval_stack.pop()
            a = eval_stack.pop()
            if tok == '+':
                eval_stack.append(a + b)
            elif tok == '-':
                eval_stack.append(a - b)
            elif tok == '*':
                eval_stack.append(a * b)

    return eval_stack[0] if eval_stack else 0