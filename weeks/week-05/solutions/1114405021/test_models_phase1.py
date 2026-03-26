"""
Phase 1 資料模型測試（Card / Deck / Hand / Player）

說明：
1. 這份測試依據 p1-test.md 的測試案例需求設計。
2. 測試目標是驗證資料模型行為是否符合規格，而不是限制你的實作方式。
3. 若目前尚未實作對應類別，執行測試時失敗屬於預期（TDD 的 Red 階段）。

使用方式（在專案根目錄執行）：
- python -m unittest test_models_phase1 -v
或
- python -m unittest discover -v
"""

from __future__ import annotations

import importlib
import unittest
from typing import Any


# 依常見專案結構嘗試多個候選模組名稱。
# 你可以把實作放在 models.py、bigtwo/models.py、src/models.py 等。
_MODULE_CANDIDATES = [
    "models",
    "bigtwo.models",
    "src.models",
    "app.models",
]


def _load_models() -> tuple[type, type, type, type]:
    """
    動態載入 Card / Deck / Hand / Player 四個類別。

    設計原因：
    - 作業環境常見不同資料夾結構，為了讓測試較有彈性，
      這裡不把 import 寫死在單一路徑。
    - 若找不到，會回傳清楚的錯誤訊息，方便你調整模組位置。
    """
    last_exc: Exception | None = None

    for mod_name in _MODULE_CANDIDATES:
        try:
            mod = importlib.import_module(mod_name)
        except Exception as exc:  # pragma: no cover - 只在載入失敗時用
            last_exc = exc
            continue

        if all(hasattr(mod, cls) for cls in ("Card", "Deck", "Hand", "Player")):
            return mod.Card, mod.Deck, mod.Hand, mod.Player

    raise ImportError(
        "找不到 Card/Deck/Hand/Player。請確認你已實作並可從以下路徑之一匯入："
        f" {_MODULE_CANDIDATES}。最後一次錯誤：{last_exc!r}"
    )


Card, Deck, Hand, Player = _load_models()


class TestCard(unittest.TestCase):
    """Card 類別測試：建立、字串表示、比較、排序鍵。"""

    def test_card_creation(self) -> None:
        c = Card(rank=14, suit=3)
        self.assertEqual(c.rank, 14)
        self.assertEqual(c.suit, 3)

    def test_card_repr_ace(self) -> None:
        self.assertEqual(repr(Card(14, 3)), "♠A")

    def test_card_repr_three(self) -> None:
        self.assertEqual(repr(Card(3, 0)), "♣3")

    def test_card_compare_suit(self) -> None:
        # 同 rank 時，比 suit 大小：♠ > ♥ > ♦ > ♣
        self.assertTrue(Card(14, 3) > Card(14, 2))
        self.assertTrue(Card(14, 2) > Card(14, 1))
        self.assertTrue(Card(14, 1) > Card(14, 0))

    def test_card_compare_rank(self) -> None:
        # 這裡沿用題目文件：2(15) > A(14) > K(13)
        self.assertTrue(Card(15, 0) > Card(14, 3))
        self.assertTrue(Card(14, 0) > Card(13, 3))

    def test_card_compare_equal(self) -> None:
        self.assertFalse(Card(14, 3) > Card(14, 3))

    def test_card_sort_key(self) -> None:
        self.assertEqual(Card(14, 3).to_sort_key(), (14, 3))


