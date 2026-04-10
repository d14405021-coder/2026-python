"""
Big Two 遊戲 - 牌型搜尋模組
提供 HandFinder 類別，用於搜尋手牌中的各種牌型組合

此模組包含靜態方法，用於尋找手牌中所有可能的牌型，
包括基本牌型（單張、對子、三條）和複雜牌型（順子、同花等），
以及根據遊戲規則找出所有合法出牌。
"""

from typing import List, Optional
from itertools import combinations
from .models import Card
from .classifier import CardType, HandClassifier


class HandFinder:
    """
    牌型搜尋器。
    
    提供靜態方法從手牌中搜尋所有可能的牌型組合。
    包括基本牌型（單張、對子、三條）、五張牌型（順子、同花、葫蘆、四條、同花順）
    以及根據遊戲規則的合法出牌。
    
    所有方法都是靜態方法，無需實例化。
    """
    
    @staticmethod
    def find_singles(cards: List[Card]) -> List[List[Card]]:
        """
        搜尋所有單張牌。
        
        此方法簡單地將每張牌作為一個單張牌型傳回。
        
        參數：
            cards: 手牌列表
        
        傳回：
            所有單張牌的列表，每個元素是包含一張牌的列表
            
        例如：
            cards = [Card(3, 0), Card(14, 0), Card(13, 1)]
            find_singles(cards) 傳回 [[Card(3, 0)], [Card(14, 0)], [Card(13, 1)]]
        """
        # 每張牌都可以單獨出牌
        return [[card] for card in cards]
    
    @staticmethod
    def find_pairs(cards: List[Card]) -> List[List[Card]]:
        """
        搜尋所有對子。
        
        對子由兩張相同牌面的牌組成。
        此方法檢查所有兩張牌的組合，找出牌面相同的對子。
        
        參數：
            cards: 手牌列表
        
        傳回：
            所有對子的列表，每個元素是包含兩張牌的列表
            
        例如：
            cards = [Card(5, 0), Card(5, 1), Card(3, 0)]
            find_pairs(cards) 傳回 [[Card(5, 0), Card(5, 1)]]
        """
        pairs = []
        
        # 統計各牌面出現的次數
        rank_cards = {}
        for card in cards:
            if card.rank not in rank_cards:
                rank_cards[card.rank] = []
            rank_cards[card.rank].append(card)
        
        # 對於有 2 張或以上的牌面，生成所有可能的對子
        for rank, rank_card_list in rank_cards.items():
            if len(rank_card_list) >= 2:
                # 從該牌面的所有牌中取 2 張，組成對子
                for pair in combinations(rank_card_list, 2):
                    pairs.append(list(pair))
        
        return pairs
    
    @staticmethod
    def find_triples(cards: List[Card]) -> List[List[Card]]:
        """
        搜尋所有三條。
        
        三條由三張相同牌面的牌組成。
        此方法檢查所有三張牌的組合，找出牌面相同的三條。
        
        參數：
            cards: 手牌列表
        
        傳回：
            所有三條的列表，每個元素是包含三張牌的列表
            
        例如：
            cards = [Card(5, 0), Card(5, 1), Card(5, 2), Card(3, 0)]
            find_triples(cards) 傳回 [[Card(5, 0), Card(5, 1), Card(5, 2)]]
        """
        triples = []
        
        # 統計各牌面出現的次數
        rank_cards = {}
        for card in cards:
            if card.rank not in rank_cards:
                rank_cards[card.rank] = []
            rank_cards[card.rank].append(card)
        
        # 對於有 3 張或以上的牌面，生成所有可能的三條
        for rank, rank_card_list in rank_cards.items():
            if len(rank_card_list) >= 3:
                # 從該牌面的所有牌中取 3 張，組成三條
                for triple in combinations(rank_card_list, 3):
                    triples.append(list(triple))
        
        return triples
    
    @staticmethod
    def find_straights(cards: List[Card]) -> List[List[Card]]:
        """
        搜尋所有順子（五張連續牌）。
        
        此方法從手牌中找出所有可能的五張連續牌組合。
        
        參數：
            cards: 手牌列表
        
        傳回：
            所有順子的列表，每個元素是包含五張牌的列表
            
        例如：
            cards = [Card(3, 0), Card(4, 1), Card(5, 2), Card(6, 3), Card(7, 0), Card(14, 3)]
            find_straights(cards) 會找到包含 [Card(3, 0), Card(4, 1), Card(5, 2), Card(6, 3), Card(7, 0)]
        """
        straights = []
        
        # 檢查所有五張牌的組合
        for five_cards in combinations(cards, 5):
            # 分類此組合
            result = HandClassifier.classify(list(five_cards))
            # 如果分類為順子，加入結果
            if result and result[0] == CardType.STRAIGHT:
                straights.append(list(five_cards))
        
        return straights
    
    @staticmethod
    def find_flushes(cards: List[Card]) -> List[List[Card]]:
        """
        搜尋所有同花（五張相同花色的牌）。
        
        此方法從手牌中找出所有可能的五張同花色牌組合。
        
        參數：
            cards: 手牌列表
        
        傳回：
            所有同花的列表，每個元素是包含五張牌的列表
            
        例如：
            cards = [Card(3, 0), Card(5, 0), Card(7, 0), Card(9, 0), Card(11, 0), Card(14, 3)]
            find_flushes(cards) 會找到包含五張梅花（花色=0）的組合
        """
        flushes = []
        
        # 檢查所有五張牌的組合
        for five_cards in combinations(cards, 5):
            # 分類此組合
            result = HandClassifier.classify(list(five_cards))
            # 如果分類為同花，加入結果
            if result and result[0] == CardType.FLUSH:
                flushes.append(list(five_cards))
        
        return flushes
    
    @staticmethod
    def find_full_houses(cards: List[Card]) -> List[List[Card]]:
        """
        搜尋所有葫蘆（三條+對子）。
        
        此方法從手牌中找出所有可能的五張葫蘆組合。
        
        參數：
            cards: 手牌列表
        
        傳回：
            所有葫蘆的列表，每個元素是包含五張牌的列表
            
        例如：
            cards = [Card(5, 0), Card(5, 1), Card(5, 2), Card(3, 0), Card(3, 1), Card(14, 3)]
            find_full_houses(cards) 會找到三 5 加對 3 的葫蘆組合
        """
        full_houses = []
        
        # 檢查所有五張牌的組合
        for five_cards in combinations(cards, 5):
            # 分類此組合
            result = HandClassifier.classify(list(five_cards))
            # 如果分類為葫蘆，加入結果
            if result and result[0] == CardType.FULL_HOUSE:
                full_houses.append(list(five_cards))
        
        return full_houses
    
    @staticmethod
    def find_four_of_a_kinds(cards: List[Card]) -> List[List[Card]]:
        """
        搜尋所有四條（四張相同牌面）。
        
        此方法從手牌中找出所有可能的五張四條組合。
        
        參數：
            cards: 手牌列表
        
        傳回：
            所有四條的列表，每個元素是包含五張牌的列表
            
        例如：
            cards = [Card(5, 0), Card(5, 1), Card(5, 2), Card(5, 3), Card(3, 0), Card(14, 3)]
            find_four_of_a_kinds(cards) 會找到包含四 5 的組合
        """
        four_of_a_kinds = []
        
        # 檢查所有五張牌的組合
        for five_cards in combinations(cards, 5):
            # 分類此組合
            result = HandClassifier.classify(list(five_cards))
            # 如果分類為四條，加入結果
            if result and result[0] == CardType.FOUR_OF_A_KIND:
                four_of_a_kinds.append(list(five_cards))
        
        return four_of_a_kinds
    
    @staticmethod
    def find_straight_flushes(cards: List[Card]) -> List[List[Card]]:
        """
        搜尋所有同花順（五張連續且同花的牌）。
        
        此方法從手牌中找出所有可能的五張同花順組合。
        
        參數：
            cards: 手牌列表
        
        傳回：
            所有同花順的列表，每個元素是包含五張牌的列表
            
        例如：
            cards = [Card(3, 0), Card(4, 0), Card(5, 0), Card(6, 0), Card(7, 0), Card(14, 3)]
            find_straight_flushes(cards) 會找到梅花 3-4-5-6-7 的同花順
        """
        straight_flushes = []
        
        # 檢查所有五張牌的組合
        for five_cards in combinations(cards, 5):
            # 分類此組合
            result = HandClassifier.classify(list(five_cards))
            # 如果分類為同花順，加入結果
            if result and result[0] == CardType.STRAIGHT_FLUSH:
                straight_flushes.append(list(five_cards))
        
        return straight_flushes
    
    @staticmethod
    def find_playable(last_play: Optional[List[Card]], cards: List[Card]) -> List[List[Card]]:
        """
        搜尋所有可以合法出牌的組合。
        
        合法出牌的規則：
        - 如果沒有上一手（last_play 為 None），只能出梅花三 (♣3)
        - 否則，必須是相同牌型且大於上一手的牌
        
        此方法先根據上一手找出可以出的牌型，然後搜尋所有該牌型中大於上一手的牌。
        
        參數：
            last_play: 上一手出的牌，或 None（如果是第一手）
            cards: 手牌列表
        
        傳回：
            所有可以出的牌組合的列表
            
        例如：
            # 第一手出牌
            last_play = None
            cards = [Card(3, 0), Card(14, 0), Card(13, 1)]
            find_playable(last_play, cards) 傳回 [[Card(3, 0)]]  # 只能出梅花三
            
            # 後續出牌
            last_play = [Card(5, 0)]  # 上一手出的單 5
            cards = [Card(6, 0), Card(5, 1), Card(5, 2)]
            find_playable(last_play, cards) 傳回 [[Card(6, 0)]]  # 只能出單 6
        """
        playable = []
        
        # 如果沒有上一手（第一手）
        if last_play is None:
            # 只能出梅花三
            for card in cards:
                if card.rank == 3 and card.suit == 0:
                    playable.append([card])
            return playable
        
        # 分類上一手的牌
        last_class = HandClassifier.classify(last_play)
        if last_class is None:
            return []
        
        last_type = last_class[0]
        
        # 根據牌型搜尋對應的組合
        if last_type == CardType.SINGLE:
            # 搜尋所有單張
            candidates = HandFinder.find_singles(cards)
        elif last_type == CardType.PAIR:
            # 搜尋所有對子
            candidates = HandFinder.find_pairs(cards)
        elif last_type == CardType.TRIPLE:
            # 搜尋所有三條
            candidates = HandFinder.find_triples(cards)
        elif last_type == CardType.STRAIGHT:
            # 搜尋所有順子
            candidates = HandFinder.find_straights(cards)
        elif last_type == CardType.FLUSH:
            # 搜尋所有同花
            candidates = HandFinder.find_flushes(cards)
        elif last_type == CardType.FULL_HOUSE:
            # 搜尋所有葫蘆
            candidates = HandFinder.find_full_houses(cards)
        elif last_type == CardType.FOUR_OF_A_KIND:
            # 搜尋所有四條
            candidates = HandFinder.find_four_of_a_kinds(cards)
        elif last_type == CardType.STRAIGHT_FLUSH:
            # 搜尋所有同花順
            candidates = HandFinder.find_straight_flushes(cards)
        else:
            return []
        
        # 篩選出大於上一手的牌
        for candidate in candidates:
            if HandClassifier.compare(candidate, last_play) > 0:
                playable.append(candidate)
        
        return playable
