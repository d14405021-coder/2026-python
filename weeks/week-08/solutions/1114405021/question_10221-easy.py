# 題目：UVA 10221 (Satellites) - 簡易版
# 說明：這個版本使用最基礎的 input() 與 while 迴圈逐行讀取資料。
# 這樣對於初學者來說比較好理解每一行代表一組測資的概念。
# 計算公式一樣為：
# 1. 將分鐘 (min) 轉為角度 (deg) (除以 60)
# 2. 若角度大於 180 度，取小於 180 的部分 (360 - 角度)
# 3. 將角度轉弧度 (rad = a * pi / 180)
# 4. 代入弧長 (r * rad) 與弦長 (2 * r * sin(rad / 2)) 公式

import math

def solve():
    # 使用 while True 不斷讀取輸入直到 EOFError
    while True:
        try:
            line = input().strip()
            # 如果是空行則跳過
            if not line:
                continue
                
            # 將輸入切割成三個部分
            parts = line.split()
            s = float(parts[0])     # 高度 s
            a = float(parts[1])     # 夾角 a
            unit = parts[2]         # 單位 (deg 或 min)
            
            # 將單位統一轉換成角度 (degree)
            if unit == "min":
                a = a / 60.0
                
            # 確保角度落在 0~360 之間
            while a >= 360.0:
                a -= 360.0
                
            # 如果超過 180 度，表示這不是最短距離的夾角，因此取 (360 - a)
            if a > 180.0:
                a = 360.0 - a
                
            # 半徑 r 為地球半徑(6440)加上衛星高度
            r = 6440.0 + s
            
            # 將角度轉為弧度
            rad = a * math.pi / 180.0
            
            # 計算弧長：半徑乘以弧度
            arc = r * rad
            
            # 計算弦長：由等腰三角形推導出來的公式
            chord = 2 * r * math.sin(rad / 2.0)
            
            # 使用 f-string 來限制小數點後 6 位
            print(f"{arc:.6f} {chord:.6f}")
            
        except EOFError:
            # 當無法繼續讀取時跳出迴圈
            break

if __name__ == '__main__':
    solve()
