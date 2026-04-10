"""
Big Two 遊戲 - 牌型搜尋單元測試
測試 HandFinder 類別的牌型搜尋功能

此測試套件使用 Python 標準函式庫 unittest 框架，驗證從手牌中有效搜尋各種牌型的功能
"""

import unittest
from typing import List, Optional
from game.models import Card, Hand
from game.classifier import CardType, HandClassifier
from game.finder import HandFinder


# ==================== 單元測試類別 ====================

class TestFindSingles(unittest.TestCase):
    """單張搜尋測試"""
    
    def test_find_singles(self):
        """測試：搜尋三張不同的牌"""
        cards = [Card(14, 3), Card(13, 2), Card(3, 0)]
        singles = HandFinder.find_singles(cards)
        # 應該找到 3 個單張
        self.assertEqual(len(singles), 3)
        # 每個單張應該包含一張牌
        for single in singles:
            self.assertEqual(len(single), 1)
    
    def test_find_singles_empty(self):
        """測試：空手牌搜尋單張"""
        cards = []
        singles = HandFinder.find_singles(cards)
        # 空手牌應該沒有單張
        self.assertEqual(len(singles), 0)


class TestFindPairs(unittest.TestCase):
    """對子搜尋測試"""
    
    def test_find_pairs_one(self):
        """測試：找出一對 A"""
        cards = [Card(14, 3), Card(14, 2), Card(3, 0)]
        pairs = HandFinder.find_pairs(cards)
        # 應該找到 1 個對子
        self.assertEqual(len(pairs), 1)
        # 對子應該包含兩張牌
        self.assertEqual(len(pairs[0]), 2)
    
    def test_find_pairs_two(self):
        """測試：找出兩個對子"""
        cards = [Card(14, 3), Card(14, 2), Card(13, 3), Card(13, 0)]
        pairs = HandFinder.find_pairs(cards)
        # 應該找到 2 個對子
        self.assertEqual(len(pairs), 2)
    
    def test_find_pairs_none(self):
        """測試：手牌中沒有對子"""
        cards = [Card(14, 3), Card(13, 2), Card(3, 0)]
        pairs = HandFinder.find_pairs(cards)
        # 應該沒有對子
        self.assertEqual(len(pairs), 0)


class TestFindTriples(unittest.TestCase):
    """三條搜尋測試"""
    
    def test_find_triples_one(self):
        """測試：找出一個三條 A"""
        cards = [Card(14, 3), Card(14, 2), Card(14, 1), Card(3, 0)]
        triples = HandFinder.find_triples(cards)
        # 應該找到 1 個三條
        self.assertEqual(len(triples), 1)
        # 三條應該包含三張牌
        self.assertEqual(len(triples[0]), 3)
    
    def test_find_triples_with_extra(self):
        """測試：三 A + 對 K，找出三條 A"""
        cards = [Card(14, 3), Card(14, 2), Card(14, 1), Card(13, 0), Card(13, 1)]
        triples = HandFinder.find_triples(cards)
        # 應該找到 1 個三條（三 A）
        self.assertEqual(len(triples), 1)


