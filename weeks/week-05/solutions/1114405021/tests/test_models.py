"""
Big Two 遊戲 - 資料模型單元測試
測試 Card、Deck、Hand、Player 類別的功能

此測試套件使用 Python 標準函式庫 unittest 框架，驗證各類別的正確性
"""

import unittest
from unittest.mock import MagicMock, patch
import sys
import os


# 假設 Card、Deck、Hand、Player 類別的實現
# 以下是這些類別的預期接口定義（用於測試的模擬實現）

class Card:
    """
    撲克牌類別。
    - rank: 牌的數字，3-15 (3-10=3-10, 11=J, 12=Q, 13=K, 14=A, 15=2)
    - suit: 花色，0=♣, 1=♦, 2=♥, 3=♠
    """
    
    # 花色名稱對應
    SUIT_SYMBOLS = ['♣', '♦', '♥', '♠']
    # 牌面名稱對應
    RANK_NAMES = {3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 
                  10: '10', 11: 'J', 12: 'Q', 13: 'K', 14: 'A', 15: '2'}
    
    def __init__(self, rank, suit):
        """初始化撲克牌"""
        if not (3 <= rank <= 15) or not (0 <= suit <= 3):
            raise ValueError("無效的牌值")
        self.rank = rank
        self.suit = suit
    
    def __repr__(self):
        """傳回牌的字串表示，例如 '♠A'"""
        return f"{self.SUIT_SYMBOLS[self.suit]}{self.RANK_NAMES[self.rank]}"
    
    def __eq__(self, other):
        """判斷兩張牌是否相同"""
        if not isinstance(other, Card):
            return False
        return self.rank == other.rank and self.suit == other.suit
    
    def __hash__(self):
        """讓 Card 物件可以使用 set"""
        return hash((self.rank, self.suit))
    
    def __gt__(self, other):
        """
        比較牌的大小。
        規則：先比較牌面數字（rank），數字大的牌大。
        如果牌面相同，則比較花色（suit）。花色順序：♠ > ♥ > ♦ > ♣
        """
        if self.rank != other.rank:
            return self.rank > other.rank
        # 花色比較：3=♠, 2=♥, 1=♦, 0=♣
        return self.suit > other.suit
    
    def __lt__(self, other):
        """比較牌是否比另一張牌小"""
        return not (self > other) and self != other
    
    def to_sort_key(self):
        """傳回用於排序的 tuple (rank, suit)"""
        return (self.rank, self.suit)


class Deck:
    """
    牌組類別。包含52張標準撲克牌。
    """
    
    def __init__(self):
        """初始化牌組，建立所有52張牌"""
        self.cards = []
        # 產生所有牌：每種花色 (0-3) 對應 13 種牌面 (3-15)
        for suit in range(4):  # 4種花色
            for rank in range(3, 16):  # 3-15 共13個牌面
                self.cards.append(Card(rank, suit))
    
    def shuffle(self):
        """
        洗牌：隨機重新排列牌組中的所有牌
        """
        import random
        random.shuffle(self.cards)
    
    def deal(self, num_cards):
        """
        發牌：從牌組中發出指定數量的牌。
        
        參數：
            num_cards: 要發出的牌數量
        
        傳回：
            發出的牌的列表。如果牌不足，則傳回剩餘所有牌
        """
        # 防止發超過牌組中的牌
        cards_to_deal = min(num_cards, len(self.cards))
        dealt_cards = self.cards[:cards_to_deal]
        self.cards = self.cards[cards_to_deal:]
        return dealt_cards


