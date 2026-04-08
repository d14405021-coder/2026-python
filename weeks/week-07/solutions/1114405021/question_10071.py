# question_10071.py
# 說明：UVA 10071 / ZeroJudge a064 (a+b+c+d+e=f) 解答
#
# 解題思路：
# 1. 題目要求找出所有滿足 a + b + c + d + e = f 的組合數量，且這六個變數都從集合 S 中挑選。
# 2. 如果直接使用 6 層的巢狀迴圈 (O(N^6))，當 N=100 時，計算次數高達 10^12，一定會超時 (TLE)。
# 3. 這是經典的「相向搜尋法 (Meet in the Middle)」題型：
#    我們可以將等式移項，變成： a + b + c = f - d - e
# 4. 這樣一來，等式被切成了「左半邊 (a+b+c)」和「右半邊 (f-d-e)」。
#    左半邊只有 3 個變數，右半邊也只有 3 個變數。
#    時間複雜度從 O(N^6) 大幅降為 O(N^3) + O(N^3) = O(N^3)，也就是最多 1,000,000 次運算，非常快。
# 5. 實作上，我們可以先用 3 層迴圈算出所有可能的「左半邊 (a+b+c)」的值，
#    並用陣列記錄每個值出現的「次數」。
#    因為 S 的元素介於 -30000 到 30000 之間，所以 3 個元素相加的範圍是 -90000 到 90000。
#    我們可以把陣列大小設為 180005，並將所有的值加上 90000 (平移位移量 Offset)，避免出現負數索引。
# 6. 接著再跑一次 3 層迴圈，算出「右半邊 (f-d-e)」，並把對應的左半邊次數加到總和中。

import sys


def solve_equation(S):
    """
    計算滿足 a + b + c = f - d - e 的組合總數
    :param S: 包含 N 個整數的陣列
    :return: 組合總數
    """
    n = len(S)
    if n == 0:
        return 0

    # a+b+c 的範圍是 -90000 ~ 90000
    # 為了讓陣列索引不為負數，我們設定一個平移量 OFFSET
    OFFSET = 90000
    # 建立一個足夠大的陣列來存放次數 (180005 大於 90000 - (-90000) + 1)
    # Python 中一維陣列的存取速度比字典 (Dict) 更快
    counts = [0] * 180005

    # 步驟 1：計算左半邊 (a + b + c) 的所有可能值與出現次數
    for a in S:
        for b in S:
            for c in S:
                # 加上平移量，將值映射到陣列索引
                val = a + b + c + OFFSET
                counts[val] += 1

    # 步驟 2：計算右半邊 (f - d - e)，並把符合的左半邊次數加起來
    ans = 0
    for f in S:
        for d in S:
            for e in S:
                val = f - d - e + OFFSET
                ans += counts[val]

    return ans


def main():
    # 讀取所有輸入資料
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    # 本題可能有多組測試資料，這裡用指標追蹤
    idx = 0
    while idx < len(input_data):
        n = int(input_data[idx])
        idx += 1

        # 讀取集合 S 中的 N 個整數
        S = []
        for _ in range(n):
            S.append(int(input_data[idx]))
            idx += 1

        # 呼叫計算函式
        result = solve_equation(S)

        # 輸出最終的組合總數量
        print(result)


if __name__ == "__main__":
    main()
