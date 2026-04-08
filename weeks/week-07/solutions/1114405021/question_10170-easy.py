# 題目：UVA 10170 (The Hotel with Infinite Rooms) - 簡易版
# 說明：這是一個非常直觀的 while 迴圈解法。
# 當 D 的值減去每天入住的人數後還大於 0，就繼續往下算。

import sys

def solve():
    # 讀取全部資料
    lines = sys.stdin.read().split()
    if not lines:
        return
        
    for i in range(0, len(lines), 2):
        # 取得初始團體人數 S 與天數 D
        s = int(lines[i])
        d = int(lines[i+1])
        
        # 只要剩餘天數 D > 0，就代表還沒遇到那一天的旅行團
        while d > 0:
            # 減掉這批人住的天數 (也就是這批人的人數 S)
            d -= s
            
            # 如果 D <= 0，代表第 D 天就是這批人，不需要再加 1 了
            if d <= 0:
                print(s)
                break
                
            # 如果 D 還是大於 0，代表還沒到，下一批人會多 1 人
            s += 1

if __name__ == '__main__':
    solve()
