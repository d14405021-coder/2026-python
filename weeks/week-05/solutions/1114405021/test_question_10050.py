# test_question_10050.py
# 說明：針對 question_10050.py 的單元測試 (Unit Test)
# 驗證各種罷會情境下的計算結果是否正確。

import unittest
from question_10050 import solve_hartals


class TestHartals(unittest.TestCase):
    def test_example_1(self):
        # 測試情境 1：題目提供的範例
        # N=14 天，政黨頻率：3, 4, 8
        # 損失工作天應為 5 (第3, 4, 8, 9, 12天)
        # 注意第 6 天(星期五)是假日，不計入損失。
        self.assertEqual(solve_hartals(14, [3, 4, 8]), 5)

    def test_example_2(self):
        # 測試情境 2：100天，多個政黨
        # 這是 UVA 的另一組常見測資範例
        self.assertEqual(solve_hartals(100, [12, 15, 25, 40]), 15)

    def test_no_hartals(self):
        # 測試情境 3：沒有任何政黨 (雖然題目說 P >= 1，但可以測極端情況)
        self.assertEqual(solve_hartals(14, []), 0)

    def test_every_day_hartal(self):
        # 測試情境 4：某個政黨每天都罷會 (h=1)
        # 14天內，扣除週末4天 (第6,7,13,14天)，剩下10天都會被罷會
        self.assertEqual(solve_hartals(14, [1]), 10)

    def test_only_weekends(self):
        # 測試情境 5：罷會剛好都發生在假日 (h=7，也就是每週六)
        # 第7, 14, 21天...剛好都是星期六，是假日，所以損失的工作天為 0
        self.assertEqual(solve_hartals(14, [7]), 0)

    def test_same_frequency(self):
        # 測試情境 6：多個政黨的罷會頻率完全相同
        # 只會扣一次工作天，不會重複扣除
        self.assertEqual(solve_hartals(14, [3, 3, 3]), 4)  # (第3, 9, 12天，不含第6天)


if __name__ == "__main__":
    unittest.main()
