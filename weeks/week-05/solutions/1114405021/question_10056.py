# question_10056.py
# 說明：UVA 10056 What is the Probability? (獲勝機率) 解答
#
# 解題思路：
# 這是一個典型的「無窮等比級數」機率問題。
# 假設有 N 個玩家，成功的機率為 p，失敗的機率為 q = 1 - p。
#
# 第 i 個玩家要獲勝，可能有以下幾種情況：
# 1. 在第 1 輪就獲勝：
#    前 i-1 個人都失敗了，輪到他時成功了。
#    機率為：q^(i-1) * p
#
# 2. 在第 2 輪才獲勝：
#    第 1 輪所有 N 個人都失敗，進入第 2 輪。
#    第 2 輪前 i-1 個人也失敗，輪到他時成功。
#    機率為：(q^N) * q^(i-1) * p
#
# 3. 在第 k 輪獲勝：
#    機率為：(q^N)^(k-1) * q^(i-1) * p
#
# 將所有輪次的獲勝機率加總起來，這是一個首項 a = q^(i-1) * p，
# 公比 r = q^N 的無窮等比級數。
#
# 根據無窮等比級數的求和公式：S = a / (1 - r)
# 也就是：總機率 = [ q^(i-1) * p ] / [ 1 - q^N ]
#
# 特別注意：
# - 若 p == 0，代表永遠不可能成功，任何人的獲勝機率都是 0。
# - 輸出需要精確到小數點後 4 位 (0.0000)。

import sys


def calculate_winning_probability(n, p, i):
    """
    計算第 i 個玩家獲勝的機率
    :param n: 玩家總人數
    :param p: 單次擲骰成功的機率
    :param i: 第幾個玩家
    :return: 獲勝機率 (精確到小數點後 4 位)
    """
    # 如果成功機率為 0，則不可能獲勝
    if p == 0:
        return 0.0

    # q 是失敗的機率
    q = 1.0 - p

    # 根據無窮等比級數公式：
    # 首項 a = 前 i-1 人失敗 * 自己成功 = (q ** (i - 1)) * p
    # 公比 r = N 個人全失敗 = q ** N
    # 總和 S = a / (1 - r)

    first_term = (q ** (i - 1)) * p
    common_ratio = q**n

    # 避免分母為 0 (理論上若 p > 0，則 q < 1，q^N 必定 < 1)
    if common_ratio == 1.0:
        return 0.0

    probability = first_term / (1.0 - common_ratio)

    return probability


def solve():
    # 讀取所有標準輸入的資料，並以空白或換行符號分割
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    # 第一個數字為測資筆數
    test_cases = int(input_data[0])
    idx = 1

    # 處理每一筆測試資料
    for _ in range(test_cases):
        if idx >= len(input_data):
            break

        n = int(input_data[idx])  # 玩家數量 N
        p = float(input_data[idx + 1])  # 成功機率 P
        i = int(input_data[idx + 2])  # 玩家編號 I
        idx += 3

        # 計算機率
        ans = calculate_winning_probability(n, p, i)

        # 輸出到小數點後 4 位
        print(f"{ans:.4f}")


if __name__ == "__main__":
    solve()
