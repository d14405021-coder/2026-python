# question_10062-manual.py
# 說明：UVA 10062 Lost Cows (乳牛排序) 的「手打基礎版 (Manual)」解答
# 針對不熟悉 sys.stdin.read() 等進階讀寫技巧的初學者設計。
# 使用最傳統的 input() 搭配 EOFError 例外處理來一行一行抓取測資。
# 邏輯上採用最直覺的「陣列 pop」方式，適合用來「理解題意」與「練習基礎邏輯」。


def solve():
    try:
        while True:
            # 讀取第一行：乳牛的總數量 N
            line = input().strip()
            if not line:
                continue

            n = int(line)

            # 建立一個列表來記錄「每頭牛前面有幾頭比牠小」
            # 注意：第一頭牛前面沒有牛，所以題目沒給，我們手動補 0
            smaller_counts = [0]

            # 接下來有 N-1 行，讀取第 2 頭到第 N 頭牛的資料
            for _ in range(n - 1):
                count = int(input().strip())
                smaller_counts.append(count)

            # 建立一個清單，存放「目前還沒被用過的編號」
            # 初始狀態是 1 到 N 都可以用
            available_ids = []
            for i in range(1, n + 1):
                available_ids.append(i)

            # 建立一個清單來存放最終計算出的正確編號
            # 為了方便由後往前填入，我們先塞滿 0
            ans = [0] * n

            # 解題核心：從「最後一頭牛」開始「由後往前」推算
            # 因為最後一頭牛後面沒人了，牠提供的數字最準確！
            for i in range(n - 1, -1, -1):
                # 取得這頭牛前面有幾個比牠小的數字
                k = smaller_counts[i]

                # 因為 available_ids 裡面的數字是「從小到大」排好的
                # 如果前面有 k 個比牠小的，代表牠就是可用清單裡面的「第 k+1 小」的數字
                # 在 Python 列表的索引中，第 k+1 小的數字剛好就在索引 k 的位置！

                # 使用 pop(k) 把這個數字拿出來，同時也會把它從可用清單中刪除
                # 這樣下一頭牛在算的時候，就不會拿到重複的編號了
                cow_id = available_ids.pop(k)

                # 記錄到答案陣列的對應位置
                ans[i] = cow_id

            # 計算完畢，由前往後把每一頭牛的編號印出來
            for cow_id in ans:
                print(cow_id)

    except EOFError:
        # 當所有測試資料都讀完，Python 會丟出 EOFError
        # 此時程式會捕捉到例外，並安全地結束迴圈，跳出程式
        pass


if __name__ == "__main__":
    solve()
