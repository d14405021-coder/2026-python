# 8 容器操作與推導式

你必須已經「不需要解釋」就能看懂：

```python
[x for x in data if x > 0]
{k: v for k, v in d.items()}
```

```python
(x * x for x in nums)
```

用途（對應第一章範例）：

- 過濾序列（1.16）
- 字典子集（1.17）
- `sum(...)` / `min(...)` / `join(...)`

---

## 8.1 核心觀念（先抓重點）

- **推導式（Comprehension）**：把「建立新容器」的流程壓縮成一行。
- **生成器（Generator Expression）**：不一次把資料全部存進記憶體，而是「需要時才產生下一個值」。

一句話記憶：

- 要得到 `list` / `set` / `dict` 成品，用推導式。
- 只想串流計算（例如總和、最小值、逐筆處理），優先用生成器。

---

## 8.2 List Comprehension 詳細拆解

基本語法：

```python
[表達式 for 變數 in 可迭代物件 if 條件]
```

範例（含繁體中文詳細註解）：

```python
data = [3, -2, 7, 0, -5, 10]

# 從 data 中挑出正數，並直接建立新的 list
# 讀法：對 data 每個 x 進行巡覽，如果 x > 0 就把 x 放進新清單
positives = [x for x in data if x > 0]

print(positives)  # [3, 7, 10]
```

等價的傳統寫法（方便理解推導式本質）：

```python
data = [3, -2, 7, 0, -5, 10]
positives = []

for x in data:
	 # 條件成立才 append
	 if x > 0:
		  positives.append(x)

print(positives)  # [3, 7, 10]
```

---

## 8.3 Dict Comprehension 詳細拆解

基本語法：

```python
{鍵表達式: 值表達式 for 變數 in 可迭代物件 if 條件}
```

範例（只保留分數 >= 60 的學生）：

```python
scores = {
	 "Amy": 95,
	 "Bob": 58,
	 "Cindy": 73,
	 "David": 40,
}

# 從原字典的 (name, score) 配對中，篩出及格者
passed = {name: score for name, score in scores.items() if score >= 60}

print(passed)  # {'Amy': 95, 'Cindy': 73}
```

---

## 8.4 Generator Expression 詳細拆解

基本語法：

```python
(表達式 for 變數 in 可迭代物件 if 條件)
```

重點差異：

- `[...]` 會立刻產生整包資料（list）。
- `(...)` 只建立「可迭代的產生器」，資料在迭代時才算出來。

範例（記憶體友善）：

```python
nums = [1, 2, 3, 4, 5]

# 建立生成器：此時還沒有把平方值全部存成 list
squares_gen = (x * x for x in nums)

# sum 會一個一個取值並累加
total = sum(squares_gen)

print(total)  # 55
```

搭配 `join`（常見於字串拼接）：

```python
words = ["python", "is", "fun"]

# 將每個單字轉大寫後用空白連接
result = " ".join(word.upper() for word in words)

print(result)  # PYTHON IS FUN
```

---

## 8.5 常見錯誤與提醒

1. 推導式塞太多邏輯會難讀
	- 建議：條件超過 1~2 個就改回一般 `for` 迴圈。
2. 生成器只能走一次
	- 被 `sum()` 消耗後，再次使用會是空的。
3. 只想算總和時，不一定要先做 list
	- `sum(x * x for x in nums)` 通常比 `sum([x * x for x in nums])` 更省記憶體。

---

## 8.6 快速總結

- `list comprehension`：快速建立清單。
- `dict comprehension`：快速建立或篩選字典。
- `generator expression`：適合串流計算、節省記憶體。

掌握這三種寫法後，你在 CPE 題目的資料前處理（過濾、轉換、聚合）會快很多、也更乾淨。
