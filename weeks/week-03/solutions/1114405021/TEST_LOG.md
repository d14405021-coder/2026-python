# TEST_LOG

> 本檔案請保留至少 1 次 Red 與 1 次 Green 紀錄。

## Run 1 - Red

- 時間：2026-03-12
- 指令：

```bash
C:/Users/USER/.local/bin/python3.14.exe -m unittest discover -s tests -p "test_*.py" -v
```

- 結果摘要：
  - 總數：11
  - 通過：10
  - 失敗：1（ERROR）
- 失敗原因：`test_turn_left_accepts_lowercase_direction` 觸發 `ValueError: Invalid direction: n`。
- 修正策略（1~2 句）：先在 `turn_left` / `turn_right` / `next_position` 加入方向大寫正規化，讓小寫方向可被接受。

## Run 2 - Green

- 時間：2026-03-12
- 指令：

```bash
C:/Users/USER/.local/bin/python3.14.exe -m unittest discover -s tests -p "test_*.py" -v
```

- 結果摘要：
  - 總數：11
  - 通過：11
  - 失敗：0
- 從失敗到通過做了哪些修改（1~2 句）：新增最小可行修正後，`test_turn_left_accepts_lowercase_direction` 由錯誤轉為通過，其餘測試維持綠燈。

## Run 3 - Refactor 後回歸（建議）

- 時間：2026-03-12
- 指令：

```bash
C:/Users/USER/.local/bin/python3.14.exe -m unittest discover -s tests -p "test_*.py" -v
```

- 結果摘要：
  - 總數：11
  - 通過：11
  - 失敗：0
- 重構內容：抽出 `normalize_direction()`，統一方向正規化與驗證流程，移除重複程式碼，測試結果維持全綠。
