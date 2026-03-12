"""Robot Lost pygame 互動視覺化。

操作說明：
- L / R / F：執行一步指令
- N：建立新機器人（保留 scent）
- C：清除 scent
- G：重播目前操作紀錄（回放機制）
- H：輸出回放 GIF（assets/replay.gif）
- S：儲存目前畫面（assets/gameplay.png）
- ESC：離開

這個檔案只處理互動與繪圖；規則判斷委託給 robot_core。
"""

import sys
from pathlib import Path
from typing import List, Set, Tuple

import pygame

try:
    from PIL import Image

    PIL_AVAILABLE = True
except ImportError:
    Image = None
    PIL_AVAILABLE = False

from robot_core import RobotState, Scent, execute_command

# 地圖大小：0..W, 0..H（含邊界）
GRID_W = 5
GRID_H = 3

CELL_SIZE = 90
MARGIN = 40
HUD_HEIGHT = 170

SCREEN_W = MARGIN * 2 + (GRID_W + 1) * CELL_SIZE
SCREEN_H = MARGIN * 2 + (GRID_H + 1) * CELL_SIZE + HUD_HEIGHT
BOARD_W = (GRID_W + 1) * CELL_SIZE
BOARD_H = (GRID_H + 1) * CELL_SIZE
HUD_TEXT_WIDTH = BOARD_W

BG_COLOR = (245, 245, 240)
GRID_COLOR = (120, 130, 140)
ROBOT_COLOR = (45, 85, 145)
SCENT_COLOR = (220, 85, 60)
TEXT_COLOR = (20, 30, 40)
LOST_COLOR = (190, 30, 30)
REPLAY_STEP_MS = 450


def grid_to_screen(x: int, y: int) -> Tuple[int, int]:
    """把格子座標轉成畫面座標（以格子中心點計算）。"""
    # 座標範圍是 0..W 與 0..H（含邊界），因此要用 (W+1) x (H+1) 個格心。
    sx = MARGIN + x * CELL_SIZE + CELL_SIZE // 2
    sy = MARGIN + (GRID_H - y) * CELL_SIZE + CELL_SIZE // 2
    return sx, sy


def robot_triangle_points(x: int, y: int, direction: str) -> List[Tuple[int, int]]:
    """回傳機器人三角形頂點，用來表達朝向。"""
    cx, cy = grid_to_screen(x, y)
    size = int(CELL_SIZE * 0.35)

    if direction == "N":
        return [(cx, cy - size), (cx - size, cy + size), (cx + size, cy + size)]
    if direction == "E":
        return [(cx + size, cy), (cx - size, cy - size), (cx - size, cy + size)]
    if direction == "S":
        return [(cx, cy + size), (cx - size, cy - size), (cx + size, cy - size)]
    # W
    return [(cx - size, cy), (cx + size, cy - size), (cx + size, cy + size)]


def draw_grid(screen: pygame.Surface) -> None:
    for x in range(GRID_W + 2):
        x_pos = MARGIN + x * CELL_SIZE
        pygame.draw.line(
            screen,
            GRID_COLOR,
            (x_pos, MARGIN),
            (x_pos, MARGIN + BOARD_H),
            1,
        )

    for y in range(GRID_H + 2):
        y_pos = MARGIN + y * CELL_SIZE
        pygame.draw.line(
            screen,
            GRID_COLOR,
            (MARGIN, y_pos),
            (MARGIN + BOARD_W, y_pos),
            1,
        )


def draw_scents(screen: pygame.Surface, scents: Set[Scent]) -> None:
    for sx, sy, _ in scents:
        cx, cy = grid_to_screen(sx, sy)
        pygame.draw.circle(screen, SCENT_COLOR, (cx, cy), 8)


def draw_robot(screen: pygame.Surface, state: RobotState) -> None:
    points = robot_triangle_points(state.x, state.y, state.direction)
    color = LOST_COLOR if state.lost else ROBOT_COLOR
    pygame.draw.polygon(screen, color, points)


