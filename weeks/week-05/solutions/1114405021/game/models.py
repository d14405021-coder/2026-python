"""
Big Two 遊戲 - 資料模型實現
實作 Card、Deck、Hand、Player 類別

此模組包含大二撲克遊戲所需的所有資料模型，
提供遊戲邏輯所需的基礎類別。
"""

import random
from typing import List, Optional, Tuple


class Card:
    """
    撲克牌類別。代表一張遊戲中的撲克牌。
    
    屬性：
        rank: 牌的數字值，範圍 3-15
               3-10: 數字卡 3-10
               11: Jack (J)
               12: Queen (Q)
               13: King (K)
               14: Ace (A)
               15: 2 (最大的牌面)
        suit: 花色，0=♣梅花, 1=♦方塊, 2=♥紅心, 3=♠黑桃
    """
    
    # 花色符號對應表 - 用於字串表示時顯示花色
    SUIT_SYMBOLS = ['♣', '♦', '♥', '♠']
    
    # 牌面名稱對應表 - 將 rank 值對應到牌面名稱
    RANK_NAMES = {
        3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 
        10: '10', 11: 'J', 12: 'Q', 13: 'K', 14: 'A', 15: '2'
    }
    
    def __init__(self, rank: int, suit: int) -> None:
        """
        初始化撲克牌。
        
        參數：
            rank: 牌的數字 (3-15)
            suit: 花色 (0-3)
        
        異常：
            ValueError: 如果 rank 或 suit 超出有效範圍
        """
        # 驗證輸入的 rank 和 suit 是否有效
        if not (3 <= rank <= 15):
            raise ValueError(f"無效的牌面值: {rank}，應該在 3-15 之間")
        if not (0 <= suit <= 3):
            raise ValueError(f"無效的花色值: {suit}，應該在 0-3 之間")
        
        self.rank = rank
        self.suit = suit
    
    def __repr__(self) -> str:
        """
        傳回牌的字串表示。
        
        範例：
            Card(14, 3) -> '♠A'
            Card(3, 0) -> '♣3'
        
        傳回：
            格式為 "花色牌面" 的字串，例如 '♠A'
        """
        return f"{self.SUIT_SYMBOLS[self.suit]}{self.RANK_NAMES[self.rank]}"
    
    def __eq__(self, other: object) -> bool:
        """
        判斷兩張牌是否相同。
        
        參數：
            other: 要比較的另一個物件
        
        傳回：
            如果兩張牌的 rank 和 suit 都相同則傳回 True，否則傳回 False
        """
        # 檢查 other 是否為 Card 實例
        if not isinstance(other, Card):
            return False
        # 比較 rank 和 suit 是否都相同
        return self.rank == other.rank and self.suit == other.suit
    
    def __hash__(self) -> int:
        """
        計算牌對象的雜湊值。
        
        讓 Card 物件可以被用在 set 和字典中。
        
        傳回：
            牌的雜湊值
        """
        return hash((self.rank, self.suit))
    
    def __gt__(self, other: 'Card') -> bool:
        """
        比較牌的大小（是否大於）。
        
        規則：
            1. 首先比較牌面數字（rank），數字大的牌大
            2. 如果牌面相同，比較花色（suit）
            3. 花色順序：♠ (3) > ♥ (2) > ♦ (1) > ♣ (0)
        
        參數：
            other: 要比較的另一張牌
        
        傳回：
            如果本牌大於另一張牌則傳回 True，否則傳回 False
        """
        # 先比較 rank，rank 大的牌大
        if self.rank != other.rank:
            return self.rank > other.rank
        # rank 相同時，suit 大的牌大（花色順序：♠>♥>♦>♣）
        return self.suit > other.suit
    
    def __lt__(self, other: 'Card') -> bool:
        """
        比較牌的大小（是否小於）。
        
        參數：
            other: 要比較的另一張牌
        
        傳回：
            如果本牌小於另一張牌則傳回 True，否則傳回 False
        """
        # 小於關係：不大於且不相等
        return not (self > other) and self != other
    
    def to_sort_key(self) -> Tuple[int, int]:
        """
        傳回用於排序的 tuple。
        
        傳回：
            (rank, suit) tuple，用於排序時的比較
        """
        return (self.rank, self.suit)


class Deck:
    """
    撲克牌組類別。代表遊戲中的牌組。
    
    包含 52 張標準撲克牌，支援洗牌和發牌功能。
    """
    
    def __init__(self) -> None:
        """
        初始化牌組。
        
        建立所有 52 張牌（4 種花色，每種花色 13 張牌）
        """
        self.cards: List[Card] = []
        self._create_cards()
    
    def _create_cards(self) -> None:
        """
        建立牌組。
        
        此方法提取牌組初始化邏輯，便於重用和測試。
        產生所有 52 張牌：每種花色 (0-3) 對應 13 種牌面 (3-15)
        """
        # 遍歷所有花色 (0=♣, 1=♦, 2=♥, 3=♠)
        for suit in range(4):
            # 遍歷當前花色的所有牌面 (3-15)
            for rank in range(3, 16):
                self.cards.append(Card(rank, suit))
    
    def shuffle(self) -> None:
        """
        洗牌。
        
        隨機重新排列牌組中的所有牌。
        """
        random.shuffle(self.cards)
    
    def deal(self, num_cards: int) -> List[Card]:
        """
        發牌。
        
        從牌組的前面發出指定數量的牌。
        
        參數：
            num_cards: 要發出的牌數量
        
        傳回：
            發出的牌的列表。如果牌不足，則傳回剩餘所有牌
        """
        # 防止發超過牌組中的牌數
        cards_to_deal = min(num_cards, len(self.cards))
        # 取出前面 num_cards 張牌
        dealt_cards = self.cards[:cards_to_deal]
        # 更新牌組，移除已發出的牌
        self.cards = self.cards[cards_to_deal:]
        return dealt_cards


