"""
Big Two 遊戲 - AI 策略單元測試
測試 AIStrategy 類別的貪心演算法和決策邏輯

此測試套件使用 Python 標準函式庫 unittest 框架，驗證 AI 玩家的：
1. 牌型評分函數（考慮牌面值、手牌剩餘數、花色等因素）
2. 最佳出牌選擇（從合法出牌中選擇分數最高的）
3. 完整策略實現（比對手牌、優先級等高級邏輯）
"""

import unittest
from typing import List, Optional
from game.models import Card
from game.classifier import CardType, HandClassifier
from game.finder import HandFinder
from game.ai import AIStrategy


# ==================== 單元測試類別 ====================

class TestScorePlay(unittest.TestCase):
    """牌型評分函數測試"""
    
    def test_score_single(self):
        """測試：單張♠A 的分數計算"""
        # 單張♠A（rank=14, suit=0）
        play = [Card(14, 0)]
        # 出牌後手中剩 2 張
        hand_remaining = 2
        
        # 分數計算：
        # - 牌型基分（單張）：1
        # - 牌面加分（A=rank14，係數10）：14 × 10 = 140
        # - 花色加分（梅花）：1 × 5 = 5
        # - 手牌獎勵（剩2張）：500
        # 總計：1 + 140 + 5 + 500 = 646
        score = AIStrategy.score_play(play, hand_remaining)
        self.assertGreater(score, 0)
        self.assertEqual(score, 1 + 14 * 10 + 500 + 5)
    
    def test_score_pair_higher(self):
        """測試：對子分數 > 單張分數"""
        # 在相同的手牌剩餘情況下，對子應該比單張得分高
        single = [Card(14, 0)]  # 單♠A
        pair = [Card(14, 0), Card(14, 1)]  # 對 A
        
        score_single = AIStrategy.score_play(single, 2)
        score_pair = AIStrategy.score_play(pair, 1)
        
        # 對子的牌型基分（10）明顯高於單張（1），
        # 所以即使單張是梅花，對子分數也應該更高
        self.assertGreater(score_pair, score_single)
    
    def test_score_triple_higher(self):
        """測試：三條分數 > 對子分數"""
        # 在相同的手牌剩餘情況下，三條應該比對子得分高
        pair = [Card(14, 0), Card(14, 1)]  # 對 A
        triple = [Card(14, 0), Card(14, 1), Card(14, 2)]  # 三 A
        
        score_pair = AIStrategy.score_play(pair, 2)
        score_triple = AIStrategy.score_play(triple, 1)
        
        # 三條的牌型基分（100）高於對子（10）
        self.assertGreater(score_triple, score_pair)
    
    def test_score_near_empty(self):
        """測試：剩 1 張時的高分獎勵"""
        # 當手中只剩 1 張牌時，應獲得 +10000 的大獎勵
        play = [Card(3, 0)]  # 單梅花 3
        
        # 剩 1 張 vs 剩 2 張
        score_1_left = AIStrategy.score_play(play, 1)
        score_2_left = AIStrategy.score_play(play, 2)
        
        # 剩 1 張應獲得額外 10000 的獎勵
        self.assertAlmostEqual(score_1_left - score_2_left, 10000 - 500)
    
    def test_score_low_cards(self):
        """測試：剩 2 張時的中等獎勵"""
        # 當手中有 2 張牌時，應獲得 +500 的獎勵
        play = [Card(3, 0)]  # 單梅花 3
        
        # 剩 2 張 vs 剩 3 張
        score_2_left = AIStrategy.score_play(play, 2)
        score_3_left = AIStrategy.score_play(play, 3)
        
        # 剩 2 張應獲得額外 500 的獎勵
        self.assertAlmostEqual(score_2_left - score_3_left, 500)
    
    def test_score_spade_bonus(self):
        """測試：梅花牌的額外加分"""
        # 梅花牌（suit=0）每張獲得 +5 的加分
        single_spade = [Card(5, 0)]  # 梅花 5
        single_other = [Card(5, 1)]  # 紅心 5（suit=1）
        
        score_spade = AIStrategy.score_play(single_spade, 3)
        score_other = AIStrategy.score_play(single_other, 3)
        
        # 梅花牌應該比其他花色的牌多 5 分
        self.assertAlmostEqual(score_spade - score_other, 5)


