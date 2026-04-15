# 題目：UVA 10189 (Minesweeper) - 手動版
# 說明：這個版本使用最基礎的語法，完全不依賴任何模組，純粹用 input() 和最基本的陣列操作。
# 把所有的八個方向用最基礎的雙層迴圈 (dr, dc) 展開，非常適合在考試環境中手打。

def solve():
    field_num = 1
    
    # 建立一個無窮迴圈來讀取多組測資
    while True:
        try:
            # 讀取第一行的 n 和 m
            line = input().strip()
            # 避免讀到空行
            if line == "":
                continue
                
            # 用空白切割字串並轉換為整數
            parts = line.split()
            n = int(parts[0])
            m = int(parts[1])
            
            # 如果 n 和 m 都是 0，代表輸入結束
            if n == 0 and m == 0:
                break
                
            # 讀取地圖資料
            grid = []
            for _ in range(n):
                row_str = input().strip()
                # 將字串轉換為字元的列表，這樣才能修改裡面的內容
                row_list = []
                for char in row_str:
                    row_list.append(char)
                grid.append(row_list)
                
            # 注意：第一組測資前不需要空行，第二組開始前面都要有一個空行
            if field_num > 1:
                print()
                
            print("Field #" + str(field_num) + ":")
            field_num += 1
            
            # 走訪每一個格子來計算地雷數量
            for r in range(n):
                for c in range(m):
                    # 如果該格子本來就是地雷，就跳過不處理
                    if grid[r][c] == '*':
                        continue
                        
                    # 用來計算周圍地雷的變數
                    mines_count = 0
                    
                    # 檢查周圍的 8 個方向 (列的變化值為 -1, 0, 1)
                    for dr in [-1, 0, 1]:
                        # 行的變化值為 -1, 0, 1
                        for dc in [-1, 0, 1]:
                            # 如果 dr 和 dc 都是 0，代表是格子自己，不用檢查
                            if dr == 0 and dc == 0:
                                continue
                                
                            # 計算旁邊格子的座標
                            nr = r + dr
                            nc = c + dc
                            
                            # 檢查旁邊的格子是否有超出地圖邊界
                            if nr >= 0 and nr < n and nc >= 0 and nc < m:
                                # 如果旁邊的格子是地雷，數量就加 1
                                if grid[nr][nc] == '*':
                                    mines_count += 1
                                    
                    # 將計算完的地雷數量轉換為字串，取代原本的 '.'
                    grid[r][c] = str(mines_count)
                    
            # 輸出計算完的地圖
            for r in range(n):
                # 把列表中的字元重新組合回字串
                row_result = ""
                for c in range(m):
                    row_result += grid[r][c]
                print(row_result)
                
        except EOFError:
            # 當沒有輸入可以讀取時，跳出迴圈
            break

if __name__ == '__main__':
    solve()
