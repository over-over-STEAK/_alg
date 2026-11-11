# 輸入前提：n 為非負整數。

def power2n_2b(n):
    """單分支遞迴：只計算一次子問題。"""
    if n == 0:
        return 1
    return 2 * power2n_2b(n - 1)


if __name__ == "__main__":
    print(power2n_2b(100))
