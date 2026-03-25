# question_10050-manual.py
# 說明：UVA 10050 Hartals 的「手打基礎版 (Manual)」解答
# 針對不熟悉 sys.stdin.read().split() 的初學者，
# 使用最傳統的 input() 一行一行讀取資料。
# 此版本的流程最接近人類閱讀題目的順序，適合初學理解。


def solve():
    try:
        # 第一行通常是測試資料的筆數 T
        line = input().strip()
        if not line:
            return

        test_cases = int(line)

        # 針對每一組測試資料進行迴圈處理
        for _ in range(test_cases):
            # 讀取天數 N
            n = int(input().strip())

            # 讀取政黨數量 P
            p = int(input().strip())

            # 建立一個空列表來存放每個政黨的罷會頻率
            hartals = []

            # 根據政黨數量 P，讀取接下來的 P 行
            for _ in range(p):
                # 每讀取一行，就轉成整數並加入列表
                h = int(input().strip())
                hartals.append(h)

            # 初始化損失的工作天數
            lost_days = 0

            # 開始模擬這 N 天
            for day in range(1, n + 1):
                # 判斷是否為假日 (星期五和星期六)
                # 第 1 天是星期日(1%7=1)，所以:
                # 星期五對應的是餘數 6 (例如第 6 天)
                # 星期六對應的是餘數 0 (例如第 7 天)
                if day % 7 == 6 or day % 7 == 0:
                    continue  # 假日不會罷會，直接跳過這天，進入下一天

                # 如果是工作天，檢查是否有政黨罷會
                # 走訪每一個政黨的頻率
                for h in hartals:
                    # 如果今天是該政黨頻率的倍數，代表今天罷會
                    if day % h == 0:
                        lost_days += 1  # 增加一天損失的工作天
                        # 重要：一天只能算損失一次，所以只要找到有政黨罷會，
                        # 就不用再檢查其他政黨了，直接 break 結束這天的檢查。
                        break

            # 輸出這組測資計算出來的損失天數
            print(lost_days)

    except EOFError:
        # 當所有資料都讀取完畢，會觸發 EOFError，程式就安全結束
        pass


# 程式進入點
if __name__ == "__main__":
    solve()
