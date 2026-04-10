"""
Big Two 遊戲 - 牌型分類單元測試
測試 HandClassifier 類別的牌型分類、比較和合法性檢查功能

此測試套件使用 Python 標準函式庫 unittest 框架，驗證各牌型的正確分類和比較
"""

import unittest
from typing import Optional, List
from game.models import Card
from game.classifier import CardType, HandClassifier


# ==================== 單元測試類別 ====================

class TestCardType(unittest.TestCase):
    """CardType 列舉的單元測試"""
    
    def test_cardtype_values(self):
        """測試：CardType 列舉值"""
        # 驗證各牌型的列舉值
        self.assertEqual(CardType.SINGLE.value, 1)
        self.assertEqual(CardType.PAIR.value, 2)
        self.assertEqual(CardType.TRIPLE.value, 3)
        self.assertEqual(CardType.STRAIGHT.value, 4)
        self.assertEqual(CardType.FLUSH.value, 5)
        self.assertEqual(CardType.FULL_HOUSE.value, 6)
        self.assertEqual(CardType.FOUR_OF_A_KIND.value, 7)
        self.assertEqual(CardType.STRAIGHT_FLUSH.value, 8)


class TestClassifySingle(unittest.TestCase):
    """單張牌分類測試"""
    
    def test_classify_single_ace(self):
        """測試：黑桃 A 單張分類"""
        cards = [Card(14, 3)]  # ♠A
        result = HandClassifier.classify(cards)
        self.assertEqual(result, (CardType.SINGLE, 14, 3))
    
    def test_classify_single_two(self):
        """測試：梅花 2 單張分類"""
        cards = [Card(15, 0)]  # ♣2
        result = HandClassifier.classify(cards)
        self.assertEqual(result, (CardType.SINGLE, 15, 0))
    
    def test_classify_single_three(self):
        """測試：梅花 3 單張分類"""
        cards = [Card(3, 0)]  # ♣3
        result = HandClassifier.classify(cards)
        self.assertEqual(result, (CardType.SINGLE, 3, 0))


class TestClassifyPair(unittest.TestCase):
    """對子分類測試"""
    
    def test_classify_pair(self):
        """測試：黑桃和紅心 A 對子分類"""
        cards = [Card(14, 3), Card(14, 2)]  # ♠A, ♥A
        result = HandClassifier.classify(cards)
        # 花色應為較大的值 (3)
        self.assertEqual(result, (CardType.PAIR, 14, 3))
    
    def test_classify_pair_diff_rank(self):
        """測試：不同牌面的牌無法分類為對子"""
        cards = [Card(14, 3), Card(13, 3)]  # ♠A, ♠K
        result = HandClassifier.classify(cards)
        # 牌面不同，無法分類為對子
        self.assertIsNone(result)


class TestClassifyTriple(unittest.TestCase):
    """三條分類測試"""
    
    def test_classify_triple(self):
        """測試：三張 A 三條分類"""
        cards = [Card(14, 3), Card(14, 2), Card(14, 1)]  # ♠A, ♥A, ♦A
        result = HandClassifier.classify(cards)
        # 花色應為最大的值 (3)
        self.assertEqual(result, (CardType.TRIPLE, 14, 3))
    
    def test_classify_triple_not_enough(self):
        """測試：兩張相同牌的 A 會被分類為對子，而非三條"""
        cards = [Card(14, 3), Card(14, 2)]  # 只有 2 張 A
        result = HandClassifier.classify(cards)
        # 牌數為 2，會被分類為 PAIR，而非 TRIPLE
        self.assertEqual(result, (CardType.PAIR, 14, 3))


class TestClassifyFive(unittest.TestCase):
    """五張牌型分類測試"""
    
    def test_classify_straight(self):
        """測試：3-4-5-6-7 順子分類"""
        cards = [Card(3, 0), Card(4, 1), Card(5, 2), Card(6, 3), Card(7, 0)]
        result = HandClassifier.classify(cards)
        # 以最大牌面值 (7) 作為代表
        self.assertEqual(result, (CardType.STRAIGHT, 7, 0))
    
    def test_classify_straight_ace_low(self):
        """測試：A-2-3-4-5 特殊順子分類"""
        cards = [Card(14, 0), Card(15, 1), Card(3, 2), Card(4, 3), Card(5, 0)]
        result = HandClassifier.classify(cards)
        # A 被當作最小牌，以 5 作為代表
        self.assertEqual(result, (CardType.STRAIGHT, 5, 0))
    
    def test_classify_flush(self):
        """測試：五張梅花同花分類"""
        cards = [Card(3, 0), Card(5, 0), Card(7, 0), Card(9, 0), Card(11, 0)]
        result = HandClassifier.classify(cards)
        # 最大牌面值為 11 (J)
        self.assertEqual(result, (CardType.FLUSH, 11, 0))
    
    def test_classify_full_house(self):
        """測試：三 A + 對 2（葫蘆）分類"""
        cards = [Card(14, 3), Card(14, 2), Card(14, 1), Card(15, 0), Card(15, 1)]
        result = HandClassifier.classify(cards)
        # 以三條的牌面值 (14) 作為代表，花色為最大值 (3)
        self.assertEqual(result, (CardType.FULL_HOUSE, 14, 3))
    
    def test_classify_four_of_a_kind(self):
        """測試：四 A + 一張 3（四條）分類"""
        cards = [Card(14, 3), Card(14, 2), Card(14, 1), Card(14, 0), Card(3, 1)]
        result = HandClassifier.classify(cards)
        # 以四條的牌面值 (14) 作為代表，花色為最大值 (3)
        self.assertEqual(result, (CardType.FOUR_OF_A_KIND, 14, 3))
    
    def test_classify_straight_flush(self):
        """測試：3♣-4♣-5♣-6♣-7♣ 同花順分類"""
        cards = [Card(3, 0), Card(4, 0), Card(5, 0), Card(6, 0), Card(7, 0)]
        result = HandClassifier.classify(cards)
        # 以最大牌面值 (7) 和花色 (0) 作為代表
        self.assertEqual(result, (CardType.STRAIGHT_FLUSH, 7, 0))


