import unittest

# 定義一個函數來計算單個數字的 cycle length
def calculate_cycle_length(n, memo):
    """
    計算 Collatz 序列的 cycle length，使用記憶化來優化效能。

    參數:
    n (int): 起始數字
    memo (dict): 記憶化字典，用來儲存已計算過的 cycle length

    返回:
    int: cycle length
    """
    if n in memo:
        return memo[n]
    original_n = n
    count = 1  # 包含起始的 n
    while n != 1:
        if n in memo:
            count += memo[n] - 1  # 減去重複的 1
            break
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        count += 1
    memo[original_n] = count
    return count

# 定義主要函數來找到區間內的最大 cycle length
def find_max_cycle_length(i, j):
    """
    找到從 i 到 j 之間（包含 i 和 j）的數字中，最大的 cycle length。

    參數:
    i (int): 起始數字
    j (int): 結束數字

    返回:
    int: 最大 cycle length
    """
    memo = {}
    start = min(i, j)
    end = max(i, j)
    max_length = 0
    for num in range(start, end + 1):
        length = calculate_cycle_length(num, memo)
        if length > max_length:
            max_length = length
    return max_length

class TestQuestion100(unittest.TestCase):
    """
    針對問題 100 的單元測試類別。
    """

    def test_calculate_cycle_length(self):
        """
        測試 calculate_cycle_length 函數的正確性。
        """
        memo = {}
        # 測試已知案例
        self.assertEqual(calculate_cycle_length(1, memo), 1)  # 1 的序列只有自己
        self.assertEqual(calculate_cycle_length(2, memo), 2)  # 2 -> 1
        self.assertEqual(calculate_cycle_length(3, memo), 8)  # 3 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1
        self.assertEqual(calculate_cycle_length(4, memo), 3)  # 4 -> 2 -> 1
        self.assertEqual(calculate_cycle_length(22, memo), 16)  # 根據題目範例

    def test_find_max_cycle_length(self):
        """
        測試 find_max_cycle_length 函數的正確性，使用題目提供的測試用例。
        """
        # 測試用例 1: 1 10 -> 20
        self.assertEqual(find_max_cycle_length(1, 10), 20)
        # 測試用例 2: 100 200 -> 125
        self.assertEqual(find_max_cycle_length(100, 200), 125)
        # 測試用例 3: 201 210 -> 89
        self.assertEqual(find_max_cycle_length(201, 210), 89)
        # 測試用例 4: 900 1000 -> 174
        self.assertEqual(find_max_cycle_length(900, 1000), 174)

    def test_edge_cases(self):
        """
        測試邊界情況。
        """
        # i == j 的情況
        self.assertEqual(find_max_cycle_length(1, 1), 1)
        self.assertEqual(find_max_cycle_length(5, 5), 6)  # 5 的 cycle length 是 6
        # 較小的區間
        self.assertEqual(find_max_cycle_length(2, 3), 8)  # 3 的 cycle length 是 8

if __name__ == '__main__':
    unittest.main()