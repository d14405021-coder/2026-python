"""GUI 渲染元件（簡化版）。"""

from typing import List

from game.models import Card


class Renderer:
    """提供可測試的卡牌與手牌渲染封裝。"""

    def __init__(self, app) -> None:
        self.app = app

    def draw_card(self, card: Card):
        """委派給 app.render_card。"""
        return self.app.render_card(card)

    def draw_hand(self, cards: List[Card]):
        """委派給 app.render_hand。"""
        return self.app.render_hand(cards)