class TestCompare(unittest.TestCase):
    """牌型比較測試"""
    
    def test_compare_single_rank(self):
        """測試：單張 A vs 單張 K（同花色）"""
        hand1 = [Card(14, 3)]  # ♠A
        hand2 = [Card(13, 3)]  # ♠K
        # A > K，應傳回 1
        self.assertEqual(HandClassifier.compare(hand1, hand2), 1)
    
    def test_compare_single_suit(self):
        """測試：黑桃 A vs 紅心 A（同牌面）"""
        hand1 = [Card(14, 3)]  # ♠A
        hand2 = [Card(14, 2)]  # ♥A
        # ♠ > ♥，應傳回 1
        self.assertEqual(HandClassifier.compare(hand1, hand2), 1)
    
    def test_compare_pair_rank(self):
        """測試：對 A vs 對 K"""
        hand1 = [Card(14, 3), Card(14, 2)]
        hand2 = [Card(13, 3), Card(13, 2)]
        # 對 A > 對 K，應傳回 1
        self.assertEqual(HandClassifier.compare(hand1, hand2), 1)
    
    def test_compare_pair_suit(self):
        """測試：對 A (♠♥) vs 對 A (♦♣)"""
        hand1 = [Card(14, 3), Card(14, 2)]  # 花色為 3
        hand2 = [Card(14, 1), Card(14, 0)]  # 花色為 1
        # 花色 3 > 花色 1，應傳回 1
        self.assertEqual(HandClassifier.compare(hand1, hand2), 1)
    
    def test_compare_different_type(self):
        """測試：對子 vs 單張"""
        hand1 = [Card(3, 0), Card(3, 1)]    # 對 3
        hand2 = [Card(15, 0)]               # 單張 2
        # 牌型 PAIR (2) > SINGLE (1)，應傳回 1
        self.assertEqual(HandClassifier.compare(hand1, hand2), 1)
    
    def test_compare_flush_vs_straight(self):
        """測試：同花 vs 順子"""
        hand1 = [Card(3, 0), Card(5, 0), Card(7, 0), Card(9, 0), Card(11, 0)]  # 同花
        hand2 = [Card(3, 1), Card(4, 2), Card(5, 3), Card(6, 0), Card(7, 1)]    # 順子
        # 牌型 FLUSH (5) > STRAIGHT (4)，應傳回 1
        self.assertEqual(HandClassifier.compare(hand1, hand2), 1)
    
    def test_compare_equal(self):
        """測試：完全相同的牌"""
        hand1 = [Card(14, 3)]
        hand2 = [Card(14, 3)]
        # 完全相同，應傳回 0
        self.assertEqual(HandClassifier.compare(hand1, hand2), 0)


class TestCanPlay(unittest.TestCase):
    """合法性檢查測試"""
    
    def test_can_play_first_3clubs(self):
        """測試：第一手必須出梅花三"""
        hand = [Card(3, 0)]  # ♣3
        # 沒有上一手（None），出梅花三應該合法
        self.assertTrue(HandClassifier.can_play(None, hand))
    
    def test_can_play_first_not_3clubs(self):
        """測試：第一手不能出非梅花三的牌"""
        hand = [Card(14, 3)]  # ♠A
        # 沒有上一手，但不是梅花三，應該違法
        self.assertFalse(HandClassifier.can_play(None, hand))
    
    def test_can_play_same_type(self):
        """測試：對 5 vs 對 6（牌型相同，且更大）"""
        last_hand = [Card(5, 0), Card(5, 1)]  # 對 5
        current_hand = [Card(6, 0), Card(6, 1)]  # 對 6
        # 牌型相同，且對 6 > 對 5，應該合法
        self.assertTrue(HandClassifier.can_play(last_hand, current_hand))
    
    def test_can_play_diff_type(self):
        """測試：對 5 vs 單張 6（牌型不同）"""
        last_hand = [Card(5, 0), Card(5, 1)]  # 對 5
        current_hand = [Card(6, 0)]  # 單張 6
        # 牌型不同，無法出牌
        self.assertFalse(HandClassifier.can_play(last_hand, current_hand))
    
    def test_can_play_not_stronger(self):
        """測試：對 10 vs 對 5（牌型相同，但更小）"""
        last_hand = [Card(10, 0), Card(10, 1)]  # 對 10
        current_hand = [Card(5, 0), Card(5, 1)]  # 對 5
        # 牌型相同，但對 5 < 對 10，無法出牌
        self.assertFalse(HandClassifier.can_play(last_hand, current_hand))


# ==================== 測試執行 ====================

if __name__ == '__main__':
    # 使用 verbose 模式輸出詳細測試結果
    unittest.main(verbosity=2)
