"""
UVA 10038 - Jolly Jumpers（手打版）

臨場快速寫法：
1. 讀每一行
2. 拆 n 和序列
3. 算相鄰差值
4. 檢查是否覆蓋 1..n-1 且無重複
"""

import sys

# 逐行讀入直到 EOF
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    # 拆成 token 清單
    parts = line.split()
    n = int(parts[0])
    
    # 讀出 n 個數字
    seq = []
    for i in range(1, n + 1):
        seq.append(int(parts[i]))
    
    # 邊界：只有 1 個數字時自動是 Jolly
    if n <= 1:
        print("Jolly")
        continue
    
    # 算每一對相鄰差值
    reached = set()
    is_valid = True
    
    for i in range(1, n):
        d = abs(seq[i] - seq[i-1])
        
        # 差值必須在 1..n-1 之間
        if d < 1 or d >= n:
            is_valid = False
            break
        
        reached.add(d)
    
    # 檢查是否恰好涵蓋 1..n-1（n-1 個差值，各不重複）
    if is_valid and len(reached) == n - 1:
        print("Jolly")
    else:
        print("Not jolly")
