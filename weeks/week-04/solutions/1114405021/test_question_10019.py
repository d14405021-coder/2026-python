"""
UVA 10019（Hashmat 差值題）- 單元測試

執行方式：
    python -m unittest -v test_question_10019.py
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

# 把目前測試檔資料夾加入模組路徑，確保可匯入同層解題檔。
CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from question_10019 import diff, solve


class TestQuestion10019(unittest.TestCase):
    """
    測試策略：
    1. 先測最小單位 diff
    2. 再測 solve 的整體輸入輸出格式
    """

    def test_diff_basic(self) -> None:
        """一般情境：兩數差值可直接計算。"""

        self.assertEqual(diff(10, 12), 2)
        self.assertEqual(diff(100, 55), 45)

    def test_diff_reverse_order_still_positive(self) -> None:
        """即使輸入順序顛倒，仍應回傳正差值。"""

        self.assertEqual(diff(12, 10), 2)

    def test_solve_multiple_lines(self) -> None:
        """
        多行輸入測試：
        - 驗證直到 EOF 的逐行處理
        - 驗證每行輸出一個差值
        """

        raw_input = """10 12
10 14
100 55
"""
        expected_output = """2
4
45"""
        self.assertEqual(solve(raw_input), expected_output)

    def test_solve_ignore_blank_lines(self) -> None:
        """含空白行時，應可穩健略過，不影響答案。"""

        raw_input = """10 12

100 55
"""
        expected_output = """2
45"""
        self.assertEqual(solve(raw_input), expected_output)


if __name__ == "__main__":
    unittest.main()
