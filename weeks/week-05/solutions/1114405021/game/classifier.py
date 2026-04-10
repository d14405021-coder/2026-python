"""
Big Two 遊戲 - 牌型分類模組
實作 HandClassifier 類別，用於分類、比較和驗證遊戲中的牌型

此模組包含遊戲中所有的牌型分類邏輯，包括：
- 牌型識別（單張、對子、三條、順子、同花、葫蘆、四條、同花順）
- 牌的大小比較
- 出牌合法性檢查
"""

from enum import Enum
from typing import Optional, Tuple, List
from .models import Card


# ==================== CardType 列舉定義 ====================

class CardType(Enum):
    """
    牌型列舉。定義大二遊戲中所有可能的牌型。
    
    牌型值從 1 到 8，數字越大牌型越強。
    
    牌型說明：
    - SINGLE (1): 單張牌
    - PAIR (2): 對子（兩張相同牌面）
    - TRIPLE (3): 三條（三張相同牌面）
    - STRAIGHT (4): 順子（五張連續牌）
    - FLUSH (5): 同花（五張相同花色）
    - FULL_HOUSE (6): 葫蘆（三條+對子）
    - FOUR_OF_A_KIND (7): 四條（四張相同牌面）
    - STRAIGHT_FLUSH (8): 同花順（五張連續且同花）
    """
    SINGLE = 1
    PAIR = 2
    TRIPLE = 3
    STRAIGHT = 4
    FLUSH = 5
    FULL_HOUSE = 6
    FOUR_OF_A_KIND = 7
    STRAIGHT_FLUSH = 8


# ==================== HandClassifier 類別 ====================

