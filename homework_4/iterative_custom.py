# 第四週習題：通用迭代框架與不動點迭代
# 自訂問題：求解 x² + x - 5 = 0 的正根

import math


def show_introduction():
    print("=" * 70)
    print("第四週習題：通用迭代框架與不動點迭代")
    print("=" * 70)

    print("\n【研究問題】")
    print("找出一個正數，使它的平方加上自己等於 5。")
    print("原方程式：x² + x - 5 = 0")

    print("\n【公式推導】")
    print("x² + x = 5")
    print("x(x + 1) = 5")
    print("x = 5 / (x + 1)")
    print("因此，迭代公式為：x[n+1] = 5 / (x[n] + 1)")

    print("\n【什麼是不動點？】")
    print("如果一個數代入函數後，輸出仍等於自己，")
    print("也就是 f(x) = x，這個數就稱為不動點。")

    print("\n【實驗設計】")
    print("分別從 0.5、2.0、5.0 開始迭代。")
    print("比較三組初始值的計算過程與迭代次數。")


def equation(x):
    """原方程式的值，用於檢查結果。"""
    return x * x + x - 5


def transition(x):
    """不動點迭代公式。"""
    return 5 / (x + 1)


def generic_iterator(
    transition_func,
    is_converged,
    initial_state,
    max_iter=100,
    observer=None
):
    """
    通用迭代框架。

    transition_func：計算下一個狀態
    is_converged：判斷是否停止
    initial_state：初始狀態
    max_iter：最多更新幾次
    observer：記錄或顯示每次更新，可省略
    """
    if not isinstance(max_iter, int) or max_iter < 1:
        raise ValueError("最大迭代次數必須是正整數。")

    state = initial_state

    for iteration in range(1, max_iter + 1):
        next_state = transition_func(state)

        if observer is not None:
            observer(state, next_state, iteration)

        if is_converged(state, next_state, iteration):
            return next_state, iteration, True

        state = next_state

    return state, max_iter, False


def run_experiment(initial_value, tolerance, max_iter):
    # 本實驗限定正數初始值，避免分母為零。
    if not math.isfinite(initial_value) or initial_value <= 0:
        raise ValueError("初始值必須是有限的正數。")

    if not math.isfinite(tolerance) or tolerance <= 0:
        raise ValueError("容許誤差必須是有限的正數。")

    history = []

    def converged(old, new, iteration):
        difference = abs(new - old)
        residual = abs(equation(new))

        return difference < tolerance and residual < tolerance

    def record_step(old, new, iteration):
        history.append({
            "iteration": iteration,
            "old": old,
            "new": new,
            "difference": abs(new - old),
            "residual": abs(equation(new)),
        })

    result, iterations, success = generic_iterator(
        transition_func=transition,
        is_converged=converged,
        initial_state=initial_value,
        max_iter=max_iter,
        observer=record_step
    )

    return {
        "initial": initial_value,
        "result": result,
        "iterations": iterations,
        "success": success,
        "history": history,
    }


def show_experiment(experiment, reference):
    print("\n" + "=" * 82)
    print(f"初始值：{experiment['initial']}")
    print("=" * 82)

    print(
        f"{'次數':>4} "
        f"{'目前數值':>15} "
        f"{'下一個數值':>15} "
        f"{'前後差距':>15} "
        f"{'方程式殘差':>15}"
    )

    print("-" * 82)

    for row in experiment["history"]:
        print(
            f"{row['iteration']:>4} "
            f"{row['old']:>15.10f} "
            f"{row['new']:>15.10f} "
            f"{row['difference']:>15.6e} "
            f"{row['residual']:>15.6e}"
        )

    result = experiment["result"]

    print(f"\n迭代次數：{experiment['iterations']}")
    print(f"最後近似值：{result:.10f}")
    print(f"參考正根：{reference:.10f}")
    print(f"絕對誤差：{abs(result - reference):.6e}")
    print(f"代回 x² + x：{result * result + result:.10f}")

    if experiment["success"]:
        print("狀態：已達到指定精度。")
    else:
        print("狀態：已達最大次數，尚未達到指定精度。")


def show_summary(experiments, reference):
    print("\n" + "=" * 76)
    print("不同初始值的實驗比較")
    print("=" * 76)

    print(
        f"{'初始值':>8} "
        f"{'迭代次數':>8} "
        f"{'最後近似值':>16} "
        f"{'絕對誤差':>14} "
        f"{'是否達標':>8}"
    )

    for experiment in experiments:
        error = abs(experiment["result"] - reference)
        status = "是" if experiment["success"] else "否"

        print(
            f"{experiment['initial']:>8.2f} "
            f"{experiment['iterations']:>8} "
            f"{experiment['result']:>16.10f} "
            f"{error:>14.6e} "
            f"{status:>8}"
        )

    successful = [
        experiment
        for experiment in experiments
        if experiment["success"]
    ]

    if successful:
        fewest = min(
            experiment["iterations"]
            for experiment in successful
        )

        best_initials = [
            str(experiment["initial"])
            for experiment in successful
            if experiment["iterations"] == fewest
        ]

        print("\n本次實驗中，達標所需更新次數最少的初始值：")
        print("、".join(best_initials))
        print(f"更新次數：{fewest}")
        print("此處比較迭代次數，不是實際執行時間。")


def show_analysis(reference):
    derivative = -5 / (reference + 1) ** 2

    print("\n" + "=" * 70)
    print("收斂原理與觀察重點")
    print("=" * 70)

    print("\n迭代函數：f(x) = 5 / (x + 1)")
    print("導數：f'(x) = -5 / (x + 1)²")
    print(f"在正根附近，f'(x) 約為 {derivative:.6f}")

    print("\n1. 導數為負，表示根附近的誤差會交替正負。")
    print("   因此數值會在答案兩側來回變化。")

    print("\n2. 導數絕對值小於 1，表示根附近的誤差會縮小。")
    print("   這就是數值雖然來回變動，仍能逐漸接近答案的原因。")

    print("\n3. 不同初始值可能需要不同次數才能達標。")
    print("   本次比較的結論只針對設定的三組初始值與容許誤差。")

    print("\n4. 程式同時檢查前後差距與方程式殘差。")
    print("   避免只因數值變化很小，就誤認為已經解對。")

    print("\n5. 參考正根只用來核對結果，沒有參與迭代更新。")


def main():
    show_introduction()

    tolerance = 1e-6
    max_iter = 100
    initial_values = [0.5, 2.0, 5.0]

    reference = (-1 + math.sqrt(21)) / 2

    print(f"\n容許誤差：{tolerance}")
    print(f"最大迭代次數：{max_iter}")
    print(f"公式計算的正根：{reference:.10f}")

    experiments = []

    for initial in initial_values:
        experiment = run_experiment(
            initial_value=initial,
            tolerance=tolerance,
            max_iter=max_iter
        )

        experiments.append(experiment)
        show_experiment(experiment, reference)

    show_summary(experiments, reference)
    show_analysis(reference)

    print("\n所有實驗完成。")


if __name__ == "__main__":
    main()