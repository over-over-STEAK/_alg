# 輸入前提：n 為非負整數。

def power2n_3(n, memo=None):
    """記憶化：每次頂層呼叫建立新快取，遞迴內共用快取。"""
    if memo is None:
        memo = {}
    if n == 0:
        return 1
    if n in memo:
        return memo[n]
    memo[n] = power2n_3(n - 1, memo) + power2n_3(n - 1, memo)
    return memo[n]


if __name__ == "__main__":
    print(power2n_3(100))
