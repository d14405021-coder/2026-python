# test_question_10041.py
# 說明：針對 question_10041.py 的單元測試 (Unit Test)
# 使用 Python 內建的 unittest 模組來驗證功能是否正確。

import unittest
from question_10041 import find_min_distance


class TestVitosFamily(unittest.TestCase):
    def test_example_1(self):
        # 測試情境 1：2 個親戚，門牌為 2, 4
        # 中位數是 4 (或 2)，距離總和：|2-4| + |4-4| = 2
        relatives = [2, 4]
        self.assertEqual(find_min_distance(relatives), 2)

    def test_example_2(self):
        # 測試情境 2：3 個親戚，門牌為 2, 4, 6
        # 中位數為 4，距離總和：|2-4| + |4-4| + |6-4| = 2 + 0 + 2 = 4
        relatives = [2, 4, 6]
        self.assertEqual(find_min_distance(relatives), 4)

    def test_example_3(self):
        # 測試情境 3：只有 1 個親戚，自己就是中位數
        # 距離和為 0
        relatives = [10]
        self.assertEqual(find_min_distance(relatives), 0)

    def test_example_4(self):
        # 測試情境 4：所有親戚的門牌號碼都相同
        relatives = [3, 3, 3]
        self.assertEqual(find_min_distance(relatives), 0)

    def test_example_5(self):
        # 測試情境 5：連續的數字序列，奇數個
        # 1, 2, 3, 4, 5 (中位數為 3)
        # 距離：2 + 1 + 0 + 1 + 2 = 6
        relatives = [1, 2, 3, 4, 5]
        self.assertEqual(find_min_distance(relatives), 6)

    def test_example_6(self):
        # 測試情境 6：隨機未排序的數字
        relatives = [12, 4, 8, 2]
        # 排序：2, 4, 8, 12，中位數 8 (index 2)
        # 距離：|2-8| + |4-8| + |8-8| + |12-8| = 6 + 4 + 0 + 4 = 14
        self.assertEqual(find_min_distance(relatives), 14)


if __name__ == "__main__":
    # 執行所有測試
    unittest.main()
