# question_10057-easy.py
# 說明：UVA 10057 A mid-summer night's dream 的「簡化好記版」解答
# 針對上機考試設計，不使用過多的函式，直接迴圈寫到底。

import sys


def solve():
    data = sys.stdin.read().split()
    if not data:
        return

    idx = 0
    while idx < len(data):
        n = int(data[idx])
        idx += 1

        # 讀取接下來 n 個數字並排序
        nums = [int(x) for x in data[idx : idx + n]]
        nums.sort()

        # 尋找中位數
        if n % 2 == 1:
            # 奇數，只有一個中間值
            mid1 = nums[n // 2]
            mid2 = nums[n // 2]
        else:
            # 偶數，取中間的兩個值
            mid1 = nums[(n // 2) - 1]
            mid2 = nums[n // 2]

        # 答案 1：最小的中位數 (密碼 A)
        ans1 = mid1

        # 答案 2：原始陣列中，有幾個數字可以當作密碼 A (落在 mid1 和 mid2 之間)
        ans2 = 0
        for x in nums:
            if mid1 <= x <= mid2:
                ans2 += 1

        # 答案 3：總共有幾種可能的密碼 A (就是 mid1 到 mid2 的整數個數)
        ans3 = mid2 - mid1 + 1

        print(f"{ans1} {ans2} {ans3}")

        # 更新讀取指標
        idx += n


if __name__ == "__main__":
    solve()
