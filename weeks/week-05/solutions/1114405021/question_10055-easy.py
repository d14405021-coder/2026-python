# question_10055-easy.py
# 說明：UVA 10055 (ZJ a048) 單調函數增減性 的「簡化好記版」解答
# 針對考試時若忘了怎麼寫 BIT (樹狀數組)，且測資不大時的備用方案 (O(N) 查詢)。
# 注意：在嚴格的 ZeroJudge 系統中，N, Q 高達 20萬，此方法可能會 TLE (Time Limit Exceeded)。
# 但此寫法最好記、邏輯最直覺，適合作為思路的基礎原型。

import sys


def solve():
    data = sys.stdin.read().split()
    if not data:
        return

    idx = 0
    while idx < len(data):
        n = int(data[idx])
        q = int(data[idx + 1])
        idx += 2

        # 建立一個長度為 N+1 的陣列 (索引 1~N)
        # 0 表示增函數，1 表示減函數，初始全為 0
        funcs = [0] * (n + 1)

        # 處理 Q 筆操作
        for _ in range(q):
            v = int(data[idx])

            if v == 1:
                # 反轉 f_i
                i = int(data[idx + 1])
                idx += 2
                # 0 變 1，1 變 0，可以使用 ^ 1 (XOR) 達成反轉
                funcs[i] ^= 1

            elif v == 2:
                # 查詢區間 [L, R]
                l = int(data[idx + 1])
                r = int(data[idx + 2])
                idx += 3

                # 計算這段區間內的總和 (也就是減函數的數量)
                # 使用 sum() 把 L 到 R 的陣列切片加起來
                # (注意 Python 的切片是包含前面、不含後面，所以要 r+1)
                total_negatives = sum(funcs[l : r + 1])

                # 若減函數數量是奇數 ( % 2 == 1 )，則複合結果是減函數(輸出1)
                # 若為偶數，複合結果為增函數(輸出0)
                print(total_negatives % 2)


if __name__ == "__main__":
    solve()
