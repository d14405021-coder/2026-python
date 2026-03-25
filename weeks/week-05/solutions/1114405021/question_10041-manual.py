# question_10041-manual.py
# 說明：UVA 10041 Vito's Family 的「手打基礎版 (Manual)」解答
# 針對不熟悉 sys.stdin.read().split() 的初學者，
# 使用最傳統的 input() 與 try...except 迴圈來手動讀取每一行資料。
# 此版本雖然程式碼稍微長一點，但邏輯最符合人類直覺。


def solve():
    try:
        # 第一行通常是測試資料的筆數
        # 使用 input() 讀取一行，並轉換成整數
        first_line = input().strip()

        # 有時候第一行可能會包含空白，所以確保我們只取數字
        if not first_line:
            return

        test_cases = int(first_line)

        # 跑 test_cases 次迴圈，處理每一筆測試資料
        for _ in range(test_cases):
            # 讀取接下來的一行字串，例如 "2 2 4"
            line_data = input().strip().split()

            # 如果這行是空的，有可能是空行，跳過繼續讀
            while not line_data:
                line_data = input().strip().split()

            # 第一個數字是親戚的數量 r
            r = int(line_data[0])

            # 後面的數字是親戚的門牌號碼
            # 將這些字串數字一一轉換為整數 (int) 放入列表
            relatives = []
            for i in range(1, r + 1):
                relatives.append(int(line_data[i]))

            # 找中位數的邏輯
            # 1. 先排序 (從小排到大)
            relatives.sort()

            # 2. 找出正中間的索引值
            mid_index = r // 2

            # 3. 取得中位數 (也就是 Vito 新家的位置)
            vito_home = relatives[mid_index]

            # 4. 手動使用 for 迴圈計算所有親戚家到 Vito 家的距離總和
            total_distance = 0
            for house in relatives:
                # abs() 函數用來取得絕對值，保證距離是正數
                distance = abs(house - vito_home)
                total_distance += distance

            # 輸出這一筆測資的最小總距離
            print(total_distance)

    except EOFError:
        # 當所有資料都讀取完畢，會觸發 EOFError (End Of File)
        # 此時程式安全結束
        pass


# 程式進入點
if __name__ == "__main__":
    solve()
