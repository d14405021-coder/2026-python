# TEST_CASES

## 測資 1：N + L = W

- 類型：正常情況（方向旋轉）
- 輸入：`(0,0,N)`, `L`
- 預期：方向 `W`
- 實際：方向 `W`
- 結果：`PASS`
- 對應測試：`test_turn_left_from_north`

## 測資 2：N + R = E

- 類型：正常情況（方向旋轉）
- 輸入：`(0,0,N)`, `R`
- 預期：方向 `E`
- 實際：方向 `E`
- 結果：`PASS`
- 對應測試：`test_turn_right_from_north`

## 測資 3：四次 R 回原方向

- 類型：正常情況（方向循環）
- 輸入：`(0,0,N)`, `RRRR`
- 預期：方向 `N`
- 實際：方向 `N`
- 結果：`PASS`
- 對應測試：`test_four_right_turns_back_to_origin_direction`

## 測資 4：邊界往外 F 會 LOST

- 類型：邊界情況
- 輸入：`(5,3,N)`, `F`，地圖 `5x3`
- 預期：`LOST`
- 實際：`lost=True`，位置維持 `(5,3)`
- 結果：`PASS`
- 對應測試：`test_out_of_bounds_marks_lost`

## 測資 5：邊界內移動不 LOST

- 類型：邊界情況
- 輸入：`(0,0,N)`, `F`，地圖 `5x3`
- 預期：`(0,1,N)` 且 `ALIVE`
- 實際：`(0,1,N)` 且 `lost=False`
- 結果：`PASS`
- 對應測試：`test_move_inside_boundary_stays_alive`

## 測資 6：第一台越界留下 scent

- 類型：正常情況（scent 建立）
- 輸入：`(5,3,N)`, `F`
- 預期：scent 包含 `(5,3,'N')`
- 實際：scent 集合包含 `(5,3,'N')`
- 結果：`PASS`
- 對應測試：`test_first_lost_robot_leaves_scent`

## 測資 7：第二台同 (x,y,dir) 忽略危險 F

- 類型：反例（容易寫錯）
- 輸入：第一台 `(5,3,N),F`；第二台 `(5,3,N),F`
- 預期：第二台不 LOST 且停在 `(5,3,N)`
- 實際：第二台 `lost=False`，位置與方向為 `(5,3,N)`
- 結果：`PASS`
- 對應測試：`test_second_robot_ignores_dangerous_forward_with_same_scent`

## 測資 8：同格不同方向不共用 scent

- 類型：scent 方向差異情況
- 輸入：先建立 `(5,3,'N')` 的 scent，再測 `(5,3,E),F`
- 預期：第二台仍會 LOST
- 實際：第二台 `lost=True`，並新增 `(5,3,'E')` scent
- 結果：`PASS`
- 對應測試：`test_same_position_but_different_direction_should_not_share_scent`

## 測資 9：LOST 後不再執行

- 類型：LOST 後仍有後續指令的情況
- 輸入：`(5,3,N)`, `FRFRF`
- 預期：LOST 後停在掉落前狀態，不再繼續
- 實際：最終狀態 `(5,3,N)` 且 `lost=True`
- 結果：`PASS`
- 對應測試：`test_lost_robot_stops_following_commands`

## 測資 10：非法指令 X

- 類型：反例（非法輸入）
- 輸入：`(0,0,N)`, `X`
- 預期：拋出 `ValueError`
- 實際：拋出 `ValueError`
- 結果：`PASS`
- 對應測試：`test_invalid_command_raises_error`
