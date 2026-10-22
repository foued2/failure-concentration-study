```python
import ast

def solve(expr):
    class SafeEval(ast.NodeVisitor):
        def visit_Expression(self, node):
            return self.visit(node.body)

        def visit_BinOp(self, node):
            left = self.visit(node.left)
            right = self.visit(node.right)
            if isinstance(node.op, ast.Add):
                return left + right
            elif isinstance(node.op, ast.Sub):
                return left - right
            elif isinstance(node.op, ast.Mult):
                return left * right
            else:
                raise ValueError("Unsupported operator")

        def visit_UnaryOp(self, node):
            operand = self.visit(node.operand)
            if isinstance(node.op, ast.USub):
                return -operand
            elif isinstance(node.op, ast.UAdd):
                return +operand
            else:
                raise ValueError("Unsupported unary operator")

        def visit_Constant(self, node):
            if isinstance(node.value, int):
                return node.value
            raise ValueError("Unsupported constant")

        def visit_Num(self, node):
            return node.n

        def generic_visit(self, node):
            raise ValueError(f"Unsupported expression structure: {type(node).__name__}")

    tree = ast.parse(expr, mode='eval')
    return SafeEval().visit(tree)
```