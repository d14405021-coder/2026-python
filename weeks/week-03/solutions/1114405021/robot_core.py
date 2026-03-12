"""Robot Lost 核心邏輯（不依賴 pygame）。

這個模組專注在規則本身：
1. 方向旋轉（L/R）
2. 前進與越界判斷（F）
3. LOST 與 scent 記錄

設計重點是讓邏輯可單獨測試，畫面層只要呼叫這裡的函式即可。
"""

from dataclasses import dataclass
from typing import Set, Tuple

Direction = str
Scent = Tuple[int, int, Direction]

DIRECTIONS = ("N", "E", "S", "W")
MOVE_TABLE = {
    "N": (0, 1),
    "E": (1, 0),
    "S": (0, -1),
    "W": (-1, 0),
}


@dataclass
class RobotState:
    """機器人狀態。

    - x, y: 座標
    - direction: 朝向，只允許 N/E/S/W
    - lost: 是否已經掉出地圖
    """

    x: int
    y: int
    direction: Direction
    lost: bool = False


def validate_direction(direction: Direction) -> None:
    """驗證方向是否合法。"""
    if direction not in DIRECTIONS:
        raise ValueError(f"Invalid direction: {direction}")


def normalize_direction(direction: Direction) -> Direction:
    """把方向字串正規化成大寫並驗證。"""
    normalized = direction.upper()
    validate_direction(normalized)
    return normalized


def turn_left(direction: Direction) -> Direction:
    """向左旋轉 90 度。"""
    direction = normalize_direction(direction)
    index = DIRECTIONS.index(direction)
    return DIRECTIONS[(index - 1) % 4]


def turn_right(direction: Direction) -> Direction:
    """向右旋轉 90 度。"""
    direction = normalize_direction(direction)
    index = DIRECTIONS.index(direction)
    return DIRECTIONS[(index + 1) % 4]


def next_position(x: int, y: int, direction: Direction) -> Tuple[int, int]:
    """計算朝目前方向前進一步後的目標座標。"""
    direction = normalize_direction(direction)
    dx, dy = MOVE_TABLE[direction]
    return x + dx, y + dy


def is_out_of_bounds(x: int, y: int, width: int, height: int) -> bool:
    """判斷座標是否超出地圖範圍。"""
    return x < 0 or x > width or y < 0 or y > height


def execute_command(
    state: RobotState,
    command: str,
    width: int,
    height: int,
    scents: Set[Scent],
) -> None:
    """執行單一步驟命令。

    規則摘要：
    - 若已 LOST，任何命令都不再處理。
    - L/R 僅改變方向。
    - F 若會越界：
      1) 若目前 (x, y, dir) 已有 scent，忽略此命令。
      2) 否則標記 lost=True，並新增 scent。
    """
    if state.lost:
        return

    command = command.upper()
    if command == "L":
        state.direction = turn_left(state.direction)
        return

    if command == "R":
        state.direction = turn_right(state.direction)
        return

    if command == "F":
        nx, ny = next_position(state.x, state.y, state.direction)
        if is_out_of_bounds(nx, ny, width, height):
            scent_key = (state.x, state.y, state.direction)
            if scent_key in scents:
                return
            scents.add(scent_key)
            state.lost = True
            return

        state.x, state.y = nx, ny
        return

    raise ValueError(f"Invalid command: {command}")


def run_commands(
    start_x: int,
    start_y: int,
    start_direction: Direction,
    commands: str,
    width: int,
    height: int,
    scents: Set[Scent],
) -> RobotState:
    """從初始狀態跑完整串命令，回傳最終狀態。"""
    start_direction = normalize_direction(start_direction)
    state = RobotState(start_x, start_y, start_direction)

    for command in commands:
        execute_command(state, command, width, height, scents)
        if state.lost:
            break

    return state
