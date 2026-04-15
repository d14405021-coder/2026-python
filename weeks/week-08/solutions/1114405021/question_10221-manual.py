# 題目：UVA 10221 (Satellites) - 手動版
# 說明：這是一個更原始的手打版本。不依賴太高階的字串切割或快速取值。
# 完全用 while 迴圈、split 切割字串、然後一個一個變數儲存。
# 使用 format 函數處理字串，對於不熟悉 f-string 的同學更容易理解字串格式化的傳統方式。

import math

def solve():
    # 永遠重複，直到遇見 EOFError 錯誤
    while True:
        try:
            # 讀取一整行的輸入資料，並去頭尾空白
            line = input().strip()
            
            # 為了避免不小心讀到空行導致錯誤，加上判斷
            if line == "":
                continue
                
            # 用空白隔開字串，將它變成陣列
            data_parts = line.split()
            
            # 第一個元素是高度 (浮點數)
            s = float(data_parts[0])
            # 第二個元素是角度或分鐘 (浮點數)
            a = float(data_parts[1])
            # 第三個元素是單位 (字串 'deg' 或 'min')
            unit = data_parts[2]
            
            # 如果單位是 'min' (分) 就除以 60 換算成度
            if unit == 'min':
                a = a / 60.0
                
            # 把角度限制在 0 到 360 度之間
            while a >= 360.0:
                a = a - 360.0
                
            # 如果角度超過 180，走另一邊會比較近 (取 360 - a)
            if a > 180.0:
                a = 360.0 - a
                
            # 地球半徑 6440 公里加上衛星高度，就是從地心算起的總半徑 r
            r = 6440.0 + s
            
            # 將角度轉換成數學上使用的弧度 (radians)
            # 公式為：角度 * 圓周率 / 180
            rad = a * math.pi / 180.0
            
            # 根據數學公式，弧長 = 半徑 * 弧度
            arc = r * rad
            
            # 根據等腰三角形公式，弦長 = 2 * 半徑 * sin(弧度的一半)
            chord = 2.0 * r * math.sin(rad / 2.0)
            
            # 用舊版的 .format 來將小數點格式化為後 6 位，方便背誦
            # {:.6f} 意思是把這個變數轉成小數點後 6 位的浮點數
            print("{:.6f} {:.6f}".format(arc, chord))
            
        except EOFError:
            # 當遇到沒有下一行時 (EOF)，安全退出迴圈
            break

if __name__ == '__main__':
    solve()
