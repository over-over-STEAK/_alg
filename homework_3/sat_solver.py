from itertools import product

def solve_sat(variable_names, formula, description):
    """列舉所有真假指派，印出真值表並回傳全部滿足解。"""

    if len(variable_names) != len(set(variable_names)):
        raise ValueError("變數名稱不能重複。")

    solutions = []
    checked = 0

    print("=" * 60)
    print(f"公式：{description}")
    print(f"變數數量：{len(variable_names)}")
    print(f"組合總數：2^{len(variable_names)} = {2 ** len(variable_names)}")
    print("0 代表 False，1 代表 True")
    print("=" * 60)

    header = " | ".join(variable_names + ["F"])
    print(header)
    print("-" * len(header))

    for values in product([False, True], repeat=len(variable_names)):
        checked += 1

        # 例如 {"A": False, "B": True, "C": False}
        assignment = dict(zip(variable_names, values))

        result = formula(assignment)

        if not isinstance(result, bool):
            raise TypeError("公式必須回傳 True 或 False。")

        row = [str(int(value)) for value in values]
        row.append(str(int(result)))

        print(" | ".join(row))

        if result:
            solutions.append(assignment)

    print(f"\n共檢查 {checked} 組指派。")

    if solutions:
        print("判定：SAT（可滿足）")
        print(f"滿足解數量：{len(solutions)}")

        for index, solution in enumerate(solutions, start=1):
            text = ", ".join(
                f"{name}={int(solution[name])}"
                for name in variable_names
            )
            print(f"解 {index}：{text}")
    else:
        print("判定：UNSAT（不可滿足）")
        print("所有指派都無法讓公式成立。")

    print()
    return solutions


def formula_sat(values):
    """範例一：三個變數的布林公式。"""
    a = values["A"]
    b = values["B"]
    c = values["C"]

    clause1 = a or b
    clause2 = (not a) or c
    clause3 = (not b) or (not c)

    return clause1 and clause2 and clause3


def formula_unsat(values):
    """範例二：A 與非 A 不可能同時成立。"""
    a = values["A"]

    return a and (not a)


def main():
    print("第三週習題：列舉真值表與暴力搜尋 SAT\n")

    solve_sat(
        variable_names=["A", "B", "C"],
        formula=formula_sat,
        description="(A OR B) AND (NOT A OR C) AND (NOT B OR NOT C)"
    )

    solve_sat(
        variable_names=["A"],
        formula=formula_unsat,
        description="A AND NOT A"
    )


if __name__ == "__main__":
    main()