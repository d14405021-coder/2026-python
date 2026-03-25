# test_question_10057.py
# 說明：針對 question_10057.py 的單元測試

import unittest
from question_10057 import solve_midsummer_dream


class TestMidSummerDream(unittest.TestCase):
    def test_example_odd(self):
        # 測試情境 1：奇數個數字
        # [2, 4, 6] -> 排序後 [2, 4, 6]
        # 中位數 mid1 = mid2 = 4
        # 1. 最小的 A：4
        # 2. 有幾個等於 4：1 個
        # 3. 有幾種可能的 A：4 - 4 + 1 = 1 種
        self.assertEqual(solve_midsummer_dream([2, 4, 6]), (4, 1, 1))

    def test_example_even(self):
        # 測試情境 2：偶數個數字
        # [1, 2, 3, 4] -> 排序後 [1, 2, 3, 4]
        # 中位數 mid1 = 2, mid2 = 3
        # 1. 最小的 A：2
        # 2. 有幾個數字落在 [2, 3]：2 和 3，共 2 個
        # 3. 有幾種可能的 A：3 - 2 + 1 = 2 種 (2 和 3)
        self.assertEqual(solve_midsummer_dream([1, 2, 3, 4]), (2, 2, 2))

    def test_all_same(self):
        # 測試情境 3：所有數字都相同
        # [5, 5, 5, 5]
        # mid1 = 5, mid2 = 5
        # 1. 最小的 A：5
        # 2. 有幾個數字落在 [5, 5]：全部 4 個
        # 3. 有幾種可能的 A：5 - 5 + 1 = 1 種
        self.assertEqual(solve_midsummer_dream([5, 5, 5, 5]), (5, 4, 1))

    def test_unsorted_input(self):
        # 測試情境 4：未排序的輸入
        # [10, 1, 4, 4, 6, 8] -> 排序 [1, 4, 4, 6, 8, 10]
        # n = 6, mid1 = index 2 = 4, mid2 = index 3 = 6
        # 1. 最小的 A：4
        # 2. 落在 [4, 6] 的數字：4, 4, 6 (共 3 個)
        # 3. 可能的 A：6 - 4 + 1 = 3 種 (4, 5, 6)
        self.assertEqual(solve_midsummer_dream([10, 1, 4, 4, 6, 8]), (4, 3, 3))


if __name__ == "__main__":
    unittest.main()
