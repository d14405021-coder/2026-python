"""
UVA 10038 - Jolly Jumpers

題意摘要：
- 每行輸入一組序列：n a1 a2 ... an
- 若相鄰差絕對值剛好涵蓋 1 到 n-1（各一次），輸出 Jolly
- 否則輸出 Not jolly
"""

from __future__ import annotations

from typing import List


def is_jolly(sequence: List[int]) -> bool:
    """
    判斷整數序列是否為 jolly jumper。

    觀念：
    - 長度 n 的序列，會有 n-1 個相鄰差值。
    - 這些差值（取絕對值）必須剛好是 1..n-1。
    """

    n = len(sequence)
    if n <= 1:
        # 長度 0 或 1 時，沒有需要滿足的差值，視為 Jolly。
        return True

    seen = set()

    for i in range(1, n):
        d = abs(sequence[i] - sequence[i - 1])

        # 差值若超出合法範圍（1..n-1）可立即判定失敗。
        if d < 1 or d >= n:
            return False

        seen.add(d)

    # 必須恰好出現 n-1 種差值，才能完整覆蓋 1..n-1。
    return len(seen) == n - 1


def parse_line_to_sequence(line: str) -> List[int]:
    """
    把單行輸入轉成序列。

    格式：n a1 a2 ... an
    若該行資料不足，回傳空清單，交給 solve 略過。
    """

    parts = line.split()
    if not parts:
        return []

    n = int(parts[0])
    if len(parts) < n + 1:
        return []

    return list(map(int, parts[1 : 1 + n]))


def solve(raw_input: str) -> str:
    """
    逐行處理輸入，輸出每行是否為 Jolly。
    """

    outputs: List[str] = []

    for line in raw_input.splitlines():
        line = line.strip()
        if not line:
            continue

        seq = parse_line_to_sequence(line)
        if not seq:
            continue

        outputs.append("Jolly" if is_jolly(seq) else "Not jolly")

    return "\n".join(outputs)


def main() -> None:
    """OJ 入口：讀 stdin，寫 stdout。"""

    import sys

    raw_input = sys.stdin.read()
    result = solve(raw_input)
    if result:
        print(result)


if __name__ == "__main__":
    main()
