"""
UVA 10038 - Jolly Jumpers（易記版）

這版強調「容易記」：
1. 算每一對相鄰數字的差絕對值 d
2. 用布林陣列 seen[d] 記錄 d 是否出現
3. 最後檢查 1..n-1 是否全部出現

記憶口訣：
算差值 -> 做記號 -> 檢查 1 到 n-1 全到齊。
"""

from __future__ import annotations

from typing import List


def is_jolly_easy(sequence: List[int]) -> bool:
    """
    用布林陣列方式判斷是否為 Jolly。

    詳細理解：
    - 長度 n 的序列，合法差值只能是 1..n-1。
    - 我們建立長度 n 的 seen，索引 0 不用，索引 1..n-1 代表差值是否出現。
    - 只要某個差值超出範圍，或最後有缺任何差值，就不是 Jolly。
    """

    n = len(sequence)
    if n <= 1:
        # 一個數字（或空序列）沒有相鄰差值，定義上可視為 Jolly。
        return True

    # seen[d] = True 表示差值 d 曾出現。
    seen = [False] * n

    for i in range(1, n):
        d = abs(sequence[i] - sequence[i - 1])

        # 合法差值範圍只能在 1..n-1。
        if d < 1 or d >= n:
            return False

        seen[d] = True

    # 檢查 1..n-1 是否全部都出現。
    for d in range(1, n):
        if not seen[d]:
            return False

    return True


def parse_line_to_sequence(line: str) -> List[int]:
    """
    解析單行：n a1 a2 ... an

    若資料不足或空行，回傳空清單，讓上層流程可安全略過。
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
    將整份輸入字串轉成輸出字串。

    輸入可能有多行，每行各自判斷一次 Jolly / Not jolly。
    """

    outputs: List[str] = []

    for line in raw_input.splitlines():
        line = line.strip()
        if not line:
            continue

        seq = parse_line_to_sequence(line)
        if not seq:
            continue

        outputs.append("Jolly" if is_jolly_easy(seq) else "Not jolly")

    return "\n".join(outputs)


def main() -> None:
    """
    線上評測入口：
    - 讀 stdin
    - 呼叫 solve
    - 印出結果
    """

    import sys

    raw_input = sys.stdin.read()
    result = solve(raw_input)
    if result:
        print(result)


if __name__ == "__main__":
    main()
