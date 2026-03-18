"""
UVA 10019（Hashmat 差值題）- 手打版

臨場快速寫法：
1. 逐行讀輸入
2. 拆出兩個數字
3. 算絕對差
4. 輸出答案
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
    
    # 算絕對差
    diff = abs(a - b)
    
    # 輸出
    print(diff)
