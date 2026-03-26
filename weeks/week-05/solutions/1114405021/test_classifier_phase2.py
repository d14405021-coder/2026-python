"""
Phase 2：牌型分類（HandClassifier）單元測試

來源依據：
- p2-test.md（測試案例需求）
- p2-dev.md（方法命名與回傳規格）

測試重點：
1. CardType 列舉值正確。
2. classify() 能正確辨識單張/對子/三條/五張牌型。
3. compare() 能依牌型與牌值做大小比較。
4. can_play() 能判斷首出規則與跟牌規則。

注意：
- 此檔以 TDD 為導向，若 game/classifier.py 尚未實作，失敗屬預期。
- 註解採繁體中文，並盡量寫出判斷背後原因，方便對照規格除錯。
"""

from __future__ import annotations

import importlib
import unittest
from typing import Optional


# 先從 Phase 1 的模型中取得 Card。
# 這裡沿用多候選載入，避免不同資料夾結構造成匯入失敗。
_MODEL_MODULE_CANDIDATES = [
    "models",
    "game.models",
    "bigtwo.models",
    "src.models",
]


# Phase 2 分類器候選模組。
_CLASSIFIER_MODULE_CANDIDATES = [
    "game.classifier",
    "classifier",
    "bigtwo.classifier",
    "src.classifier",
]


def _load_symbol(module_candidates: list[str], symbol: str):
    """從候選模組清單中尋找指定符號，找不到時拋出清楚錯誤。"""
    last_exc: Exception | None = None
    for mod_name in module_candidates:
        try:
            mod = importlib.import_module(mod_name)
        except Exception as exc:  # pragma: no cover
            last_exc = exc
            continue
        if hasattr(mod, symbol):
            return getattr(mod, symbol)
    raise ImportError(
        f"找不到符號 {symbol}，請確認模組路徑。候選: {module_candidates}。"
        f"最後一次載入錯誤: {last_exc!r}"
    )


Card = _load_symbol(_MODEL_MODULE_CANDIDATES, "Card")
CardType = _load_symbol(_CLASSIFIER_MODULE_CANDIDATES, "CardType")
HandClassifier = _load_symbol(_CLASSIFIER_MODULE_CANDIDATES, "HandClassifier")


def C(rank: int, suit: int):
    """建立卡牌的縮寫輔助函式，讓測試案例更精簡可讀。"""
    return Card(rank, suit)


class TestCardTypeEnum(unittest.TestCase):
    """CardType 列舉值檢查：確保牌型等級與規格一致。"""

    def test_cardtype_values(self):
        self.assertEqual(CardType.SINGLE, 1)
        self.assertEqual(CardType.PAIR, 2)
        self.assertEqual(CardType.TRIPLE, 3)
        self.assertEqual(CardType.STRAIGHT, 4)
        self.assertEqual(CardType.FLUSH, 5)
        self.assertEqual(CardType.FULL_HOUSE, 6)
        self.assertEqual(CardType.FOUR_OF_A_KIND, 7)
        self.assertEqual(CardType.STRAIGHT_FLUSH, 8)


class TestClassifySingle(unittest.TestCase):
    """單張分類測試。"""

    def test_classify_single_ace(self):
        got = HandClassifier.classify([C(14, 3)])
        self.assertEqual(got, (CardType.SINGLE, 14, 3))

    def test_classify_single_two(self):
        got = HandClassifier.classify([C(15, 0)])
        self.assertEqual(got, (CardType.SINGLE, 15, 0))

    def test_classify_single_three(self):
        got = HandClassifier.classify([C(3, 0)])
        self.assertEqual(got, (CardType.SINGLE, 3, 0))


class TestClassifyPair(unittest.TestCase):
    """對子分類測試。"""

    def test_classify_pair(self):
        # 規格定義 pair 的 tie-break 用 rank，suit 固定回傳 0。
        got = HandClassifier.classify([C(14, 3), C(14, 2)])
        self.assertEqual(got, (CardType.PAIR, 14, 0))

    def test_classify_pair_diff_rank(self):
        got = HandClassifier.classify([C(14, 3), C(13, 3)])
        self.assertIsNone(got)

    def test_classify_pair_from_three_take_two(self):
        got = HandClassifier.classify([C(14, 3), C(14, 2)])
        self.assertEqual(got, (CardType.PAIR, 14, 0))