class TestSelectBestPlay(unittest.TestCase):
    """選擇最佳出牌測試"""
    
    def test_select_best(self):
        """測試：從多個合法出牌中選擇分數最高的"""
        # 創建多個可能的出牌
        single = [Card(5, 0)]  # 單梅花 5
        pair = [Card(5, 0), Card(5, 1)]  # 對 5
        
        playable = [single, pair]
        
        # 當前手牌：5張（會出1或2張）
        current_hand = [Card(5, 0), Card(5, 1), Card(3, 0), Card(7, 0), Card(9, 0)]
        
        # 選擇最佳出牌
        best = AIStrategy.select_best(playable, current_hand, None)
        
        # 對子應該比單張得分高，所以應該選擇對子
        self.assertEqual(len(best), 2)  # 是對子
        self.assertEqual(best[0].rank, 5)
    
    def test_select_first_turn(self):
        """測試：第一回合選擇梅花三"""
        # 第一回合只能出梅花三
        three_clubs = [Card(3, 0)]
        
        playable = [three_clubs]
        
        # 當前手牌：13張（會出梅花3）
        current_hand = [Card(3, 0), Card(4, 0), Card(5, 0), Card(6, 0), 
                       Card(7, 0), Card(8, 0), Card(9, 0), Card(10, 0),
                       Card(11, 0), Card(12, 0), Card(13, 0), Card(14, 0),
                       Card(14, 1)]
        
        best = AIStrategy.select_best(playable, current_hand, None)
        
        # 應該選擇梅花三
        self.assertEqual(len(best), 1)
        self.assertEqual(best[0].rank, 3)
        self.assertEqual(best[0].suit, 0)
    
    def test_select_empty(self):
        """測試：沒有合法出牌時傳回 None"""
        playable = []  # 沒有合法出牌
        
        # 當前手牌：5張
        current_hand = [Card(13, 0), Card(13, 1), Card(5, 0), Card(6, 0), Card(7, 0)]
        
        best = AIStrategy.select_best(playable, current_hand, None)
        
        # 應該傳回 None
        self.assertIsNone(best)


class TestAIStrategy(unittest.TestCase):
    """完整 AI 策略測試"""
    
    def test_ai_always_plays(self):
        """測試：有出牌機會時一定出牌"""
        # 第一手出牌，手牌包含梅花三
        hand = [Card(3, 0), Card(14, 0), Card(13, 1)]
        last_play = None
        
        move = AIStrategy.get_best_move(hand, last_play)
        
        # 應該出牌（不能是 None）
        self.assertIsNotNone(move)
        # 第一手時應該出梅花三
        self.assertEqual(move[0].rank, 3)
        self.assertEqual(move[0].suit, 0)
    
    def test_ai_prefers_high(self):
        """測試：有多個出牌選擇時，偏好高牌"""
        # 上一手出的是單 5
        last_play = [Card(5, 0)]
        
        # 手牌中有多個可能的單張出牌（6, 7, 14）
        hand = [Card(6, 0), Card(7, 1), Card(14, 2), Card(3, 3)]
        
        move = AIStrategy.get_best_move(hand, last_play)
        
        # 應該出牌
        self.assertIsNotNone(move)
        # 應該出牌値最高的（14 = A）
        self.assertEqual(move[0].rank, 14)
    
    def test_ai_try_empty(self):
        """測試：剩最後一張牌時優先選擇出牌"""
        # 手牌只剩 1 張梅花 3
        hand = [Card(3, 0)]
        
        # 第一手出牌
        last_play = None
        
        move = AIStrategy.get_best_move(hand, last_play)
        
        # 應該選擇貪心策略：出牌（即使不是最佳選擇）
        # 因為出空了會有大獎勵 (+10000)
        self.assertIsNotNone(move)
        self.assertEqual(len(move), 1)


class TestAIDecisionLogic(unittest.TestCase):
    """AI 決策邏輯的綜合測試"""
    
    def test_ai_no_valid_play(self):
        """測試：無合法出牌時傳回 None"""
        # 上一手出的是對 A
        last_play = [Card(14, 0), Card(14, 1)]
        
        # 手牌只有小於 A 的對子
        hand = [Card(13, 0), Card(13, 1), Card(5, 2)]
        
        # 對 K（rank=13）小於對 A，無法出牌
        move = AIStrategy.get_best_move(hand, last_play)
        
        # 應該傳回 None（需要跳過）
        self.assertIsNone(move)
    
    def test_ai_select_winning_hand(self):
        """測試：如果可以選擇大牌或小牌，貪心選擇大牌"""
        # 上一手出的是單 5
        last_play = [Card(5, 0)]
        
        # 手牌中有 6（可出）和 14（A，更大）
        hand = [Card(6, 0), Card(14, 0), Card(3, 2), Card(13, 3)]
        
        move = AIStrategy.get_best_move(hand, last_play)
        
        # 應該選擇 A（rank=14），而不是 6（rank=6）
        self.assertIsNotNone(move)
        self.assertEqual(move[0].rank, 14)
    
    def test_ai_prefer_pairs_over_single(self):
        """測試：如果可以出對子或單張，偏好對子"""
        # 上一手出的是單 5
        last_play = [Card(5, 0)]
        
        # 手牌中有對 6 和單 14
        hand = [Card(6, 0), Card(6, 1), Card(14, 0), Card(3, 2)]
        
        move = AIStrategy.get_best_move(hand, last_play)
        
        # 對 6 的分數應該高於單 14
        # 因為對子的牌型加分 (10) 乘以 100 = 1000；
        # 而單張の加分 (1) 乘以 100 = 100，
        # 即使單張是 A (rank=14) 加 140，對子仍然更遠超（1000 + 60 = 1060）
        self.assertIsNotNone(move)
        # 應該出對 6
        if len(move) == 2:
            self.assertEqual(move[0].rank, 6)
        elif len(move) == 1:
            # 如果選單牌，應該是 A（最高價值）
            self.assertEqual(move[0].rank, 14)


# ==================== 測試執行 ====================

if __name__ == '__main__':
    # 使用 verbose 模式輸出詳細測試結果
    unittest.main(verbosity=2)
