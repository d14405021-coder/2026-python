# Week 02 - Test-Oriented Development Solution

## 完成題目清單

- [x] Task 1: Sequence Clean (30 分)
- [x] Task 2: Student Ranking (35 分)
- [x] Task 3: Log Summary (35 分)

## 執行環境

- **Python 版本**: Python 3 (3.6+)
- **測試框架**: unittest (Python 內建)
- **額外套件**: None (所有代碼使用 Python 標準庫)

## 程式執行指令

### Task 1: Sequence Clean
```bash
echo "5 3 5 2 9 2 8 3 1" | python3 task1_sequence_clean.py
```

### Task 2: Student Ranking
```bash
python3 task2_student_ranking.py
# 輸入:
# 6 3
# amy 88 20
# bob 88 19
# (... 其他學生資料)
```

### Task 3: Log Summary
```bash
python3 task3_log_summary.py
# 輸入:
# 8
# alice login
# bob login
# (... 其他日誌)
```

## 測試執行指令

```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
```

## 資料結構選擇理由

### Task 1: Sequence Clean
- **去重 (dictinary tracking)**: 使用字典而非集合，因為需要保留第一次出現的順序。字典在 Python 3.7+ 保證插入順序，是最優選擇。
- **排序**: 使用內建 `sorted()` 函數，時間複雜度 O(n log n)，簡潔清晰。

### Task 2: Student Ranking
- **Multi-level sorting key**: 使用 `sorted()` 配合 lambda 函數的複合鍵 `(-score, age, name)`，可在單次遍歷中完成所有排序條件，時間複雜度 O(n log n)。

### Task 3: Log Summary
- **defaultdict**: 用於統計用戶事件數，提供自動初始化為 0 的便利。
- **Counter**: 用於統計 action 出現次數，提供 `most_common()` 方法直接取得最頻繁的動作。

## 遇到的主要錯誤與修正

### 錯誤 1: Task 2 排序邏輯錯誤
**問題**: 初始實現未正確處理多層排序優先級，導致同分學生排序混亂。
**修正**: 使用 lambda 函數配合 `-score` 確保從高到低排序，同時 `age` 和 `name` 保持升序。

## Red → Green → Refactor 摘要

### Task 1: Sequence Clean
- **Red**: 編寫測試涵蓋去重、升序、降序、提取偶數四種操作，各含3+個邊界測試案例。
- **Green**: 實現 4 個函數，分別處理去重（dictionary tracking）、排序（內建 sorted()）、提取偶數（list comprehension）。
- **Refactor**: 優化函數文檔，加入時間/空間複雜度說明，提高代碼可維護性。

### Task 2: Student Ranking
- **Red**: 設計涵蓋正常案例、邊界案例（k=1, k=n）、複雜同分排序的測試。
- **Green**: 實現 `rank_students()` 函數使用 lambda 多層排序鍵，時間複雜度 O(n log n)。
- **Refactor**: 改進函數簽名和文檔，加入使用案例 (docstring example)，提升可讀性。

### Task 3: Log Summary
- **Red**: 設計包含空輸入、單筆紀錄、複雜排序條件的完整測試套組。
- **Green**: 實現 `analyze_logs()` 使用 defaultdict 和 Counter，優雅處理用戶計數和 top action 查詢。
- **Refactor**: 簡化排序邏輯使用 `sorted()` 直接取代手寫排序，加強異常處理和文檔。

## 技術亮點

1. **TDD 完整流程**: Red → Green → Refactor 各階段嚴格執行
2. **全面的測試涵蓋**: 33 個測試涵蓋正常、邊界、反例、特殊情況
3. **Pythonic 代碼風格**: 使用 list comprehension、lambda、內建函數
4. **無額外依賴**: 完全使用 Python 標準庫 (collections, unittest)
