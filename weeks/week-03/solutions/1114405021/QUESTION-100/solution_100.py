import sys

# 記憶化字典，用來儲存已計算過的 cycle length，避免重複計算
memo = {}

def cycle_length(n):
    """
    計算給定數字 n 的 Collatz 序列 cycle length。

    參數:
    n (int): 起始數字

    返回:
    int: cycle length（從 n 到 1 的步數，包含 n 和 1）
    """
    if n in memo:
        return memo[n]
    count = 1
    original = n
    while n != 1:
        if n in memo:
            count += memo[n] - 1
            break
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        count += 1
    memo[original] = count
    return count

# 讀取標準輸入，每行處理一對 i, j
for line in sys.stdin:
    # 解析輸入的兩個整數
    i, j = map(int, line.split())
    # 確定區間的起始和結束
    start = min(i, j)
    end = max(i, j)
    # 初始化最大 cycle length
    max_len = 0
    # 遍歷區間內的每個數字，計算其 cycle length，取最大值
    for num in range(start, end + 1):
        max_len = max(max_len, cycle_length(num))
    # 輸出結果：i j 最大 cycle length
    print(i, j, max_len)