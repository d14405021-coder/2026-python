# 10 模組、類別、例外與 Big-O（最低門檻）

## import 基礎

你必須已經「不需要解釋」就能看懂：

```python
import heapq
from collections import deque
```

用途（對應第一章範例）：

- 幾乎所有進階工具

### 詳細說明

- import 的目的：把外部模組中的功能載入到目前程式。
- 常見兩種寫法：
    - `import 模組名`：使用時要加模組前綴，較不容易撞名。
    - `from 模組 import 名稱`：語法較短，但要注意名稱衝突。

範例（含繁體中文註解）：

```python
# 載入整個 heapq 模組，使用時需寫 heapq.heappush
import heapq

# 從 collections 模組直接載入 deque 類別
from collections import deque

nums = [5, 2, 9]

# 將 list 原地轉成最小堆
heapq.heapify(nums)

# deque 適合做佇列，兩端操作都快
q = deque(["A", "B"])
q.append("C")

print(nums)  # 例如 [2, 5, 9]
print(q)     # deque(['A', 'B', 'C'])
```

常見提醒：

1. 不建議濫用 `from xxx import *`，可讀性與可維護性較差。
2. 檔名避免與標準庫同名（例如把檔案命名成 `heapq.py`），否則可能導致匯入錯誤。

---

## class 與物件（看得懂即可）

```python
class User:
    def __init__(self, user_id):
        self.user_id = user_id
```

```python
user.user_id
```

用途（對應第一章範例）：

- PriorityQueue Item
- attrgetter
- namedtuple 對照 class

### 詳細說明

- `class` 是藍圖；`object` 是依照藍圖建立的實體。
- `__init__` 是建構子：建立物件時會自動執行。
- `self` 代表「目前這個物件本身」。

範例（含繁體中文註解）：

```python
class User:
    def __init__(self, user_id, name):
        # 將外部傳入的資料存到物件屬性
        self.user_id = user_id
        self.name = name

    def intro(self):
        # 物件方法可以直接使用自己的屬性
        return f"{self.user_id}-{self.name}"

# 建立一個 User 物件
user = User(101, "Amy")

print(user.user_id)  # 101
print(user.intro())  # 101-Amy
```

與 namedtuple 的概念比較：

- namedtuple：輕量、通常偏向「資料容器」。
- class：可放更多行為（方法）、驗證邏輯、狀態控制。

---

### PriorityQueue Item 為何常用 class

當你要放進優先佇列的資料較複雜時，常見做法是：

- 用 tuple 放比較鍵（priority, index）
- 用 class 放實際資料（item）

這樣可以讓排序規則清楚，資料結構也更可讀。

---

## 例外處理（try / except）

```python
try:
    int(val)
except ValueError:
    pass
```

用途（對應第一章範例）：

- `filter(is_int, values)`

### 詳細說明

- `try`：放可能出錯的程式。
- `except`：出現指定錯誤時要執行的補救流程。
- 優點：避免整支程式因單一壞資料而中止。

範例（含繁體中文註解）：

```python
values = ["10", "x", "-3", "7.5", "42"]

def is_int(text):
    try:
        # 嘗試轉成整數，成功代表是可解析整數字串
        int(text)
        return True
    except ValueError:
        # 轉型失敗（例如 x、7.5）就回傳 False
        return False

only_int_text = [v for v in values if is_int(v)]
print(only_int_text)  # ['10', '-3', '42']
```

常見提醒：

1. 除非必要，避免用裸 `except:`，容易吃掉不該忽略的錯誤。
2. `except` 內不要只寫 `pass`，至少可記錄 log 或回傳合理預設值。

---

## 基本 Big-O 觀念（聽得懂即可）

你需要知道：

- O(1), O(N), O(log N)

用途（對應第一章範例）：

- deque vs list
- heap push/pop
- sorted vs nlargest

### 詳細說明

- O(1)：資料量變大，單次操作時間幾乎不變。
- O(N)：資料量變 2 倍，操作量大致也變 2 倍。
- O(log N)：成長很慢，常見於堆積或二元搜尋等結構。

常見操作對照：

1. `deque.appendleft()` 約 O(1)，很適合佇列前端插入。
2. `list.insert(0, x)` 約 O(N)，因為後面元素要整段搬移。
3. `heapq.heappush/heappop` 約 O(log N)。
4. `sorted(data)` 約 O(N log N)。
5. 只取前 k 大時，`heapq.nlargest(k, data)` 在 k 遠小於 N 時通常更划算。

範例（觀念示意）：

```python
from collections import deque
import heapq

data = [9, 1, 7, 3, 8, 2]

# 全排序：通常 O(N log N)
all_sorted = sorted(data, reverse=True)

# 只取前 2 大：常可避免完整排序成本
top2 = heapq.nlargest(2, data)

dq = deque()
dq.appendleft(10)  # 典型 O(1)

print(all_sorted)  # [9, 8, 7, 3, 2, 1]
print(top2)        # [9, 8]
```

---

## 本章快速總結

1. import 決定你能使用哪些工具，寫法要清楚避免撞名。
2. class 用來管理「資料 + 行為」，可讀性與擴充性都比裸資料高。
3. 例外處理是防呆關鍵，讓程式面對壞輸入仍能穩定運作。
4. Big-O 幫你在同功能下選更合理的資料結構與演算法。
