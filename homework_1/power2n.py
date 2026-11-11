"""執行：py power2n.py 或 py power2n.py 20。"""
import argparse
from time import perf_counter
from power2n1 import power2n_1
from power2n2a import power2n_2a
from power2n2b import power2n_2b
from power2n3 import power2n_3


def main():
    parser = argparse.ArgumentParser(description="比較四種 2^n 算法")
    parser.add_argument("n", type=int, nargs="?", default=100)
    args = parser.parse_args()
    if not 0 <= args.n <= 200:
        parser.error("本展示限定 0 <= n <= 200，以避免過深遞迴。")
    expected = 2 ** args.n
    print(f"n = {args.n}\n正確答案：{expected}\n")
    for label, fn in [("內建次方", power2n_1), ("雙分支遞迴", power2n_2a),
                      ("單分支遞迴", power2n_2b), ("記憶化遞迴", power2n_3)]:
        if fn is power2n_2a and args.n > 20:
            print(f"{label}：跳過（n > 20，避免指數級重複計算）")
            continue
        start = perf_counter()
        result = fn(args.n)
        elapsed = perf_counter() - start
        assert result == expected, f"{label} 計算結果不正確"
        print(f"{label}：{result}，耗時 {elapsed:.8f} 秒，驗算通過")
    print("\n耗時會隨電腦及執行狀態改變，單次測量不能證明 Big O。")


if __name__ == "__main__":
    main()
