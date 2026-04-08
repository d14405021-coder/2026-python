# 題目：UVA 10093 (炮兵陣地 Artillery Troops Deployment) - 簡易版
# 說明：此版本保留狀態壓縮 DP 的核心邏輯，但加上最詳細的中文註解，幫助在考試時快速理解與撰寫。

import sys


def solve():
    # 讀取全部輸入資料
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    # 取得網格的列數 N 與行數 M
    n = int(input_data[0])
    m = int(input_data[1])

    # 如果地圖大小為 0，則無法部署任何炮兵
    if n == 0 or m == 0:
        print(0)
        return

    # terrain 陣列用來儲存每一列的地形狀態
    # 將 'H' (山地) 轉為二進位的 1，表示該位置無法部署炮兵
    terrain = []
    idx = 2
    for _ in range(n):
        row_str = input_data[idx]
        idx += 1
        state = 0
        for i in range(m):
            if row_str[i] == "H":
                state |= 1 << i  # 將第 i 位設為 1
        terrain.append(state)

    # 找出單一列中，所有不互相攻擊的合法放置方式
    # 條件：炮兵左右攻擊範圍為 2 格，所以不能有距離 1 或 2 的炮兵
    valid_states = []
    state_sum = []  # 記錄每個合法狀態部署了幾支炮兵

    # 窮舉所有可能的二進位狀態 (0 到 2^M - 1)
    for i in range(1 << m):
        # i & (i << 1) 檢查是否有相鄰的炮兵
        # i & (i << 2) 檢查是否有間隔一格的炮兵
        if (i & (i << 1)) == 0 and (i & (i << 2)) == 0:
            valid_states.append(i)
            # bin(i).count('1') 可以快速算出狀態 i 中有幾個 1 (即炮兵數量)
            state_sum.append(bin(i).count("1"))

    num_states = len(valid_states)

    # dp[i][j][k] 代表：目前在第 i 列，上一列狀態是 j，當前列狀態是 k 時，最多的炮兵數
    # 為了節省記憶體，我們只保留前一列與當前列的狀態
    # dp[j][k] = 上一列狀態 j，當前列狀態 k 的最大炮兵數
    dp = [[0] * num_states for _ in range(num_states)]

    # --- 處理第 0 列 ---
    for k in range(num_states):
        # 狀態 k 與地形沒有衝突 (沒有部署在山地上)
        if (valid_states[k] & terrain[0]) == 0:
            dp[0][k] = state_sum[k]

    # --- 處理第 1 列 ---
    if n > 1:
        next_dp = [[0] * num_states for _ in range(num_states)]
        for j in range(num_states):  # 第 0 列的狀態
            for k in range(num_states):  # 第 1 列的狀態
                # 檢查兩列各自是否符合地形
                if (valid_states[j] & terrain[0]) == 0 and (
                    valid_states[k] & terrain[1]
                ) == 0:
                    # 檢查第 0 列與第 1 列的炮兵是否會互相攻擊 (上下相鄰)
                    if (valid_states[j] & valid_states[k]) == 0:
                        next_dp[j][k] = dp[0][j] + state_sum[k]
        dp = next_dp

        # --- 處理第 2 列到第 N-1 列 ---
        for i in range(2, n):
            next_dp = [[0] * num_states for _ in range(num_states)]
            for j in range(num_states):  # 第 i-1 列的狀態
                for k in range(num_states):  # 第 i 列的狀態
                    # 檢查第 i 列地形，且第 i 列與第 i-1 列不衝突
                    if (valid_states[k] & terrain[i]) == 0 and (
                        valid_states[j] & valid_states[k]
                    ) == 0:
                        max_prev = 0
                        # 尋找最佳的第 i-2 列狀態 (m_idx)
                        for m_idx in range(num_states):
                            # 檢查第 i-2 列與第 i-1 列不衝突，且與第 i 列不衝突
                            if (valid_states[m_idx] & valid_states[j]) == 0 and (
                                valid_states[m_idx] & valid_states[k]
                            ) == 0:
                                if dp[m_idx][j] > max_prev:
                                    max_prev = dp[m_idx][j]

                        next_dp[j][k] = max_prev + state_sum[k]
            dp = next_dp

    # 找出所有最後狀態中的最大值，即為答案
    ans = 0
    for j in range(num_states):
        for k in range(num_states):
            if dp[j][k] > ans:
                ans = dp[j][k]

    print(ans)


if __name__ == "__main__":
    solve()
