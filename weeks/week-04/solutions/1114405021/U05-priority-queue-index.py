# U5. 優先佇列為何要加 index（1.5）
# 說明：本程式說明在使用 heapq 實作「優先佇列（Priority Queue）」時
# 為何需要在 priority 後面加入一個「遞增索引（index）」
# 原因：當多個元素具有相同優先級時，heapq 會嘗試比較下一個元素
# 若該元素不支援比較運算，就會發生 TypeError

import heapq

# ===== 1. 自訂 Item 類別 =====


# 定義一個簡單的 Item 類別，用來表示佇列中的項目
class Item:
    def __init__(self, name):
        self.name = name

    # 這個類別沒有定義任何比較方法（如 __lt__、__gt__ 等）
    # 因此無法使用 <、> 等比較運算子进行比较


# ===== 2. 問題：相同優先級導致比較失敗 =====

# 建立優先佇列
pq = []

# 若只放 (priority, item) 的格式
# heapq 會將 tuple 中的元素依序作為比較依據
# 當 priority相同時，會嘗試比較第二個元素（item）
# 但 Item 類別沒有定義比較方法，會導致 TypeError

# 錯誤寫法（已註解）：
# heapq.heappush(pq, (-1, Item('a')))
# heapq.heappush(pq, (-1, Item('b')))  # TypeError
#
# 錯誤原因：
# - 第一個元素的 priority 都是 -1（相同）
# - Python 嘗試比較第二個元素：Item('a') < Item('b')
# - Item 類別沒有實作 __lt__ 方法，無法比較
# - 抛出 TypeError: '<' not supported between instances of 'Item'

# ===== 3. 解決方案：加入遞增索引 =====

# 正解：加 index 避免比較 item
# 方法：在 tuple 中加入第三個元素作為「比較基準」
# 這個索引會隨著每次 push 而遞增，確保每個元素的索引都不同
# 當 priority 相同時，會比較 index，而 index 是整數，必定可以比較

idx = 0  # 初始化索引計數器

# 將 Item('a') 以 priority=-1 加入佇列
heapq.heappush(pq, (-1, idx, Item("a")))
idx += 1
# tuple 結構：(-1, 0, Item('a'))
# - 第一個元素 -1：優先級（越小越優先，因為是 min-heap）
# - 第二個元素 0：索引（用於區分相同優先級的元素）
# - 第三個元素：實際的資料

# 將 Item('b') 以相同的 priority=-1 加入佇列
heapq.heappush(pq, (-1, idx, Item("b")))
idx += 1
# tuple 結構：(-1, 1, Item('b'))
# - 第一個元素 -1：優先級相同
# - 第二個元素 1：索引不同（0 與 1）
# - 當比較時，會依序比較 (-1,0) vs (-1,1)，0 < 1，所以第一個先出隊

# ===== 4. 為何使用遞增索引 =====

# 索引的特點：
# - 永不重複：每 push 一次就 +1，確保唯一性
# - 必定可比較：整數型別支援所有比較運算
# - 保持 FIFO 順序：先加入的元素索引較小，會先出隊

# 這樣就能確保：
# - 即使 priority 相同，也不會嘗試比較 Item 物件
# - 元素的加入順序會被正確保留

# ===== 5. 取出元素 =====

# 使用 heappop() 取出最高優先級的元素
# item = heapq.heappop(pq)
# 結果會是 (-1, 0, Item('a'))，索引 0 的先出隊
# 若要取出原始的 Item：item[2].name → 'a'
