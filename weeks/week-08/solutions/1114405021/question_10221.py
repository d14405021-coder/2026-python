# 題目：UVA 10221 (Satellites)
# 說明：這題要求給定地球半徑 (6440公里)、衛星高度 (s)、以及夾角 (a) 的單位 (deg 或 min)，
# 計算出兩顆衛星的「弧長 (arc distance)」與「弦長 (chord distance)」。
# 注意：
# 1. 1度 = 60分 (min)。
# 2. 如果角度超過 180 度，我們必須取較小的夾角 (360 - 角度)。
# 3. 弧度 (rad) = 角度 * pi / 180
# 4. 弧長 = r * rad
# 5. 弦長 = 2 * r * sin(rad / 2)

import sys
import math

def solve():
    # 讀取全部輸入資料
    input_data = sys.stdin.read().split()
    if not input_data:
        return
        
    # 每筆測資有三個元素：s (高度), a (角度), unit (單位)
    for i in range(0, len(input_data), 3):
        # 避免輸入資料不完整導致 index out of range
        if i + 2 >= len(input_data):
            break
            
        s = float(input_data[i])
        a = float(input_data[i+1])
        unit = input_data[i+2]
        
        # 如果單位是 'min' (分)，轉換為度
        if unit == 'min':
            a = a / 60.0
            
        # 將角度限制在 360 度以內
        while a >= 360.0:
            a -= 360.0
            
        # 如果夾角超過 180 度，取較小的夾角
        if a > 180.0:
            a = 360.0 - a
            
        # 計算總半徑 r (地球半徑 6440 + 衛星高度 s)
        r = 6440.0 + s
        
        # 將角度轉為弧度 (radians)
        rad = a * math.pi / 180.0
        
        # 弧長公式：半徑 * 弧度
        arc_length = r * rad
        
        # 弦長公式：2 * 半徑 * sin(弧度 / 2)
        chord_length = 2.0 * r * math.sin(rad / 2.0)
        
        # 輸出結果，保留到小數點後 6 位
        print(f"{arc_length:.6f} {chord_length:.6f}")

if __name__ == '__main__':
    solve()