class TestFindFiveCardTypes(unittest.TestCase):
    """五張牌型搜尋測試"""
    
    def test_find_straight(self):
        """測試：找出順子"""
        # 3-4-5-6-7
        cards = [
            Card(3, 0), Card(4, 1), Card(5, 2), Card(6, 3), Card(7, 0),
            Card(14, 3)  # 額外的 A 作為干擾
        ]
        straights = HandFinder.find_straights(cards)
        # 應該找到至少 1 個順子
        self.assertGreater(len(straights), 0)
    
    def test_find_flush(self):
        """測試：找出同花"""
        # 五張梅花
        cards = [
            Card(3, 0), Card(5, 0), Card(7, 0), Card(9, 0), Card(11, 0),
            Card(14, 3)  # 額外的 A 作為干擾
        ]
        flushes = HandFinder.find_flushes(cards)
        # 應該找到至少 1 個同花
        self.assertGreater(len(flushes), 0)
    
    def test_find_full_house(self):
        """測試：找出葫蘆"""
        # 三 A + 對 2
        cards = [
            Card(14, 3), Card(14, 2), Card(14, 1),
            Card(15, 0), Card(15, 1),
            Card(3, 0)  # 額外的 3 作為干擾
        ]
        full_houses = HandFinder.find_full_houses(cards)
        # 應該找到至少 1 個葫蘆
        self.assertGreater(len(full_houses), 0)
    
    def test_find_four_of_a_kind(self):
        """測試：找出四條"""
        # 四 A + 一張 3
        cards = [
            Card(14, 3), Card(14, 2), Card(14, 1), Card(14, 0),
            Card(3, 0),
            Card(13, 2)  # 額外的 K 作為干擾
        ]
        four_of_a_kinds = HandFinder.find_four_of_a_kinds(cards)
        # 應該找到至少 1 個四條
        self.assertGreater(len(four_of_a_kinds), 0)
    
    def test_find_straight_flush(self):
        """測試：找出同花順"""
        # 3♣-4♣-5♣-6♣-7♣
        cards = [
            Card(3, 0), Card(4, 0), Card(5, 0), Card(6, 0), Card(7, 0),
            Card(14, 3)  # 額外的 A 作為干擾
        ]
        straight_flushes = HandFinder.find_straight_flushes(cards)
        # 應該找到至少 1 個同花順
        self.assertGreater(len(straight_flushes), 0)


class TestFindPlayable(unittest.TestCase):
    """合法出牌搜尋測試"""
    
    def test_first_turn_with_3clubs(self):
        """測試：有梅花三時，第一手可以出梅花三"""
        hand = [Card(3, 0), Card(14, 3), Card(13, 2)]
        playable = HandFinder.find_playable(None, hand)
        # 應該找到 1 個可出的牌（梅花三）
        self.assertEqual(len(playable), 1)
        # 該牌應該是梅花三
        self.assertEqual(playable[0][0].rank, 3)
        self.assertEqual(playable[0][0].suit, 0)
    
    def test_first_turn_without_3clubs(self):
        """測試：沒有梅花三時，第一手無法出牌"""
        hand = [Card(14, 3), Card(13, 2), Card(12, 1)]
        playable = HandFinder.find_playable(None, hand)
        # 應該沒有可出的牌
        self.assertEqual(len(playable), 0)
    
    def test_with_last_single(self):
        """測試：上一手是單 5，只回單張"""
        last = [Card(5, 0)]  # 上一手出的單 5
        hand = [Card(6, 0), Card(5, 1), Card(5, 2)]  # 手牌包含 6、兩個 5
        playable = HandFinder.find_playable(last, hand)
        # 應該只找到單張 6（大於單 5）
        self.assertGreater(len(playable), 0)
        # 所有可出的牌應該都是單張
        for play in playable:
            result = HandClassifier.classify(play)
            self.assertEqual(result[0], CardType.SINGLE)
    
    def test_with_last_pair(self):
        """測試：上一手是對 5，只回對子"""
        last = [Card(5, 0), Card(5, 1)]  # 上一手出的對 5
        hand = [Card(6, 0), Card(6, 1), Card(5, 2)]  # 手牌包含對 6、一張 5
        playable = HandFinder.find_playable(last, hand)
        # 應該只找到對 6（大於對 5）
        self.assertGreater(len(playable), 0)
        # 所有可出的牌應該都是對子
        for play in playable:
            result = HandClassifier.classify(play)
            self.assertEqual(result[0], CardType.PAIR)
    
    def test_no_valid_play(self):
        """測試：無法大於上一手"""
        last = [Card(14, 3), Card(14, 2)]  # 上一手出的對 A
        hand = [Card(13, 0), Card(13, 1), Card(3, 0)]  # 手牌只有對 K 和一張 3
        playable = HandFinder.find_playable(last, hand)
        # 對 K 小於對 A，應該無法出牌
        self.assertEqual(len(playable), 0)


# ==================== 測試執行 ====================

if __name__ == '__main__':
    # 使用 verbose 模式輸出詳細測試結果
    unittest.main(verbosity=2)