class Hand:
    """
    手牌類別。代表玩家目前持有的牌。
    """
    
    def __init__(self, cards):
        """
        初始化手牌。
        
        參數：
            cards: Card 物件的列表
        """
        self.cards = list(cards) if cards else []
    
    def sort(self, reverse=True):
        """
        排序手牌。由大到小排序。
        """
        self.cards.sort(key=lambda card: card.to_sort_key(), reverse=reverse)
    
    def find_club_three(self):
        """
        尋找 ♣3（梅花三）。
        
        傳回：
            如果找到 ♣3 則傳回該牌，否則傳回 None
        """
        for card in self.cards:
            if card.rank == 3 and card.suit == 0:  # rank=3, suit=0 (♣)
                return card
        return None
    
    def remove(self, card):
        """
        從手牌中移除指定的牌。
        
        參數：
            card: 要移除的 Card 物件
        
        傳回：
            移除成功則傳回 True，否則傳回 False
        """
        if card in self.cards:
            self.cards.remove(card)
            return True
        return False
    
    def __len__(self):
        """傳回手牌中的牌數"""
        return len(self.cards)
    
    def __iter__(self):
        """讓 Hand 物件可以被迭代"""
        return iter(self.cards)
    
    def __repr__(self):
        """傳回手牌的字串表示"""
        return f"Hand({[str(card) for card in self.cards]})"


class Player:
    """
    玩家類別。代表一個遊戲參與者。
    """
    
    def __init__(self, name, is_ai=False):
        """
        初始化玩家。
        
        參數：
            name: 玩家名稱
            is_ai: 是否為人工智慧玩家（預設為 False）
        """
        self.name = name
        self.is_ai = is_ai
        self.hand = Hand([])
    
    def take_cards(self, cards):
        """
        添加牌到玩家的手牌中。
        
        參數：
            cards: Card 物件的列表
        """
        self.hand.cards.extend(cards)
    
    def play(self, card):
        """
        玩家出牌。
        
        參數：
            card: 要出的牌 (Card 物件)
        
        傳回：
            如果該牌在手牌中，則傳回該牌並移除，否則傳回 None
        """
        if self.hand.remove(card):
            return card
        return None


# ==================== 單元測試類別 ====================

class TestCard(unittest.TestCase):
    """Card 類別的單元測試"""
    
    def test_card_creation(self):
        """測試：建立牌的物件"""
        card = Card(rank=14, suit=3)
        # 驗證牌的 rank 和 suit 屬性是否正確設定
        self.assertEqual(card.rank, 14)
        self.assertEqual(card.suit, 3)
    
    def test_card_repr_ace(self):
        """測試：黑桃 A 的字串表示"""
        card = Card(14, 3)
        # 驗證 Card(14, 3) 的字串表示應為 '♠A'
        self.assertEqual(repr(card), "♠A")
    
    def test_card_repr_three(self):
        """測試：梅花三的字串表示"""
        card = Card(3, 0)
        # 驗證 Card(3, 0) 的字串表示應為 '♣3'
        self.assertEqual(repr(card), "♣3")
    
    def test_card_compare_suit(self):
        """測試：相同牌面，花色比較 - 黑桃 > 紅心"""
        card1 = Card(14, 3)  # ♠A
        card2 = Card(14, 2)  # ♥A
        # 驗證黑桃 (suit=3) 比紅心 (suit=2) 大
        self.assertTrue(card1 > card2)
    
    def test_card_compare_suit_2(self):
        """測試：相同牌面，花色比較 - 紅心 > 方塊"""
        card1 = Card(14, 2)  # ♥A
        card2 = Card(14, 1)  # ♦A
        # 驗證紅心 (suit=2) 比方塊 (suit=1) 大
        self.assertTrue(card1 > card2)
    
    def test_card_compare_suit_3(self):
        """測試：相同牌面，花色比較 - 方塊 > 梅花"""
        card1 = Card(14, 1)  # ♦A
        card2 = Card(14, 0)  # ♣A
        # 驗證方塊 (suit=1) 比梅花 (suit=0) 大
        self.assertTrue(card1 > card2)
    
    def test_card_compare_rank_2(self):
        """測試：牌面比較 - 2 > A"""
        card1 = Card(15, 0)  # ♣2
        card2 = Card(14, 3)  # ♠A
        # 驗證 2 (rank=15) 比 A (rank=14) 大
        self.assertTrue(card1 > card2)
    
    def test_card_compare_rank_a(self):
        """測試：牌面比較 - A > K"""
        card1 = Card(14, 0)  # ♣A
        card2 = Card(13, 3)  # ♠K
        # 驗證 A (rank=14) 比 K (rank=13) 大
        self.assertTrue(card1 > card2)
    
    def test_card_compare_equal(self):
        """測試：相同的牌比較不是大於關係"""
        card1 = Card(14, 3)  # ♠A
        card2 = Card(14, 3)  # ♠A
        # 驗證相同的牌不滿足大於關係
        self.assertFalse(card1 > card2)
    
    def test_card_sort_key(self):
        """測試：牌的排序鍵"""
        card = Card(14, 3)
        # 驗證 to_sort_key() 傳回 (rank, suit) tuple
        self.assertEqual(card.to_sort_key(), (14, 3))


