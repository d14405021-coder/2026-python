"""
Big Two 遊戲 - Phase 5 遊戲流程控制

本模組提供 BigTwoGame 類別，負責管理完整遊戲流程：
1. 初始化牌局（建立玩家、洗牌、發牌、決定先手）
2. 玩家出牌與過牌
3. 回合切換與回合重置
4. 勝負判定與遊戲結束狀態

設計重點：
- 優先與既有 models.py / classifier.py / ai.py 相容。
- 提供多個別名方法，方便不同測試命名風格呼叫。
"""

from typing import List, Optional

from .ai import AIStrategy
from .classifier import HandClassifier
from .models import Card, Deck, Player


class BigTwoGame:
    """Big Two 遊戲流程控制器。"""

    def __init__(self) -> None:
        """
        建立遊戲物件，但不立即發牌。

        使用者可在建立後呼叫 setup() 進行正式初始化。
        """
        self.deck: Deck = Deck()

        # 固定 4 位玩家：1 人類 + 3 AI
        self.players: List[Player] = [
            Player("Player", is_ai=False),
            Player("AI-1", is_ai=True),
            Player("AI-2", is_ai=True),
            Player("AI-3", is_ai=True),
        ]

        # 目前輪到哪位玩家（0-3）
        self.current_player_index: int = 0

        # 上一手出的牌；None 代表新回合首出（或三次過牌後重置）
        self.last_play: Optional[List[Card]] = None

        # 連續過牌計數（不含打出 last_play 的玩家）
        self.pass_count: int = 0

        # 獲勝者與遊戲狀態
        self.winner: Optional[Player] = None
        self.is_game_over: bool = False

        # 回合編號，可做除錯或紀錄用
        self.round_number: int = 1

    # ==================== 初始化 ====================

    def setup(self) -> None:
        """
        初始化整局遊戲。

        步驟：
        1. 重新建立並洗牌
        2. 清空玩家手牌
        3. 每位玩家發 13 張（共 52 張）
        4. 找出持有梅花 3 的玩家作為先手
        5. 重置回合狀態與勝負狀態
        """
        self.deck = Deck()
        self.deck.shuffle()

        # 先清空舊手牌，避免重複 setup 時累加
        for player in self.players:
            player.hand.cards = []

        # 每人發 13 張
        for player in self.players:
            player.take_cards(self.deck.deal(13))

        # 找出先手（持有 ♣3 的玩家）
        self.current_player_index = self._find_player_with_three_of_clubs()

        # 重置局面狀態
        self.last_play = None
        self.pass_count = 0
        self.winner = None
        self.is_game_over = False
        self.round_number = 1

    def start_game(self) -> None:
        """setup() 的別名，提供相容介面。"""
        self.setup()

    # ==================== 回合資訊 ====================

    def get_current_player(self) -> Player:
        """取得目前輪到的玩家。"""
        return self.players[self.current_player_index]

    def next_turn(self) -> None:
        """輪到下一位玩家。"""
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    # ==================== 出牌與過牌 ====================

    def play_turn(self, cards: List[Card]) -> bool:
        """
        目前玩家嘗試出牌。

        回傳：
        - True：出牌成功
        - False：出牌失敗（例如不合法、牌不在手上、遊戲已結束）
        """
        if self.is_game_over:
            return False

        current_player = self.get_current_player()

        # 1) 基本防呆：不能出空牌
        if not cards:
            return False

        # 2) 卡牌所有權檢查：出的每一張都必須在當前玩家手牌中
        hand_cards_set = set(current_player.hand.cards)
        if any(card not in hand_cards_set for card in cards):
            return False

        # 3) 牌型合法性檢查（第一手必須是 ♣3；其他手需同牌型且更大）
        if not HandClassifier.can_play(self.last_play, cards):
            return False

        # 4) 真正移除手牌
        played = current_player.play_cards(cards)
        if played is None:
            return False

        # 5) 更新局面
        self.last_play = list(cards)
        self.pass_count = 0

        # 6) 檢查是否有人出完牌
        self.check_winner()
        return True

    def play_cards(self, cards: List[Card]) -> bool:
        """play_turn() 的別名，提供相容介面。"""
        return self.play_turn(cards)

    def play(self, cards: List[Card]) -> bool:
        """play_turn() 的別名，提供相容介面。"""
        return self.play_turn(cards)

    def pass_turn(self) -> bool:
        """
        目前玩家選擇過牌。

        規則：
        - 過牌後 pass_count + 1
        - 若 pass_count >= 3，表示一輪已結束，重置 last_play 與 pass_count
        """
        if self.is_game_over:
            return False

        self.pass_count += 1
        self.check_round_reset()
        return True

    def pass_play(self) -> bool:
        """pass_turn() 的別名，提供相容介面。"""
        return self.pass_turn()

    def player_pass(self) -> bool:
        """pass_turn() 的別名，提供相容介面。"""
        return self.pass_turn()

    def pass_(self, player: Player) -> bool:
        """
        與開發文件相容的方法名稱。

        目前以 current_player 為主控，故忽略傳入 player，統一呼叫 pass_turn()。
        """
        _ = player
        return self.pass_turn()

    # ==================== 勝負與回合重置 ====================

    def check_round_reset(self) -> None:
        """
        檢查是否需要重置回合。

        當連續 3 次過牌時，重置：
        - last_play = None
        - pass_count = 0
        """
        if self.pass_count >= 3:
            self.last_play = None
            self.pass_count = 0
            self.round_number += 1

    def check_winner(self) -> Optional[Player]:
        """
        檢查是否有人已出完手牌。

        回傳：
        - Player：第一位手牌為空的玩家
        - None：尚無獲勝者
        """
        for player in self.players:
            if len(player.hand.cards) == 0:
                self.winner = player
                self.is_game_over = True
                return player

        self.winner = None
        self.is_game_over = False
        return None

    def get_winner(self) -> Optional[Player]:
        """check_winner() 的別名，提供相容介面。"""
        return self.check_winner()

    # ==================== AI 回合 ====================

    def ai_turn(self) -> bool:
        """
        執行目前 AI 玩家的一個回合。

        策略：
        - 若當前玩家不是 AI，直接回傳 False
        - AI 有可出牌時出最佳牌（回傳 True）
        - 否則過牌（也回傳 True，表示回合動作已執行）
        """
        if self.is_game_over:
            return False

        player = self.get_current_player()
        if not player.is_ai:
            return False

        move = AIStrategy.get_best_move(player.hand.cards, self.last_play)
        if move:
            return self.play_turn(move)
        return self.pass_turn()

    # ==================== 私有輔助 ====================

    def _find_player_with_three_of_clubs(self) -> int:
        """找出持有梅花三 (♣3) 的玩家索引。"""
        three_clubs = Card(3, 0)
        for idx, player in enumerate(self.players):
            if three_clubs in player.hand.cards:
                return idx

        # 正常 52 張牌分完一定會有人有 ♣3，若真的沒有就保底回傳 0
        return 0
