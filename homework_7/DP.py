# -*- coding: utf-8 -*-
"""連續字串搜尋的二維動態規劃，刻意保留完整表格方便學習。"""


def search(text, pattern):
    n, m = len(text), len(pattern)
    if m == 0:
        return list(range(n + 1))
    # dp[i][j]：text[:i] 與 pattern[:j] 結尾的最長共同連續長度。
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    result = []
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if text[i - 1] == pattern[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            # 不相同時維持 0，不可以跳過字元。
        if dp[i][m] == m:
            result.append(i - m)
    return result


if __name__ == '__main__':
    import sys
    text, pattern = sys.argv[1:3] if len(sys.argv) == 3 else ('banana', 'ana')
    print('動態規劃搜尋位置：', search(text, pattern))
