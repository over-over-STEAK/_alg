# -*- coding: utf-8 -*-
"""Boyer–Moore：壞字元與強好後綴規則，回傳所有匹配位置。"""


def good_suffix_shifts(pattern):
    """shift[j+1]：在位置 j 失配時的好後綴位移；shift[0]：完整匹配。"""
    m = len(pattern)
    shift = [0] * (m + 1)
    border = [0] * (m + 1)
    i, j = m, m + 1
    border[i] = j
    while i > 0:
        while j <= m and pattern[i - 1] != pattern[j - 1]:
            if shift[j] == 0:
                shift[j] = j - i
            j = border[j]
        i -= 1
        j -= 1
        border[i] = j
    j = border[0]
    for i in range(m + 1):
        if shift[i] == 0:
            shift[i] = j
        if i == j:
            j = border[j]
    return shift


def search(text, pattern):
    """大小寫敏感；以 Unicode 碼位計位置；空關鍵字匹配所有邊界。"""
    n, m = len(text), len(pattern)
    if m == 0:
        return list(range(n + 1))
    last = {char: i for i, char in enumerate(pattern)}
    shift = good_suffix_shifts(pattern)
    result = []
    start = 0
    while start <= n - m:
        j = m - 1
        # 從右往左比較，不呼叫 find 或正規表示式。
        while j >= 0 and pattern[j] == text[start + j]:
            j -= 1
        if j < 0:
            result.append(start)
            start += shift[0]  # 保留可能重疊的匹配
        else:
            bad = j - last.get(text[start + j], -1)
            start += max(1, bad, shift[j + 1])
    return result


if __name__ == '__main__':
    import sys
    text, pattern = sys.argv[1:3] if len(sys.argv) == 3 else ('banana', 'ana')
    print('Boyer–Moore 搜尋位置：', search(text, pattern))
