# question_10056-easy.py
# 說明：UVA 10056 What is the Probability? 的「簡化好記版」解答
# 針對考試時快速寫出，省略函式封裝，直接套用無窮等比級數公式。

import sys


def solve():
    # 1. 一次性讀取所有輸入資料
    data = sys.stdin.read().split()
    if not data:
        return

    # 第一個數字是測資數量，我們從第二個數字開始讀取
    idx = 1

    # 2. 逐筆處理測試資料
    while idx < len(data):
        n = int(data[idx])  # 總人數
        p = float(data[idx + 1])  # 成功機率
        i = int(data[idx + 2])  # 第幾個玩家
        idx += 3  # 更新指標到下一組

        # 3. 如果成功機率是 0，代表沒人能贏
        if p == 0:
            print("0.0000")
            continue

        # 4. 計算失敗機率 q
        q = 1.0 - p

        # 5. 套用無窮等比級數公式
        # 首項 a = 第 i 個人第一輪就贏 = 前面 i-1 人都失敗 * 自己成功
        a = (q ** (i - 1)) * p

        # 公比 r = 這一輪沒人贏，全部 N 人都失敗
        r = q**n

        # 總和公式 S = a / (1 - r)
        ans = a / (1.0 - r)

        # 6. 輸出精確到小數點後四位
        print(f"{ans:.4f}")


if __name__ == "__main__":
    solve()