def build_font(size: int) -> pygame.font.Font:
    """優先選擇可顯示繁中介面的字型，避免 HUD 亂碼。"""
    font_candidates = [
        "Microsoft JhengHei",
        "Microsoft JhengHei UI",
        "Noto Sans CJK TC",
        "PingFang TC",
        "Heiti TC",
        "Arial Unicode MS",
    ]

    for font_name in font_candidates:
        font_path = pygame.font.match_font(font_name)
        if font_path:
            return pygame.font.Font(font_path, size)

    return pygame.font.SysFont(None, size)


def extract_action(event: pygame.event.Event) -> str | None:
    """從鍵盤事件中解析操作字元，降低不同輸入法下的按鍵判斷問題。"""
    if event.key == pygame.K_ESCAPE:
        return "ESC"

    typed_char = event.unicode.upper() if event.unicode else ""
    if typed_char in {"L", "R", "F", "N", "C", "G", "H", "S"}:
        return typed_char

    key_name = pygame.key.name(event.key).upper()
    if key_name in {"L", "R", "F", "N", "C", "G", "H", "S"}:
        return key_name

    return None


def draw_hud(
    screen: pygame.Surface,
    font: pygame.font.Font,
    state: RobotState,
    scents: Set[Scent],
    history: List[str],
    mode: str,
    save_status: str,
) -> None:
    status_text = "LOST" if state.lost else "ALIVE"
    if mode == "REPLAY":
        hint_text = "目前是回放模式，手動操作暫停；按 G 可結束回放。"
    elif state.lost:
        hint_text = "機器人已掉落，後續指令不會生效；按 N 建立新機器人。"
    else:
        hint_text = "L/R 只會旋轉方向，F 才會前進一格。"

    lines = [
        f"機器人：({state.x}, {state.y}) {state.direction} | 狀態：{status_text}",
        f"模式：{mode}",
        f"scent 數量：{len(scents)}",
        "操作：L/R 旋轉，F 前進，N 新機器人，C 清除 scent，G 回放，H 匯出GIF，S 存檔，ESC 離開",
        hint_text,
        save_status,
        f"操作紀錄：{' '.join(history[-15:]) if history else '(empty)'}",
    ]

    pygame.draw.line(
        screen,
        GRID_COLOR,
        (MARGIN, MARGIN + BOARD_H + 8),
        (MARGIN + BOARD_W, MARGIN + BOARD_H + 8),
        1,
    )

    y_start = MARGIN + BOARD_H + 18
    rendered_line_index = 0
    for line in lines:
        wrapped_lines = wrap_text(line, font, HUD_TEXT_WIDTH)
        for wrapped_line in wrapped_lines:
            text_surface = font.render(wrapped_line, True, TEXT_COLOR)
            screen.blit(text_surface, (MARGIN, y_start + rendered_line_index * 22))
            rendered_line_index += 1


def wrap_text(text: str, font: pygame.font.Font, max_width: int) -> List[str]:
    """依畫面寬度自動換行，避免 HUD 文字被右側裁切。"""
    if font.size(text)[0] <= max_width:
        return [text]

    lines: List[str] = []
    current = ""
    for char in text:
        candidate = current + char
        if current and font.size(candidate)[0] > max_width:
            lines.append(current)
            current = char
        else:
            current = candidate

    if current:
        lines.append(current)

    return lines


def apply_action(
    action: str,
    state: RobotState,
    scents: Set[Scent],
) -> RobotState:
    """套用單一步驟操作，供一般互動與回放共用。"""
    if action == "N":
        return RobotState(0, 0, "N")

    if action == "C":
        scents.clear()
        return state

    if action in ("L", "R", "F"):
        execute_command(state, action, GRID_W, GRID_H, scents)
        return state

    return state


def render_scene(
    screen: pygame.Surface,
    font: pygame.font.Font,
    state: RobotState,
    scents: Set[Scent],
    history: List[str],
    mode: str,
    save_status: str,
) -> None:
    """集中處理單張畫面渲染，供即時顯示與 GIF 匯出共用。"""
    screen.fill(BG_COLOR)
    draw_grid(screen)
    draw_scents(screen, scents)
    draw_robot(screen, state)
    draw_hud(screen, font, state, scents, history, mode, save_status)


