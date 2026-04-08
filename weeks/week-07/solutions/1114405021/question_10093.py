import sys


def solve():
    # 讀取所有輸入
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    # 讀取 N 和 M
    n = int(input_data[0])
    m = int(input_data[1])

    if n == 0 or m == 0:
        print(0)
        return

    # 讀取地圖資訊，將平原(P)視為0，山地(H)視為1（1表示不能放置）
    # 使用二進位表示每一行的地形限制
    terrain = []
    idx = 2
    for _ in range(n):
        row_str = input_data[idx]
        idx += 1
        state = 0
        for i, char in enumerate(row_str):
            if char == "H":
                state |= 1 << i
        terrain.append(state)

    # 預處理所有合法的單行狀態
    # 合法狀態是指：該行內沒有任何兩個炮兵相鄰或間隔為1（即距離<=2）
    valid_states = []
    state_sum = []  # 記錄每個合法狀態上的炮兵數量

    # 遍歷所有可能的二進位狀態 (0 到 2^m - 1)
    for i in range(1 << m):
        # 檢查是否有距離為1或2的炮兵
        if (i & (i << 1)) == 0 and (i & (i << 2)) == 0:
            valid_states.append(i)
            # 計算該狀態有多少個 1 (炮兵數量)
            count = bin(i).count("1")
            state_sum.append(count)

    num_states = len(valid_states)

    # dp 陣列：dp[i][j][k] 表示第 i 行狀態為 j，第 i-1 行狀態為 k 時的最大炮兵數
    # 為了節省空間，我們可以使用滾動陣列，只需要記錄 i, i-1, i-2 行的關係
    # 這裡我們使用前一行的狀態(j)和當前行的狀態(k)
    # dp[j][k] 表示上一行(i-1)狀態為j，當前行(i)狀態為k的最大炮兵數

    dp = [[0] * num_states for _ in range(num_states)]

    # 初始化第 0 行
    for k in range(num_states):
        # 檢查狀態 k 是否符合第 0 行的地形限制
        if (valid_states[k] & terrain[0]) == 0:
            dp[0][k] = state_sum[k]

    if n > 1:
        # 記錄前兩行的dp狀態
        next_dp = [[0] * num_states for _ in range(num_states)]

        # 處理第 1 行
        for j in range(num_states):
            for k in range(num_states):
                # 檢查第 0 行和第 1 行的地形限制
                if (valid_states[j] & terrain[0]) == 0 and (
                    valid_states[k] & terrain[1]
                ) == 0:
                    # 檢查第 0 行和第 1 行的炮兵是否衝突 (上下相鄰)
                    if (valid_states[j] & valid_states[k]) == 0:
                        next_dp[j][k] = dp[0][j] + state_sum[k]

        dp = next_dp

        # 處理第 2 行到第 n-1 行
        for i in range(2, n):
            next_dp = [[0] * num_states for _ in range(num_states)]
            for j in range(num_states):  # i-1 行的狀態
                for k in range(num_states):  # i 行的狀態
                    # 檢查 i 行的地形限制和 i 與 i-1 行的衝突
                    if (valid_states[k] & terrain[i]) == 0 and (
                        valid_states[j] & valid_states[k]
                    ) == 0:
                        # 尋找最佳的 i-2 行狀態 (m_state)
                        max_prev = 0
                        for m_idx in range(num_states):  # i-2 行的狀態
                            # 檢查 i-2 行的地形限制（在之前的dp已經隱含檢查過），
                            # 這裡只需檢查 i-2 行與 i 行、i-1 行的衝突
                            if (valid_states[m_idx] & valid_states[j]) == 0 and (
                                valid_states[m_idx] & valid_states[k]
                            ) == 0:
                                if dp[m_idx][j] > max_prev:
                                    max_prev = dp[m_idx][j]

                        next_dp[j][k] = max_prev + state_sum[k]
            dp = next_dp

    # 找出最後一行的最大值
    max_artillery = 0
    for j in range(num_states):
        for k in range(num_states):
            if dp[j][k] > max_artillery:
                max_artillery = dp[j][k]

    print(max_artillery)


if __name__ == "__main__":
    solve()
