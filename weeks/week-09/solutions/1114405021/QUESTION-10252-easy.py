"""
UVA 10252 - 費馬點問題 (簡化版 Easy版本)

核心思想：
1. 計算距離的平方根時，可能有浮點誤差
2. 所以我們只存整數形式的距離平方
3. 然後找出最小的整數距離和

實現方式：簡單暴力搜尋
- 遍歷可能的 (x, y) 座標範圍
- 對每個座標計算到所有點的距離和
- 找出最小值和個數
"""

import math

def solve():
    """簡單直接的費馬點解法"""
    t = int(input())
    
    for _ in range(t):
        n = int(input())
        points = []
        
        for _ in range(n):
            x, y = map(int, input().split())
            points.append((x, y))
        
        # 確定搜尋範圍（在所有點周圍加些邊距）
        all_x = [p[0] for p in points]
        all_y = [p[1] for p in points]
        
        min_x = min(all_x) - 10
        max_x = max(all_x) + 10
        min_y = min(all_y) - 10
        max_y = max(all_y) + 10
        
        best_dist = float('inf')
        count = 0
        
        # 逐個檢查每個整數座標
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                # 計算這個點到所有輸入點的距離和
                total = 0
                for px, py in points:
                    dist = math.sqrt((x - px)**2 + (y - py)**2)
                    total += dist
                
                # 更新最小值
                if total < best_dist:
                    best_dist = total
                    count = 1
                elif total == best_dist:
                    count += 1
        
        print(int(best_dist), count)

if __name__ == "__main__":
    solve()
