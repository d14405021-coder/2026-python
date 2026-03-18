"""
UVA 10008 / ZeroJudge a001

題意摘要：
- 讀入 n 行文字。
- 統計 A~Z 各字母出現次數（大小寫視為相同）。
- 依「次數由大到小」排序；若次數相同，依「字母由小到大」排序。
- 只輸出有出現過的字母。
"""

from __future__ import annotations

import string
from typing import Dict, List, Tuple


def count_letters(lines: List[str]) -> Dict[str, int]:
    """
    統計所有字母 A~Z 的出現次數（大小寫不分）。

    為什麼用 upper()：
    - 先轉大寫可把 A/a 視為同一類，邏輯最直觀。

    為什麼用 ascii_uppercase：
    - 題目只要求英文字母，數字、空白、標點都應忽略。
    """

    # freq 結構範例：{"A": 10, "B": 3, ...}
    # key 是大寫字母，value 是累計次數。
    freq: Dict[str, int] = {}

    # 外層逐行讀取，內層逐字元掃描。
    # 時間複雜度約 O(輸入總字元數)。
    for line in lines:
        for ch in line.upper():
            if ch in string.ascii_uppercase:
                freq[ch] = freq.get(ch, 0) + 1

    return freq


def sort_result(freq: Dict[str, int]) -> List[Tuple[str, int]]:
    """
    依題目規則排序：
    1. 次數降冪（大到小）
    2. 字母升冪（A 到 Z）
    """

    # 排序鍵說明：
    # -item[1]：把次數改成負值，讓 sorted 以升冪做出「次數降冪」效果。
    # item[0]：若次數相同，依字母自然升冪（A 到 Z）。
    return sorted(freq.items(), key=lambda item: (-item[1], item[0]))


def solve(raw_input: str) -> str:
    """
    接收完整輸入字串，回傳題目要求的輸出字串。

    輸入格式：
    - 第 1 行：n
    - 接下來 n 行：要分析的字串（可含空白）
    """

    # splitlines() 會保留「逐行」語意，這題第 1 行是 n，
    # 後面每行都要視為原始文本（可含空白），所以用它最直觀。
    lines = raw_input.splitlines()
    if not lines:
        return ""

    # 第 1 行是要分析的行數 n。
    n = int(lines[0].strip())

    # 若實際行數不足 n，切片仍安全，不會拋錯。
    # 在正式 OJ 測資通常不會發生，但保留此寫法可增加健壯性。
    text_lines = lines[1 : 1 + n]

    freq = count_letters(text_lines)
    ordered = sort_result(freq)

    # 輸出格式為「字母 空白 次數」，每筆一行。
    return "\n".join(f"{ch} {cnt}" for ch, cnt in ordered)


def main() -> None:
    """
    OJ 入口：從 stdin 讀資料，將結果印到 stdout。
    """

    import sys

    # 一次讀完整個輸入最簡潔，交由 solve 做格式解析。
    raw_input = sys.stdin.read()
    if raw_input.strip():
        print(solve(raw_input))


if __name__ == "__main__":
    main()
