# AI_USAGE

## AI 使用原則檢核

- 可以使用 AI 協助拆解規格、產生雛形、建議測試案例。
- 不可直接貼上 AI 回答後不驗證就提交。

## 你必須能口頭解釋的重點

### 1) 為什麼 scent 要記錄方向

若 scent 只記錄 `(x, y)`，會把「不同方向」的危險錯誤地視為相同，導致不該被忽略的 `F` 被忽略。
因此 scent 應記錄 `(x, y, dir)`，才符合題目規則。

### 2) 為什麼 LOST 後要停止該機器人

題目把 LOST 視為終止狀態（terminal state）。
一旦掉出地圖，該機器人已不存在於可操作範圍，後續命令不應再影響它。

### 3) 你的測試如何覆蓋旋轉、越界、scent 三大重點

- 旋轉：`test_turn_left_from_north`、`test_turn_right_from_north`、`test_four_right_turns_back_to_origin_direction`
- 越界：`test_out_of_bounds_marks_lost`、`test_move_inside_boundary_stays_alive`、`test_lost_robot_stops_following_commands`
- scent：`test_first_lost_robot_leaves_scent`、`test_second_robot_ignores_dangerous_forward_with_same_scent`、`test_same_position_but_different_direction_should_not_share_scent`

## 我實際問 AI 的問題（3~5 題）

1. `scent` 應該記錄 `(x, y)` 還是 `(x, y, dir)`？兩者在規則上差異是什麼？
2. 如何把 `robot_core.py` 與 `robot_game.py` 拆開，讓規則可單元測試、畫面層可重用？
3. `unittest` 最低測試清單要怎麼設計，才能完整覆蓋旋轉、越界、scent 三大面向？
4. pygame MVP 的回放需求，如果先不輸出 GIF，有沒有可接受的替代方案？

## 我採用的建議與原因

- 採用：`scent` 用 `set[tuple[int, int, str]]`。
	- 原因：查詢與去重效率高，且能正確區分同座標不同方向。
- 採用：核心邏輯獨立在 `robot_core.py`，pygame 只做輸入與渲染。
	- 原因：更容易做 TDD，測試不需要依賴圖形介面。
- 採用：先做 Red -> Green -> Refactor 並把執行結果寫進 `TEST_LOG.md`。
	- 原因：可追蹤開發過程，也符合課程要求。
- 採用：在 pygame 以 `G` 觸發逐步回放（Replay Mode）。
	- 原因：先滿足「可重播」功能，再視時間加做 GIF 匯出。

## 我拒絕的建議與原因

- 拒絕：把 `scent` 簡化成只存 `(x, y)`。
	- 原因：會錯誤忽略不同方向的危險前進，與題目規則不一致。
- 拒絕：把遊戲流程、規則判斷、資料結構都寫在 `robot_game.py`。
	- 原因：耦合過高，單元測試與後續重構困難。
- 拒絕：只提供手動截圖，不做任何回放能力。
	- 原因：未滿足作業「可重播 play 過程」的要求。

## 一個 AI 建議不完整、我自行修正的案例

- 不完整建議：AI 一開始只建議把方向驗證寫成 `if direction not in DIRECTIONS: raise ValueError`，但沒處理小寫輸入（如 `n`）。
- 我的修正：新增方向正規化流程（先 `upper()` 再驗證），並在測試加入 `test_turn_left_accepts_lowercase_direction`。
- 修正後效果：先出現 Red（失敗），修正後 Green（全通過），再 Refactor 抽出 `normalize_direction()` 保持行為一致。
