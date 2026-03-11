"""
手動輸入版 - UVA 118 機器人問題簡易版本

這個檔案是在沒有 AI 幫助下手動鍵入的簡單版本，
邏輯與 solution_118-easy.py 相同，但特別標記為手寫。
所有註解也使用繁體中文，方便閱讀。
"""

import sys

# 定義轉向與移動規則
left_turn = {
    'N': 'W',
    'W': 'S',
    'S': 'E',
    'E': 'N'
}
right_turn = {
    'N': 'E',
    'E': 'S',
    'S': 'W',
    'W': 'N'
}
move = {
    'N': (0, 1),
    'S': (0, -1),
    'E': (1, 0),
    'W': (-1, 0)
}


def process_robot(x, y, direction, instructions, max_x, max_y, scent):
    """模擬機器人按指令移動

    參數同簡易版註解。
    """
    lost = False
    for cmd in instructions:
        if cmd == 'L':
            direction = left_turn[direction]
        elif cmd == 'R':
            direction = right_turn[direction]
        elif cmd == 'F':
            dx, dy = move[direction]
            new_x, new_y = x + dx, y + dy
            if new_x < 0 or new_x > max_x or new_y < 0 or new_y > max_y:
                if (x, y) not in scent:
                    scent.add((x, y))
                    lost = True
                    break
            else:
                x, y = new_x, new_y
    return x, y, direction, lost


# 主程式，與簡易版一致
# 將邏輯放在 '__main__' 保護區塊
if __name__ == '__main__':
    input_lines = sys.stdin.readlines()
    if input_lines:
        max_x, max_y = map(int, input_lines[0].split())
        scent = set()
        i = 1
        while i < len(input_lines):
            pos_line = input_lines[i].strip()
            if not pos_line:
                i += 1
                continue
            x, y, direction = pos_line.split()
            x, y = int(x), int(y)
            i += 1
            if i >= len(input_lines):
                break
            instructions = input_lines[i].strip()
            x, y, direction, lost = process_robot(
                x, y, direction, instructions,
                max_x, max_y, scent)
            print(x, y, direction, "LOST" if lost else "")
            i += 1
