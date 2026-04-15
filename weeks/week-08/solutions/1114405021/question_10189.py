# 題目：UVA 10189 (Minesweeper)
# 說明：標準解法。讀取整個輸入，然後對每個無地雷的格子計算其周圍八個方向的地雷總數。
# 注意：輸出時，兩組測試資料之間必須有一個空行。

import sys

def solve():
    # 一次讀取所有輸入資料
    input_data = sys.stdin.read().split()
    if not input_data:
        return
        
    idx = 0
    field_num = 1
    
    # 只要還能讀到 n 和 m
    while idx < len(input_data):
        n = int(input_data[idx])
        m = int(input_data[idx+1])
        idx += 2
        
        # 當 n=0 且 m=0 時結束
        if n == 0 and m == 0:
            break
            
        # 如果不是第一組，先印一個空行
        if field_num > 1:
            print()
            
        print(f"Field #{field_num}:")
        field_num += 1
        
        # 讀取地圖網格
        grid = []
        for _ in range(n):
            grid.append(list(input_data[idx]))
            idx += 1
            
        # 定義八個方向的相對座標 (上, 下, 左, 右, 左上, 右上, 左下, 右下)
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ]
        
        # 遍歷網格的每一個格子
        for r in range(n):
            for c in range(m):
                # 如果該格子不是地雷，則計算周圍地雷數量
                if grid[r][c] == '.':
                    mine_count = 0
                    # 檢查八個方向
                    for dr, dc in directions:
                        nr = r + dr
                        nc = c + dc
                        # 確保相鄰座標在網格範圍內，且該格子是地雷
                        if 0 <= nr < n and 0 <= nc < m and grid[nr][nc] == '*':
                            mine_count += 1
                    # 將結果轉換為字串並填入格子中
                    grid[r][c] = str(mine_count)
                    
        # 印出計算好的地圖
        for r in range(n):
            print("".join(grid[r]))

if __name__ == '__main__':
    solve()
