# 9 比較、排序與 key 函式

你必須已經「不需要解釋」就能看懂：

```python
a < b
```

```python
sorted(data, key=lambda x: x.price)
min(data, key=itemgetter('uid'))
```

用途（對應第一章範例）：

- tuple 比較順序
- 為何 `(priority, index, item)` 可排序
- Top-N
- dict / object 排序
- groupby 前置排序

---

## 9.1 比較運算的核心觀念

在 Python 中，`a < b` 的本質是「比較規則是否已定義」。

- 數字、字串、tuple 都有內建比較規則。
- 自訂物件若沒定義比較邏輯，直接用 `<` 可能出錯。

範例：

```python
print(3 < 7)          # True，數字大小比較
print("apple" < "bee") # True，字典序比較
```

---

## 9.2 tuple 為什麼可以直接排序

tuple 採用「逐欄位（lexicographic）」比較：

1. 先比第 1 個元素
2. 若相同，再比第 2 個元素
3. 依此類推

範例（含詳細中文註解）：

```python
rows = [
	(2, 10, "B"),
	(1, 30, "C"),
	(1, 20, "A"),
]

# sorted 會先比第 1 欄（1, 2）
# 若第 1 欄一樣（例如都是 1），再比第 2 欄（20, 30）
# 所以結果會先 (1, 20, "A")，再 (1, 30, "C")，最後 (2, 10, "B")
result = sorted(rows)

print(result)
```

這也是 `(priority, index, item)` 常被拿來做優先佇列排序的原因：

- 先按 `priority` 排優先度
- 同優先度再按 `index` 保持插入順序
- `item` 只是攜帶資料（通常不會走到比 `item`）

---

## 9.3 sorted 與 list.sort 的差異

- `sorted(iterable, key=...)`：回傳新清單，不改原資料。
- `list.sort(key=...)`：就地排序，直接改原清單。

範例：

```python
nums = [5, 2, 9, 1]

# 不改原 nums，建立新排序結果
new_nums = sorted(nums)

print(nums)     # [5, 2, 9, 1]
print(new_nums) # [1, 2, 5, 9]

# 直接修改 nums 本身
nums.sort(reverse=True)
print(nums)     # [9, 5, 2, 1]
```

---

## 9.4 key 函式：排序前先抽出比較依據

`key` 的工作是：

- 對每個元素計算一個「可比較的鍵值」
- Python 依鍵值排序，而不是直接比原物件

### 9.4.1 物件排序（lambda）

```python
class Product:
	def __init__(self, name, price):
		self.name = name
		self.price = price

items = [
	Product("pen", 35),
	Product("book", 120),
	Product("eraser", 20),
]

# 用 price 當排序依據（由小到大）
by_price = sorted(items, key=lambda x: x.price)

for p in by_price:
	print(p.name, p.price)
```

### 9.4.2 字典資料排序（itemgetter）

```python
from operator import itemgetter

users = [
	{"uid": 1003, "name": "Amy"},
	{"uid": 1001, "name": "Bob"},
	{"uid": 1002, "name": "Cindy"},
]

# 依 uid 由小到大排序
ordered = sorted(users, key=itemgetter("uid"))

print(ordered)
```

---

## 9.5 Top-N：只拿前 N 筆最大或最小

當資料很大時，比起整包排序再切片，更常使用 `heapq.nlargest` / `nsmallest`。

```python
import heapq

scores = [88, 95, 76, 100, 91, 84]

# 取前 3 名最高分
top3 = heapq.nlargest(3, scores)

# 取最低 2 分
low2 = heapq.nsmallest(2, scores)

print(top3)  # [100, 95, 91]
print(low2)  # [76, 84]
```

若是物件或字典，也可搭配 `key`：

```python
import heapq

players = [
	{"name": "A", "score": 70},
	{"name": "B", "score": 95},
	{"name": "C", "score": 88},
]

# 依 score 取最高 2 人
top2 = heapq.nlargest(2, players, key=lambda x: x["score"])
print(top2)
```

---

## 9.6 groupby 的前置條件：先排序

`itertools.groupby` 只會把「連續相同 key」分成一組，
所以在 groupby 前通常必須先用同一個 key 排序。

```python
from itertools import groupby
from operator import itemgetter

rows = [
	{"dept": "A", "name": "Amy"},
	{"dept": "B", "name": "Bob"},
	{"dept": "A", "name": "Alex"},
]

# 先依 dept 排序，讓同部門資料靠在一起
rows_sorted = sorted(rows, key=itemgetter("dept"))

# 再 groupby 才會得到正確群組
for dept, group in groupby(rows_sorted, key=itemgetter("dept")):
	members = [x["name"] for x in group]
	print(dept, members)
```

---

## 9.7 常見錯誤與提醒

1. 忘記 `groupby` 前要先排序，導致同類資料被拆成多段。
2. 對自訂物件直接排序但沒提供 `key`，可能噴 `TypeError`。
3. 想拿 Top-N 卻先全排序，對大資料效能較差。

---

## 9.8 快速總結

- tuple 天生可比較，適合多欄位排序。
- `key` 是排序最重要的技巧，能把複雜物件轉成可比鍵值。
- Top-N 用 `heapq` 通常更有效率。
- `groupby` 前先排序，是避免邏輯錯誤的關鍵步驟。
