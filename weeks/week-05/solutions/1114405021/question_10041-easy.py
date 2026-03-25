# question_10041-easy.py
# 說明：UVA 10041 Vito's Family 的「簡化好記版」解答
# 針對考試或快速解題時，省略複雜的函式封裝，使用最基礎的語法完成。

import sys


def solve():
    # 1. 一次性讀取所有的輸入資料
    # sys.stdin.read().split() 會自動將所有文字（包含空白、換行）切分成單字（字串陣列）
    data = sys.stdin.read().split()
    if not data:
        return

    # 2. 略過第一個數字（因為 data[0] 是測資筆數，但我們直接看後面的資料去跳就可以了，所以用 index 追蹤）
    # test_cases = int(data[0])

    # 設定目前的讀取位置（指標），從第二個數字開始（索引值為 1）
    idx = 1

    # 使用 while 迴圈確保我們讀完所有的資料
    while idx < len(data):
        # 3. 取出這組測資的「親戚數量」
        r = int(data[idx])

        # 4. 取出後續的 r 個門牌號碼，並直接轉換成整數列表
        # data[idx+1 : idx+1+r] 意思是「從數量後面那個數字開始，往後抓 r 個數字」
        relatives = [int(x) for x in data[idx + 1 : idx + 1 + r]]

        # 5. 核心邏輯：找中位數
        # 先將陣列由小到大排序 (sort)
        relatives.sort()
        # 取最中間的那個數字當作中位數（若為偶數長度，取中間靠左的也行）
        median = relatives[len(relatives) // 2]

        # 6. 計算距離總和
        # 使用串列生成式 (List Comprehension) 搭配 sum 計算絕對值 (abs) 差的總和
        ans = sum(abs(x - median) for x in relatives)

        # 輸出結果
        print(ans)

        # 7. 更新指標，準備處理下一組測資
        # 跳過「這組的親戚數量 (1個)」加上「所有親戚的門牌 (r個)」
        idx += 1 + r


# 如果直接執行此程式，就呼叫 solve 函式
if __name__ == "__main__":
    solve()
