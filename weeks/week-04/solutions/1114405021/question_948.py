"""
UVA 948 / ZeroJudge c095 假幣問題

此程式提供：
1. 可提交到 OJ 的主程式入口（讀 stdin、寫 stdout）。
2. 可被單元測試匯入的核心函式（find_fake_coin、parse_cases、solve）。
"""

from __future__ import annotations

from typing import List, Sequence, Tuple

# 型別說明：
# - left / right：本次秤重放在左右盤的硬幣編號
# - result：秤重結果，可能是 '<'、'>'、'='
Weighing = Tuple[Sequence[int], Sequence[int], str]


def find_fake_coin(n: int, weighings: Sequence[Weighing]) -> int:
    """
    根據所有秤重紀錄，回傳唯一可能的假幣編號；若無法唯一判定，回傳 0。

    核心想法：
    - 對每枚硬幣各做兩個假設（偏重、偏輕）。
    - 只要其中一個假設能同時滿足所有秤重紀錄，該硬幣就仍是候選。
    - 最後候選硬幣若剛好只有一枚，回傳該編號；否則回傳 0。
    """

    # possible_coins 只記錄「硬幣編號」，不記錄重/輕。
    # 原因：題目只要求找出是哪一枚硬幣，不需要輸出偏重或偏輕。
    possible_coins = set()

    # 逐枚硬幣做假設：
    # - 先測 coin 偏重是否能解釋所有秤重
    # - 若不行，再測 coin 偏輕是否可行
    # 只要其中一種狀態可行，就把 coin 留在候選集合裡。
    for coin in range(1, n + 1):
        if _is_consistent(coin, is_heavier=True, weighings=weighings):
            possible_coins.add(coin)
            continue

        if _is_consistent(coin, is_heavier=False, weighings=weighings):
            possible_coins.add(coin)

    # 依題意：
    # - 只剩唯一候選硬幣 -> 可確定答案
    # - 0 個或多於 1 個候選 -> 無法唯一判定，輸出 0
    return next(iter(possible_coins)) if len(possible_coins) == 1 else 0


def _is_consistent(coin: int, is_heavier: bool, weighings: Sequence[Weighing]) -> bool:
    """
    檢查「假幣是 coin 且偏重/偏輕」這個假設是否與全部秤重結果一致。

    差值定義為：left_weight - right_weight。
    - 假幣在左盤：偏重 +1，偏輕 -1。
    - 假幣在右盤：效果相反。
    """

    # 用 +1 / -1 表示假幣相對真幣的重量差。
    # 偏重 => +1；偏輕 => -1。
    weight_delta = 1 if is_heavier else -1

    for left, right, result in weighings:
        # diff 代表「左盤總重 - 右盤總重」的相對差值。
        # 因為只有一枚假幣，其它真幣互相抵消，所以只需看該 coin 是否出現在左右盤。
        diff = 0

        if coin in left:
            diff += weight_delta
        if coin in right:
            diff -= weight_delta

        # 將計算出的 diff 與秤重符號做一致性檢查：
        # '<' 需要 diff < 0、'>' 需要 diff > 0、'=' 需要 diff == 0。
        # 任一筆不一致就可立即判定此假設失敗。
        if result == '<' and not (diff < 0):
            return False
        if result == '>' and not (diff > 0):
            return False
        if result == '=' and diff != 0:
            return False

    return True


def parse_cases(raw_input: str) -> List[Tuple[int, List[Weighing]]]:
    """
    解析題目輸入字串。

    題目包含空白列，因此用 split() 逐 token 解析可自動忽略多餘空白。
    """

    # split() 會把所有空白（空格、換行、空白列）都當作分隔符，
    # 能自然處理題目中的「測資間空白列」。
    tokens = raw_input.split()
    if not tokens:
        return []

    idx = 0
    t = int(tokens[idx])
    idx += 1

    cases: List[Tuple[int, List[Weighing]]] = []

    for _ in range(t):
        n = int(tokens[idx])
        k = int(tokens[idx + 1])
        idx += 2

        weighings: List[Weighing] = []

        for _ in range(k):
            # 每次秤重格式：
            # p, left_1...left_p, right_1...right_p, result_symbol
            p = int(tokens[idx])
            idx += 1

            left = list(map(int, tokens[idx : idx + p]))
            idx += p

            right = list(map(int, tokens[idx : idx + p]))
            idx += p

            result = tokens[idx]
            idx += 1

            weighings.append((left, right, result))

        cases.append((n, weighings))

    return cases


def solve(raw_input: str) -> str:
    """
    依題目格式輸出每組測資答案，組與組之間保留一個空白行。
    """

    outputs = []
    for n, weighings in parse_cases(raw_input):
        outputs.append(str(find_fake_coin(n, weighings)))

    # 題目要求測資之間印一個空白行，因此用雙換行串接。
    return "\n\n".join(outputs)


def main() -> None:
    """
    OJ 入口：從標準輸入讀入，將答案輸出到標準輸出。
    """

    import sys

    # 一次讀完整個 stdin，方便交給 parse_cases 統一處理。
    raw_input = sys.stdin.read()
    if not raw_input.strip():
        return

    print(solve(raw_input))


if __name__ == "__main__":
    main()
