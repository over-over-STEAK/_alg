# -*- coding: utf-8 -*-
"""直接 py main.py 展示範例；也可指定文字或 UTF-8 檔案。"""
import argparse
from pathlib import Path
from BM import search as bm_search
from DP import search as dp_search


def show(text, pattern):
    bm = bm_search(text, pattern)
    dp = dp_search(text, pattern)
    print('文字：', repr(text))
    print('關鍵字：', repr(pattern))
    print('BM 結果：', bm)
    print('DP 結果：', dp)
    print('結果一致：', bm == dp)
    assert bm == dp, '兩種方法結果不一致'
    print()


def main():
    parser = argparse.ArgumentParser(description='單字搜尋：Boyer–Moore 與 DP')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--text', help='直接輸入搜尋文字')
    group.add_argument('--file', type=Path, help='讀取 UTF-8 檔案')
    parser.add_argument('--pattern', help='搜尋的關鍵字')
    args = parser.parse_args()
    print('=== 單字搜尋：Boyer–Moore vs. 動態規劃 ===')
    if args.text is None and args.file is None and args.pattern is None:
        for text, pattern in [('banana', 'ana'), ('金門大學在金門', '金門'),
                              ('hello world', 'xyz'), ('aaaaa', 'aaa')]:
            show(text, pattern)
        return
    if args.pattern is None or (args.text is None and args.file is None):
        parser.error('請同時指定 --pattern，以及 --text 或 --file')
    try:
        text = args.file.read_text(encoding='utf-8-sig') if args.file else args.text
    except (OSError, UnicodeError) as exc:
        parser.error(str(exc))
    show(text, args.pattern)


if __name__ == '__main__':
    main()
