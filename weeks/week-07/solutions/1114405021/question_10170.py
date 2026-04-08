# 題目：UVA 10170 (The Hotel with Infinite Rooms)
# 說明：使用數學公式解 (等差數列求和公式) 以達到 O(1) 的時間複雜度，
# 這樣就算 D 高達 10^15 也能瞬間算出答案。

import sys
import math

def solve():
    # 讀取所有的輸入資料
    input_data = sys.stdin.read().split()
    if not input_data:
        return
        
    # 每兩個一組 (S, D) 進行處理
    for i in range(0, len(input_data), 2):
        s = int(input_data[i])
        d = int(input_data[i+1])
        
        # 尋找滿足 k(k+1)/2 - s(s-1)/2 >= d 的最小整數 k
        # 這等價於尋找 k 使得 k(k+1) >= 2*d + s*(s-1)
        # 令 C = 2*d + s*(s-1)
        c = 2 * d + s * (s - 1)
        
        # 解一元二次不等式 k^2 + k - c >= 0
        # k = (-1 + sqrt(1 + 4*c)) / 2
        # 因為數字可能很大，我們使用 math.isqrt 來避免浮點數精確度問題
        discriminant = 1 + 4 * c
        
        # math.isqrt 取得整數平方根 (無條件捨去)
        sqrt_val = math.isqrt(discriminant)
        
        # 計算 k 的值。如果 sqrt_val 是精確的整數平方根，就不用調整
        # 由於 k 必須是無條件進位，所以我們可以這樣算：
        k = (-1 + sqrt_val) // 2
        
        # 因為 isqrt 是捨去，所以 k 有可能稍微偏小，
        # 我們往上檢查確保 k(k+1) >= c
        while k * (k + 1) < c:
            k += 1
            
        print(k)

if __name__ == '__main__':
    solve()
