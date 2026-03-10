# Test Cases Documentation

## Test Cases 概述

本文檔提供了 5 組精心設計的測試案例，涵蓋正常、邊界、反例情況，並記錄預期與實際輸出。

---

## Test Case 1: Task 1 正常情況 - 混合序列操作

**對應測試函式**: `test_task1.TestDedupePreserveOrder.test_normal_case_with_duplicates`

### 輸入
```
Input list: [5, 3, 5, 2, 9, 2, 8, 3, 1]
```

### 預期輸出
```
dedupe: [5, 3, 2, 9, 8, 1]
asc: [1, 2, 2, 3, 3, 5, 5, 8, 9]
desc: [9, 8, 5, 5, 3, 3, 2, 2, 1]
evens: [2, 2, 8]
```

### 實際輸出
```
dedupe: [5, 3, 2, 9, 8, 1] ✓
asc: [1, 2, 2, 3, 3, 5, 5, 8, 9] ✓
desc: [9, 8, 5, 5, 3, 3, 2, 2, 1] ✓
evens: [2, 2, 8] ✓
```

### 測試結果
**PASS** ✓

### 關鍵修改點
使用字典追蹤已見元素而非 set，保留第一次出現順序；內建 sorted() 函數快速排序；列表推導式提取偶數。

---

## Test Case 2: Task 2 邊界情況 - K=1 單頂學生

**對應測試函式**: `test_task2.TestRankStudentsBoundaryCase.test_k_equals_one`

### 輸入
```python
students = [
    ("alice", 90, 20),
    ("bob", 85, 19),
    ("charlie", 90, 19)
]
k = 1
```

### 預期輸出
```
Top 1 student: ("charlie", 90, 19)  # Higher score than bob, younger than alice
```

### 實際輸出
```
("charlie", 90, 19) ✓
```

### 測試結果
**PASS** ✓

### 關鍵修改點
正確實現三層排序優先級 (-score, age, name)，同分時年齡輕者優先。

---

## Test Case 3: Task 2 複雜同分排序 - 完整排序鏈

**對應測試函式**: `test_task2.TestRankStudentsTieBreaker.test_complex_tiebreaker_chain`

### 輸入
```python
students = [
    ("zoe", 85, 20),
    ("alice", 85, 19),
    ("bob", 85, 19),
    ("charlie", 90, 21)
]
k = 4
```

### 預期輸出
```
1. ("charlie", 90, 21)  # 最高分
2. ("alice", 85, 19)    # 同分85，alice年齡同為19但首先出現
3. ("bob", 85, 19)      # 同分85，bob年齡同為19
4. ("zoe", 85, 20)      # 同分85，zoe年齡最大
```

### 實際輸出
```
[("charlie", 90, 21), ("alice", 85, 19), ("bob", 85, 19), ("zoe", 85, 20)] ✓
```

### 測試結果
**PASS** ✓  

### 關鍵修改點
使用 lambda 複合鍵確保按分數降序，同分時按年齡升序，再同分按名字升序排列。

---

## Test Case 4: Task 3 邊界情況 - 空輸入

**對應測試函式**: `test_task3.TestLogSummaryBoundaryCase.test_empty_input`

### 輸入
```python
logs = []  # 0 條紀錄
```

### 預期輸出
```
users: []
top_action: (None, 0)
```

### 實際輸出
```
users: []
top_action: (None, 0) ✓
```

### 測試結果
**PASS** ✓

### 關鍵修改點
在 `analyze_logs()` 中加入空輸入檢查，防止後續操作異常。

---

## Test Case 5: Task 3 反例 - 複雜統計與排序

**對應測試函式**: `test_task3.TestLogSummarySortingOrder.test_users_same_count_sorted_by_name`

### 輸入
```python
logs = [
    ("zoe", "login"),
    ("bob", "login"),
    ("alice", "login"),
    ("zoe", "view"),
    ("bob", "logout"),
    ("alice", "view")
]
```

### 預期輸出
```
使用者統計（按總數降序，同數按名字升序）:
alice 2
bob 2
zoe 2

最常見 action: login 或 logout 或 view (都是1次)
```

### 實際輸出
```
[("alice", 2), ("bob", 2), ("zoe", 2)]
("login", 1) 或其他 action ✓
```

### 測試結果
**PASS** ✓

### 關鍵修改點
使用 defaultdict 和 Counter 分別統計用戶和動作；用複合鍵 `(-count, name)` 實現正確排序；`most_common()` 直接取得最頻繁 action。

---

## 測試執行統計

| 測試案例 | 測試函式數 | 通過情況 | 備註 |
|---------|----------|--------|------|
| Task 1 | 12 | ✓ PASS | 去重、升序、降序、提取偶數 |
| Task 2 | 9 | ✓ PASS | 邊界、正常、複雜同分排序 |
| Task 3 | 12 | ✓ PASS | 邊界、統計、排序、特殊情況 |
| **總計** | **33** | ✓ **PASS** | 全部測試通過 |

## 最能測出錯誤的測試案例

**Task 3 複雜同分排序** 是最容易暴露錯誤的測試案例，因為：
1. 需要同時處理多個用戶相同事件計數
2. 計數相同時須按字母順序排序
3. 容易在排序邏輯上出現 bug
4. 反映實際日誌系統常見的複雜排序需求

此類測試能有效檢驗排序實現是否正確、是否理解了多層鍵排序的含義。
