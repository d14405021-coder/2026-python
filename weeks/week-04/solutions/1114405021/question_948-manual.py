"""
UVA 948 - 假幣問題（手打版）

臨場快速寫法：
1. 用 token 逐個拆解輸入
2. 逐組讀 n 與 k
3. 逐筆讀秤重紀錄
4. 逐枚硬幣假設為假幣，測試偏重/偏輕相容性
5. 只剩唯一假設就輸出 coin，否則輸出 0
"""

import sys

# 把輸入全部拆成 token
raw = sys.stdin.read().split()
idx = 0

# 讀測資組數
t = int(raw[idx])
idx += 1

for _ in range(t):
    # 讀 n 與 k
    n = int(raw[idx])
    k = int(raw[idx + 1])
    idx += 2
    
    # 讀 k 次秤重紀錄
    weighings = []
    for _ in range(k):
        p = int(raw[idx])
        idx += 1
        
        left = list(map(int, raw[idx : idx + p]))
        idx += p
        
        right = list(map(int, raw[idx : idx + p]))
        idx += p
        
        result = raw[idx]
        idx += 1
        
        weighings.append((left, right, result))
    
    # 逐枚硬幣檢查是否為假幣
    candidates = []
    
    for coin in range(1, n + 1):
        # 假設 coin 偏重是否成立
        can_heavy = True
        for left, right, result in weighings:
            diff = 0
            if coin in left:
                diff += 1
            if coin in right:
                diff -= 1
            
            if result == '<' and diff >= 0:
                can_heavy = False
                break
            if result == '>' and diff <= 0:
                can_heavy = False
                break
            if result == '=' and diff != 0:
                can_heavy = False
                break
        
        # 假設 coin 偏輕是否成立
        can_light = True
        for left, right, result in weighings:
            diff = 0
            if coin in left:
                diff -= 1
            if coin in right:
                diff += 1
            
            if result == '<' and diff >= 0:
                can_light = False
                break
            if result == '>' and diff <= 0:
                can_light = False
                break
            if result == '=' and diff != 0:
                can_light = False
                break
        
        # 若任一假設成立，coin 仍是候選
        if can_heavy or can_light:
            candidates.append(coin)
    
    # 輸出結果
    if len(candidates) == 1:
        print(candidates[0])
    else:
        print(0)
    
    # 多組測資之間空一行
    if _ < t - 1:
        print()
