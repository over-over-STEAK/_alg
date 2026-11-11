"""用原始遞迴式核對精確公式；僅使用 Python 標準功能。"""

def recurrence(n, question):
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise ValueError('n 必須為正整數')
    if question not in (1, 2, 3, 4):
        raise ValueError('題號必須為 1～4')
    if question in (3, 4) and n & (n - 1):
        raise ValueError('第 3、4 題的 n 必須為 2 的整數次方')
    if n == 1:
        return 1
    if question == 1:
        return recurrence(n - 1, 1) + 8
    if question == 2:
        return 2 * recurrence(n - 1, 2) + 9
    if question == 3:
        return 2 * recurrence(n // 2, 3) + 1
    return recurrence(n // 2, 4) + 1


def exact(n, question):
    return (8 * n - 7, 10 * 2 ** (n - 1) - 9,
            2 * n - 1, n.bit_length())[question - 1]


def main():
    # 第1、2題驗算1至64；第3、4題驗算2的0至10次方。
    for question in (1, 2, 3, 4):
        inputs = range(1, 65) if question <= 2 else [2 ** k for k in range(11)]
        for n in inputs:
            actual = recurrence(n, question)
            expected = exact(n, question)
            assert actual == expected, (question, n, actual, expected)
    print('驗算通過：原始遞迴式與精確公式一致。')
    print(f'{"n":>4} {"第1題":>8} {"第2題":>12} {"第3題":>8} {"第4題":>8}')
    for n in (1, 2, 4, 8, 16):
        values = [recurrence(n, q) for q in (1, 2, 3, 4)]
        print(f'{n:4d} {values[0]:10d} {values[1]:14d} {values[2]:10d} {values[3]:10d}')


if __name__ == '__main__':
    main()
