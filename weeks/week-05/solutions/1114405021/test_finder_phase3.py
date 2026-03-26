"""
Phase 3：牌型搜尋（HandFinder）單元測試

設計依據：
- p3-test.md（測試需求）
- p3-dev.md（方法名稱與回傳介面）

此測試檔目的：
1. 驗證 HandFinder 是否能找出各類候選牌型。
2. 驗證 get_all_valid_plays() 是否會依 last_play 規則過濾。
3. 讓你可以用 TDD 流程先 Red，再實作到 Green。
"""

from __future__ import annotations

import importlib
import unittest
from typing import Any


_MODEL_MODULE_CANDIDATES = [
    "models",
    "game.models",
    "bigtwo.models",
    "src.models",
]

_CLASSIFIER_MODULE_CANDIDATES = [
    "classifier",
    "game.classifier",
    "bigtwo.classifier",
    "src.classifier",
]

_FINDER_MODULE_CANDIDATES = [
    "game.finder",
    "finder",
    "bigtwo.finder",
    "src.finder",
]


def _load_symbol(module_candidates: list[str], symbol: str):
    """從候選模組中嘗試載入指定符號。"""
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
        f"找不到符號 {symbol}，候選模組：{module_candidates}，最後錯誤：{last_exc!r}"
    )


Card = _load_symbol(_MODEL_MODULE_CANDIDATES, "Card")
Hand = _load_symbol(_MODEL_MODULE_CANDIDATES, "Hand")
HandClassifier = _load_symbol(_CLASSIFIER_MODULE_CANDIDATES, "HandClassifier")
CardType = _load_symbol(_CLASSIFIER_MODULE_CANDIDATES, "CardType")
HandFinder = _load_symbol(_FINDER_MODULE_CANDIDATES, "HandFinder")


def C(rank: int, suit: int):
    """建立卡牌縮寫，讓測試案例更精簡。"""
    return Card(rank, suit)


def _is_type(play: list[Card], t: Any) -> bool:
    """用分類器判斷某組牌是否屬於指定牌型。"""
    x = HandClassifier.classify(play)
    return x is not None and x[0] == t


class TestFindSingles(unittest.TestCase):
    """單張搜尋測試。"""

    def test_find_singles(self):
        hand = Hand([C(14, 3), C(13, 2), C(3, 0)])
        singles = HandFinder.find_singles(hand)
        self.assertEqual(len(singles), 3)
        self.assertTrue(all(len(p) == 1 for p in singles))

    def test_find_singles_empty(self):
        hand = Hand([])
        singles = HandFinder.find_singles(hand)
        self.assertEqual(len(singles), 0)


class TestFindPairs(unittest.TestCase):
    """對子搜尋測試。"""

    def test_find_pairs_one(self):
        hand = Hand([C(14, 3), C(14, 2), C(3, 0)])
        pairs = HandFinder.find_pairs(hand)
        self.assertEqual(len(pairs), 1)
        self.assertTrue(_is_type(pairs[0], CardType.PAIR))

    def test_find_pairs_two(self):
        hand = Hand([C(14, 3), C(14, 2), C(13, 3), C(13, 0)])
        pairs = HandFinder.find_pairs(hand)
        self.assertEqual(len(pairs), 2)
        self.assertTrue(all(_is_type(p, CardType.PAIR) for p in pairs))

    def test_find_pairs_none(self):
        hand = Hand([C(14, 3), C(13, 2), C(3, 0)])
        pairs = HandFinder.find_pairs(hand)
        self.assertEqual(len(pairs), 0)


class TestFindTriples(unittest.TestCase):
    """三條搜尋測試。"""

    def test_find_triples_one(self):
        hand = Hand([C(14, 3), C(14, 2), C(14, 1), C(3, 0)])
        triples = HandFinder.find_triples(hand)
        self.assertEqual(len(triples), 1)
        self.assertTrue(_is_type(triples[0], CardType.TRIPLE))

    def test_find_triples_with_extra(self):
        hand = Hand([C(14, 3), C(14, 2), C(14, 1), C(13, 3), C(13, 0)])
        triples = HandFinder.find_triples(hand)
        self.assertEqual(len(triples), 1)
        self.assertTrue(_is_type(triples[0], CardType.TRIPLE))


class TestFindFives(unittest.TestCase):
    """五張牌型搜尋：順子、同花、葫蘆、四條、同花順。"""

    def test_find_straight(self):
        hand = Hand([C(3, 0), C(4, 1), C(5, 2), C(6, 3), C(7, 0), C(14, 3)])
        fives = HandFinder.find_fives(hand)
        self.assertTrue(any(_is_type(p, CardType.STRAIGHT) for p in fives))

    def test_find_flush(self):
        hand = Hand([C(3, 0), C(5, 0), C(7, 0), C(9, 0), C(11, 0), C(14, 3)])
        fives = HandFinder.find_fives(hand)
        self.assertTrue(any(_is_type(p, CardType.FLUSH) for p in fives))

    def test_find_full_house(self):
        hand = Hand([C(14, 3), C(14, 2), C(14, 1), C(13, 3), C(13, 0), C(3, 0)])
        fives = HandFinder.find_fives(hand)
        self.assertTrue(any(_is_type(p, CardType.FULL_HOUSE) for p in fives))

    def test_find_four_of_a_kind(self):
        hand = Hand([C(14, 3), C(14, 2), C(14, 1), C(14, 0), C(3, 1), C(5, 2)])
        fives = HandFinder.find_fives(hand)
        self.assertTrue(any(_is_type(p, CardType.FOUR_OF_A_KIND) for p in fives))

    def test_find_straight_flush(self):
        hand = Hand([C(3, 0), C(4, 0), C(5, 0), C(6, 0), C(7, 0), C(14, 3)])
        fives = HandFinder.find_fives(hand)
        self.assertTrue(any(_is_type(p, CardType.STRAIGHT_FLUSH) for p in fives))


class TestGetAllValidPlays(unittest.TestCase):
    """合法出牌搜尋測試。"""

    def test_first_turn_only_3clubs(self):
        hand = Hand([C(3, 0), C(14, 3), C(14, 2)])
        plays = HandFinder.get_all_valid_plays(hand, None)

        # 規格要求首出必須包含 3♣。
        self.assertTrue(all(any(c.rank == 3 and c.suit == 0 for c in p) for p in plays))

    def test_with_last_single(self):
        hand = Hand([C(6, 0), C(7, 1), C(8, 2), C(9, 3), C(10, 0)])
        last = [C(5, 0)]
        plays = HandFinder.get_all_valid_plays(hand, last)

        # 只應回單張且都能壓過上一手單張。
        self.assertTrue(all(len(p) == 1 for p in plays))
        self.assertTrue(all(HandClassifier.compare(p, last) == 1 for p in plays))

    def test_with_last_pair(self):
        hand = Hand([C(6, 0), C(6, 1), C(7, 2), C(9, 3)])
        last = [C(5, 0), C(5, 1)]
        plays = HandFinder.get_all_valid_plays(hand, last)

        self.assertTrue(all(_is_type(p, CardType.PAIR) for p in plays))
        self.assertTrue(all(HandClassifier.compare(p, last) == 1 for p in plays))

    def test_no_valid(self):
        hand = Hand([C(3, 0), C(4, 1), C(6, 2)])
        last = [C(15, 3)]
        plays = HandFinder.get_all_valid_plays(hand, last)
        self.assertEqual(plays, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
