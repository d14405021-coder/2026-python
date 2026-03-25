# question_10055-manual.py
# 說明：單調函數的增減性 的「手打基礎版 (Manual)」解答
# 針對不熟悉樹狀數組(BIT)與系統讀寫的初學者設計。
# 使用最傳統的 input() 搭配基本的串列(List)來記錄狀態與迴圈加總。
# 雖然遇到 N=200,000 的極大測資時會因為 O(N*Q) 導致 Time Limit Exceeded (超時)，
# 但此版本最適合用來「理解題意」與「練習基礎邏輯」。


def solve():
    try:
        # 第一行讀取 N (函數數量) 和 Q (操作次數)
        line = input().strip().split()
        if not line:
            return

        n = int(line[0])
        q = int(line[1])

        # 建立一個長度為 N+1 的陣列來代表每個函數的狀態
        # 狀態：0 代表增函數，1 代表減函數
        # 初始時全部都是增函數 (0)
        # 為了讓編號對齊 f_1 到 f_N，我們多宣告一個格子，從索引 1 開始使用
        funcs = [0] * (n + 1)

        # 執行 Q 次操作
        for _ in range(q):
            # 讀取每次操作的指令
            op = input().strip().split()
            v = int(op[0])

            if v == 1:
                # 操作 1：反轉第 i 個函數的增減性
                i = int(op[1])

                # 如果本來是增函數(0)，就變成減函數(1)
                # 如果本來是減函數(1)，就變成增函數(0)
                if funcs[i] == 0:
                    funcs[i] = 1
                else:
                    funcs[i] = 0

            elif v == 2:
                # 操作 2：查詢區間 [L, R] 複合函數的增減性
                l = int(op[1])
                r = int(op[2])

                # 計算這段區間裡面，總共有幾個「減函數(1)」
                negatives_count = 0
                for index in range(l, r + 1):
                    if funcs[index] == 1:
                        negatives_count += 1

                # 複合函數的規則：
                # 負負得正 (減函數代入減函數 = 增函數)
                # 所以只要「減函數」的數量是奇數個，結果就是減函數(1)
                # 如果是偶數個，結果就是增函數(0)
                if negatives_count % 2 == 1:
                    print("1")
                else:
                    print("0")

    except EOFError:
        # 當沒有資料可以讀取時，安全結束程式
        pass


if __name__ == "__main__":
    solve()
