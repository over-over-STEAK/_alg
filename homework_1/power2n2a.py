# 輸入前提：n 為非負整數。

def power2n_2a(n):
    """雙分支遞迴：每次重複計算相同的子問題。"""
    if n == 0:
        return 1
    return power2n_2a(n - 1) + power2n_2a(n - 1)


if __name__ == "__main__":
    print(power2n_2a(20))
