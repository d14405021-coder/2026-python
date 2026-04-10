"""
Big Two 遊戲 - AI 策略模組
使用貪心演算法選擇最佳出牌

此模組包含 AIStrategy 類別，提供靜態方法用於：
1. 評分出牌：根據牌型、牌面值、手牌剩餘數等因素計算分數
2. 選擇最佳出牌：從所有合法出牌中選擇分數最高的

AIStrategy 類別完全無狀態，所有方法都是靜態方法，可直接調用。
"""

from typing import List, Optional
from .models import Card
from .classifier import CardType, HandClassifier
from .finder import HandFinder


class AIStrategy:
    """
    人工智能策略類。
    
    使用貪心演算法選擇最佳出牌。
    評分基於牌型、牌面值、手牌剩餘數和花色等因素。
    
    評分系統：
    1. 牌型分數：不同牌型有不同基礎分數
    2. 牌面分數：更高的牌面獲得更高分數
    3. 手牌獎勵：鼓勵快速清空手牌
    4. 花色加分：梅花牌獲得額外加分
    """
    
    # ==================== 評分常數 ====================
    
    # 牌型分數（用於計算基礎分數）
    TYPE_SCORES = {
        CardType.SINGLE: 1,
        CardType.PAIR: 2,
        CardType.TRIPLE: 3,
        CardType.STRAIGHT: 4,
        CardType.FLUSH: 5,
        CardType.FULL_HOUSE: 6,
        CardType.FOUR_OF_A_KIND: 7,
        CardType.STRAIGHT_FLUSH: 8,
    }
    
    # 手牌剩餘獎勵
    EMPTY_HAND_BONUS = 10000      # 剩 1 張時的獎勵
    NEAR_EMPTY_BONUS = 500         # 剩 2 張時的獎勵
    
    # 花色獎勵
    SPADE_BONUS = 5               # 梅花牌每張的加分
    
    # ==================== 評分方法 ====================
    
    @staticmethod
    def score_play(play: List[Card], hand_remaining: int) -> float:
        """
        計算一手牌的分數。
        
        評分公式包含四個維度：
        1. 牌型分數 - 牌型越高分數越高
        2. 最大牌面 × 10 - 鼓勵出大牌
        3. 手牌剩餘獎勵 - 鼓勵快速清空
        4. 梅花加分 × 5 - 額外獎勵梅花
        
        參數：
            play: 要評分的出牌（List[Card]）
            hand_remaining: 出牌後手中剩餘的牌數（int）
        
        傳回：
            綜合分值（越高越好）
            
        例如：
            play = [Card(14, 0)]  # 單梅花 A
            hand_remaining = 2  # 出完后剩 2 張
            # score = 1 + 14×10 + 500 + 5 = 646
        """
        if not play:
            return 0.0
        
        # 分類此出牌
        classification = HandClassifier.classify(play)
        if not classification:
            return 0.0
        
        card_type = classification[0]
        
        # 1. 牌型基分（直接使用，不乘以倍數）
        # 牌型分數從 1-8，高牌型獲得高分
        type_base = float(AIStrategy.TYPE_SCORES.get(card_type, 0))
        score = type_base
        
        # 2. 牌面加分（乘以 10）
        # 出牌中最大的牌面值，乘以 10 用於排序同類型牌
        max_rank = max(card.rank for card in play)
        score += max_rank * 10
        
        # 3. 手牌剩餘獎勵
        # hand_remaining 已由調用方計算並傳入
        if hand_remaining == 1:
            # 剩最後一張：獲得大獎勵，激勵 AI 快速清空
            score += AIStrategy.EMPTY_HAND_BONUS
        elif hand_remaining == 2:
            # 剩 2 張：獲得中等獎勵
            score += AIStrategy.NEAR_EMPTY_BONUS
        
        # 4. 花色加分
        # 梅花牌（suit=0）每張獲得 5 分的額外獎勵
        spade_count = sum(1 for card in play if card.suit == 0)
        score += spade_count * AIStrategy.SPADE_BONUS
        
        return score
    
    # ==================== 選擇方法 ====================
    
    @staticmethod
    def select_best(valid_plays: List[List[Card]], 
                   hand: List[Card],
                   last_play: Optional[List[Card]] = None) -> Optional[List[Card]]:
        """
        從所有合法出牌中選擇評分最高的一手牌。
        
        此方法實現貪心策略：計算每手合法出牌的分數，然後選擇分數最高的。
        
        參數：
            valid_plays: 所有合法出牌的列表（從 HandFinder.find_playable() 得到）
            hand: 當前手牌（用於計算剩餘手牌數）
            last_play: 上一家玩家出的牌（可選，用於驗證第一手出梅花三）
        
        傳回：
            評分最高的出牌列表，或 None（如果沒有合法出牌）
            
        例如：
            valid_plays = [
                [Card(3, 0)],                           # 梅花 3
                [Card(5, 0), Card(5, 1)],              # 對 5
                [Card(14, 0), Card(14, 1)]             # 對 A
            ]
            hand = [Card(3, 0), Card(5, 0), Card(5, 1), Card(14, 0), Card(14, 1)]
            
            best = select_best(valid_plays, hand, last_play=None)
            # 傳回對 A（分數最高）
        """
        if not valid_plays:
            return None
        
        # 計算每手出牌的分數
        best_play = None
        best_score = -1.0
        
        for play in valid_plays:
            # 計算出牌後剩餘的手牌數
            hand_remaining = len(hand) - len(play)
            score = AIStrategy.score_play(play, hand_remaining)
            if score > best_score:
                best_score = score
                best_play = play
        
        return best_play
    
    # ==================== 完整決策方法 ====================
    
    @staticmethod
    def get_best_move(hand: List[Card], 
                     last_play: Optional[List[Card]]) -> Optional[List[Card]]:
        """
        根據當前手牌和上一手牌，決定最佳出牌。
        
        此方法整合 HandFinder 和評分邏輯，實現完整的 AI 決策：
        1. 使用 HandFinder.find_playable() 尋找所有合法出牌
        2. 如果沒有合法出牌，傳回 None（玩家需要跳過）
        3. 使用 select_best() 選擇分數最高的出牌
        
        參數：
            hand: 玩家當前的手牌
            last_play: 上一家玩家出的牌，或 None（如果是第一手）
        
        傳回：
            AI 決定要出的牌，或 None（如果無合法出牌要跳過）
            
        例子：
        玩家手牌 = [♠3, ♠5, ♠5, ♠14]，上一手出牌 = None（第一手）
        find_playable() 會傳回 [[♠3]]（第一手只能出梅花 3）
        select_best() 會選擇 [♠3]
        傳回值 = [♠3]
        
        另一例：
        玩家手牌 = [♠13, ♠13, ♠5]，上一手 = [♠6]（出了單 6）
        find_playable() 會傳回 [[♠13], [♠13, ♠13]]（單 13 或對 13）
        select_best() 會計算分數並選擇分數最高的
        傳回值 = [♠13, ♠13]（對子評分高於單張）
        """
        # 尋找所有合法出牌
        playable = HandFinder.find_playable(last_play, hand)
        
        if not playable:
            # 沒有合法出牌，玩家必須跳過
            return None
        
        # 選擇最佳出牌
        best_move = AIStrategy.select_best(playable, hand, last_play)
        
        return best_move
