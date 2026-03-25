# question_10055.py
# 說明：UVA 10055 (ZeroJudge a048) 單調函數的增減性 解答
# 注意：雖然題號標示 UVA 10055，但根據題目敘述與連結，這其實是一道利用「樹狀數組 (Fenwick Tree / BIT)」
# 或「線段樹」來解決的區間查詢與單點修改問題 (更像是 ZJ a048)。
#
# 解題思路：
# 1. 複合函數的增減性規則與「正負號相乘」完全相同：
#    - 增函數(0) 代入 增函數(0) -> 增函數(0)  (同號得正：+ * + = +)
#    - 減函數(1) 代入 增函數(0) -> 減函數(1)  (異號得負：- * + = -)
#    - 減函數(1) 代入 減函數(1) -> 增函數(0)  (負負得正：- * - = +)
# 2. 也就是說，區間 [L, R] 的複合函數，其實就是看這段區間內「減函數(1)」的數量。
#    - 若有「偶數」個減函數，結果是增函數 (輸出 0)。
#    - 若有「奇數」個減函數，結果是減函數 (輸出 1)。
# 3. 操作 1：反轉 f_i 的增減性。
# 4. 操作 2：查詢區間 [L, R] 的增減性總和，判斷奇偶性。
# 5. 因為 N, Q 高達 200,000，使用普通的陣列去算會超時 (O(N*Q))。
#    必須使用樹狀數組 (Binary Indexed Tree, BIT) 來將單點修改與區間查詢的時間複雜度降為 O(log N)。

import sys


class FenwickTree:
    def __init__(self, size):
        # 建立大小為 size + 1 的陣列，索引從 1 開始
        self.tree = [0] * (size + 1)
        self.size = size

    def add(self, i, delta):
        # 單點修改：將第 i 個位置加上 delta
        while i <= self.size:
            self.tree[i] += delta
            # i & (-i) 用來取得 i 的二進位中最右邊的 1 (lowbit)
            i += i & (-i)

    def query(self, i):
        # 前綴和查詢：計算 1 到 i 的總和
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & (-i)
        return s

    def query_range(self, l, r):
        # 區間和查詢：計算 L 到 R 的總和
        return self.query(r) - self.query(l - 1)


def solve():
    # 讀取所有輸入
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    idx = 0
    # 本題可能有多組測試資料，使用 while 迴圈處理到 EOF
    while idx < len(input_data):
        n = int(input_data[idx])
        q = int(input_data[idx + 1])
        idx += 2

        # 建立樹狀數組 (BIT)，初始全為增函數 (值為 0)，所以不用特別初始化塞值
        bit = FenwickTree(n)

        # 紀錄目前的狀態，0 代表增函數，1 代表減函數
        # 因為 BIT 存的是總和，我們需要一個陣列來知道當前位置到底是 0 還是 1
        # 才好決定反轉時是要 +1 還是 -1
        state = [0] * (n + 1)

        for _ in range(q):
            v = int(input_data[idx])

            if v == 1:
                # 操作 1：反轉 f_i
                i = int(input_data[idx + 1])
                idx += 2

                # 如果原本是 0 (增)，變成 1 (減)，則要 +1
                # 如果原本是 1 (減)，變成 0 (增)，則要 -1
                if state[i] == 0:
                    bit.add(i, 1)
                    state[i] = 1
                else:
                    bit.add(i, -1)
                    state[i] = 0

            elif v == 2:
                # 操作 2：查詢區間 [L, R]
                l = int(input_data[idx + 1])
                r = int(input_data[idx + 2])
                idx += 3

                # 取得區間內「減函數」的總數
                total_negatives = bit.query_range(l, r)

                # 判斷奇偶性：
                # 奇數個減函數 -> 減函數 -> 輸出 1
                # 偶數個減函數 -> 增函數 -> 輸出 0
                if total_negatives % 2 == 1:
                    print("1")
                else:
                    print("0")


if __name__ == "__main__":
    solve()
