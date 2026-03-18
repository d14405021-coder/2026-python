"""
UVA 10019（題敘對應 Hashmat 差值題）- 易記版

這版目標是「最短、最好記」：
1. 每讀到一行就拆成兩個數字
2. 直接算 abs(a - b)
3. 把答案存起來，最後逐行輸出

記憶口訣：
讀一行、拆兩數、取絕對差、印一行。
"""

from __future__ import annotations

from typing import List


def solve(raw_input: str) -> str:
    """
    將整份輸入字串轉為答案字串。

    詳細流程說明：
    - 題目是 EOF 型輸入，代表你不知道有幾組資料；
      所以最自然的做法是「把所有行都巡過一遍」。
    - 每行應該有兩個整數，分別代表兩方士兵數。
    - 我們只要輸出兩者差距的正值，也就是 abs(a - b)。
    """

    outputs: List[str] = []

    # splitlines() 會把整份輸入切成每一行，
    # 非常適合這題「一行一組資料」的格式。
    for line in raw_input.splitlines():
        line = line.strip()

        # 若遇到空白行，直接跳過，避免 split 失敗。
        if not line:
            continue

        # 每行固定兩個數字：a b
        a_str, b_str = line.split()
        a = int(a_str)
        b = int(b_str)

        # abs() 可確保輸出一定是正差值。
        outputs.append(str(abs(a - b)))

    # 題目要求每組答案一行，因此用換行接起來。
    return "\n".join(outputs)


def main() -> None:
    """
    線上評測入口：
    - 從標準輸入讀取全部內容
    - 呼叫 solve 計算
    - 輸出結果
    """

    import sys

    raw_input = sys.stdin.read()
    if raw_input.strip():
        print(solve(raw_input))


if __name__ == "__main__":
    main()
