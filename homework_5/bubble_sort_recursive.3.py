import ast

def sym_diff(expr):
    # 組合運算式，同時做基本化簡
    def make(op, a, b):
        if op == "+":
            if a == "0":
                return b
            if b == "0":
                return a

        elif op == "-":
            if b == "0":
                return a
            if a == b:
                return "0"

        elif op == "*":
            if a == "0" or b == "0":
                return "0"
            if a == "1":
                return b
            if b == "1":
                return a

        elif op == "/":
            if b == "1":
                return a

        elif op == "**":
            if b == "0":
                return "1"
            if b == "1":
                return a

        return f"({a} {op} {b})"

    # 取得數值常數，支援負數次方
    def number(node):
        if isinstance(node, ast.Constant):
            if type(node.value) in (int, float):
                return node.value

        if isinstance(node, ast.UnaryOp):
            if isinstance(node.op, ast.USub):
                return -number(node.operand)
            if isinstance(node.op, ast.UAdd):
                return number(node.operand)

        raise ValueError("次方必須是數值常數")

    # 遞迴微分
    def diff(node):
        # 常數的微分是 0
        if isinstance(node, ast.Constant):
            number(node)
            return "0"

        # x 的微分是 1，其他變數視為常數
        if isinstance(node, ast.Name):
            return "1" if node.id == "x" else "0"

        # 正號與負號
        if isinstance(node, ast.UnaryOp):
            d = diff(node.operand)

            if isinstance(node.op, ast.USub):
                return make("*", "-1", d)
            if isinstance(node.op, ast.UAdd):
                return d

        if isinstance(node, ast.BinOp):
            u = ast.unparse(node.left)
            v = ast.unparse(node.right)

            # 遞迴計算左邊的微分
            du = diff(node.left)

            # 次方規則：(u**n)' = n * u**(n-1) * u'
            if isinstance(node.op, ast.Pow):
                n = number(node.right)

                if n == 0:
                    return "0"
                if n == 1:
                    return du

                power = make("**", u, str(n - 1))
                return make("*", make("*", str(n), power), du)

            # 遞迴計算右邊的微分
            dv = diff(node.right)

            if isinstance(node.op, ast.Add):
                return make("+", du, dv)

            if isinstance(node.op, ast.Sub):
                return make("-", du, dv)

            # 乘法規則：(uv)' = u'v + uv'
            if isinstance(node.op, ast.Mult):
                return make(
                    "+",
                    make("*", du, v),
                    make("*", u, dv)
                )

            # 除法規則：(u/v)' = (u'v - uv') / v**2
            if isinstance(node.op, ast.Div):
                numerator = make(
                    "-",
                    make("*", du, v),
                    make("*", u, dv)
                )
                return make("/", numerator, make("**", v, "2"))

        raise ValueError("不支援這種運算式")

    tree = ast.parse(expr, mode="eval").body
    return diff(tree)


print(sym_diff("x**3 + 2*x + 5"))
print(sym_diff("(x + 1)**2"))
print(sym_diff("x*x"))
print(sym_diff("5"))