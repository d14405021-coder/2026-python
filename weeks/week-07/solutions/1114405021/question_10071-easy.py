# question_10071-easy.py
# 說明：UVA 10071 / ZeroJudge a064 (a+b+c+d+e=f) 解答「簡化好記版」
# 針對考試時，不想要處理陣列索引跟平移值(Offset)的寫法。
# 我們可以直接使用 Python 強大的 collections.Counter 模組，
# 把「左邊 a+b+c」的所有可能結果當成 Dictionary 存起來！
# 雖然字典操作比陣列稍微慢一點，但由於 N=100 的 3 次方只有 100 萬，
# 在 Python 中這個效能還是非常可以接受的，而且代碼會變得超級簡單。

import sys
from collections import Counter


def solve():
    # 1. 讀取所有資料
    data = sys.stdin.read().split()
    if not data:
        return

    idx = 0
    # 處理所有的測資 (可能有好幾筆)
    while idx < len(data):
        n = int(data[idx])
        idx += 1

        # 2. 將 S 的 N 個元素抓進陣列中
        S = [int(x) for x in data[idx : idx + n]]

        # 3. 核心邏輯：將 a+b+c+d+e=f 改寫為 a+b+c = f-d-e (相向搜尋法)
        # 用 Counter 來計算「左半邊」 (a + b + c) 的所有可能結果出現了幾次
        # 這樣寫比三層 for 迴圈更加簡潔易讀
        left_counts = Counter(a + b + c for a in S for b in S for c in S)

        # 4. 對於「右半邊」 (f - d - e)，去剛才算好的左半邊表裡面找
        # 找到了就加起來 (如果找不到會回傳 0)
        ans = sum(left_counts[f - d - e] for f in S for d in S for e in S)

        # 5. 輸出答案
        print(ans)

        # 更新指標
        idx += n


if __name__ == "__main__":
    solve()
