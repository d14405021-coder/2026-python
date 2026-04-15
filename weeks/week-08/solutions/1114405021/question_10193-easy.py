# 題目：UVA 10193 (ZeroJudge a186) - 簡易版
# 說明：此版本針對初學者，將所有的數學概念轉換為最直接的變數來運算。
# 根據等式化簡：(b-a) * (c-a) = a*a + 1
# 令 x = b-a, y = c-a，則 x*y = a*a + 1。
# 若要 b+c 最小，也就是 x+y 最小，x 和 y 的數值要盡可能靠近 (即接近 sqrt(a*a+1))。
# 我們可以直接從 x = int(sqrt(a*a+1)) 往下找，能整除的第一個數字就是最接近的因數。

import math

def solve():
    # 持續讀取輸入直到遇到 EOFError (檔案結尾)
    while True:
        try:
            line = input().strip()
            if not line:
                continue
                
            # 將字串轉換成整數 a
            a = int(line)
            
            # 要尋找因數的目標數字 target = a*a + 1
            target = a * a + 1
            
            # 找到 target 的平方根，從這裡往下找最快
            # math.isqrt 可以取得最接近的整數平方根
            limit = math.isqrt(target)
            
            # 找最接近平方根的因數 d
            best_d = 1
            for d in range(limit, 0, -1):
                if target % d == 0:
                    best_d = d
                    break
                    
            # 根據公式 x*y = target, d 就是 x，target // d 就是 y
            # 而 b = a + x, c = a + y
            # 所求 b + c = a + x + a + y = 2*a + x + y
            ans = 2 * a + best_d + (target // best_d)
            
            print(ans)
            
        except EOFError:
            # 讀到檔案結尾時跳出迴圈
            break

if __name__ == '__main__':
    solve()
