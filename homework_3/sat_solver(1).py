from itertools import product

def solve_sat(variable_names, formula, description):
    """列出完整真值表，並回傳所有滿足公式的指派。"""

    if len(variable_names) != len(set(variable_names)):
        raise ValueError("變數名稱不能重複。")

    solutions = []

    print("=" * 60)
    print(f"公式：{description}")
    print(f"變數數量：{len(variable_names)}")
    print(f"組合總數：{2 ** len(variable_names)}")
    print("0：False（假），1：True（真）")
    print("=" * 60)

    print(" | ".join(variable_names + ["F"]))
    print("-" * 30)

    for values in product([False, True], repeat=len(variable_names)):
        assignment = dict(zip(variable_names, values))
        result = formula(assignment)

        if not isinstance(result, bool):
            raise TypeError("公式必須回傳 True 或 False。")

        row = [str(int(value)) for value in values]
        row.append(str(int(result)))
        print(" | ".join(row))

        if result:
            solutions.append(assignment)

    print(f"\n共檢查 {2 ** len(variable_names)} 組指派。")

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
        print("所有組合都無法讓公式成立。")

    print()
    return solutions


def formula_sat(values):
    a = values["A"]
    b = values["B"]
    c = values["C"]

    return (
        (a or b)
        and ((not a) or c)
        and ((not b) or (not c))
    )


def formula_unsat(values):
    a = values["A"]

    return a and (not a)


def main():
    print("第三週習題：列舉真值表與 SAT 求解\n")

    print("【範例一：可滿足的公式】")
    solve_sat(
        ["A", "B", "C"],
        formula_sat,
        "(A OR B) AND (NOT A OR C) AND (NOT B OR NOT C)"
    )

    print("【範例二：不可滿足的公式】")
    solve_sat(
        ["A"],
        formula_unsat,
        "A AND NOT A"
    )


if __name__ == "__main__":
    main()