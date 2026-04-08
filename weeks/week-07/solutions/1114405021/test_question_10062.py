# test_question_10062.py
# 說明：針對 question_10062.py 的單元測試

import unittest
from question_10062 import solve_lost_cows


class TestLostCows(unittest.TestCase):
    def test_example_1(self):
        # 測試情境 1：題目提供的典型範例 (5 頭牛)
        # N = 5
        # 第2到第5頭分別為：1, 2, 1, 0
        # 因此 smaller_counts = [0, 1, 2, 1, 0]
        n = 5
        smaller_counts = [0, 1, 2, 1, 0]

        # 正確順序：
        # 第 5 頭前面有 0 個比牠小的 -> 第 1 小的數字 (從 1,2,3,4,5 中挑) -> 1
        # 第 4 頭前面有 1 個比牠小的 -> 第 2 小的數字 (從 2,3,4,5 中挑) -> 3
        # 第 3 頭前面有 2 個比牠小的 -> 第 3 小的數字 (從 2,4,5 中挑) -> 5
        # 第 2 頭前面有 1 個比牠小的 -> 第 2 小的數字 (從 2,4 中挑) -> 4
        # 第 1 頭前面有 0 個比牠小的 -> 第 1 小的數字 (從 2 中挑) -> 2
        expected = [2, 4, 5, 3, 1]

        self.assertEqual(solve_lost_cows(n, smaller_counts), expected)

    def test_all_increasing(self):
        # 測試情境 2：牛的編號剛好由小到大排好
        # N = 3
        # 編號: 1, 2, 3
        # 前面比牠小的數量分別為：0, 1, 2
        n = 3
        smaller_counts = [0, 1, 2]
        expected = [1, 2, 3]

        self.assertEqual(solve_lost_cows(n, smaller_counts), expected)

    def test_all_decreasing(self):
        # 測試情境 3：牛的編號剛好由大到小排好
        # N = 4
        # 編號: 4, 3, 2, 1
        # 因為數字越來越小，所以前面沒有任何數字比自己小
        # smaller_counts 分別為：0, 0, 0, 0
        n = 4
        smaller_counts = [0, 0, 0, 0]
        expected = [4, 3, 2, 1]

        self.assertEqual(solve_lost_cows(n, smaller_counts), expected)

    def test_single_cow(self):
        # 測試情境 4：只有 1 頭牛 (邊界條件測試)
        n = 1
        smaller_counts = [0]
        expected = [1]

        self.assertEqual(solve_lost_cows(n, smaller_counts), expected)


if __name__ == "__main__":
    unittest.main()
