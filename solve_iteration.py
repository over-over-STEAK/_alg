def f(x):
    return x**3 - 2*x - 5

def df(x):
    return 3*x**2 - 2

def newton_method(x0=2.0, tolerance=1e-8, max_iterations=100):
    x = x0

    for n in range(1, max_iterations + 1):
        derivative = df(x)

        if abs(derivative) < 1e-12:
            print("導數太接近 0，無法繼續計算。")
            return None

        next_x = x - f(x) / derivative
        print(f"第 {n} 次迭代：x = {next_x:.10f}")

        if abs(next_x - x) < tolerance and abs(f(next_x)) < tolerance:
            print(f"\n近似解：{next_x:.10f}")
            print(f"方程式殘差：{f(next_x):.10e}")
            print(f"迭代次數：{n}")
            return next_x

        x = next_x

    print("達到最大迭代次數，仍未收斂。")
    return None

newton_method()