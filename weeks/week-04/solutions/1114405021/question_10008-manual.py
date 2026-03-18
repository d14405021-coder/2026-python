"""
UVA 10008 - 密碼分析（手打版）

臨場快速寫法：
1. 讀 n
2. 讀 n 行，統計 A~Z 各出現幾次
3. 按「次數降冪、字母升冪」排序輸出
"""

import sys

# 讀第一行得到 n
n = int(input())

# 初始化 26 個計數器
counts = [0] * 26

# 逐行讀 n 行文字
for _ in range(n):
    line = input()
    
    # 逐字元掃描
    for ch in line:
        # 轉大寫
        ch = ch.upper()
        
        # 只數 A~Z
        if 'A' <= ch <= 'Z':
            # 轉成索引（A->0, B->1, ..., Z->25）
            idx = ord(ch) - ord('A')
            counts[idx] += 1

# 收集有出現的字母及其次數
result = []
for i in range(26):
    if counts[i] > 0:
        letter = chr(ord('A') + i)
        result.append((letter, counts[i]))

# 排序：先看次數（大到小），次數相同再看字母（小到大）
result.sort(key=lambda x: (-x[1], x[0]))

# 輸出
for letter, cnt in result:
    print(f"{letter} {cnt}")