class HandClassifier:
    """
    牌型分類器。
    
    提供靜態方法進行牌型分類、大小比較和合法性檢查。
    """
    
    # ==================== 公開方法 ====================
    
    @staticmethod
    def classify(cards: List[Card]) -> Optional[Tuple[CardType, int, int]]:
        """
        對牌進行分類。
        
        根據牌的數量和組合，將牌分類為不同的牌型。
        此方法會嘗試所有可能的分類，並按優先級傳回最高的牌型。
        
        參數：
            cards: Card 物件的列表
        
        傳回：
            如果牌能被分類，傳回 (牌型, 代表牌面值, 代表花色值) 的 tuple
            如果無法分類（例如列表為空或牌數錯誤），傳回 None
        
        範例：
            >>> classify([Card(14, 3)])
            (CardType.SINGLE, 14, 3)
            
            >>> classify([Card(14, 3), Card(14, 2)])
            (CardType.PAIR, 14, 3)
        """
        # 根據牌的數量進行分類
        if len(cards) == 1:
            return HandClassifier._classify_single(cards)
        elif len(cards) == 2:
            return HandClassifier._classify_pair(cards)
        elif len(cards) == 3:
            return HandClassifier._classify_triple(cards)
        elif len(cards) == 5:
            return HandClassifier._classify_five(cards)
        else:
            # 其他數量的牌無法分類
            return None
    
    @staticmethod
    def compare(hand1: Optional[List[Card]], hand2: Optional[List[Card]]) -> int:
        """
        比較兩手牌的大小。
        
        先分類兩手牌，然後按牌型、牌面、花色的順序比較。
        
        參數：
            hand1: 第一手牌（Card 物件的列表）
            hand2: 第二手牌（Card 物件的列表）
        
        傳回：
            1: hand1 > hand2
            -1: hand1 < hand2
            0: hand1 == hand2
        """
        # 分類兩手牌
        class1 = HandClassifier.classify(hand1)
        class2 = HandClassifier.classify(hand2)
        
        # 如果任一方無法分類，則無法比較
        if class1 is None or class2 is None:
            return 0
        
        # 比較牌型
        type1, rank1, suit1 = class1
        type2, rank2, suit2 = class2
        
        # 先比較牌型值（枚舉的數字值）
        if type1.value > type2.value:
            return 1
        elif type1.value < type2.value:
            return -1
        
        # 牌型相同，比較牌面值
        if rank1 > rank2:
            return 1
        elif rank1 < rank2:
            return -1
        
        # 牌面相同，比較花色值
        if suit1 > suit2:
            return 1
        elif suit1 < suit2:
            return -1
        
        # 完全相同
        return 0
    
    @staticmethod
    def can_play(last_play: Optional[List[Card]], cards: List[Card]) -> bool:
        """
        檢查是否能出牌。
        
        規則：
        1. 如果 last_play 為 None（第一手），必須出梅花三 (♣3)
        2. 否則，當前牌必須是相同牌型且大於上一手牌
        
        參數：
            last_play: 上一手出的牌，或 None（如果現在是第一手）
            cards: 當前要出的牌
        
        傳回：
            如果能出則傳回 True，否則傳回 False
        """
        # 如果沒有上一手（第一手）
        if last_play is None:
            # 必須是梅花三 (♣3)
            if len(cards) == 1:
                card = cards[0]
                return card.rank == 3 and card.suit == 0
            return False
        
        # 分類當前牌
        current_class = HandClassifier.classify(cards)
        last_class = HandClassifier.classify(last_play)
        
        # 無法分類則無法出牌
        if current_class is None or last_class is None:
            return False
        
        # 牌型必須相同
        if current_class[0] != last_class[0]:
            return False
        
        # 當前牌必須大於上一手牌
        return HandClassifier.compare(cards, last_play) > 0
    
    # ==================== 私有助手方法 ====================
    
    @staticmethod
    def _classify_single(cards: List[Card]) -> Tuple[CardType, int, int]:
        """
        分類單張牌。
        
        參數：
            cards: 只包含一張牌的列表
        
        傳回：
            (SINGLE, 牌面值, 花色值) 的 tuple
        """
        card = cards[0]
        return (CardType.SINGLE, card.rank, card.suit)
    
    @staticmethod
    def _classify_pair(cards: List[Card]) -> Optional[Tuple[CardType, int, int]]:
        """
        分類對子（兩張相同牌面的牌）。
        
        參數：
            cards: 兩張牌的列表
        
        傳回：
            如果兩張牌牌面相同，傳回 (PAIR, 牌面值, 花色值)
            否則傳回 None
        """
        # 檢查兩張牌是否是相同牌面
        if cards[0].rank == cards[1].rank:
            # 取較大的花色值作為對子的花色代表
            suit = max(cards[0].suit, cards[1].suit)
            return (CardType.PAIR, cards[0].rank, suit)
        return None
    
    @staticmethod
    def _classify_triple(cards: List[Card]) -> Optional[Tuple[CardType, int, int]]:
        """
        分類三條（三張相同牌面的牌）。
        
        參數：
            cards: 三張牌的列表
        
        傳回：
            如果三張牌牌面相同，傳回 (TRIPLE, 牌面值, 花色值)
            否則傳回 None
        """
        # 檢查三張牌是否都是相同牌面
        if cards[0].rank == cards[1].rank == cards[2].rank:
            # 取最大的花色值作為三條的花色代表
            suit = max(cards[0].suit, cards[1].suit, cards[2].suit)
            return (CardType.TRIPLE, cards[0].rank, suit)
        return None
    
    @staticmethod
    def _classify_five(cards: List[Card]) -> Optional[Tuple[CardType, int, int]]:
        """
        分類五張牌。
        
        檢查五張牌的各種組合，按優先級返回牌型：
        1. 同花順（STRAIGHT_FLUSH）- 最高
        2. 四條（FOUR_OF_A_KIND）
        3. 葫蘆（FULL_HOUSE）
        4. 同花（FLUSH）
        5. 順子（STRAIGHT）
        
        參數：
            cards: 五張牌的列表
        
        傳回：
            相應牌型的 (牌型, 牌面值, 花色值) tuple，或 None
        """
        # 優先檢查同花順
        sf = HandClassifier._check_straight_flush(cards)
        if sf:
            return sf
        
        # 檢查四條
        foak = HandClassifier._check_four_of_a_kind(cards)
        if foak:
            return foak
        
        # 檢查葫蘆
        fh = HandClassifier._check_full_house(cards)
        if fh:
            return fh
        
        # 檢查同花
        f = HandClassifier._check_flush(cards)
        if f:
            return f
        
        # 檢查順子
        s = HandClassifier._check_straight(cards)
        if s:
            return s
        
        # 無法分類為任何五張牌型
        return None
    
    # ==================== 五張牌型檢查方法 ====================
    
    @staticmethod
    def _is_straight(ranks: List[int]) -> bool:
        """
        檢查是否為順子。
        
        順子需要五張牌的牌面值連續。
        特殊情況：A-2-3-4-5 視為最小順子（其中 A=14, 2=15）
        
        參數：
            ranks: 五張牌的牌面值列表
        
        傳回：
            如果是順子則傳回 True，否則傳回 False
        """
        # 將牌面值排序
        sorted_ranks = sorted(ranks)
        
        # 特殊情況：A-2-3-4-5 順子
        # 在大二中：A=14, 2=15，所以排序後為 [3, 4, 5, 14, 15]
        if sorted_ranks == [3, 4, 5, 14, 15]:
            return True
        
        # 一般情況：相鄰牌面的差值都應該是 1
        return all(sorted_ranks[i+1] - sorted_ranks[i] == 1 for i in range(4))
    
    @staticmethod
    def _is_flush(suits: List[int]) -> bool:
        """
        檢查是否為同花。
        
        同花需要五張牌都是相同的花色。
        
        參數：
            suits: 五張牌的花色值列表
        
        傳回：
            如果是同花則傳回 True，否則傳回 False
        """
        # 檢查所有花色是否都相同
        return len(set(suits)) == 1
    
    @staticmethod
    def _check_straight(cards: List[Card]) -> Optional[Tuple[CardType, int, int]]:
        """
        檢查是否為順子。
        
        參數：
            cards: 五張牌的列表
        
        傳回：
            如果是順子，傳回 (STRAIGHT, 最大牌面值, 0)
            否則傳回 None
        """
        ranks = [card.rank for card in cards]
        
        if HandClassifier._is_straight(ranks):
            # 特殊情況：A-2-3-4-5，最大值是 5
            if sorted(ranks) == [3, 4, 5, 14, 15]:
                return (CardType.STRAIGHT, 5, 0)
            # 一般情況：取最大的牌面值
            return (CardType.STRAIGHT, max(ranks), 0)
        
        return None
    
    @staticmethod
    def _check_flush(cards: List[Card]) -> Optional[Tuple[CardType, int, int]]:
        """
        檢查是否為同花。
        
        參數：
            cards: 五張牌的列表
        
        傳回：
            如果是同花，傳回 (FLUSH, 最大牌面值, 花色值)
            否則傳回 None
        """
        suits = [card.suit for card in cards]
        
        if HandClassifier._is_flush(suits):
            # 所有牌是同一花色
            suit = suits[0]
            max_rank = max(card.rank for card in cards)
            return (CardType.FLUSH, max_rank, suit)
        
        return None
    
    @staticmethod
    def _check_full_house(cards: List[Card]) -> Optional[Tuple[CardType, int, int]]:
        """
        檢查是否為葫蘆（三條+對子）。
        
        參數：
            cards: 五張牌的列表
        
        傳回：
            如果是葫蘆，傳回 (FULL_HOUSE, 三條的牌面值, 最大花色值)
            否則傳回 None
        """
        # 統計各牌面出現的次數
        rank_counts = HandClassifier._count_ranks(cards)
        
        # 檢查是否有一個牌面出現 3 次，另一個出現 2 次
        counts = sorted(rank_counts.values())
        if counts == [2, 3]:
            # 找出三條的牌面值
            triple_rank = None
            for rank, count in rank_counts.items():
                if count == 3:
                    triple_rank = rank
                    break
            
            # 取最大的花色值
            max_suit = max(card.suit for card in cards)
            return (CardType.FULL_HOUSE, triple_rank, max_suit)
        
        return None
    
    @staticmethod
    def _check_four_of_a_kind(cards: List[Card]) -> Optional[Tuple[CardType, int, int]]:
        """
        檢查是否為四條（四張相同牌面）。
        
        參數：
            cards: 五張牌的列表
        
        傳回：
            如果是四條，傳回 (FOUR_OF_A_KIND, 四條的牌面值, 最大花色值)
            否則傳回 None
        """
        # 統計各牌面出現的次數
        rank_counts = HandClassifier._count_ranks(cards)
        
        # 檢查是否有牌面出現 4 次
        for rank, count in rank_counts.items():
            if count == 4:
                # 找出四條的最大花色值
                max_suit = max(card.suit for card in cards if card.rank == rank)
                return (CardType.FOUR_OF_A_KIND, rank, max_suit)
        
        return None
    
    @staticmethod
    def _check_straight_flush(cards: List[Card]) -> Optional[Tuple[CardType, int, int]]:
        """
        檢查是否為同花順（順子+同花）。
        
        參數：
            cards: 五張牌的列表
        
        傳回：
            如果是同花順，傳回 (STRAIGHT_FLUSH, 最大牌面值, 花色值)
            否則傳回 None
        """
        ranks = [card.rank for card in cards]
        suits = [card.suit for card in cards]
        
        # 必須既是順子又是同花
        if HandClassifier._is_straight(ranks) and HandClassifier._is_flush(suits):
            suit = suits[0]
            
            # 特殊情況：A-2-3-4-5 同花順
            if sorted(ranks) == [3, 4, 5, 14, 15]:
                return (CardType.STRAIGHT_FLUSH, 5, suit)
            
            # 一般情況
            return (CardType.STRAIGHT_FLUSH, max(ranks), suit)
        
        return None
    
    # ==================== 輔助方法 ====================
    
    @staticmethod
    def _count_ranks(cards: List[Card]) -> dict:
        """
        統計牌中各牌面出現的次數。
        
        參數：
            cards: Card 物件的列表
        
        傳回：
            {牌面值: 出現次數} 的字典
        """
        rank_counts = {}
        for card in cards:
            rank_counts[card.rank] = rank_counts.get(card.rank, 0) + 1
        return rank_counts
