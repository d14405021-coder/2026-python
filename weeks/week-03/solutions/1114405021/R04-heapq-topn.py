# R4. heapq 取 Top-N（1.4）

import heapq

# 1) 在一般數字序列中找最大/最小的前 N 筆
nums = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]
# nlargest(n, iterable)：回傳「最大」的 n 個元素（由大到小）
# 注意：這不會修改原本 nums，而是回傳新 list。
heapq.nlargest(3, nums)

# nsmallest(n, iterable)：回傳「最小」的 n 個元素（由小到大）
# 同樣是回傳新 list，不會就地改動 nums。
heapq.nsmallest(3, nums)

# 2) 針對複合資料（dict）取 Top-N：使用 key 指定比較欄位
portfolio = [
    {'name': 'IBM', 'shares': 100, 'price': 91.1},
    {'name': 'AAPL', 'shares': 50, 'price': 543.22},
]

# key=lambda s: s['price'] 表示「用 price 欄位當排序/比較依據」
# 這行會找出 price 最小的 1 筆（最便宜的股票資料）。
heapq.nsmallest(1, portfolio, key=lambda s: s['price'])

# 3) 轉成 heap（最小堆）並取出最小值
heap = list(nums)
# heapify 會把 list 原地轉成最小堆結構（in-place）。
# 最小堆特性：heap[0] 永遠是目前最小元素。
heapq.heapify(heap)

# heappop 會彈出並回傳最小元素，且維持 heap 的堆性質。
heapq.heappop(heap)

# 閱讀這類程式的重點流程：
# 1) 先分辨是「一次取 Top-N」（nlargest/nsmallest）還是「維持堆結構反覆取值」（heapify/heappop）
# 2) 若資料是 dict/object，先看 key 用哪個欄位比較
# 3) 注意哪些函式是「回傳新結果」(nlargest/nsmallest)，哪些是「原地改動」(heapify/heappop)