def surface_to_pil_image(surface: pygame.Surface):
    """把 pygame surface 轉成 PIL 影像。"""
    rgb_bytes = pygame.image.tostring(surface, "RGB")
    return Image.frombytes("RGB", surface.get_size(), rgb_bytes)


def export_replay_gif(
    actions: List[str],
    font: pygame.font.Font,
    output_path: Path,
) -> Tuple[bool, str]:
    """把操作紀錄重播成動畫 GIF。"""
    if not PIL_AVAILABLE:
        return False, "匯出失敗：缺少 Pillow（請安裝 pip install pillow）。"

    if not actions:
        return False, "匯出失敗：尚無操作紀錄。"

    replay_state = RobotState(0, 0, "N")
    replay_scents: Set[Scent] = set()
    replay_history: List[str] = []

    frame_surface = pygame.Surface((SCREEN_W, SCREEN_H))
    frames = []

    render_scene(
        frame_surface,
        font,
        replay_state,
        replay_scents,
        replay_history,
        "REPLAY",
        "正在準備 GIF 匯出...",
    )
    frames.append(surface_to_pil_image(frame_surface))

    for action in actions:
        replay_state = apply_action(action, replay_state, replay_scents)
        replay_history.append(action)
        render_scene(
            frame_surface,
            font,
            replay_state,
            replay_scents,
            replay_history,
            "REPLAY",
            "正在匯出 replay.gif...",
        )
        frames.append(surface_to_pil_image(frame_surface))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=REPLAY_STEP_MS,
        loop=0,
    )

    return True, f"已匯出：{output_path.name}"


def main() -> None:
    pygame.init()
    pygame.display.set_caption("Robot Lost Visualizer")
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    clock = pygame.time.Clock()
    font = build_font(18)

    scents: Set[Scent] = set()
    state = RobotState(0, 0, "N")
    history: List[str] = []
    actions: List[str] = []

    replay_mode = False
    replay_state = RobotState(0, 0, "N")
    replay_scents: Set[Scent] = set()
    replay_history: List[str] = []
    replay_index = 0
    replay_last_tick = 0
    save_status = "尚未存檔。"
    save_path = Path(__file__).resolve().parent / "assets" / "gameplay.png"
    replay_gif_path = Path(__file__).resolve().parent / "assets" / "replay.gif"
    pending_save = False
    pending_gif_export = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                action = extract_action(event)
                if action == "ESC":
                    running = False
                elif action == "G":
                    if replay_mode:
                        replay_mode = False
                    elif actions:
                        replay_mode = True
                        replay_state = RobotState(0, 0, "N")
                        replay_scents = set()
                        replay_history = []
                        replay_index = 0
                        replay_last_tick = pygame.time.get_ticks()
                elif not replay_mode:
                    if action == "N":
                        state = apply_action("N", state, scents)
                        history.append("N")
                        actions.append("N")
                    elif action == "C":
                        state = apply_action("C", state, scents)
                        history.append("C")
                        actions.append("C")
                    elif action in ("L", "R", "F"):
                        state = apply_action(action, state, scents)
                        history.append(action)
                        actions.append(action)

                if action == "S":
                    pending_save = True

                if action == "H":
                    pending_gif_export = True

        if replay_mode and replay_index < len(actions):
            now = pygame.time.get_ticks()
            if now - replay_last_tick >= REPLAY_STEP_MS:
                action = actions[replay_index]
                replay_state = apply_action(action, replay_state, replay_scents)
                replay_history.append(action)
                replay_index += 1
                replay_last_tick = now
        elif replay_mode and replay_index >= len(actions):
            replay_mode = False

        view_state = replay_state if replay_mode else state
        view_scents = replay_scents if replay_mode else scents
        view_history = replay_history if replay_mode else history
        mode_text = "REPLAY" if replay_mode else "LIVE"

        render_scene(screen, font, view_state, view_scents, view_history, mode_text, save_status)

        if pending_save:
            save_path.parent.mkdir(parents=True, exist_ok=True)
            pygame.image.save(screen, str(save_path))
            save_status = f"已存檔：{save_path.name}"
            pending_save = False

        if pending_gif_export:
            _, message = export_replay_gif(actions, font, replay_gif_path)
            save_status = message
            pending_gif_export = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
