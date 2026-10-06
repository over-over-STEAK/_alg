# 第三週習題：列舉真值表與 SAT 問題

## 一、作業目標

撰寫 Python 程式，系統性列舉布林變數的所有真假組合，產生完整真值表，並判斷指定公式是否存在滿足解。

本程式採用暴力搜尋：不預先排除任何指派，逐一將全部組合代入公式。找到第一組解之後仍繼續執行，以列出完整真值表與所有滿足解。

## 二、SAT 是什麼？

SAT（Boolean Satisfiability Problem，布林可滿足性問題）是在問：是否存在一組變數的真假指派，讓整個布林公式成立？

- **SAT（可滿足）**：至少存在一組使公式為真的指派。
- **UNSAT（不可滿足）**：所有指派都使公式為假。

每個變數只有 True、False 兩種可能。n 個變數共有 2ⁿ 種組合。

| 變數數量 | 指派組合數 |
| ---: | ---: |
| 1 | 2 |
| 2 | 4 |
| 3 | 8 |
| 4 | 16 |
| 10 | 1024 |

輸出中的 0 表示 False，1 表示 True。

## 三、邏輯運算符號

| 數學符號 | Python 寫法 | 意義 |
| --- | --- | --- |
| ∨ | `or` | OR：至少一個條件為真 |
| ∧ | `and` | AND：兩個條件都必須為真 |
| ¬ | `not` | NOT：將真假反轉 |

## 四、自訂公式

### 範例一：三變數公式

$$
F(A,B,C)=(A\lor B)\land(\neg A\lor C)\land(\neg B\lor\neg C)
$$

它包含三個條件，必須同時成立：

1. A 或 B 至少一個為真。
2. 非 A 或 C 至少一個為真。
3. 非 B 或非 C 至少一個為真。

例如指派 A=0、B=1、C=0：

- A OR B = 0 OR 1 = 1。
- NOT A OR C = 1 OR 0 = 1。
- NOT B OR NOT C = 0 OR 1 = 1。
- 最後結果為 1 AND 1 AND 1 = 1，所以這是一組滿足解。

### 範例二：矛盾公式

$$
G(A)=A\land\neg A
$$

A 與非 A 不可能同時為真，因此這個公式不可滿足，用來示範 UNSAT 的判定。

## 五、完整程式

將以下程式另存為 `sat_solver.py`。本文件 `sat_solver.md` 是說明文件，不是 Python 執行檔。

```python
from itertools import product


# 第三週習題：列舉＋暴力
# 系統性列舉真值表，解決 SAT 問題


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

    # 依序列舉所有真假組合
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
```

## 六、執行方式

程式使用 Python 標準函式庫 `itertools`，不需要額外安裝套件。

1. 在 VS Code 建立 `sat_solver.py`。
2. 貼上完整程式並儲存。
3. 開啟「終端機 → 新增終端機」。
4. 在程式所在資料夾執行：

```bash
python sat_solver.py
```

Windows 若使用 Python Launcher，也可執行：

```bash
py sat_solver.py
```

建議將 `sat_solver.py` 與 `sat_solver.md` 放在同一個 `homework_3` 資料夾中。

## 七、程式如何系統性列舉？

核心程式是：

```python
product([False, True], repeat=len(variable_names))
```

三個變數時，依序產生：

```text
000、001、010、011、100、101、110、111
```

這相當於從 0 到 7 的三位元二進位排列，每種指派都恰好出現一次，不會遺漏或重複。

接著：

```python
assignment = dict(zip(variable_names, values))
```

會將變數名稱和真假值配對，例如：

```python
{"A": False, "B": True, "C": False}
```

再以 `formula(assignment)` 求值。結果為真時，將該指派加入 `solutions`。最後依照清單是否為空，判斷 SAT 或 UNSAT。

## 八、真值表與結果

以下真值表及判定已以本文件的完整程式執行核對。

### 範例一

| A | B | C | F |
| ---: | ---: | ---: | ---: |
| 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 0 |
| 0 | 1 | 0 | 1 |
| 0 | 1 | 1 | 0 |
| 1 | 0 | 0 | 0 |
| 1 | 0 | 1 | 1 |
| 1 | 1 | 0 | 0 |
| 1 | 1 | 1 | 0 |

```text
共檢查 8 組指派。
判定：SAT（可滿足）
滿足解數量：2
解 1：A=0, B=1, C=0
解 2：A=1, B=0, C=1
```

### 範例二

| A | NOT A | A AND NOT A |
| ---: | ---: | ---: |
| 0 | 1 | 0 |
| 1 | 0 | 0 |

此處額外列出 NOT A 欄位方便理解；程式實際輸出只包含 A 與最終結果 F。

```text
共檢查 2 組指派。
判定：UNSAT（不可滿足）
所有組合都無法讓公式成立。
```

UNSAT 是正常的求解結果，不是程式發生錯誤。若終端機只看到第二個範例的結尾，可以向上捲動查看第一個範例的真值表與結果。

## 九、複雜度與限制

若共有 n 個變數，每次公式求值最多需要 L 個基本運算：

- 真值表有 2ⁿ 列。
- 單看公式求值，總時間上界為 O(2ⁿL)。
- 加上每列建立指派與格式化 n 個值的成本，時間上界為 O(2ⁿ(n+L))，不計終端機輸出字元的額外成本。
- 若有 S 組滿足解，保存它們約需 O(Sn) 空間；列舉器與目前指派另需 O(n) 空間，公式自身的求值空間另計。

`product` 逐組產生指派，不會一次建立整張真值表，但程式會保留全部滿足解。變數增加時，組合數呈指數成長，因此本方法適合小型問題與教學展示。

公式透過 Python 函式提供，必須回傳布林值，且引用的變數名稱必須出現在 `variable_names` 中。本程式不會解析使用者輸入的公式文字；`description` 只用於顯示，不參與求值。

## 十、如何更換公式？

例如想求解：

$$
H(A,B)=(A\lor B)\land\neg(A\land B)
$$

意思是 A、B 恰好有一個為真。可新增函式：

```python
def formula_custom(values):
    a = values["A"]
    b = values["B"]
    return (a or b) and not (a and b)
```

將函式放在 `main()` 被呼叫之前，並在 `main()` 中增加：

```python
solve_sat(
    ["A", "B"],
    formula_custom,
    "(A OR B) AND NOT (A AND B)"
)
```

## 十一、結論

本程式將 SAT 問題轉換成有限組合的搜尋：先系統性列舉所有指派，再逐一代入公式，最後收集滿足解並判定是否可滿足。透過 SAT 與 UNSAT 兩個範例，可以確認程式同時能找出解，以及在所有指派檢查完畢後判定無解。

## 參考資料

- [Boolean satisfiability problem — Wikipedia](https://en.wikipedia.org/wiki/Boolean_satisfiability_problem)
