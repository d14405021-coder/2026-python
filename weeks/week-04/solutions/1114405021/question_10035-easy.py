"""
UVA 10035 - Primary Arithmetic（易記版）

這版主打「好記憶」：
1. 先把兩個數字字串左側補 0，補到同長度
2. 從右到左逐位相加
3. 若該位總和 >= 10，進位次數 +1，並把 carry 設為 1
4. 組出題目要求句型

記憶口訣：
補零對齊 -> 右到左加 -> 看有沒有 >= 10 -> 統計 carry 次數
"""

from __future__ import annotations

from typing import List


def count_carries_easy(a: int, b: int) -> int:
    """
    易記版進位計算：用字串補零後逐位相加。

    為什麼這樣好背：
    - 和小學直式加法完全同一個畫面。
    - 不需要一直做 %10、//10，對初學者通常更直觀。
    """

    sa = str(a)
    sb = str(b)

    # 讓兩個字串長度一致，才能直接用同一個索引逐位對齊。
    max_len = max(len(sa), len(sb))
    sa = sa.zfill(max_len)
    sb = sb.zfill(max_len)

    carry = 0
    carry_count = 0

    # 從最右邊（個位）一路往左邊（高位）處理。
    for i in range(max_len - 1, -1, -1):
        digit_a = ord(sa[i]) - ord("0")
        digit_b = ord(sb[i]) - ord("0")

        s = digit_a + digit_b + carry

        if s >= 10:
            carry = 1
            carry_count += 1
        else:
            carry = 0

    return carry_count


def to_message(carry_count: int) -> str:
    """把進位次數轉成題目要求的英文句型。"""

    if carry_count == 0:
        return "No carry operation."
    if carry_count == 1:
        return "1 carry operation."
    return f"{carry_count} carry operations."


def solve(raw_input: str) -> str:
    """
    把整份輸入字串轉為輸出字串。

    輸入重點：
    - 每行兩個整數
    - 讀到 0 0 立刻停止
    """

    outputs: List[str] = []

    for line in raw_input.splitlines():
        line = line.strip()
        if not line:
            continue

        a_str, b_str = line.split()
        a = int(a_str)
        b = int(b_str)

        if a == 0 and b == 0:
            break

        outputs.append(to_message(count_carries_easy(a, b)))

    return "\n".join(outputs)


def main() -> None:
    """
    線上評測入口：
    - 從 stdin 讀全部資料
    - 呼叫 solve 計算
    - 把結果印到 stdout
    """

    import sys

    raw_input = sys.stdin.read()
    result = solve(raw_input)
    if result:
        print(result)


if __name__ == "__main__":
    main()
