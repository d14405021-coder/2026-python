# 題目：UVA 10170 (The Hotel with Infinite Rooms) - 手動版
# 說明：此版本使用 while True 與 input() 進行標準輸入處理，非常適合基礎學習。

def solve():
    while True:
        try:
            # 讀取一行，如果 EOF 則結束
            line = input().strip()
            if not line:
                continue
                
            # 將輸入依據空白切割，取得 S 和 D
            parts = line.split()
            s = int(parts[0])
            d = int(parts[1])
            
            # 使用最簡單的減法：每次減掉這批人的數量，
            # 若減到零以下，就代表這個時候正是這批人住在那一天。
            while d > 0:
                d = d - s
                if d <= 0:
                    print(s)
                else:
                    s = s + 1
                    
        except EOFError:
            # 檔案讀取結束時跳出
            break

if __name__ == '__main__':
    solve()
