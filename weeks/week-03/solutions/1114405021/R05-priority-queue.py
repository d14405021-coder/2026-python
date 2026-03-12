# R5. 優先佇列 PriorityQueue（1.5）

import heapq

class PriorityQueue:
    def __init__(self):
        # _queue：實際存放資料的最小堆（min-heap）
        # 每個元素會存成 tuple：(-priority, index, item)
        self._queue = []

        # _index：遞增序號，用來解決「priority 相同」時的比較問題
        # 也能保留「先進先出」的穩定性（同優先級時，先 push 的先 pop）
        self._index = 0

    def push(self, item, priority):
        # heapq 是最小堆：數值越小，越先被 pop。
        # 但我們通常希望「priority 越大越先出」，所以改存 -priority。
        # 例：priority=10 會變 -10，比 -5 更小，因此會更早被取出。
        #
        # tuple 比較規則：先比第 1 格，再比第 2 格...
        # 1) 先比 -priority（決定主要優先順序）
        # 2) priority 相同時再比 _index（確保穩定順序）
        # 3) item 放最後，通常不參與比較
        heapq.heappush(self._queue, (-priority, self._index, item))

        # 每次 push 後遞增，確保每個元素都有唯一序號
        self._index += 1

    def pop(self):
        # heappop 會取出目前 tuple 最小者，也就是「原始 priority 最大」者
        # 回傳 tuple 的最後一格 item，對外隱藏內部排序細節
        return heapq.heappop(self._queue)[-1]

# 閱讀這段程式的重點：
# 1) 看懂資料是如何編碼進堆：(-priority, index, item)
# 2) 把「最小堆」轉念成「最大優先先出」：靠負號技巧
# 3) index 不只是計數器，還是同優先級的 tie-breaker（平手判定）
