import ast


def sym_diff(expr):
    tree = ast.parse(expr, mode="eval").body

    def constant_value(node):
        if isinstance(node, ast.Constant):
            if type(node.value) in (int, float):
                return node.value

        if isinstance(node, ast.UnaryOp):
            value = constant_value(node.operand)

            if isinstance(node.op, ast.USub):
                return -value
            if isinstance(node.op, ast.UAdd):
                return value

        raise ValueError("次方必須是數值常數")

    def diff(node):
        if isinstance(node, ast.Constant):
            if type(node.value) not in (int, float):
                raise ValueError("只支援數值常數")
            return "0"

        if isinstance(node, ast.Name):
            return "1" if node.id == "x" else "0"

        if isinstance(node, ast.UnaryOp):
            derivative = diff(node.operand)

            if isinstance(node.op, ast.USub):
                return f"(-({derivative}))"
            if isinstance(node.op, ast.UAdd):
                return derivative

        if isinstance(node, ast.BinOp):
            u = ast.unparse(node.left)
            v = ast.unparse(node.right)
            du = diff(node.left)

            if isinstance(node.op, ast.Pow):
                n = constant_value(node.right)

                if n == 0:
                    return "0"
                if n == 1:
                    return du

                return f"({n} * ({u})**({n - 1}) * ({du}))"

            dv = diff(node.right)

            if isinstance(node.op, ast.Add):
                return f"(({du}) + ({dv}))"

            if isinstance(node.op, ast.Sub):
                return f"(({du}) - ({dv}))"

            if isinstance(node.op, ast.Mult):
                return f"(({du}) * ({v}) + ({u}) * ({dv}))"

            if isinstance(node.op, ast.Div):
                return (
                    f"((({du}) * ({v}) - ({u}) * ({dv}))"
                    f" / ({v})**2)"
                )

        raise ValueError("不支援這種運算式")

    return diff(tree)


print(sym_diff("x**3 + 2*x + 5"))
print(sym_diff("(x + 1)**2"))
print(sym_diff("x / (x + 1)"))