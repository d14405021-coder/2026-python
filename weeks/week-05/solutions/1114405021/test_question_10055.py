# test_question_10055.py
# 說明：針對 question_10055.py (Fenwick Tree 寫法) 的單元測試

import unittest
from question_10055 import FenwickTree


class TestMonotonicFunction(unittest.TestCase):
    def setUp(self):
        # 每次測試前建立一個大小為 5 的樹狀數組
        # 狀態：全部為 0 (增函數)
        self.n = 5
        self.bit = FenwickTree(self.n)
        self.state = [0] * (self.n + 1)

    def toggle(self, i):
        """模擬操作 1：反轉第 i 個函數的增減性"""
        if self.state[i] == 0:
            self.bit.add(i, 1)
            self.state[i] = 1
        else:
            self.bit.add(i, -1)
            self.state[i] = 0

    def query(self, l, r):
        """模擬操作 2：查詢區間 [L, R] 的複合函數增減性"""
        total = self.bit.query_range(l, r)
        return total % 2

    def test_all_increasing_initially(self):
        # 一開始全部都是增函數 (0)，不管怎麼查應該都是 0
        self.assertEqual(self.query(1, 5), 0)
        self.assertEqual(self.query(2, 4), 0)
        self.assertEqual(self.query(3, 3), 0)

    def test_single_toggle(self):
        # 把第 3 個函數改成減函數 (1)
        self.toggle(3)

        # 包含第 3 個的區間應該變成減函數 (1)
        self.assertEqual(self.query(1, 5), 1)
        self.assertEqual(self.query(2, 4), 1)
        self.assertEqual(self.query(3, 3), 1)

        # 不包含第 3 個的區間應該還是增函數 (0)
        self.assertEqual(self.query(1, 2), 0)
        self.assertEqual(self.query(4, 5), 0)

    def test_multiple_toggles(self):
        # 反轉 2 和 4，目前為：0, 1, 0, 1, 0 (對應索引 1~5)
        self.toggle(2)
        self.toggle(4)

        # 查詢 [1, 5]，有兩個減函數，負負得正 -> 0 (增函數)
        self.assertEqual(self.query(1, 5), 0)

        # 查詢 [1, 3]，只有一個減函數 (在 2) -> 1 (減函數)
        self.assertEqual(self.query(1, 3), 1)

        # 再反轉一次 2，變回增函數：0, 0, 0, 1, 0
        self.toggle(2)

        # 此時 [1, 5] 只有一個減函數 (在 4) -> 1 (減函數)
        self.assertEqual(self.query(1, 5), 1)

    def test_continuous_toggles(self):
        # 模擬反覆反轉同一個位置
        self.toggle(1)  # 1
        self.assertEqual(self.query(1, 1), 1)
        self.toggle(1)  # 0
        self.assertEqual(self.query(1, 1), 0)
        self.toggle(1)  # 1
        self.assertEqual(self.query(1, 1), 1)


if __name__ == "__main__":
    unittest.main()
