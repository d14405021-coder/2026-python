# 題目：UVA 10193 (ZeroJudge a186)
# 注意：Markdown 的題目描述為 Machin's formula (計算 Pi 的 arctan 公式)，
# 但 UVA 10193 實際上是 "All You Need Is Love" (判斷兩個二進位字串是否具有 >1 的公因數)。
# 若原意是指 arctan(1/a) = arctan(1/b) + arctan(1/c) 求解 b+c 的最小值，這實際上是中國 NOIP 的一題 (Machin Formula)。
# 根據等式：arctan(1/a) = arctan(1/b) + arctan(1/c) 展開可得：1/a = (1/b + 1/c) / (1 - 1/bc)
# 化簡後為：b*c - a*b - a*c = 1 => (b-a)(c-a) = a^2 + 1
# 為了讓 b+c 最小，(b-a) 與 (c-a) 必須盡可能接近。
# 因此我們尋找 (a^2+1) 的因數中，最接近 a 的因數 (也就是最接近 sqrt(a^2+1) 的因數)。
# 令 d 為 (a^2+1) 的因數，則 b-a = d, c-a = (a^2+1)/d。
# b+c = (b-a) + (c-a) + 2a = d + (a^2+1)/d + 2a。
# 當 d 越接近 (a^2+1)/d，b+c 越小。

import sys
import math

def solve():
    # 讀取輸入資料
    input_data = sys.stdin.read().split()
    if not input_data:
        return
        
    for item in input_data:
        a = int(item)
        target = a * a + 1
        
        # 尋找 target 的因數 d，使 d 盡量接近 sqrt(target)
        # 我們從 int(sqrt(target)) 開始往下找，找到的第一個因數就是最接近的
        limit = math.isqrt(target)
        
        best_d = 1
        for d in range(limit, 0, -1):
            if target % d == 0:
                best_d = d
                break
                
        # d 和 target/d 分別對應 b-a 和 c-a
        # b = a + best_d
        # c = a + target // best_d
        # 答案要求 b + c
        ans = best_d + (target // best_d) + 2 * a
        
        print(ans)

if __name__ == '__main__':
    solve()
