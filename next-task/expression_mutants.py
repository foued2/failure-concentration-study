"""Prespecified hand-built expression-evaluator variants for calibration."""
from __future__ import annotations

VARIANTS = {
    "reference_parser": {
        "target_family": None,
        "defect": "none; correct reference control",
        "source": r'''def solve(expr):
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
        if token == "(":
            pos += 1
            value = parse_expr()
            if peek() != ")":
                raise ValueError("missing closing parenthesis")
            pos += 1
            return value
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
''',
    },
    "precedence_flat": {
        "target_family": "F1",
        "defect": "evaluates all binary operators strictly left-to-right",
        "source": r'''def solve(expr):
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
        value = parse_factor()
        while peek() in ("+", "-", "*"):
            op = expr[pos]
            pos += 1
            right = parse_factor()
            if op == "+":
                value += right
            elif op == "-":
                value -= right
            else:
                value *= right
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
        if token == "(":
            pos += 1
            value = parse_expr()
            if peek() != ")":
                raise ValueError("missing closing parenthesis")
            pos += 1
            return value
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
''',
    },
    "minus_right_assoc": {
        "target_family": "F2",
        "defect": "evaluates addition and subtraction right-associatively",
        "source": r'''def solve(expr):
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
        token = peek()
        if token in ("+", "-"):
            pos += 1
            right = parse_expr()
            return value + right if token == "+" else value - right
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
        if token == "(":
            pos += 1
            value = parse_expr()
            if peek() != ")":
                raise ValueError("missing closing parenthesis")
            pos += 1
            return value
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
''',
    },
    "parens_dropped": {
        "target_family": "F3",
        "defect": "removes parentheses before evaluating",
        "source": r'''def solve(expr):
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
''',
    },
    "unary_rejected": {
        "target_family": "F4",
        "defect": "rejects a leading unary minus",
        "source": r'''def solve(expr):
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
        return parse_primary()

    def parse_primary():
        nonlocal pos
        token = peek()
        if token == "(":
            pos += 1
            value = parse_expr()
            if peek() != ")":
                raise ValueError("missing closing parenthesis")
            pos += 1
            return value
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
''',
    },
    "single_digit_tokenizer": {
        "target_family": "F5",
        "defect": "reads only one digit per integer literal",
        "source": r'''def solve(expr):
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
        if token == "(":
            pos += 1
            value = parse_expr()
            if peek() != ")":
                raise ValueError("missing closing parenthesis")
            pos += 1
            return value
        if token.isdigit():
            pos += 1
            return int(token)
        raise ValueError("unexpected token")

    result = parse_expr()
    skip()
    if pos != len(expr):
        raise ValueError("trailing input")
    return result
''',
    },
    "whitespace_rejected": {
        "target_family": "F6",
        "defect": "does not skip whitespace between tokens",
        "source": r'''def solve(expr):
    pos = 0

    def skip():
        return None

    def peek():
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
        if token == "(":
            pos += 1
            value = parse_expr()
            if peek() != ")":
                raise ValueError("missing closing parenthesis")
            pos += 1
            return value
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
''',
    },
}

VARIANT_ORDER = [
    "reference_parser",
    "precedence_flat",
    "minus_right_assoc",
    "parens_dropped",
    "unary_rejected",
    "single_digit_tokenizer",
    "whitespace_rejected",
]
