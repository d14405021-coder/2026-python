# question_10057.py
# 說明：UVA 10057 A mid-summer night's dream. (仲夏夜之夢) 解答
#
# 解題思路：
# 1. 這題本質上是找「中位數 (Median)」，因為在數線上，要讓某個點到其他所有點的距離總和最小，
#    那個點必定是這群數字的「中位數」。
# 2. 如果資料個數 (n) 是奇數：中位數只有 1 個，剛好是最中間那個數。
#    如果資料個數 (n) 是偶數：中位數會有 2 個，也就是中間那兩個數 (稱它們為 mid1, mid2)。
#    事實上，介於 [mid1, mid2] 之間的所有整數，算出來的距離總和都會是一樣的最小值。
#
# 3. 題目要求輸出三個數字：
#    (1) 能得到最小值的最小的 A：如果 n 是奇數，就是中間那個數；如果 n 是偶數，就是左邊的中位數 (mid1)。
#    (2) 陣列中有多少個數字剛好等於「能產生最小值的 A 們」(也就是陣列中介於 mid1 和 mid2 之間的數字有幾個)。
#    (3) 有多少種不同的整數 A 可以產生最小值：也就是計算從 mid1 到 mid2 有幾個整數 (包含頭尾)，即 mid2 - mid1 + 1。
#
# 舉例：
# 陣列 [1, 2, 3, 4] -> 偶數長度，mid1=2, mid2=3。
# A 可以是 2 或 3，最小的 A=2。
# 陣列中有幾個數字剛好等於 A 們 (也就是 2, 3)？ 有 2 個 (數字2 和 數字3)。
# 總共有幾種 A 的選擇？ 3 - 2 + 1 = 2 種。

import sys


def solve_midsummer_dream(numbers):
    """
    計算並回傳題目的三個要求數字
    :param numbers: 整數陣列
    :return: (最小的A, 陣列中符合條件的數字個數, 可能的A的總數)
    """
    n = len(numbers)
    if n == 0:
        return None

    # 步驟 1：先將陣列由小到大排序
    numbers.sort()

    # 步驟 2：找中位數
    if n % 2 == 1:
        # 奇數長度，中位數只有一個
        mid_index = n // 2
        mid1 = numbers[mid_index]
        mid2 = numbers[mid_index]
    else:
        # 偶數長度，中位數有兩個
        # 因為索引從 0 開始，所以左邊的中位數是 (n//2)-1，右邊是 n//2
        mid_index1 = (n // 2) - 1
        mid_index2 = n // 2
        mid1 = numbers[mid_index1]
        mid2 = numbers[mid_index2]

    # 第一個答案：最小的 A，就是左邊的中位數 mid1
    ans_min_a = mid1

    # 第二個答案：陣列中，有多少個數字的值剛好落在 [mid1, mid2] 的範圍內
    # 這些數字就是原始輸入中能當作「能產生最小值的 A 們」的數字
    ans_count = sum(1 for x in numbers if mid1 <= x <= mid2)

    # 第三個答案：有多少種不同的整數 A 可以產生最小值
    # 也就是區間 [mid1, mid2] 包含幾個整數
    ans_possibilities = mid2 - mid1 + 1

    return (ans_min_a, ans_count, ans_possibilities)


def main():
    # 讀取所有輸入資料
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    idx = 0
    while idx < len(input_data):
        n = int(input_data[idx])
        idx += 1

        # 抓取接下來的 n 個數字
        numbers = [int(x) for x in input_data[idx : idx + n]]

        # 呼叫計算函式
        result = solve_midsummer_dream(numbers)

        if result:
            # 輸出三個結果，用空白隔開
            print(f"{result[0]} {result[1]} {result[2]}")

        # 更新指標
        idx += n


if __name__ == "__main__":
    main()
