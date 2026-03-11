"""
UVA 118 機器人問題解決方案

問題描述：
給定一個矩形網格和多個機器人的初始位置及指令序列，
模擬機器人在網格中的移動行為。機器人會根據指令轉向或前進，
如果嘗試走出邊界會掉落並留下標記，後續機器人會忽略導致掉落的指令。

輸入格式：
第一行：兩個正整數 max_x max_y，表示網格右上角坐標
接下來每兩個行為一組：
  第一行：x y direction（初始位置和方向）
  第二行：指令序列（由 L、R、F 組成）

輸出格式：
每行輸出一個機器人的最終狀態：x y direction [LOST]
如果掉落則加上 LOST

解題思路：
1. 使用類別封裝機器人邏輯，便於管理狀態
2. 使用集合儲存掉落標記，提高查找效率
3. 依序處理每個機器人，模擬其完整移動過程
4. 正確處理邊界檢查和標記機制
"""

import sys

class RobotSimulator:
    """
    機器人模擬器類別，用於處理 UVA 118 題目的機器人移動邏輯。

    這個類別負責管理網格邊界、掉落標記，以及處理單個機器人的移動行為。
    """

    def __init__(self, max_x, max_y):
        """
        初始化模擬器，設定網格範圍和標記系統。

        參數:
        max_x (int): 網格的最大 x 坐標 (0 到 max_x)
        max_y (int): 網格的最大 y 坐標 (0 到 max_y)
        """
        self.max_x = max_x  # 網格右邊界
        self.max_y = max_y  # 網格上邊界
        self.scent = set()  # 儲存掉落標記的坐標集合，使用 set 提高查找效率

    def turn_left(self, direction):
        """
        處理機器人左轉 90 度的操作。

        參數:
        direction (str): 當前面向的方向 ('N', 'S', 'E', 'W')

        返回:
        str: 左轉後的新方向

        轉向規則：
        N(北) -> W(西) -> S(南) -> E(東) -> N(北)
        """
        # 使用字典定義左轉對應關係
        turns = {'N': 'W', 'W': 'S', 'S': 'E', 'E': 'N'}
        return turns[direction]

    def turn_right(self, direction):
        """
        處理機器人右轉 90 度的操作。

        參數:
        direction (str): 當前面向的方向 ('N', 'S', 'E', 'W')

        返回:
        str: 右轉後的新方向

        轉向規則：
        N(北) -> E(東) -> S(南) -> W(西) -> N(北)
        """
        # 使用字典定義右轉對應關係
        turns = {'N': 'E', 'E': 'S', 'S': 'W', 'W': 'N'}
        return turns[direction]

    def move_forward(self, x, y, direction):
        """
        根據當前方向計算前進一步的新坐標。

        參數:
        x (int): 當前 x 坐標
        y (int): 當前 y 坐標
        direction (str): 當前面向的方向

        返回:
        tuple: (new_x, new_y) 前進後的新坐標

        移動規則：
        - N(北): y 坐標 +1
        - S(南): y 坐標 -1
        - E(東): x 坐標 +1
        - W(西): x 坐標 -1
        """
        if direction == 'N':
            return x, y + 1  # 向北移動
        elif direction == 'S':
            return x, y - 1  # 向南移動
        elif direction == 'E':
            return x + 1, y  # 向東移動
        elif direction == 'W':
            return x - 1, y  # 向西移動

    def is_out_of_bounds(self, x, y):
        """
        檢查給定的坐標是否超出網格邊界。

        參數:
        x (int): 要檢查的 x 坐標
        y (int): 要檢查的 y 坐標

        返回:
        bool: True 如果坐標超出邊界 (x < 0 or x > max_x or y < 0 or y > max_y)，否則 False

        邊界定義：
        - 左邊界: x >= 0
        - 右邊界: x <= max_x
        - 下邊界: y >= 0
        - 上邊界: y <= max_y
        """
        return x < 0 or x > self.max_x or y < 0 or y > self.max_y

    def process_robot(self, start_x, start_y, start_direction, instructions):
        """
        處理單個機器人的完整移動過程。

        參數:
        start_x (int): 機器人初始 x 坐標
        start_y (int): 機器人初始 y 坐標
        start_direction (str): 機器人初始面向方向
        instructions (str): 指令序列字串，由 'L'、'R'、'F' 組成

        返回:
        tuple: (final_x, final_y, final_direction, is_lost)
               final_x, final_y: 最終坐標
               final_direction: 最終方向
               is_lost: 是否掉落 (bool)

        處理邏輯：
        1. 依序執行每個指令
        2. L/R: 改變方向
        3. F: 計算新坐標，如果超出邊界則檢查標記
        4. 如果有標記則忽略指令，否則掉落並留下標記
        """
        # 初始化機器人狀態
        x, y, direction = start_x, start_y, start_direction
        lost = False  # 標記是否掉落

        # 依序處理每個指令
        for instruction in instructions:
            if instruction == 'L':
                # 左轉 90 度
                direction = self.turn_left(direction)
            elif instruction == 'R':
                # 右轉 90 度
                direction = self.turn_right(direction)
            elif instruction == 'F':
                # 前進指令：計算新坐標
                new_x, new_y = self.move_forward(x, y, direction)

                if self.is_out_of_bounds(new_x, new_y):
                    # 新坐標超出邊界
                    if (x, y) not in self.scent:
                        # 當前位置沒有標記，機器人掉落
                        self.scent.add((x, y))  # 留下標記
                        lost = True  # 標記為掉落狀態
                        break  # 停止處理後續指令
                    # 如果有標記，忽略此指令，繼續下一指令
                else:
                    # 新坐標在邊界內，更新位置
                    x, y = new_x, new_y

        # 返回最終狀態
        return x, y, direction, lost

def main():
    """
    主程式：讀取輸入資料並處理所有機器人。

    輸入處理流程：
    1. 第一行：讀取網格大小 max_x, max_y
    2. 後續每兩行：一個機器人的資料
       - 第一行：x y direction
       - 第二行：instructions
    3. 對每個機器人呼叫 process_robot 處理
    4. 輸出最終狀態

    輸入結束條件：讀取到 EOF (檔案結尾)
    """
    # 讀取所有輸入行
    input_lines = sys.stdin.readlines()

    # 如果沒有輸入，直接返回
    if not input_lines:
        return

    # 第一行：網格大小
    max_x, max_y = map(int, input_lines[0].split())
    # 建立模擬器實例
    simulator = RobotSimulator(max_x, max_y)

    # 處理剩下的行，每兩個行為一組機器人資料
    i = 1  # 從第二行開始
    while i < len(input_lines):
        # 第一行：位置和方向
        position_line = input_lines[i].strip()
        if not position_line:  # 跳過空行
            i += 1
            continue

        # 解析位置和方向：x y direction
        x, y, direction = position_line.split()
        x, y = int(x), int(y)  # 轉換為整數

        # 第二行：指令序列
        i += 1
        if i >= len(input_lines):  # 防止超出範圍
            break
        instructions = input_lines[i].strip()

        # 處理這個機器人的移動
        final_x, final_y, final_direction, is_lost = simulator.process_robot(
            x, y, direction, instructions
        )

        # 準備輸出結果
        output = f"{final_x} {final_y} {final_direction}"
        if is_lost:
            output += " LOST"  # 如果掉落，加上 LOST 標記

        # 輸出結果
        print(output)

        # 移到下一組機器人資料
        i += 1

# 程式進入點
if __name__ == '__main__':
    main()