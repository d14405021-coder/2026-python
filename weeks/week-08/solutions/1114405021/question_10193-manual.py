# 題目：UVA 10193 (ZeroJudge a186) - 手動版
# 說明：這個版本完全不使用 math 模組的 isqrt 函數，
# 自己寫一個用 while 迴圈尋找平方根的簡單方法，適合考試手寫記憶。

def solve():
    while True:
        try:
            line = input().strip()
            if not line:
                continue
                
            # 將字串轉換成整數 a
            a = int(line)
            
            # 要尋找因數的目標數字 target = a*a + 1
            target = a * a + 1
            
            # 自己用最簡單的方式找出不大於 sqrt(target) 的最大整數 limit
            limit = 1
            while limit * limit <= target:
                limit += 1
            limit -= 1
            
            # 從 limit 開始往下尋找因數 d
            best_d = 1
            d = limit
            while d > 0:
                if target % d == 0:
                    best_d = d
                    break
                d -= 1
                
            # 找到最接近平方根的因數 d 後，計算出 x = d, y = target // d
            # 而 b+c 就是 x+a + y+a = 2*a + x + y
            ans = 2 * a + best_d + (target // best_d)
            
            print(ans)
            
        except EOFError:
            # 讀到檔案結尾時跳出迴圈
            break

if __name__ == '__main__':
    solve()
