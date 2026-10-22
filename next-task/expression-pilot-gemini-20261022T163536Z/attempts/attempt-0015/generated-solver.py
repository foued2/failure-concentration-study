import ast

def solve(expr):
    class Evaluator(ast.NodeVisitor):
        def visit(self, node):
            if isinstance(node, ast.Expression):
                return self.visit(node.body)
            elif isinstance(node, ast.Constant):
                return node.value
            elif isinstance(node, ast.Num):
                return node.n
            elif isinstance(node, ast.BinOp):
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
            elif isinstance(node, ast.UnaryOp):
                operand = self.visit(node.operand)
                if isinstance(node.op, ast.UAdd):
                    return +operand
                elif isinstance(node.op, ast.USub):
                    return -operand
                else:
                    raise ValueError("Unsupported unary operator")
            else:
                raise ValueError("Unsupported expression")

    tree = ast.parse(expr.strip(), mode='eval')
    return Evaluator().visit(tree)