class TestDeck(unittest.TestCase):
    """Deck 類別測試：牌組完整性、洗牌、發牌。"""

    def _card_identity(self, c: Any) -> tuple[int, int]:
        # 使用 (rank, suit) 做身分值，避免卡在 __hash__ 是否有實作。
        return (c.rank, c.suit)

    def test_deck_has_52_cards(self) -> None:
        deck = Deck()
        self.assertEqual(len(deck.cards), 52)

    def test_deck_all_unique(self) -> None:
        deck = Deck()
        uniq = {self._card_identity(c) for c in deck.cards}
        self.assertEqual(len(uniq), 52)

    def test_deck_all_ranks(self) -> None:
        deck = Deck()
        ranks = {c.rank for c in deck.cards}
        # Big Two 牌面包含 3..15，其中 15 代表數字 2。
        self.assertEqual(ranks, set(range(3, 16)))

    def test_deck_all_suits(self) -> None:
        deck = Deck()
        suits = {c.suit for c in deck.cards}
        self.assertEqual(suits, {0, 1, 2, 3})

    def test_deck_shuffle(self) -> None:
        deck = Deck()
        before = [self._card_identity(c) for c in deck.cards]
        deck.shuffle()
        after = [self._card_identity(c) for c in deck.cards]

        # 理論上極低機率會洗牌後順序剛好一樣，
        # 若你希望完全無隨機風險，可在 Deck.shuffle 支援 seed 並固定種子測試。
        self.assertNotEqual(before, after)

    def test_deal_5_cards(self) -> None:
        deck = Deck()
        dealt = deck.deal(5)
        self.assertEqual(len(dealt), 5)
        self.assertEqual(len(deck.cards), 47)

    def test_deal_multiple(self) -> None:
        deck = Deck()
        deck.deal(5)
        deck.deal(3)
        self.assertEqual(len(deck.cards), 44)

    def test_deal_exceed(self) -> None:
        deck = Deck()
        dealt = deck.deal(60)
        self.assertEqual(len(dealt), 52)
        self.assertEqual(len(deck.cards), 0)


class TestHand(unittest.TestCase):
    """Hand 類別測試：排序、查找、移除、迭代。"""

    def test_hand_creation(self) -> None:
        h = Hand([Card(14, 3), Card(3, 0), Card(13, 2)])
        self.assertEqual(len(h.cards), 3)

    def test_hand_sort_desc(self) -> None:
        # 規格期望排序後：♠A, ♥K, ♠3, ♣3
        h = Hand([Card(3, 0), Card(14, 3), Card(3, 3), Card(13, 2)])
        h.sort_desc()
        self.assertEqual([repr(c) for c in h.cards], ["♠A", "♥K", "♠3", "♣3"])

    def test_hand_find_3_clubs(self) -> None:
        h = Hand([Card(14, 3), Card(3, 0), Card(3, 1)])
        found = h.find_3_of_clubs()
        self.assertIsNotNone(found)
        self.assertEqual(repr(found), "♣3")

    def test_hand_find_3_clubs_none(self) -> None:
        h = Hand([Card(14, 3), Card(3, 1)])
        self.assertIsNone(h.find_3_of_clubs())

    def test_hand_remove(self) -> None:
        c1 = Card(14, 3)
        c2 = Card(3, 0)
        h = Hand([c1, c2])
        h.remove_card(c1)
        self.assertEqual(len(h.cards), 1)
        self.assertEqual(repr(h.cards[0]), repr(c2))

    def test_hand_remove_not_found(self) -> None:
        h = Hand([Card(14, 3), Card(3, 0)])
        h.remove_card(Card(13, 2))
        self.assertEqual(len(h.cards), 2)

    def test_hand_iteration(self) -> None:
        h = Hand([Card(14, 3), Card(3, 0)])
        self.assertEqual(len(list(h)), 2)


class TestPlayer(unittest.TestCase):
    """Player 類別測試：初始化、拿牌、出牌。"""

    def test_player_human(self) -> None:
        p = Player("Player1", False)
        self.assertFalse(p.is_ai)

    def test_player_ai(self) -> None:
        p = Player("AI_1", True)
        self.assertTrue(p.is_ai)

    def test_player_take(self) -> None:
        p = Player("P", False)
        p.take_cards([Card(14, 3), Card(3, 0)])
        self.assertEqual(len(p.hand.cards), 2)

    def test_player_play(self) -> None:
        p = Player("P", False)
        c = Card(14, 3)
        p.take_cards([c, Card(3, 0)])

        played = p.play_card(c)

        self.assertEqual(repr(played), repr(c))
        self.assertEqual(len(p.hand.cards), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
