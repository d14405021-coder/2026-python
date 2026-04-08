# question_10062.py
# 說明：UVA 10062 / POJ 2182 / ZeroJudge a055 (Lost Cows) 解答
#
# 解題思路：
# 1. 題目給定 N 頭牛 (編號 1~N)，以及從第 2 頭到第 N 頭牛，每頭牛前面「編號比它小」的數量。
# 2. 如果我們從「最後一頭牛」開始往前推算，事情會變得很簡單：
#    對於最後一頭牛，如果牠前面有 K 頭比牠小的牛，
#    這意味著牠的編號一定是目前「剩下可用編號」中的第 K+1 小的數字。
# 3. 決定好最後一頭牛的編號後，我們就把這個數字從可用清單中「移除」。
#    接著處理倒數第二頭牛，依此類推，直到第一頭牛。
# 4. 為了讓時間複雜度在 N=80000 時不會超時 (Time Limit Exceeded)，
#    我們需要使用「樹狀數組 (Binary Indexed Tree, BIT)」加上「二分搜尋法 (Binary Search)」
#    來達成 O(N log^2 N) 的時間複雜度，快速找出第 K+1 小的可用數字。

import sys


class FenwickTree:
    def __init__(self, size):
        self.size = size
        # 初始時每個編號 (1~N) 都是可用的，所以初始化為 1
        # 但在建構樹狀數組時，我們要遵守 lowbit 規則來初始化
        self.tree = [0] * (size + 1)
        for i in range(1, size + 1):
            self.add(i, 1)

    def add(self, i, delta):
        # 單點修改：將第 i 個位置的值加上 delta (用來標記編號是否被用過)
        while i <= self.size:
            self.tree[i] += delta
            i += i & (-i)

    def query(self, i):
        # 前綴和查詢：回傳 1~i 之間有幾個數字是「還可用」的
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & (-i)
        return s


def solve_lost_cows(n, smaller_counts):
    """
    計算每頭牛的正確編號
    :param n: 牛的總數
    :param smaller_counts: 長度為 n 的陣列，表示每頭牛前面有幾頭比牠小 (第一頭固定為 0)
    :return: 正確順序的牛編號列表
    """
    # 建立樹狀數組，大小為 n，用來記錄 1~N 每個數字是否還沒被用過
    bit = FenwickTree(n)

    # 準備一個存放答案的陣列，長度為 n
    ans = [0] * n

    # 從最後一頭牛開始「由後往前」推算
    for i in range(n - 1, -1, -1):
        # 牠的編號必須是目前可用數字中的第 K 小 (K = 前面比牠小的數量 + 1)
        target_k = smaller_counts[i] + 1

        # 使用二分搜尋法在 1~N 尋找第 target_k 小的可用數字
        left, right = 1, n
        chosen_id = 1

        while left <= right:
            mid = (left + right) // 2
            # 查詢 1~mid 之間有幾個可用的數字
            available_count = bit.query(mid)

            if available_count >= target_k:
                # 數量足夠，答案可能在左半邊或就是 mid
                chosen_id = mid
                right = mid - 1
            else:
                # 數量不夠，答案一定在右半邊
                left = mid + 1

        # 找到這頭牛的編號了，記錄到答案陣列中
        ans[i] = chosen_id

        # 將這個編號從可用清單中移除 (也就是在樹狀數組中 -1)
        bit.add(chosen_id, -1)

    return ans


def solve():
    # 讀取所有標準輸入
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    # 第一個數字是 N
    n = int(input_data[0])

    # 建立 smaller_counts 陣列
    # 第一頭牛前面沒有比牠小的，所以預設為 0
    smaller_counts = [0] * n

    # 從第二頭牛開始讀取資料 (總共讀取 N-1 個數字)
    for i in range(1, n):
        smaller_counts[i] = int(input_data[i])

    # 取得結果
    ans = solve_lost_cows(n, smaller_counts)

    # 逐行輸出每頭牛的編號
    for cow_id in ans:
        print(cow_id)


if __name__ == "__main__":
    solve()
