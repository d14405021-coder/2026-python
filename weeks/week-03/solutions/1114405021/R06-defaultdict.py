# R6. 多值字典 defaultdict / setdefault（1.6）

from collections import defaultdict

# 1) defaultdict(list)：每個新 key 的預設值是空 list
# 適合「一個 key 對應多筆資料（可重複、保序）」的情境。
d = defaultdict(list)

# 第一次存取 d['a'] 時，若 key 不存在，會自動建立 d['a'] = []
# 然後再執行 append。
d['a'].append(1); d['a'].append(2)
# 結果：d['a'] == [1, 2]

# 2) defaultdict(set)：每個新 key 的預設值是空 set
# 適合「一個 key 對應多筆但要去重」的情境。
d = defaultdict(set)

# set 的 add 不會重複加入相同元素。
d['a'].add(1); d['a'].add(2)
# 結果：d['a'] == {1, 2}

# 3) 一般 dict + setdefault：不使用 defaultdict 的替代寫法
d = {}

# setdefault(key, default)：
# - 若 key 存在，回傳既有值
# - 若 key 不存在，先放入 default 再回傳
# 這行等價於：
# if 'a' not in d:
#     d['a'] = []
# d['a'].append(1)
d.setdefault('a', []).append(1)

# 閱讀重點整理：
# 1) defaultdict 是「在讀取不存在 key 時自動建立預設容器」
# 2) list 與 set 的差別在於是否允許重複，以及是否保留插入順序
# 3) setdefault 適合偶爾處理預設值；大量累加情境通常 defaultdict 更直觀
