# R3. deque 保留最後 N 筆（1.3）

from collections import deque

# deque（double-ended queue）是「雙端佇列」：
# - 左右兩端都能快速新增/刪除
# - 很適合做固定長度歷史紀錄、滑動視窗、最近 N 筆資料

# 1) 設定 maxlen=3：最多只保留 3 筆
q = deque(maxlen=3)
# 初始：[]
q.append(1); q.append(2); q.append(3)
# 現在：deque([1, 2, 3], maxlen=3)

q.append(4)  # 自動丟掉最舊的 1
# 原因：已達上限 3，再 append 新值時，會從另一端自動淘汰最舊資料
# 結果：deque([2, 3, 4], maxlen=3)

# 2) 不設 maxlen：可無限制成長（除非記憶體不足）
q = deque()

# append(x)：加到右端
# appendleft(x)：加到左端
q.append(1); q.appendleft(2)
# 此時內容：deque([2, 1])

# pop()：從右端移除並回傳
# popleft()：從左端移除並回傳
q.pop(); q.popleft()
# 上行結束後，deque 會變回空的：deque([])

# 閱讀這類程式的技巧：
# 1) 每做一個操作就手動畫一次狀態（例如 [2, 3, 4]）
# 2) 特別注意「左端」與「右端」是不同方向
# 3) 若有 maxlen，看到新增就要同時思考「誰會被淘汰」
