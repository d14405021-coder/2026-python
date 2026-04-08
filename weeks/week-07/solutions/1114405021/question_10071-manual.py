# question_10071-manual.py
# 說明：UVA 10071 / ZeroJudge a064 的「手打基礎版 (Manual)」解答
# 針對不熟悉 sys.stdin.read().split() 或 collections.Counter 的初學者設計。
# 使用最傳統的 input() 來抓資料，並配合一維陣列平移法(Offset)來找答案。
# 此版本因為不用高階工具，在邏輯上最「原汁原味」。


def solve():
    try:
        # 有好幾筆測試資料，所以要一直循環到讀不到資料 (EOFError)
        while True:
            # 讀取這筆測資的 N (集合 S 的元素個數)
            line = input().strip()
            if not line:
                continue

            n = int(line)

            # 將集合 S 中的元素讀進來
            s = []
            for _ in range(n):
                element = int(input().strip())
                s.append(element)

            # 我們要解的等式是 a + b + c + d + e = f
            # 移項後變成：a + b + c = f - d - e
            # 這樣左邊 3 個變數、右邊 3 個變數，時間複雜度才不會超時

            # 因為最大值是 30000，三個數字加起來最多 90000，最少 -90000
            # 陣列沒有「負數索引」這個概念 (Python的負數索引是從尾巴算，會導致邏輯錯亂)
            # 所以我們統一加上 90000 當作「平移量」
            offset = 90000

            # 建立一個長度 180005 的陣列，預設裡面都是 0 次
            counts = [0] * 180005

            # 步驟一：處理左半邊的「所有可能值」出現次數
            for a in s:
                for b in s:
                    for c in s:
                        val = a + b + c + offset
                        counts[val] += 1

            # 步驟二：處理右半邊，看看剛才左半邊有沒有算出一樣的值
            ans = 0
            for f in s:
                for d in s:
                    for e in s:
                        val = f - d - e + offset
                        ans += counts[val]

            # 輸出最後結果
            print(ans)

    except EOFError:
        # 測資讀完時，會觸發 EOFError，我們就安靜地結束程式
        pass


if __name__ == "__main__":
    solve()
