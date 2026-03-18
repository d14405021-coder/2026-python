"""
UVA 10008 / ZeroJudge a001（易記版）

記憶口訣：
1. 全部轉大寫
2. 只數 A~Z
3. 26 格陣列累加
4. 依「次數降冪、字母升冪」輸出
"""

from __future__ import annotations

from typing import List, Tuple


def solve(raw_input: str) -> str:
    """
    讀取完整輸入字串並回傳輸出字串。

    輸入：
    - 第 1 行是 n
    - 接下來 n 行是要分析的文字

    輸出：
    - 每行格式為「字母 空白 次數」
    - 只輸出有出現過的字母
    """

    # splitlines() 會按照「每一行」切開，
    # 正好符合題目「第 1 行是 n，後面 n 行是文字」的結構。
    lines = raw_input.splitlines()
    if not lines:
        return ""

    # 第 1 行是要分析的行數 n。
    n = int(lines[0].strip())

    # 真正要分析的內容在第 2 行到第 n+1 行。
    # 用切片可避免索引越界；若輸入行數不足，會自動取到可用範圍。
    text_lines = lines[1 : 1 + n]

    # counts[0] 代表 A，counts[1] 代表 B ... counts[25] 代表 Z。
    # 這種陣列寫法比 dict 更容易背，也很省記憶體。
    counts = [0] * 26

    # 逐行、逐字元掃描所有輸入文字。
    # 複雜度 O(總字元數)，對題目規模完全足夠。
    for line in text_lines:
        for ch in line.upper():
            # 題目只計算英文字母，其他字元（數字、符號、空白）都忽略。
            if "A" <= ch <= "Z":
                # 例：
                # ch='A' -> idx=0
                # ch='C' -> idx=2
                # ch='Z' -> idx=25
                idx = ord(ch) - ord("A")
                counts[idx] += 1

    # 把有出現的字母整理成 (字母, 次數) 清單。
    # 沒出現的字母不輸出（題目要求）。
    result: List[Tuple[str, int]] = []
    for i in range(26):
        if counts[i] > 0:
            result.append((chr(ord("A") + i), counts[i]))

    # 排序規則對應題目：
    # 1) 次數由大到小 -> 用負號 -item[1] 做降冪
    # 2) 次數相同時字母由小到大 -> item[0]
    result.sort(key=lambda item: (-item[1], item[0]))

    # 最後組成指定格式：每列「字母 空白 次數」。
    return "\n".join(f"{ch} {cnt}" for ch, cnt in result)


def main() -> None:
    """
    OJ 入口：從標準輸入讀取資料並輸出結果。

    為什麼保留 main()：
    - 方便直接提交到線上評測（stdin -> stdout）
    - 也保留 solve() 供單元測試直接呼叫
    """

    import sys

    # 一次讀完整份輸入，再交給 solve 統一處理。
    raw_input = sys.stdin.read()
    if raw_input.strip():
        print(solve(raw_input))


if __name__ == "__main__":
    main()
