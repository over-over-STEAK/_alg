# -*- coding: utf-8 -*-
"""計時包含預處理與輸出位置建立；不含印出、I/O。記憶體另跑。"""
import platform
import random
import statistics
import time
import tracemalloc
from BM import search as bm
from DP import search as dp


def main():
    rng = random.Random(42)
    print('Python:', platform.python_version(), '平台:', platform.platform())
    print('每組 5 次，中位數；記憶體為 tracemalloc 追蹤的 Python 配置峰值。')
    print('情境,n,m,匹配數,方法,時間ms,峰值KiB')
    for n in (1000, 5000, 10000):
        random_text = ''.join(rng.choices('abcdefghijklmnopqrstuvwxyz', k=n))
        for name, text, pattern in [('一般文字', random_text, 'algorithm'),
                                     ('大量重疊', 'a' * n, 'a' * 20),
                                     ('無匹配', 'a' * n, 'b' + 'a' * 19)]:
            expected = [i for i in range(len(text) - len(pattern) + 1)
                        if text[i:i + len(pattern)] == pattern]
            for label, fn in [('BM', bm), ('DP', dp)]:
                assert fn(text, pattern) == expected
                times = []
                for _ in range(5):
                    start = time.perf_counter()
                    result = fn(text, pattern)
                    times.append((time.perf_counter() - start) * 1000)
                tracemalloc.start()
                fn(text, pattern)
                _, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                print(f'{name},{n},{len(pattern)},{len(result)},{label},'
                      f'{statistics.median(times):.4f},{peak / 1024:.2f}')


if __name__ == '__main__':
    main()
