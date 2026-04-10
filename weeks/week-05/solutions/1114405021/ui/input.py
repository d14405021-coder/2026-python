"""GUI 輸入元件（簡化版）。"""

from typing import Tuple


class InputHandler:
    """封裝按鈕與手牌點擊處理。"""

    def __init__(self, app) -> None:
        self.app = app

    def handle_click(self, pos: Tuple[int, int]):
        """先檢查按鈕，再檢查手牌。"""
        action = self.app.handle_button_click(pos)
        if action is not None:
            return action
        return self.app.handle_hand_click(pos)
