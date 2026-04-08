# test_question_10071.py
# 說明：針對 question_10071.py 的單元測試

import unittest
from question_10071 import solve_equation


class TestSolveEquation(unittest.TestCase):
    def test_example_1(self):
        # 測試情境 1：S 只有一個元素 [0]
        # 唯一的等式是 0 + 0 + 0 + 0 + 0 = 0，只有 1 種可能
        self.assertEqual(solve_equation([0]), 1)

    def test_example_2(self):
        # 測試情境 2：S 有兩個元素 [1, -1]
        # a+b+c = f-d-e 的組合。
        # a+b+c 的可能：
        # -3: (-1, -1, -1) -> 1種
        # -1: (-1, -1, 1), (-1, 1, -1), (1, -1, -1) -> 3種
        #  1: (1, 1, -1), (1, -1, 1), (-1, 1, 1) -> 3種
        #  3: (1, 1, 1) -> 1種

        # f-d-e 的可能 (f從中挑, d,e從中挑)：
        # 若 f=1, d,e可以組出的值：
        # d,e=(1,1) -> 1-1-1 = -1 (1種)
        # d,e=(1,-1) -> 1-1-(-1) = 1 (1種)
        # d,e=(-1,1) -> 1-(-1)-1 = 1 (1種)
        # d,e=(-1,-1) -> 1-(-1)-(-1) = 3 (1種)
        # 若 f=-1:
        # d,e=(1,1) -> -1-1-1 = -3 (1種)
        # d,e=(1,-1) -> -1-1-(-1) = -1 (1種)
        # d,e=(-1,1) -> -1-(-1)-1 = -1 (1種)
        # d,e=(-1,-1) -> -1-(-1)-(-1) = 1 (1種)

        # 統計右邊(f-d-e)產生的次數：
        # -3: 1次
        # -1: 3次
        #  1: 3次
        #  3: 1次

        # 兩邊相乘並加總：(1*1) + (3*3) + (3*3) + (1*1) = 1 + 9 + 9 + 1 = 20
        self.assertEqual(solve_equation([1, -1]), 20)

    def test_example_3(self):
        # 測試情境 3：S 有三個元素 [1, 2, 3]
        # 稍微大一點的數字，測試會不會超出迴圈限制
        ans = solve_equation([1, 2, 3])
        # 我們不手算答案，而是確認程式不會報錯，且答案大於 0
        self.assertTrue(ans > 0)

    def test_empty_set(self):
        # 測試情境 4：空集合
        self.assertEqual(solve_equation([]), 0)


if __name__ == "__main__":
    unittest.main()
