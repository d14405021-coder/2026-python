import sys

def cycle_length(n):
    """
    計算單個數字 n 的 Collatz 序列長度。

    參數:
    n (int): 要計算的數字

    返回:
    int: 序列長度（從 n 到 1 的步數）
    """
    count = 1  # 包含起始的 n
    while n != 1:
        if n % 2 == 0:
            n = n // 2  # 偶數時除以 2
        else:
            n = 3 * n + 1  # 奇數時乘 3 加 1
        count += 1  # 每一步增加計數
    return count

# 主程式：處理輸入並計算結果
for line in sys.stdin:
    # 讀取一行輸入，解析為兩個整數 i 和 j
    i, j = map(int, line.split())

    # 確定區間的起始和結束（處理 i > j 的情況）
    start = min(i, j)
    end = max(i, j)

    # 初始化最大長度為 0
    max_cycle = 0

    # 對區間內的每個數字計算 cycle length，取最大值
    for num in range(start, end + 1):
        current_cycle = cycle_length(num)
        if current_cycle > max_cycle:
            max_cycle = current_cycle

    # 輸出結果：原始的 i j 和最大 cycle length
    print(i, j, max_cycle)