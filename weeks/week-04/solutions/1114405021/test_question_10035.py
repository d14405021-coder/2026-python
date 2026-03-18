"""
UVA 10035 - 單元測試

執行方式：
    python -m unittest -v test_question_10035.py
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

# 確保可以匯入同資料夾中的 question_10035.py
CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from question_10035 import count_carries, format_carry_message, solve


class TestQuestion10035(unittest.TestCase):
    """測試進位邏輯、輸出句型與整體輸入輸出流程。"""

    def test_count_carries_basic_cases(self) -> None:
        """
        驗證常見案例：0 次、1 次、3 次進位。

        這組案例有助於快速檢查核心邏輯是否正確：
        - 123 + 456：每位都不滿 10 => 0 次
        - 123 + 594：只有個位產生進位 => 1 次
        - 555 + 555：每位都會進位 => 3 次
        """

        self.assertEqual(count_carries(123, 456), 0)
        self.assertEqual(count_carries(555, 555), 3)
        self.assertEqual(count_carries(123, 594), 1)

    def test_count_carries_with_different_digit_lengths(self) -> None:
        """位數不同時也要正確處理，避免只處理到較短位數就停止。"""

        self.assertEqual(count_carries(1, 99999), 5)
        self.assertEqual(count_carries(10, 90), 1)

    def test_format_carry_message(self) -> None:
        """驗證 operation / operations 字尾規則，避免文案格式錯誤。"""

        self.assertEqual(format_carry_message(0), "No carry operation.")
        self.assertEqual(format_carry_message(1), "1 carry operation.")
        self.assertEqual(format_carry_message(2), "2 carry operations.")

    def test_solve_until_terminator(self) -> None:
        """
        驗證整體流程：
        - 多組資料
        - 讀到 0 0 就停止
        - 0 0 之後的資料不應再處理
        """

        raw_input = """123 456
555 555
123 594
0 0
1 99999
"""

        # 預期只處理到 0 0 前三行資料。
        expected_output = """No carry operation.
3 carry operations.
1 carry operation."""

        self.assertEqual(solve(raw_input), expected_output)


if __name__ == "__main__":
    unittest.main()
