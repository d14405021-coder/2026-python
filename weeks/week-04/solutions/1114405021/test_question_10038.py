"""
UVA 10038 - 單元測試

執行方式：
    python -m unittest -v test_question_10038.py
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

# 讓測試可匯入同資料夾中的解題程式。
CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from question_10038 import is_jolly, parse_line_to_sequence, solve


class TestQuestion10038(unittest.TestCase):
    """測試核心判斷、解析流程與整體輸出。"""

    def test_is_jolly_true_cases(self) -> None:
        """驗證經典 Jolly 範例與邊界案例。"""

        self.assertTrue(is_jolly([1, 4, 2, 3]))
        self.assertTrue(is_jolly([1]))
        self.assertTrue(is_jolly([5, 4]))

    def test_is_jolly_false_cases(self) -> None:
        """驗證差值重複或超範圍時應為 Not jolly。"""

        self.assertFalse(is_jolly([1, 4, 2, -1, 6]))
        self.assertFalse(is_jolly([1, 4, 7, 10]))

    def test_parse_line_to_sequence(self) -> None:
        """驗證單行解析：正常資料與資料不足情況。"""

        self.assertEqual(parse_line_to_sequence("4 1 4 2 3"), [1, 4, 2, 3])
        self.assertEqual(parse_line_to_sequence("5 1 2 3"), [])

    def test_solve_multiple_lines(self) -> None:
        """
        驗證整體流程：
        - 可處理多行測資
        - 逐行輸出 Jolly / Not jolly
        """

        raw_input = """4 1 4 2 3
5 1 4 2 -1 6
1 100
"""
        expected_output = """Jolly
Not jolly
Jolly"""
        self.assertEqual(solve(raw_input), expected_output)


if __name__ == "__main__":
    unittest.main()
