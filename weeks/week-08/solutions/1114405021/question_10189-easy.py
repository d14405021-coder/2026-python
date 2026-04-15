# 題目：UVA 10189 (Minesweeper) - 簡易版
# 說明：此版本針對初學者設計，使用 while True 搭配 input() 的方式讀取輸入，
# 這樣在迴圈和邊界條件判斷上會更直覺，不需要使用 sys 模組或計算索引。

def solve():
    field_num = 1
    
    # 持續讀取輸入直到遇到 EOFError (檔案結尾)
    while True:
        try:
            # 讀取兩個整數：n 和 m
            line = input().strip()
            if not line:
                continue
                
            n, m = map(int, line.split())
            
            # 若輸入為 0 0，則結束迴圈
            if n == 0 and m == 0:
                break
                
            # 每組測資之間必須有空行，如果是第一組就不用
            if field_num > 1:
                print()
                
            print(f"Field #{field_num}:")
            field_num += 1
            
            # 逐行讀取地雷網格，將每行的字串轉換成字元陣列
            grid = []
            for _ in range(n):
                grid.append(list(input().strip()))
                
            # 定義周圍 8 個格子的相對位移 (dx, dy)
            dx = [-1, -1, -1, 0, 0, 1, 1, 1]
            dy = [-1, 0, 1, -1, 1, -1, 0, 1]
            
            # 走訪網格的每一個格子
            for r in range(n):
                for c in range(m):
                    # 若當前格子不是地雷，就計算周圍有幾個地雷
                    if grid[r][c] == '.':
                        count = 0
                        # 檢查周遭的八個方向
                        for i in range(8):
                            nr = r + dx[i]
                            nc = c + dy[i]
                            
                            # 確認這個新座標沒有超出網格邊界
                            if 0 <= nr < n and 0 <= nc < m:
                                # 如果是地雷，地雷數量就加 1
                                if grid[nr][nc] == '*':
                                    count += 1
                        
                        # 把算好的數字轉成字串，放回格子中
                        grid[r][c] = str(count)
                        
            # 把每一行的字元合併成字串並印出
            for row in grid:
                print("".join(row))
                
        except EOFError:
            # 讀到檔案結尾時安全跳出迴圈
            break

if __name__ == '__main__':
    solve()
