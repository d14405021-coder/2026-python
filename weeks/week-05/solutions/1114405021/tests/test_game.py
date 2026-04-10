"""
Phase 5: Big Two 遊戲流程單元測試

此測試檔對應 p5-test.md 的需求，目標是驗證 BigTwoGame 類別是否能正確控制：
1. 遊戲初始化
2. 出牌流程
3. 回合判定
4. 獲勝判定

說明：
- 本檔採用 Python 標準函式庫 unittest。
- 測試以「介面行為」為中心，讓你在實作 game.py 時可依此逐步通過。
- 若目前尚未建立 game.py / BigTwoGame，測試會在 setUp 時明確提示失敗原因（TDD 的 Red 階段）。
"""

import unittest
from typing import Any, List, Optional

from game.models import Card


class TestBigTwoGameFlow(unittest.TestCase):
    """BigTwoGame 遊戲流程測試集合。"""

    def setUp(self) -> None:
        """
        每個測試前都重新建立一局新遊戲，避免測試彼此污染。

        為了讓錯誤訊息更清楚，這裡不在檔案頂端直接 import BigTwoGame，
        而是在 setUp 才嘗試載入，若失敗會給出具體提示。
        """
        try:
            from game import BigTwoGame  # pylint: disable=import-outside-toplevel
        except Exception as exc:
            self.fail(
                "無法匯入 BigTwoGame。請確認已建立 game.py 並定義 BigTwoGame 類別。"
                f"\n原始錯誤：{exc}"
            )

        self.game = BigTwoGame()
        self._call_setup(self.game)

    # ==================== 測試輔助方法 ====================

    def _call_setup(self, game: Any) -> None:
        """呼叫初始化方法；優先使用 setup()，其次接受 start_game()。"""
        if hasattr(game, "setup"):
            game.setup()
            return
        if hasattr(game, "start_game"):
            game.start_game()
            return
        self.fail("BigTwoGame 缺少 setup()（或 start_game()）初始化方法。")

    def _players(self) -> List[Any]:
        """統一取得 players 清單。"""
        if not hasattr(self.game, "players"):
            self.fail("BigTwoGame 應包含 players 屬性。")
        return self.game.players

    def _current_player_index(self) -> int:
        """統一取得目前輪到哪位玩家的索引。"""
        for attr_name in ("current_player_index", "current_turn", "turn_index", "player_index"):
            if hasattr(self.game, attr_name):
                return int(getattr(self.game, attr_name))
        self.fail("BigTwoGame 應包含 current_player_index（或等價）屬性。")

    def _last_play(self) -> Optional[List[Card]]:
        """統一取得上一手牌。"""
        if hasattr(self.game, "last_play"):
            return self.game.last_play
        self.fail("BigTwoGame 應包含 last_play 屬性。")

    def _pass_count(self) -> int:
        """統一取得目前連續過牌數。"""
        if hasattr(self.game, "pass_count"):
            return int(self.game.pass_count)
        self.fail("BigTwoGame 應包含 pass_count 屬性。")

    def _call_play(self, cards: List[Card]) -> Any:
        """
        呼叫出牌方法。

        預期介面優先順序：
        1. play_turn(cards)
        2. play_cards(cards)
        3. play(cards)
        """
        for method_name in ("play_turn", "play_cards", "play"):
            if hasattr(self.game, method_name):
                method = getattr(self.game, method_name)
                return method(cards)
        self.fail("BigTwoGame 缺少出牌方法：play_turn(cards) / play_cards(cards) / play(cards)。")

    def _call_pass(self) -> Any:
        """
        呼叫過牌方法。

        預期介面優先順序：
        1. pass_turn()
        2. pass_play()
        3. player_pass()
        """
        for method_name in ("pass_turn", "pass_play", "player_pass"):
            if hasattr(self.game, method_name):
                return getattr(self.game, method_name)()
        self.fail("BigTwoGame 缺少過牌方法：pass_turn() / pass_play() / player_pass()。")

    def _call_next_turn(self) -> None:
        """呼叫換手方法 next_turn()。"""
        if hasattr(self.game, "next_turn"):
            self.game.next_turn()
            return
        self.fail("BigTwoGame 缺少 next_turn() 方法。")

    def _call_check_winner(self) -> Any:
        """
        呼叫勝負檢查方法。

        預期介面優先順序：
        1. check_winner()
        2. get_winner()
        """
        for method_name in ("check_winner", "get_winner"):
            if hasattr(self.game, method_name):
                return getattr(self.game, method_name)()
        self.fail("BigTwoGame 缺少 check_winner() / get_winner() 方法。")

    # ==================== 1. 遊戲初始化 ====================

    def test_game_has_4_players(self):
        """測試：setup 後應有 4 位玩家。"""
        self.assertEqual(len(self._players()), 4)

    def test_each_player_13_cards(self):
        """測試：setup 後每位玩家應持有 13 張牌。"""
        for player in self._players():
            self.assertEqual(len(player.hand.cards), 13)

    def test_total_cards_distributed(self):
        """測試：setup 後 4 位玩家總牌數應為 52。"""
        total_cards = sum(len(player.hand.cards) for player in self._players())
        self.assertEqual(total_cards, 52)

    def test_first_player_has_3_clubs(self):
        """
        測試：先手必須持有梅花 3 (♣3)。

        大老二常見規則是持有梅花 3 的玩家先手。
        這裡驗證目前回合玩家手中確實有 Card(3, 0)。
        """
        first_idx = self._current_player_index()
        first_player = self._players()[first_idx]
        self.assertIn(Card(3, 0), first_player.hand.cards)

    def test_one_human_three_ai(self):
        """測試：玩家組成應為 1 人類 + 3 AI。"""
        players = self._players()
        ai_count = sum(1 for p in players if getattr(p, "is_ai", False))
        human_count = len(players) - ai_count

        self.assertEqual(ai_count, 3)
        self.assertEqual(human_count, 1)

    # ==================== 2. 出牌流程 ====================

    def test_play_removes_cards(self):
        """
        測試：出牌成功後，玩家手牌數應減少。

        這裡用開局合法牌 ♣3 測試，避免測試因牌型合法性受影響。
        """
        idx = self._current_player_index()
        player = self._players()[idx]
        before = len(player.hand.cards)

        result = self._call_play([Card(3, 0)])

        self.assertTrue(result)
        self.assertEqual(len(player.hand.cards), before - 1)

    def test_play_sets_last_play(self):
        """測試：出牌成功後，game.last_play 應被正確設定。"""
        self._call_play([Card(3, 0)])
        self.assertEqual(self._last_play(), [Card(3, 0)])

    def test_invalid_play(self):
        """
        測試：非法出牌應回傳 False。

        測試策略：找一張「當前玩家手上沒有」的牌嘗試出牌。
        """
        idx = self._current_player_index()
        player_cards = set(self._players()[idx].hand.cards)

        invalid_card = None
        for suit in range(4):
            for rank in range(3, 16):
                candidate = Card(rank, suit)
                if candidate not in player_cards:
                    invalid_card = candidate
                    break
            if invalid_card is not None:
                break

        self.assertIsNotNone(invalid_card, "測試資料異常：找不到不在玩家手中的牌。")

        result = self._call_play([invalid_card])
        self.assertFalse(result)

    def test_pass_increments(self):
        """測試：玩家過牌後，pass_count 應 +1。"""
        before = self._pass_count()
        self._call_pass()
        self.assertEqual(self._pass_count(), before + 1)

    # ==================== 3. 回合判定 ====================

    def test_three_passes_resets(self):
        """
        測試：連續 3 次過牌後，應重置 last_play 與 pass_count。

        為了聚焦規則本身，先直接設定一個可識別的 last_play 與 pass_count=2，
        再呼叫一次過牌，期待觸發「第三次過牌」的重置邏輯。
        """
        self.game.last_play = [Card(3, 0)]
        self.game.pass_count = 2

        self._call_pass()

        self.assertIsNone(self._last_play())
        self.assertEqual(self._pass_count(), 0)

    def test_turn_rotates(self):
        """測試：呼叫 next_turn() 後，應輪到下一家。"""
        before = self._current_player_index()

        self._call_next_turn()

        after = self._current_player_index()
        self.assertEqual(after, (before + 1) % 4)

    # ==================== 4. 獲勝判定 ====================

    def test_detect_winner(self):
        """測試：若有玩家手牌為空，應能回傳該玩家作為贏家。"""
        players = self._players()
        players[0].hand.cards = []

        winner = self._call_check_winner()

        self.assertIsNotNone(winner)
        self.assertEqual(winner, players[0])

    def test_no_winner_yet(self):
        """測試：若所有玩家仍有手牌，應回傳 None。"""
        winner = self._call_check_winner()
        self.assertIsNone(winner)

    def test_game_ends(self):
        """
        測試：有贏家時，遊戲結束旗標應為 True。

        預期 BigTwoGame 在 check_winner() 後，會更新 is_game_over。
        """
        players = self._players()
        players[1].hand.cards = []

        _ = self._call_check_winner()

        self.assertTrue(
            getattr(self.game, "is_game_over", False),
            "有玩家獲勝後，BigTwoGame.is_game_over 應為 True。",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
