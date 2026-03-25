# question_10050.py
# 說明：UVA 10050 Hartals (罷會) 解答
#
# 解題思路：
# 1. 這是一個模擬問題，需要計算在 N 天內，因為政黨罷會 (hartal) 而損失的「工作天」數。
# 2. 已知第 1 天是星期日 (Sunday)，依此推算：
#    - 第 1 天 (星期日)：day % 7 == 1
#    - 第 6 天 (星期五)：day % 7 == 6 -> 假日
#    - 第 7 天 (星期六)：day % 7 == 0 -> 假日
# 3. 只要天數 (day) 不是假日 (day % 7 != 6 且 day % 7 != 0)，
#    我們就檢查是否有任何一個政黨在這天罷會 (day % h_i == 0)。
# 4. 如果有，損失的工作天數 +1，並換下一天繼續檢查 (避免同一天重複計算)。

import sys


def solve_hartals(n_days, parties):
    """
    計算 N 天內損失的工作天數
    :param n_days: 總模擬天數
    :param parties: 每個政黨的罷會間隔參數陣列
    :return: 損失的工作天數
    """
    lost_days = 0

    # 從第 1 天模擬到第 N 天
    for day in range(1, n_days + 1):
        # 如果是星期五 (餘數 6) 或 星期六 (餘數 0)，則是假日，不會有罷會
        if day % 7 == 6 or day % 7 == 0:
            continue

        # 檢查每一個政黨
        for h in parties:
            if day % h == 0:
                # 只要有一個政黨在這天罷會，這天的工作天就損失了
                lost_days += 1
                break  # 避免多個政黨同一天罷會時重複計算

    return lost_days


def main():
    # 讀取所有的標準輸入資料，並用空白字元切割成陣列
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    # 取得測試資料的組數
    num_test_cases = int(input_data[0])
    idx = 1

    # 逐一處理每一組測試資料
    for _ in range(num_test_cases):
        if idx >= len(input_data):
            break

        n_days = int(input_data[idx])  # 天數 N
        num_parties = int(input_data[idx + 1])  # 政黨數量 P

        # 讀取每個政黨的罷會頻率 h
        parties = []
        for i in range(num_parties):
            parties.append(int(input_data[idx + 2 + i]))

        # 計算並輸出結果
        print(solve_hartals(n_days, parties))

        # 更新指標，跳到下一組測資的開頭
        idx += 2 + num_parties


if __name__ == "__main__":
    main()
