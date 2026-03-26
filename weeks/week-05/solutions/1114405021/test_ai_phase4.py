"""
Phase 4：AI 策略（AIStrategy）單元測試

設計依據：
- p4-test.md（測試案例）
- p4-dev.md（方法介面與評分公式）

測試目標：
1. 驗證 score_play() 是否符合評分邏輯。
2. 驗證 select_best() 是否依規格做貪心選擇。
3. 驗證在完整情境下，AI 是否能做出合理且合法的出牌。

注意：
- 若 game/ai.py 尚未實作，這份測試在 Red 階段失敗是正常現象。
- 註解採繁體中文，強調「為什麼這樣測」與「要保證的行為」。
"""

from __future__ import annotations

import importlib
import unittest


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

_AI_MODULE_CANDIDATES = [
    "game.ai",
    "ai",
    "bigtwo.ai",
    "src.ai",
]


def _load_symbol(module_candidates: list[str], symbol: str):
    """從候選模組清單嘗試載入符號，提升測試對專案結構的相容性。"""
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
CardType = _load_symbol(_CLASSIFIER_MODULE_CANDIDATES, "CardType")
HandClassifier = _load_symbol(_CLASSIFIER_MODULE_CANDIDATES, "HandClassifier")
AIStrategy = _load_symbol(_AI_MODULE_CANDIDATES, "AIStrategy")


def C(rank: int, suit: int) -> Card:
    """建立卡牌縮寫，讓測試案例更精簡易讀。"""
    return Card(rank, suit)


class TestScorePlay(unittest.TestCase):
    """評分函數 score_play 測試。"""

    def test_score_single(self):
        # 規格公式：牌型*100 + 數字*10 + 其他加分
        # 單張♠A 在手牌 2 張情況下，至少會有 1*100 + 14*10 = 240。
        hand = Hand([C(14, 3), C(13, 2)])
        score = AIStrategy.score_play([C(14, 3)], hand)
        self.assertGreaterEqual(score, 240)

    def test_score_pair_higher(self):
        # 在同手牌背景下，對子分數應高於單張（牌型權重較高）。
        hand = Hand([C(10, 3), C(10, 2), C(9, 0)])
        single_score = AIStrategy.score_play([C(10, 3)], hand)
        pair_score = AIStrategy.score_play([C(10, 3), C(10, 2)], hand)
        self.assertGreater(pair_score, single_score)

    def test_score_triple_higher(self):
        # 三條分數應高於對子（牌型等級更高）。
        hand = Hand([C(8, 3), C(8, 2), C(8, 1), C(5, 0)])
        pair_score = AIStrategy.score_play([C(8, 3), C(8, 2)], hand)
        triple_score = AIStrategy.score_play([C(8, 3), C(8, 2), C(8, 1)], hand)
        self.assertGreater(triple_score, pair_score)

    def test_score_near_empty(self):
        # 若出牌後手牌可清空，規格要求加上 EMPTY_HAND_BONUS（10000 級距）。
        hand = Hand([C(14, 3)])
        score = AIStrategy.score_play([C(14, 3)], hand)
        self.assertGreater(score, 10000)

    def test_score_low_cards(self):
        # 若出牌後進入接近出完狀態（剩 <=3），應有 NEAR_EMPTY_BONUS（500 級距）。
        hand = Hand([C(7, 0), C(8, 1)])
        score = AIStrategy.score_play([C(7, 0)], hand)
        self.assertGreater(score, 500)

    def test_score_spade_bonus(self):
        # 同 rank 的單張，♠ 應因 SPADE_BONUS 比非♠分數更高。
        hand = Hand([C(9, 3), C(9, 2), C(4, 0)])
        spade = AIStrategy.score_play([C(9, 3)], hand)
        heart = AIStrategy.score_play([C(9, 2)], hand)
        self.assertGreater(spade, heart)


class TestSelectBest(unittest.TestCase):
    """最佳選擇 select_best 測試。"""

    def test_select_best(self):
        # 當合法候選有單張與對子，規格預期偏好對子（更高牌型分數）。
        hand = Hand([C(10, 3), C(10, 2), C(5, 0)])
        valid_plays = [[C(10, 3)], [C(10, 3), C(10, 2)]]
        best = AIStrategy.select_best(valid_plays, hand)
        self.assertIsNotNone(best)
        self.assertEqual(len(best), 2)
        self.assertEqual(HandClassifier.classify(best)[0], CardType.PAIR)

    def test_select_first_turn(self):
        # 第一回合只能出包含 3♣ 的牌。
        hand = Hand([C(3, 0), C(14, 3), C(14, 2)])
        valid_plays = [[C(14, 3)], [C(3, 0)]]
        best = AIStrategy.select_best(valid_plays, hand, is_first=True)
        self.assertIsNotNone(best)
        self.assertTrue(any(c.rank == 3 and c.suit == 0 for c in best))

    def test_select_empty(self):
        hand = Hand([C(14, 3)])
        best = AIStrategy.select_best([], hand)
        self.assertIsNone(best)


class TestAIStrategyE2E(unittest.TestCase):
    """完整策略情境測試。"""

    def test_ai_always_plays(self):
        # 只要有合法候選，就不應回傳 None。
        hand = Hand([C(6, 0), C(7, 1), C(9, 3)])
        valid_plays = [[C(6, 0)], [C(7, 1)], [C(9, 3)]]
        best = AIStrategy.select_best(valid_plays, hand)
        self.assertIsNotNone(best)

    def test_ai_prefers_high(self):
        # 在同牌型（單張）候選下，應偏好更高牌。
        hand = Hand([C(6, 0), C(12, 1), C(14, 3)])
        valid_plays = [[C(6, 0)], [C(12, 1)], [C(14, 3)]]
        best = AIStrategy.select_best(valid_plays, hand)
        self.assertIsNotNone(best)
        self.assertEqual(best[0].rank, 14)

    def test_ai_try_empty(self):
        # 只剩最後一張時，應優先選擇可直接出完的牌。
        hand = Hand([C(11, 3)])
        valid_plays = [[C(11, 3)]]
        best = AIStrategy.select_best(valid_plays, hand)
        self.assertEqual(best, [C(11, 3)])


if __name__ == "__main__":
    unittest.main(verbosity=2)
