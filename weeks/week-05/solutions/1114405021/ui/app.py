"""
Big Two 遊戲 - Phase 6 GUI（簡化可測版本）

此模組提供 BigTwoApp，目標是：
1. 與 Phase 5 的 BigTwoGame 整合
2. 提供可測試的渲染介面（render_card / render_hand）
3. 提供可測試的輸入介面（點擊座標轉牌索引、按鈕點擊）
4. 提供可推進流程的方法（run_one_frame / update）

說明：
- 這是「教學與測試優先」版本，先確保行為正確。
- 若安裝了真實 pygame，會使用真實圖形能力。
- 若未安裝 pygame，會使用內建 fallback，讓測試仍可在無 GUI 環境執行。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from game import BigTwoGame
from game.models import Card

# ==================== pygame 匯入與 fallback ====================

try:
    import pygame  # type: ignore
except Exception:  # pragma: no cover - 測試環境通常會注入 fake pygame
    pygame = None


class _FallbackSurface:
    """當 pygame 不可用時使用的最小 Surface 實作。"""

    def __init__(self, size: Tuple[int, int]):
        self._width, self._height = size

    def get_width(self) -> int:
        return self._width

    def get_height(self) -> int:
        return self._height

    def fill(self, *_args, **_kwargs) -> None:
        return None

    def blit(self, *_args, **_kwargs) -> None:
        return None


@dataclass
class UIButton:
    """GUI 按鈕資料結構。"""

    name: str
    rect: object


class BigTwoApp:
    """Big Two GUI 主應用（簡化版本）。"""

    # 視窗與牌面尺寸設定
    SCREEN_WIDTH = 960
    SCREEN_HEIGHT = 640
    CARD_WIDTH = 60
    CARD_HEIGHT = 90

    # 手牌區域（提供點擊轉索引用）
    HAND_START_X = 40
    HAND_Y = 500
    CARD_SPACING = 36

    # 色彩設定（RGB）
    BG_COLOR = (45, 45, 45)
    CARD_COLOR = (250, 250, 250)
    CARD_BORDER = (30, 30, 30)

    def __init__(self) -> None:
        """
        初始化 App。

        初始化內容：
        1. 建立遊戲實例並 setup
        2. 初始化 pygame 或 fallback surface
        3. 建立按鈕矩形
        4. 建立選牌狀態
        """
        # 1) 遊戲初始化
        self.game = BigTwoGame()
        self.game.setup()

        # 2) 圖形初始化
        self._use_pygame = pygame is not None
        if self._use_pygame:
            pygame.init()
            pygame.font.init()
            self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
            pygame.display.set_caption("Big Two")
            self.font = pygame.font.SysFont(None, 24)
        else:
            self.screen = _FallbackSurface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
            self.font = None

        # 3) 按鈕區（配合測試點擊座標 (700, 550)）
        self.buttons: Dict[str, UIButton] = {
            "play": UIButton("play", self._make_rect(640, 520, 120, 44)),
            "pass": UIButton("pass", self._make_rect(780, 520, 120, 44)),
        }

        # 4) 已選手牌索引
        self.selected_indices: List[int] = []

    # ==================== 基礎工具 ====================

    def _make_rect(self, x: int, y: int, w: int, h: int):
        """建立 pygame.Rect 或 fallback Rect。"""
        if self._use_pygame:
            return pygame.Rect(x, y, w, h)

        class _Rect:
            def __init__(self, x0, y0, w0, h0):
                self.x = x0
                self.y = y0
                self.w = w0
                self.h = h0

            def collidepoint(self, pos: Tuple[int, int]) -> bool:
                px, py = pos
                return self.x <= px <= self.x + self.w and self.y <= py <= self.y + self.h

        return _Rect(x, y, w, h)

    def _new_surface(self, size: Tuple[int, int]):
        """建立 Surface（pygame 或 fallback）。"""
        if self._use_pygame:
            return pygame.Surface(size)
        return _FallbackSurface(size)

    # ==================== 渲染方法 ====================

    def render_card(self, card: Card):
        """
        渲染單張牌為 surface。

        教學重點：
        - 測試主要檢查 surface 是否存在、寬度是否 > 0。
        - 真實 UI 可在這裡加入花色顏色、字型、陰影等細節。
        """
        surface = self._new_surface((self.CARD_WIDTH, self.CARD_HEIGHT))

        # 真實 pygame 模式下，先填底色；fallback 中 fill 也是 no-op，可安全呼叫
        surface.fill(self.CARD_COLOR)

        # 在 pygame 模式補上外框與文字，提升可視性
        if self._use_pygame:
            pygame.draw.rect(surface, self.CARD_BORDER, pygame.Rect(0, 0, self.CARD_WIDTH, self.CARD_HEIGHT), 2)
            text = f"{card}"
            text_surf = self.font.render(text, True, (10, 10, 10))
            surface.blit(text_surf, (8, 8))

        return surface

    def draw_card_surface(self, card: Card):
        """render_card 的別名。"""
        return self.render_card(card)

    def create_card_surface(self, card: Card):
        """render_card 的別名。"""
        return self.render_card(card)

    def render_hand(self, cards: List[Card]):
        """
        渲染整手牌為單一 surface。

        教學重點：
        - 寬度依牌數與重疊間距計算，至少為一張牌寬。
        - 這樣可以讓測試穩定驗證寬高 > 0。
        """
        card_count = max(1, len(cards))
        width = self.CARD_WIDTH + (card_count - 1) * self.CARD_SPACING
        height = self.CARD_HEIGHT + 16

        hand_surface = self._new_surface((width, height))
        hand_surface.fill((60, 60, 60))

        for idx, card in enumerate(cards):
            card_surface = self.render_card(card)
            x = idx * self.CARD_SPACING
            hand_surface.blit(card_surface, (x, 0))

        return hand_surface

    def draw_hand_surface(self, cards: List[Card]):
        """render_hand 的別名。"""
        return self.render_hand(cards)

    def create_hand_surface(self, cards: List[Card]):
        """render_hand 的別名。"""
        return self.render_hand(cards)

    # ==================== 輸入處理 ====================

    def screen_to_card_index(self, pos: Tuple[int, int]) -> int:
        """
        將螢幕座標轉為人類玩家手牌索引。

        回傳：
        - >=0 的索引：點到某張牌
        - -1：不在手牌區域或超出範圍
        """
        x, y = pos

        # 先檢查是否在手牌 Y 範圍內
        if y < self.HAND_Y or y > self.HAND_Y + self.CARD_HEIGHT:
            return -1

        # 轉為相對手牌起點的 x
        rel_x = x - self.HAND_START_X
        if rel_x < 0:
            return -1

        # 以間距換算索引
        idx = rel_x // self.CARD_SPACING
        human_player = self.game.players[0]
        if idx < 0 or idx >= len(human_player.hand.cards):
            return -1
        return int(idx)

    def position_to_card_index(self, pos: Tuple[int, int]) -> int:
        """screen_to_card_index 的別名。"""
        return self.screen_to_card_index(pos)

    def get_card_index_from_pos(self, pos: Tuple[int, int]) -> int:
        """screen_to_card_index 的別名。"""
        return self.screen_to_card_index(pos)

    def handle_hand_click(self, pos: Tuple[int, int]):
        """處理手牌點擊並切換選擇狀態。"""
        idx = self.screen_to_card_index(pos)
        if idx < 0:
            return False

        if idx in self.selected_indices:
            self.selected_indices.remove(idx)
        else:
            self.selected_indices.append(idx)
        return list(self.selected_indices)

    def handle_button_click(self, pos: Tuple[int, int]):
        """
        處理按鈕點擊。

        回傳：
        - 'play' / 'pass'：點到對應按鈕
        - None：未點到任何按鈕
        """
        if self.buttons["play"].rect.collidepoint(pos):
            return "play"
        if self.buttons["pass"].rect.collidepoint(pos):
            return "pass"
        return None

    def on_button_click(self, pos: Tuple[int, int]):
        """handle_button_click 的別名。"""
        return self.handle_button_click(pos)

    def handle_click(self, pos: Tuple[int, int]):
        """handle_button_click 的別名。"""
        return self.handle_button_click(pos)

    # ==================== 主迴圈驅動 ====================

    def update(self) -> None:
        """
        推進一個更新步驟。

        這個方法在測試中會被用來驅動流程，核心是：
        1. 檢查是否有贏家
        2. 若輪到 AI 且尚未結束，執行 AI 回合
        """
        self.game.check_winner()
        if self.game.is_game_over:
            return

        current = self.game.get_current_player()
        if current.is_ai:
            self.game.ai_turn()
            self.game.next_turn()

    def run_one_frame(self) -> None:
        """update 的別名，讓測試可用 run_one_frame() 推進。"""
        self.update()

    def run(self) -> None:
        """
        簡化主迴圈。

        此版本僅示範結構；完整互動可再擴充事件處理與完整繪製流程。
        """
        if not self._use_pygame:
            # 無 pygame 時不進入無窮迴圈，避免在測試或無頭環境卡住
            return

        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill(self.BG_COLOR)
            self.update()
            pygame.display.flip()
            clock.tick(30)

        pygame.quit()
