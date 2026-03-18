"""
UVA 10019（依題敘實際為 Hashmat 差值題）

題意精簡：
- 每行輸入兩個整數 a, b（直到 EOF）。
- 輸出 |a - b|。

這題重點非常單純：
1. 逐行讀到 EOF
2. 取兩數絕對差
3. 逐行輸出
"""

from __future__ import annotations

from typing import List


def diff(a: int, b: int) -> int:
    """
    回傳兩整數的正差值（絕對值）。

    使用 abs(a - b) 可以同時涵蓋：
    - Hashmat 人數較少
    - Hashmat 人數較多（雖題目通常保證不會，但程式可容錯）
    """

    return abs(a - b)


def solve(raw_input: str) -> str:
    """
    將原始輸入字串轉換為題目要求輸出字串。

    輸入格式（直到 EOF）：
    a b
    a b
    ...

    輸出格式：
    每行一個整數（該行兩數差的絕對值）。
    """

    outputs: List[str] = []

    for line in raw_input.splitlines():
        line = line.strip()
        if not line:
            # 遇到空白行時直接略過，讓解析更穩健。
            continue

        a_str, b_str = line.split()
        a = int(a_str)
        b = int(b_str)

        outputs.append(str(diff(a, b)))

    return "\n".join(outputs)


def main() -> None:
    """OJ 入口：讀 stdin，寫 stdout。"""

    import sys

    raw_input = sys.stdin.read()
    if raw_input.strip():
        print(solve(raw_input))


if __name__ == "__main__":
    main()
