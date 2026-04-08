# question_10062-easy.py
# 說明：UVA 10062 (Lost Cows) 的「簡化好記版」解答
# 針對考試時若忘了怎麼寫 BIT (樹狀數組)，使用 Python 的 list 配合 pop()。
# 雖然 pop() 操作是 O(N)，導致總時間複雜度變成 O(N^2)，
# 在嚴格的 80,000 測資下可能會 Time Limit Exceeded，但這寫法邏輯超級簡單。

import sys


def solve():
    # 1. 讀取所有資料
    data = sys.stdin.read().split()
    if not data:
        return

    n = int(data[0])

    # 2. 建立每頭牛前面有幾頭比牠小的數字清單
    # 第一頭牛前面沒有人，固定為 0
    smaller_counts = [0]

    # 從輸入中讀取後面 N-1 個數字
    for i in range(1, n):
        smaller_counts.append(int(data[i]))

    # 3. 建立一個「目前所有可用編號」的串列 (從 1 排到 N)
    available_ids = list(range(1, n + 1))

    # 4. 準備一個陣列存放最終結果，預先放滿 0
    ans = [0] * n

    # 5. 從「最後一頭牛」開始「由後往前」推算
    for i in range(n - 1, -1, -1):
        # 牠前面有 k 個數字比牠小
        k = smaller_counts[i]

        # 由於 available_ids 已經從小排到大
        # 第 k+1 小的數字，剛好就在索引 k 的位置！
        # 直接用 pop(k) 取出並將它從清單中移除
        cow_id = available_ids.pop(k)

        # 記錄到答案陣列中
        ans[i] = cow_id

    # 6. 由前往後，逐行輸出每頭牛的正確編號
    for cow_id in ans:
        print(cow_id)


if __name__ == "__main__":
    solve()
