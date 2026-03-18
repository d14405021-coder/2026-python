"""
UVA 10008 / ZeroJudge a001 - 單元測試範例

這份檔案目標：
1. 提供可直接執行的 unittest 測試。
2. 用教學式註解示範題目規格如何轉成可測試邏輯。
3. 內含一份參考實作，方便先驗證測試正確性。

執行方式（在此檔案所在資料夾）：
    python -m unittest -v test_question_10008.py
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path
from typing import List

# 把測試檔所在目錄加入模組搜尋路徑，確保可以匯入同資料夾的解題檔。
# 這樣不論你從哪個工作目錄執行 unittest，都能正確找到目標模組。
CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from question_10008 import count_letters, solve, sort_result


class TestUva10008Cryptanalysis(unittest.TestCase):
    """
    測試策略：
    1. 先測核心統計與排序規則。
    2. 再測 solve 的整體輸入輸出格式。
    """

    def test_count_letters_ignore_non_alphabet(self) -> None:
        """
        驗證統計時會忽略非英文字母，並正確處理大小寫合併。

        這個測試重點：
        - "A-a! 1" 中只有 A、a 會被計入，符號與數字都應忽略。
        - "bB?" 可驗證大小寫合併後 B 的累計是否正確。
        """

        lines = ["A-a! 1", "bB?", "###"]
        freq = count_letters(lines)

        self.assertEqual(freq.get("A"), 2)
        self.assertEqual(freq.get("B"), 2)
        self.assertNotIn("1", freq)

    def test_sort_result_by_count_then_alphabet(self) -> None:
        """
        驗證排序規則：先看次數降冪，再看字母升冪。

        這裡刻意讓 A 與 H 次數相同，
        用來驗證 tie-break 是否真的依字母排序。
        """

        freq = {"H": 3, "A": 3, "Z": 1}
        ordered = sort_result(freq)

        self.assertEqual(ordered, [("A", 3), ("H", 3), ("Z", 1)])

    def test_solve_with_mixed_case_and_symbols(self) -> None:
        """
        綜合案例：
        - 含大小寫混合
        - 含標點符號與空白
        - 驗證只輸出出現過的英文字母
        """

        raw_input = """3
This is a test.
a!A!b?b?
12345
"""

        # 手算示範：
        # "This is a test." -> T,H,I,S,I,S,A,T,E,S,T
        # "a!A!b?b?"      -> A,A,B,B（符號忽略）
        # "12345"          -> 全忽略
        # 合併後得到以下次數：
        # A:3, B:2, E:1, H:1, I:2, S:3, T:3
        # 排序後：A 3, S 3, T 3, B 2, I 2, E 1, H 1
        expected_output = "\n".join([
            "A 3",
            "S 3",
            "T 3",
            "B 2",
            "I 2",
            "E 1",
            "H 1",
        ])

        self.assertEqual(solve(raw_input), expected_output)

    def test_solve_empty_effective_content(self) -> None:
        """
        當 n 行內容都沒有英文字母時，應輸出空字串（不印任何列）。

        這個測試可避免常見錯誤：
        - 不小心輸出多餘空白行
        - 把數字或符號誤算進統計結果
        """

        raw_input = """2
123
!@#
"""
        self.assertEqual(solve(raw_input), "")


if __name__ == "__main__":
    unittest.main()
