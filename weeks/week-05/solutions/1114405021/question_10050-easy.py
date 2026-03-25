# question_10050-easy.py
# 說明：UVA 10050 Hartals 的「簡化好記版」解答
# 針對考試或快速解題時使用，將邏輯壓平在同一個函式中。

import sys


def solve():
    # 1. 一次性讀取所有輸入資料並切割
    data = sys.stdin.read().split()
    if not data:
        return

    idx = 1  # 略過 data[0] (測資筆數)，直接從第一筆測資開始

    # 2. 當還沒讀完所有資料時，繼續迴圈
    while idx < len(data):
        n = int(data[idx])  # 總天數 N
        p = int(data[idx + 1])  # 政黨數量 P

        # 3. 取得這 p 個政黨的罷會頻率列表
        # data[idx+2 : idx+2+p] 代表往後抓 p 個數字
        hartals = [int(x) for x in data[idx + 2 : idx + 2 + p]]

        lost_days = 0

        # 4. 模擬每一天 (從 1 到 n)
        for day in range(1, n + 1):
            # 星期五 (day%7 == 6) 和 星期六 (day%7 == 0) 是假日，不扣工作天
            if day % 7 == 6 or day % 7 == 0:
                continue

            # 檢查今天是否有任何一個政黨要罷會
            for h in hartals:
                if day % h == 0:  # 這天剛好是該政黨罷會頻率的倍數
                    lost_days += 1  # 損失一個工作天
                    break  # 只要有人罷會就確定損失了，不用再檢查其他政黨

        # 輸出損失的工作天數
        print(lost_days)

        # 5. 更新指標，跳到下一組測資的位置
        # 包含了 n(1個), p(1個) 以及所有政黨頻率(p個)
        idx += 2 + p


if __name__ == "__main__":
    solve()
