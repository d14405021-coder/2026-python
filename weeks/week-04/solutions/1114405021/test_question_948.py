"""
UVA 948 / ZeroJudge c095 假幣問題 - 單元測試

執行方式（在此檔案所在資料夾）：
    python -m unittest -v test_question_948.py
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path
from typing import List

# 把測試檔所在目錄加入模組搜尋路徑，確保可匯入同資料夾的解題程式。
# 這樣不論你從專案根目錄或目前資料夾執行 unittest，都能正確 import。
CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from question_948 import Weighing, find_fake_coin, solve


class TestUva948FakeCoin(unittest.TestCase):
    """
    測試策略：
    1. 先測核心邏輯 find_fake_coin。
    2. 再測 parse + solve 的整合行為（含空白行格式）。
    """

    def test_unique_coin_can_be_determined(self) -> None:
        """
        案例設計：
        - 第一次 1 vs 2 平衡，表示 1、2 都是真幣。
        - 第二次 3 vs 1 出現 '<'，因 1 為真幣，可推出 3 偏輕。
        - 第三次 4 vs 1 平衡，排除 4。
        最終可唯一定位假幣為 3。
        """

        # 用一個小而清楚的案例，讓「逐步排除」邏輯容易人工驗證。
        n = 4
        weighings: List[Weighing] = [
            ([1], [2], '='),
            ([3], [1], '<'),
            ([4], [1], '='),
        ]
        self.assertEqual(find_fake_coin(n, weighings), 3)

    def test_ambiguous_should_return_zero(self) -> None:
        """
        只有一筆秤重 1 vs 2 且結果是 '<'，
        可能是 1 偏輕，也可能是 2 偏重，無法唯一判定。
        """

        # 只有一筆不平衡資訊時，通常不足以區分「左輕」與「右重」兩種情況。
        n = 4
        weighings: List[Weighing] = [
            ([1], [2], '<'),
        ]
        self.assertEqual(find_fake_coin(n, weighings), 0)

    def test_inconsistent_records_should_return_zero(self) -> None:
        """
        兩次平衡秤重把 1、2、3 都證明為真幣，
        代表不存在可行假幣假設，依題意也應輸出 0。
        """

        # 這組資料刻意讓所有硬幣都被平衡秤重證明為真幣，
        # 用來驗證程式面對「無可行假設」時會回傳 0。
        n = 3
        weighings: List[Weighing] = [
            ([1], [2], '='),
            ([1], [3], '='),
        ]
        self.assertEqual(find_fake_coin(n, weighings), 0)

    def test_solve_output_format_with_blank_line_between_cases(self) -> None:
        """
        驗證 solve 是否正確處理多組測資與「組間空白行」格式。
        """

        # 使用字串模擬 OJ 原始輸入，直接測試 solve 的最終輸出格式。
        raw_input = """2

4 3
1 1 2
=
1 3 1
<
1 4 1
=

4 1
1 1 2
<
"""
        # 題目要求案例之間有一個空白行，因此預期字串採雙換行。
        expected_output = """3

0"""
        self.assertEqual(solve(raw_input), expected_output)


if __name__ == "__main__":
    unittest.main()
