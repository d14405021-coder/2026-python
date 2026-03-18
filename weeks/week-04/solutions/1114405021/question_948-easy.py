"""
UVA 948 / ZeroJudge c095 假幣問題（易記版）

這一版刻意用「步驟式、好記憶」的寫法：
1. 先用 '=' 的秤重把真幣全部標記出來。
2. 剩下沒被標記的才可能是假幣。
3. 對每個可疑硬幣，分別假設它「偏重」或「偏輕」，檢查是否能解釋所有秤重。
4. 若最後只剩一枚硬幣可行，就輸出它；否則輸出 0。
"""

from __future__ import annotations

from typing import List, Sequence, Tuple

Weighing = Tuple[Sequence[int], Sequence[int], str]


def parse_cases(raw_input: str) -> List[Tuple[int, List[Weighing]]]:
    """
    把題目輸入解析成 (n, weighings) 的案例清單。

    這題輸入在測資之間可能有空白列，若用逐行硬切常容易踩格式坑。
    這裡改用 split() 做 token 解析，所有空白（空格、換行、空白列）都會被
    視為分隔符，因此資料結構更穩定、也更容易除錯。
    """

    # 先把輸入切成 token，後面用索引 idx 逐一讀取。
    tokens = raw_input.split()
    if not tokens:
        return []

    # 第一個數字是測資組數 t。
    t = int(tokens[0])
    idx = 1
    cases: List[Tuple[int, List[Weighing]]] = []

    for _ in range(t):
        # 每組先讀 n（硬幣數）與 k（秤重次數）。
        n = int(tokens[idx])
        k = int(tokens[idx + 1])
        idx += 2

        weighings: List[Weighing] = []
        for _ in range(k):
            # 每次秤重格式：
            # p left1...leftp right1...rightp result
            # 其中 p 代表左右兩盤各放幾枚硬幣。
            p = int(tokens[idx])
            idx += 1

            # 讀左盤 p 枚、右盤 p 枚。
            left = list(map(int, tokens[idx : idx + p]))
            idx += p

            right = list(map(int, tokens[idx : idx + p]))
            idx += p

            # result 只會是 '<'、'>'、'=' 三者之一。
            result = tokens[idx]
            idx += 1

            weighings.append((left, right, result))

        cases.append((n, weighings))

    return cases


def _fits_one_weighing(coin: int, state: str, left: Sequence[int], right: Sequence[int], result: str) -> bool:
    """
    檢查「coin 是假幣且狀態為 state（heavy/light）」是否符合單次秤重。

    教學理解：
    - '='：兩邊一樣重，表示假幣不可能在這次上秤的左右盤。
    - '<'：左邊較輕，可能情況只有兩種：
      1) 假幣在左盤且偏輕
      2) 假幣在右盤且偏重
    - '>'：左邊較重，可能情況也只有兩種：
      1) 假幣在左盤且偏重
      2) 假幣在右盤且偏輕
    """

    in_left = coin in left
    in_right = coin in right

    if result == '=':
        # 兩盤平衡 => 假幣不可能出現在任一盤。
        # 只要 coin 有出現在左或右，就和平衡結果衝突。
        return (not in_left) and (not in_right)

    # 若秤重不平衡，假幣一定要出現在這次的某一側，否則無法造成重量差。
    if (not in_left) and (not in_right):
        return False

    if result == '<':
        return (in_left and state == "light") or (in_right and state == "heavy")

    # result == '>'
    return (in_left and state == "heavy") or (in_right and state == "light")


def find_fake_coin_easy(n: int, weighings: Sequence[Weighing]) -> int:
    """
    易記版核心：先排除真幣，再驗證可疑硬幣。

    記憶口訣：
    1. '=' 先劃掉真幣
    2. 剩下當嫌疑
    3. 每個嫌疑測 heavy / light 兩種身份
    4. 只剩唯一嫌疑就輸出，否則 0
    """

    # 第一步：用 '=' 直接收集真幣。
    # 理由：若左右平衡，代表這次上秤的硬幣全部都是真幣。
    genuine = set()
    for left, right, result in weighings:
        if result == '=':
            genuine.update(left)
            genuine.update(right)

    # 第二步：沒被證明是真幣的，才列為可疑。
    # 注意：可疑不等於一定是假幣，只是「尚未被排除」。
    suspects = [coin for coin in range(1, n + 1) if coin not in genuine]

    # 第三步：檢查每個可疑硬幣是否存在可行狀態（偏重或偏輕）。
    candidates = []
    for coin in suspects:
        # can_heavy / can_light 表示該假設是否仍存活。
        # 一開始都先假設可行，再被秤重逐步淘汰。
        can_heavy = True
        can_light = True

        for left, right, result in weighings:
            # heavy 假設若和任一秤重衝突，就標記為 False。
            if can_heavy and (not _fits_one_weighing(coin, "heavy", left, right, result)):
                can_heavy = False
            # light 假設同理。
            if can_light and (not _fits_one_weighing(coin, "light", left, right, result)):
                can_light = False

            # 兩種狀態都失敗，代表這枚硬幣不可能是假幣，可提前結束。
            # 這個 early break 可減少不必要檢查，資料大時會更有效率。
            if (not can_heavy) and (not can_light):
                break

        # 只要 heavy 或 light 至少一種能成立，這枚硬幣就仍是最終候選。
        if can_heavy or can_light:
            candidates.append(coin)

    # 依題意：只能唯一判定時輸出硬幣編號，否則輸出 0。
    return candidates[0] if len(candidates) == 1 else 0


def solve(raw_input: str) -> str:
    """
    把所有測資答案組裝成輸出字串。

    題目規定每組答案間要空一行，因此使用 "\n\n" 串接。
    """

    outputs: List[str] = []
    for n, weighings in parse_cases(raw_input):
        outputs.append(str(find_fake_coin_easy(n, weighings)))

    return "\n\n".join(outputs)


def main() -> None:
    """
    OJ 入口：讀 stdin，寫 stdout。

    這種寫法可直接提交線上評測；
    同時 solve 也能被測試程式單獨呼叫，方便做單元測試。
    """

    import sys

    raw_input = sys.stdin.read()
    if raw_input.strip():
        print(solve(raw_input))


if __name__ == "__main__":
    main()
