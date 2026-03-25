# question_10057-manual.py
# 說明：UVA 10057 A mid-summer night's dream 的「手打基礎版 (Manual)」解答
# 針對不熟悉陣列切片與系統進階讀寫的初學者設計。
# 使用傳統的 input() 搭配 EOFError 例外處理來一行一行抓取測資。


def solve():
    try:
        # 當還有測資可以讀的時候，會一直卡在這個無窮迴圈中
        while True:
            # 讀取這筆測資的資料數量 n
            line = input().strip()
            # 如果讀到空行，跳過
            if not line:
                continue

            n = int(line)

            # 使用一個空列表來存放這些數字
            nums = []

            # 跑 n 次迴圈，把接下來的 n 個數字讀進來
            for _ in range(n):
                num = int(input().strip())
                nums.append(num)

            # 1. 將所有數字從小到大排序
            nums.sort()

            # 2. 判斷數字個數是奇數還是偶數，並找中位數
            if n % 2 == 1:
                # 奇數個數字：最中間只有一個數
                # 索引是 n // 2
                mid1 = nums[n // 2]
                mid2 = nums[n // 2]
            else:
                # 偶數個數字：中間有兩個數
                # 索引分別是 (n // 2) - 1 和 (n // 2)
                mid1 = nums[(n // 2) - 1]
                mid2 = nums[n // 2]

            # 3. 計算答案
            # (1) 能產生最小距離和的「最小的 A」就是左邊的中位數 (mid1)
            ans_min_a = mid1

            # (2) 原始數字中有多少個數字能當作最小值的密碼 A
            # 只要數字落在 mid1 到 mid2 之間就算
            ans_count = 0
            for x in nums:
                if mid1 <= x <= mid2:
                    ans_count += 1

            # (3) 總共有幾種可能的密碼 A
            # 在整數的世界裡，從 mid1 到 mid2 總共有 (mid2 - mid1 + 1) 個數字
            ans_possibilities = mid2 - mid1 + 1

            # 輸出三個答案，並用空白隔開
            print(f"{ans_min_a} {ans_count} {ans_possibilities}")

    except EOFError:
        # 當所有測試資料都讀完，Python 會丟出 EOFError (End Of File)
        # 此時程式會捕捉到例外，並安全地結束迴圈，跳出程式
        pass


if __name__ == "__main__":
    solve()
