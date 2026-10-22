# -*- coding: utf-8 -*-
import itertools
import random
import unittest
from BM import search as bm
from DP import search as dp


def oracle(text, pattern):
    # 暴力法只用於測試，不是作業的兩個正式演算法。
    return [i for i in range(len(text) - len(pattern) + 1)
            if text[i:i + len(pattern)] == pattern]


class SearchTests(unittest.TestCase):
    def check_case(self, text, pattern, expected=None):
        expected = oracle(text, pattern) if expected is None else expected
        self.assertEqual(bm(text, pattern), expected, (text, pattern, 'BM'))
        self.assertEqual(dp(text, pattern), expected, (text, pattern, 'DP'))

    def test_examples_and_edges(self):
        for t, p, e in [('banana', 'ana', [1, 3]), ('金門大學在金門', '金門', [0, 5]),
                        ('aaaaa', 'aaa', [0, 1, 2]), ('', '', [0]),
                        ('abc', '', [0, 1, 2, 3]), ('', 'a', []),
                        ('a', 'abc', []), ('ABCabc', 'abc', [3]),
                        ('a\nb', '\n', [1]), ('🙂a🙂', '🙂', [0, 2])]:
            self.check_case(t, p, e)

    def test_exhaustive_binary(self):
        texts = [''.join(x) for n in range(8) for x in itertools.product('ab', repeat=n)]
        patterns = [''.join(x) for n in range(5) for x in itertools.product('ab', repeat=n)]
        for t in texts:
            for p in patterns:
                self.check_case(t, p)

    def test_seeded_random(self):
        rng = random.Random(20261021)
        for _ in range(500):
            t = ''.join(rng.choices('abc金門🙂', k=rng.randrange(80)))
            p = ''.join(rng.choices('abc金門🙂', k=rng.randrange(15)))
            self.check_case(t, p)


if __name__ == '__main__':
    unittest.main(verbosity=2)
