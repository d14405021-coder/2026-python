# test_question_10056.py
# 說明：針對 question_10056.py 的單元測試
# 驗證機率計算的準確度。由於涉及到浮點數，我們會使用 assertAlmostEqual 來容許微小的誤差。

import unittest
from question_10056 import calculate_winning_probability


class TestProbability(unittest.TestCase):
    def test_example_1(self):
        # 測試情境 1：2個玩家，成功機率 0.166666 (約 1/6)，求第 1 個人獲勝機率
        # p = 1/6, q = 5/6
        # a = 1/6
        # r = 25/36
        # 1 - r = 11/36
        # ans = (1/6) / (11/36) = 6/11 ≈ 0.545454... -> 0.5455
        ans = calculate_winning_probability(2, 0.166666, 1)
        # 用字串格式化來比對最終輸出結果
        self.assertEqual(f"{ans:.4f}", "0.5455")

    def test_example_2(self):
        # 測試情境 2：2個玩家，成功機率 0.166666，求第 2 個人獲勝機率
        # ans = (5/6 * 1/6) / (11/36) = 5/11 ≈ 0.454545... -> 0.4545
        ans = calculate_winning_probability(2, 0.166666, 2)
        self.assertEqual(f"{ans:.4f}", "0.4545")

    def test_zero_probability(self):
        # 測試情境 3：成功機率為 0 的極端情況
        ans = calculate_winning_probability(5, 0.0, 3)
        self.assertEqual(f"{ans:.4f}", "0.0000")

    def test_certain_probability(self):
        # 測試情境 4：成功機率為 1 (100% 成功)
        # 第一個玩家必定獲勝
        ans_p1 = calculate_winning_probability(3, 1.0, 1)
        self.assertEqual(f"{ans_p1:.4f}", "1.0000")

        # 之後的玩家必定失敗
        ans_p2 = calculate_winning_probability(3, 1.0, 2)
        self.assertEqual(f"{ans_p2:.4f}", "0.0000")

    def test_single_player(self):
        # 測試情境 5：只有 1 個玩家
        # 只要成功機率 > 0，那他最終一定會贏 (無限次重擲)
        ans = calculate_winning_probability(1, 0.5, 1)
        self.assertEqual(f"{ans:.4f}", "1.0000")


if __name__ == "__main__":
    unittest.main()