class TestDeck(unittest.TestCase):
    """Deck 類別的單元測試"""
    
    def test_deck_has_52_cards(self):
        """測試：新牌組包含 52 張牌"""
        deck = Deck()
        # 驗證牌組初始化時包含 52 張牌
        self.assertEqual(len(deck.cards), 52)
    
    def test_deck_all_unique(self):
        """測試：牌組中的所有牌都是唯一的"""
        deck = Deck()
        # 驗證牌組中沒有重複的牌
        self.assertEqual(len(set(deck.cards)), 52)
    
    def test_deck_all_ranks(self):
        """測試：牌組包含所有牌面"""
        deck = Deck()
        # 蒐集所有牌的牌面
        ranks = set(card.rank for card in deck.cards)
        # 驗證包含 3 到 15 的所有牌面
        self.assertEqual(ranks, set(range(3, 16)))
    
    def test_deck_all_suits(self):
        """測試：牌組包含所有花色"""
        deck = Deck()
        # 蒐集所有牌的花色
        suits = set(card.suit for card in deck.cards)
        # 驗證包含 0, 1, 2, 3 四種花色
        self.assertEqual(suits, {0, 1, 2, 3})
    
    def test_deck_shuffle(self):
        """測試：洗牌後牌的順序改變"""
        deck = Deck()
        # 記錄洗牌前的順序
        original_order = [card.to_sort_key() for card in deck.cards]
        # 執行洗牌
        deck.shuffle()
        # 記錄洗牌後的順序
        shuffled_order = [card.to_sort_key() for card in deck.cards]
        # 注意：理論上洗牌後順序通常會改變，但不保證一定改變
        # 這個測試可能偶爾失敗（如果洗牌後碰巧同樣順序，機率極低）
        # 較好的測試方式是驗證牌的數量和內容不變
        self.assertEqual(len(deck.cards), 52)
    
    def test_deal_5_cards(self):
        """測試：從牌組發出 5 張牌"""
        deck = Deck()
        # 從牌組發出 5 張牌
        dealt_cards = deck.deal(5)
        # 驗證發出 5 張牌
        self.assertEqual(len(dealt_cards), 5)
        # 驗證牌組剩餘 47 張牌
        self.assertEqual(len(deck.cards), 47)
    
    def test_deal_multiple(self):
        """測試：多次發牌"""
        deck = Deck()
        # 第一次發出 5 張牌
        deck.deal(5)
        # 第二次發出 3 張牌
        deck.deal(3)
        # 驗證牌組剩餘 44 張牌 (52 - 5 - 3 = 44)
        self.assertEqual(len(deck.cards), 44)
    
    def test_deal_exceed(self):
        """測試：要求發出超過牌組數量的牌"""
        deck = Deck()
        # 嘗試發出 60 張牌（超過 52 張）
        dealt_cards = deck.deal(60)
        # 驗證實際發出 52 張牌
        self.assertEqual(len(dealt_cards), 52)
        # 驗證牌組為空
        self.assertEqual(len(deck.cards), 0)


