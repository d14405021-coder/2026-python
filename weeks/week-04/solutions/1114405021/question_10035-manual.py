"""
UVA 10035 - Primary Arithmetic（手打版）

臨場快速寫法：
1. 逐行讀輸入
2. 拆出兩個數字
3. 從右到左逐位相加，算進位次數
4. 輸出對應句型
"""

import sys

# 直接讀 stdin 逐行處理
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    # 拆成兩個數字
    parts = line.split()
    a = int(parts[0])
    b = int(parts[1])
    
    # 從個位開始逐位相加
    carry = 0
    carry_count = 0
    
    while a > 0 or b > 0:
        # 取個位數
        da = a % 10
        db = b % 10
        
        # 加上前一位進位
        s = da + db + carry
        
        # 若結果 >= 10，產生進位
        if s >= 10:
            carry = 1
            carry_count += 1
        else:
            carry = 0
        
        # 進到下一位
        a //= 10
        b //= 10
    
    # 輸出題目要求的句型
    if carry_count == 0:
        print("No carry operation.")
    elif carry_count == 1:
        print("1 carry operation.")
    else:
        print(f"{carry_count} carry operations.")
