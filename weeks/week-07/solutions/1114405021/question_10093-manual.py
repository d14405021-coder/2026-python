# 題目：UVA 10093 (炮兵陣地 Artillery Troops Deployment) - 基礎版
# 說明：此版本不使用 sys.stdin.read().split() 來讀取資料，而是依賴基礎的 input() 迴圈。
# 適合給剛開始接觸 Python 或不熟悉 sys 模組的同學學習。


def solve():
    while True:
        try:
            # 讀取第一行 N 和 M，若讀到 EOF 會引發 EOFError 跳出迴圈
            line = input().strip()
            if not line:
                continue

            parts = line.split()
            n = int(parts[0])
            m = int(parts[1])

            if n == 0 or m == 0:
                print(0)
                continue

            # 讀取地圖，將山地 (H) 當作 1，平原 (P) 當作 0
            terrain = []
            for _ in range(n):
                row = input().strip()
                # 把字串轉為對應的二進位整數 (狀態壓縮)
                state = 0
                for i in range(m):
                    if row[i] == "H":
                        # 這是將第 i 個位置設為 1 的方式
                        state = state | (1 << i)
                terrain.append(state)

            # 計算該行所有可能的炮兵合法排法 (只考慮左右不互相攻擊，不考慮上下)
            valid_states = []
            state_sum = []  # 記錄每個合法狀態上的炮兵數量

            # 從 0 一路數到 2 的 m 次方減 1
            max_state = 1 << m
            for state in range(max_state):
                # 檢查是否有距離 1 或 2 的炮兵 (左移 1 位及 2 位後做 AND)
                if (state & (state << 1)) == 0 and (state & (state << 2)) == 0:
                    valid_states.append(state)
                    # 計算這個狀態有多少個 1，也就是放了幾支炮兵
                    count_ones = 0
                    temp = state
                    while temp > 0:
                        if temp % 2 == 1:
                            count_ones += 1
                        temp = temp // 2
                    state_sum.append(count_ones)

            num_states = len(valid_states)

            # dp 陣列：用來儲存狀態和最大炮兵數
            # dp[j][k] = 上一列的狀態編號是 j，這一列的狀態編號是 k 時的最大數量
            dp = []
            for _ in range(num_states):
                row_dp = [0] * num_states
                dp.append(row_dp)

            # 第 0 列的初始化
            for k in range(num_states):
                # 確保炮兵沒有放在山地上
                if (valid_states[k] & terrain[0]) == 0:
                    dp[0][k] = state_sum[k]

            if n > 1:
                # 若大於 1 列，繼續處理
                next_dp = []
                for _ in range(num_states):
                    row_dp = [0] * num_states
                    next_dp.append(row_dp)

                # 處理第 1 列
                for j in range(num_states):  # 上一列
                    for k in range(num_states):  # 這一列
                        if (valid_states[j] & terrain[0]) == 0 and (
                            valid_states[k] & terrain[1]
                        ) == 0:
                            if (
                                valid_states[j] & valid_states[k]
                            ) == 0:  # 確保上下不互相攻擊
                                next_dp[j][k] = dp[0][j] + state_sum[k]
                dp = next_dp

                # 處理第 2 列到最後一列
                for i in range(2, n):
                    next_dp = []
                    for _ in range(num_states):
                        row_dp = [0] * num_states
                        next_dp.append(row_dp)

                    for j in range(num_states):  # 第 i-1 列
                        for k in range(num_states):  # 第 i 列
                            # 第 i 列地形是否合法且 i 與 i-1 列不衝突
                            if (valid_states[k] & terrain[i]) == 0 and (
                                valid_states[j] & valid_states[k]
                            ) == 0:
                                # 尋找最好的第 i-2 列 (m_idx) 狀態
                                max_prev = 0
                                for m_idx in range(num_states):
                                    if (
                                        valid_states[m_idx] & valid_states[j]
                                    ) == 0 and (
                                        valid_states[m_idx] & valid_states[k]
                                    ) == 0:
                                        if dp[m_idx][j] > max_prev:
                                            max_prev = dp[m_idx][j]

                                next_dp[j][k] = max_prev + state_sum[k]
                    dp = next_dp

            # 尋找最後一列的所有可能性中的最大值
            ans = 0
            for j in range(num_states):
                for k in range(num_states):
                    if dp[j][k] > ans:
                        ans = dp[j][k]

            print(ans)

        except EOFError:
            # 檔案結尾結束迴圈
            break


if __name__ == "__main__":
    solve()