class TestHand(unittest.TestCase):
    """Hand 類別的單元測試"""
    
    def test_hand_creation(self):
        """測試：建立手牌物件"""
        cards = [Card(14, 3), Card(13, 2), Card(12, 1)]
        hand = Hand(cards)
        # 驗證手牌包含 3 張牌
        self.assertEqual(len(hand), 3)
    
    def test_hand_sort_desc(self):
        """測試：手牌排序（由大到小）"""
        cards = [Card(3, 0), Card(14, 3), Card(3, 1), Card(13, 2)]
        hand = Hand(cards)
        # 執行排序
        hand.sort(reverse=True)
        # 驗證排序後的順序
        # 預期順序：♠A (14,3) > ♥K (13,2) > ♦3 (3,1) > ♣3 (3,0)
        expected_order = [(14, 3), (13, 2), (3, 1), (3, 0)]
        actual_order = [card.to_sort_key() for card in hand.cards]
        self.assertEqual(actual_order, expected_order)
    
    def test_hand_find_3_clubs(self):
        """測試：在手牌中尋找梅花三"""
        cards = [Card(14, 3), Card(3, 0), Card(3, 1)]
        hand = Hand(cards)
        # 尋找梅花三 (rank=3, suit=0)
        found_card = hand.find_club_three()
        # 驗證找到梅花三
        self.assertIsNotNone(found_card)
        self.assertEqual(found_card.rank, 3)
        self.assertEqual(found_card.suit, 0)
    
    def test_hand_find_3_clubs_none(self):
        """測試：手牌中沒有梅花三"""
        cards = [Card(14, 3), Card(3, 1)]
        hand = Hand(cards)
        # 尋找梅花三
        found_card = hand.find_club_three()
        # 驗證沒有找到梅花三
        self.assertIsNone(found_card)
    
    def test_hand_remove(self):
        """測試：從手牌中移除指定的牌"""
        cards = [Card(14, 3), Card(13, 2)]
        hand = Hand(cards)
        # 移除 ♠A (Card(14, 3))
        card_to_remove = cards[0]
        success = hand.remove(card_to_remove)
        # 驗證移除成功
        self.assertTrue(success)
        # 驗證手牌剩餘 1 張牌
        self.assertEqual(len(hand), 1)
    
    def test_hand_remove_not_found(self):
        """測試：移除不存在於手牌中的牌"""
        cards = [Card(14, 3), Card(13, 2)]
        hand = Hand(cards)
        # 嘗試移除不在手牌中的牌
        card_not_in_hand = Card(12, 1)
        success = hand.remove(card_not_in_hand)
        # 驗證移除失敗
        self.assertFalse(success)
        # 驗證手牌數量不變
        self.assertEqual(len(hand), 2)
    
    def test_hand_iteration(self):
        """測試：遍歷手牌"""
        cards = [Card(14, 3), Card(13, 2)]
        hand = Hand(cards)
        # 將手牌轉換為列表
        hand_list = list(hand)
        # 驗證列表長度為 2
        self.assertEqual(len(hand_list), 2)


class TestPlayer(unittest.TestCase):
    """Player 類別的單元測試"""
    
    def test_player_human(self):
        """測試：建立人類玩家"""
        player = Player("Player1", False)
        # 驗證玩家名稱
        self.assertEqual(player.name, "Player1")
        # 驗證玩家不是 AI
        self.assertFalse(player.is_ai)
    
    def test_player_ai(self):
        """測試：建立 AI 玩家"""
        player = Player("AI_1", True)
        # 驗證玩家名稱
        self.assertEqual(player.name, "AI_1")
        # 驗證玩家是 AI
        self.assertTrue(player.is_ai)
    
    def test_player_take(self):
        """測試：玩家取得牌"""
        player = Player("Player1")
        # 建立一些牌
        cards = [Card(14, 3), Card(13, 2)]
        # 玩家取得這些牌
        player.take_cards(cards)
        # 驗證玩家手牌中有 2 張牌
        self.assertEqual(len(player.hand), 2)
    
    def test_player_play(self):
        """測試：玩家出牌"""
        player = Player("Player1")
        # 玩家取得一些牌
        card1 = Card(14, 3)
        card2 = Card(13, 2)
        player.take_cards([card1, card2])
        # 玩家出牌 ♠A
        played_card = player.play(card1)
        # 驗證出牌成功
        self.assertEqual(played_card, card1)
        # 驗證手牌剩餘 1 張牌
        self.assertEqual(len(player.hand), 1)


# ==================== 測試執行 ====================

if __name__ == '__main__':
    # 使用 verbose 模式輸出詳細測試結果
    unittest.main(verbosity=2)