class Hand:
    """
    手牌類別。代表玩家目前持有的牌。
    
    這個類別用來管理玩家的手牌，提供排序、尋找和移除特定牌的功能。
    """
    
    def __init__(self, cards: Optional[List[Card]] = None) -> None:
        """
        初始化手牌。
        
        參數：
            cards: Card 物件的列表。如果為 None，則初始化為空列表
        """
        # 如果沒有提供牌，則初始化為空列表
        self.cards: List[Card] = list(cards) if cards else []
    
    def sort(self, reverse: bool = True) -> None:
        """
        排序手牌。
        
        根據牌的大小進行排序。
        排序規則：先按照 rank 排，同一 rank 再按 suit 排。
        
        參數：
            reverse: 是否進行反向排序（由大到小）。預設為 True
        """
        # 使用 to_sort_key() 方法進行排序
        self.cards.sort(key=lambda card: card.to_sort_key(), reverse=reverse)
    
    def find_club_three(self) -> Optional[Card]:
        """
        尋找梅花三 (♣3)。
        
        在手牌中尋找梅花三 (rank=3, suit=0)。
        梅花三是大二遊戲中的特殊牌，通常是開局牌。
        
        傳回：
            如果找到梅花三則傳回該 Card 物件，否則傳回 None
        """
        # 遍歷所有牌
        for card in self.cards:
            # 梅花三的特徵：rank=3 且 suit=0 (♣)
            if card.rank == 3 and card.suit == 0:
                return card
        # 如果沒找到則傳回 None
        return None
    
    def remove(self, card: Card) -> bool:
        """
        從手牌中移除指定的牌。
        
        參數：
            card: 要移除的 Card 物件
        
        傳回：
            移除成功則傳回 True，牌不存在於手牌中則傳回 False
        """
        # 檢查牌是否在手牌中
        if card in self.cards:
            # 移除該牌
            self.cards.remove(card)
            return True
        # 如果牌不在手牌中，傳回 False
        return False
    
    def __len__(self) -> int:
        """
        傳回手牌中的牌數。
        
        傳回：
            手牌數量
        """
        return len(self.cards)
    
    def __iter__(self):
        """
        讓 Hand 物件可以被迭代。
        
        允許使用 for 迴圈遍歷手牌中的所有牌。
        
        傳回：
            手牌列表的迭代器
        """
        return iter(self.cards)
    
    def __repr__(self) -> str:
        """
        傳回手牌的字串表示。
        
        傳回：
            格式為 "Hand([♠A, ♥K, ...])" 的字串
        """
        card_strs = [str(card) for card in self.cards]
        return f"Hand({card_strs})"


class Player:
    """
    玩家類別。代表遊戲中的一個參與者。
    
    玩家可以是人類玩家或人工智慧玩家，擁有手牌和得分。
    """
    
    def __init__(self, name: str, is_ai: bool = False) -> None:
        """
        初始化玩家。
        
        參數：
            name: 玩家名稱
            is_ai: 是否為人工智慧玩家。預設為 False（人類玩家）
        """
        self.name: str = name
        self.is_ai: bool = is_ai
        self.hand: Hand = Hand()  # 初始化為空的 Hand 物件
        self.score: int = 0  # 初始得分為 0
    
    def take_cards(self, cards: List[Card]) -> None:
        """
        玩家取得牌。
        
        將一批牌添加到玩家的手牌中。
        
        參數：
            cards: Card 物件的列表，要添加到手牌中
        """
        # 將牌添加到手牌的列表中
        self.hand.cards.extend(cards)
    
    def play_cards(self, cards: List[Card]) -> Optional[List[Card]]:
        """
        玩家出牌。
        
        玩家嘗試出牌。此方法會檢查這些牌是否都在玩家的手牌中。
        
        參數：
            cards: 玩家要出的牌的列表
        
        傳回：
            如果所有牌都在手牌中，則移除這些牌並傳回它們。
            否則傳回 None。
        """
        # 檢查所有要出的牌是否都在手牌中
        for card in cards:
            if card not in self.hand.cards:
                return None
        
        # 所有牌都在手牌中，移除它們
        for card in cards:
            self.hand.remove(card)
        
        # 傳回出聲的牌
        return cards
    
    def play(self, card: Card) -> Optional[Card]:
        """
        玩家出單張牌。
        
        參數：
            card: 要出的牌 (Card 物件)
        
        傳回：
            如果該牌在手牌中，則傳回該牌並移除，否則傳回 None
        """
        # 檢查牌是否在手牌中
        if self.hand.remove(card):
            return card
        return None
    
    def __repr__(self) -> str:
        """
        傳回玩家的字串表示。
        
        傳回：
            格式為 "Player(name='...', is_ai=..., score=...)" 的字串
        """
        return f"Player(name='{self.name}', is_ai={self.is_ai}, score={self.score})"