class TestClassifyTriple(unittest.TestCase):
    """三條分類測試。"""

    def test_classify_triple(self):
        got = HandClassifier.classify([C(14, 3), C(14, 2), C(14, 1)])
        self.assertEqual(got, (CardType.TRIPLE, 14, 0))

    def test_classify_triple_not_enough(self):
        # 兩張且點數不同，既不是三條也不是對子，應回傳 None。
        got = HandClassifier.classify([C(14, 3), C(13, 2)])
        self.assertIsNone(got)


class TestClassifyFiveCards(unittest.TestCase):
    """五張牌型：順子、同花、葫蘆、四條、同花順。"""

    def test_classify_straight(self):
        # 3,4,5,6,7
        got = HandClassifier.classify([C(3, 0), C(4, 1), C(5, 2), C(6, 3), C(7, 0)])
        self.assertEqual(got, (CardType.STRAIGHT, 7, 0))

    def test_classify_straight_ace_low(self):
        # A,2,3,4,5 的特例；最高點視為 5
        got = HandClassifier.classify([C(14, 0), C(15, 1), C(3, 2), C(4, 3), C(5, 0)])
        self.assertEqual(got, (CardType.STRAIGHT, 5, 0))

    def test_classify_flush(self):
        got = HandClassifier.classify([C(3, 0), C(5, 0), C(7, 0), C(9, 0), C(11, 0)])
        self.assertEqual(got, (CardType.FLUSH, 11, 0))

    def test_classify_full_house(self):
        got = HandClassifier.classify([C(14, 3), C(14, 2), C(14, 1), C(15, 0), C(15, 1)])
        self.assertEqual(got, (CardType.FULL_HOUSE, 14, 0))

    def test_classify_four_of_a_kind(self):
        got = HandClassifier.classify([C(14, 3), C(14, 2), C(14, 1), C(14, 0), C(3, 1)])
        self.assertEqual(got, (CardType.FOUR_OF_A_KIND, 14, 0))

    def test_classify_straight_flush(self):
        got = HandClassifier.classify([C(3, 0), C(4, 0), C(5, 0), C(6, 0), C(7, 0)])
        self.assertEqual(got, (CardType.STRAIGHT_FLUSH, 7, 0))


class TestCompare(unittest.TestCase):
    """牌型比較測試：1=左大、-1=右大、0=平手。"""

    def test_compare_single_rank(self):
        self.assertEqual(HandClassifier.compare([C(14, 3)], [C(13, 3)]), 1)

    def test_compare_single_suit(self):
        self.assertEqual(HandClassifier.compare([C(14, 3)], [C(14, 2)]), 1)

    def test_compare_pair_rank(self):
        self.assertEqual(HandClassifier.compare([C(14, 3), C(14, 2)], [C(13, 3), C(13, 2)]), 1)

    def test_compare_pair_suit(self):
        # 規格對 pair 的第三欄位固定 0，
        # 實務上多數實作會視為平手（此測試採規格文件敘述，期望左大）。
        # 若你採平手策略，可把期望改為 0。
        self.assertEqual(HandClassifier.compare([C(14, 3), C(14, 2)], [C(14, 1), C(14, 0)]), 1)

    def test_compare_different_type(self):
        self.assertEqual(HandClassifier.compare([C(5, 3), C(5, 2)], [C(6, 3)]), 1)

    def test_compare_flush_vs_straight(self):
        flush_cards = [C(3, 0), C(5, 0), C(7, 0), C(9, 0), C(11, 0)]
        straight_cards = [C(3, 0), C(4, 1), C(5, 2), C(6, 3), C(7, 0)]
        self.assertEqual(HandClassifier.compare(flush_cards, straight_cards), 1)


class TestCanPlay(unittest.TestCase):
    """合法性檢查：首出 3♣、同型跟牌、強度比較。"""

    def test_can_play_first_3clubs(self):
        self.assertTrue(HandClassifier.can_play(None, [C(3, 0)]))

    def test_can_play_first_not_3clubs(self):
        self.assertFalse(HandClassifier.can_play(None, [C(14, 3)]))

    def test_can_play_same_type(self):
        # 對 6 壓過對 5
        self.assertTrue(
            HandClassifier.can_play([C(5, 3), C(5, 2)], [C(6, 3), C(6, 2)])
        )

    def test_can_play_diff_type(self):
        # 規格：跟牌時牌型不同不可出
        self.assertFalse(HandClassifier.can_play([C(5, 3), C(5, 2)], [C(6, 3)]))

    def test_can_play_not_stronger(self):
        # 對 5 無法壓過對 10
        self.assertFalse(
            HandClassifier.can_play([C(10, 3), C(10, 2)], [C(5, 3), C(5, 2)])
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
