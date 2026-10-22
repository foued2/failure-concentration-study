"""Bounded integer arithmetic expression task: oracles and family classifier."""
from __future__ import annotations

import ast
import re

FAMILY_ORDER = ["F1", "F2", "F3", "F4", "F5", "F6"]
FAMILY_NAMES = {
    "F1": "operator_precedence",
    "F2": "left_associativity",
    "F3": "parentheses",
    "F4": "unary_minus",
    "F5": "multi_digit_tokenization",
    "F6": "whitespace",
}


class ExpressionError(ValueError):
    """The expression is outside the declared grammar."""


class _Parser:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0

    def _skip(self) -> None:
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self.pos += 1

    def _peek(self) -> str | None:
        self._skip()
        return self.text[self.pos] if self.pos < len(self.text) else None

    def parse(self) -> int:
        value = self._expr()
        self._skip()
        if self.pos != len(self.text):
            raise ExpressionError(f"unexpected token at {self.pos}")
        return value

    def _expr(self) -> int:
        value = self._term()
        while self._peek() in {"+", "-"}:
            op = self.text[self.pos]
            self.pos += 1
            right = self._term()
            value = value + right if op == "+" else value - right
        return value

    def _term(self) -> int:
        value = self._factor()
        while self._peek() == "*":
            self.pos += 1
            value *= self._factor()
        return value

    def _factor(self) -> int:
        if self._peek() == "-":
            self.pos += 1
            return -self._factor()
        return self._primary()

    def _primary(self) -> int:
        token = self._peek()
        if token is None:
            raise ExpressionError("unexpected end of expression")
        if token == "(":
            self.pos += 1
            value = self._expr()
            if self._peek() != ")":
                raise ExpressionError("missing closing parenthesis")
            self.pos += 1
            return value
        if token.isdigit():
            start = self.pos
            while self.pos < len(self.text) and self.text[self.pos].isdigit():
                self.pos += 1
            return int(self.text[start:self.pos])
        raise ExpressionError(f"unexpected token {token!r} at {self.pos}")


def evaluate(expr: str) -> int:
    return _Parser(expr).parse()


def _eval_ast_node(node: ast.AST) -> int:
    if isinstance(node, ast.Expression):
        return _eval_ast_node(node.body)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, bool) or not isinstance(node.value, int):
            raise ExpressionError("only integer constants are allowed")
        return node.value
    if isinstance(node, ast.BinOp):
        left = _eval_ast_node(node.left)
        right = _eval_ast_node(node.right)
        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        raise ExpressionError("unsupported binary operator")
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return -_eval_ast_node(node.operand)
    raise ExpressionError(f"unsupported syntax: {type(node).__name__}")


def evaluate_ast(expr: str) -> int:
    try:
        tree = ast.parse(expr.strip(), mode="eval")
    except SyntaxError as exc:
        raise ExpressionError(str(exc)) from exc
    return _eval_ast_node(tree)


def classify_features(expr: str) -> dict[str, object]:
    has_ws = any(char.isspace() for char in expr)
    has_paren = "(" in expr or ")" in expr
    leading_unary = expr.startswith("-")
    has_multidigit = any(len(run) > 1 for run in re.findall(r"\d+", expr))
    has_mul = "*" in expr
    has_plus = "+" in expr
    binary_minus = expr.count("-") - (1 if leading_unary else 0)
    f1 = has_mul and has_plus and not (has_ws or has_paren or leading_unary or has_multidigit) and binary_minus <= 1
    f2 = binary_minus >= 2 and not (has_ws or has_paren or leading_unary or has_multidigit or has_mul)
    f3 = has_paren and not (has_ws or leading_unary or has_multidigit or has_mul)
    f4 = leading_unary and not (has_ws or has_paren or has_multidigit or has_mul) and binary_minus <= 1
    f5 = has_multidigit and not (has_ws or has_paren or leading_unary or has_mul) and binary_minus <= 1
    f6 = has_ws and not (has_paren or leading_unary or has_multidigit or has_mul) and binary_minus <= 1
    sat = {"F1": f1, "F2": f2, "F3": f3, "F4": f4, "F5": f5, "F6": f6}
    family = next((name for name in FAMILY_ORDER if sat[name]), None)
    return {
        "has_ws": has_ws,
        "has_paren": has_paren,
        "leading_unary": leading_unary,
        "has_multidigit": has_multidigit,
        "has_mul": has_mul,
        "has_plus": has_plus,
        "binary_minus": binary_minus,
        "sat_vector": sat,
        "family": family,
        "exact_one": sum(sat.values()) == 1,
    }


def classify_family(expr: str) -> str:
    features = classify_features(expr)
    family = features["family"]
    if not features["exact_one"] or not isinstance(family, str):
        raise ExpressionError(f"expression does not satisfy exactly one family: {expr!r}")
    return family


def validate_record(record: dict) -> dict:
    expr = record["expr"]
    family = classify_family(expr)
    if record.get("family") != family:
        raise ExpressionError(f"family mismatch for {expr!r}")
    expected = evaluate(expr)
    if evaluate_ast(expr) != expected:
        raise ExpressionError(f"oracle mismatch for {expr!r}")
    if record.get("expected") != expected:
        raise ExpressionError(f"expected-value mismatch for {expr!r}")
    return {**record, "features": classify_features(expr)}


def validate_bank(records: list[dict], expected_per_family: int) -> None:
    ids = [record.get("id") or record.get("probe_id") or record.get("hid") for record in records]
    expressions = [record["expr"] for record in records]
    if len(ids) != len(set(ids)):
        raise ExpressionError("duplicate record IDs")
    if len(expressions) != len(set(expressions)):
        raise ExpressionError("duplicate expression strings")
    counts = {name: 0 for name in FAMILY_ORDER}
    for record in records:
        counts[classify_family(record["expr"])] += 1
    if any(counts[name] != expected_per_family for name in FAMILY_ORDER):
        raise ExpressionError(f"family counts are not {expected_per_family}: {counts}")
    for record in records:
        validate_record(record)
