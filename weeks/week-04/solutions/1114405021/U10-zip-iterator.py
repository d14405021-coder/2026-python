# U10. zip 為何只能用一次（1.8）
# 說明：本程式說明 Python 中 zip() 函數的一個重要特性
# zip() 回傳的是一個「疊代器（Iterator）」，而非列表
# 疊代器的特點是「只能遍歷一次」，遍歷完後就會耗盡（Exhausted）

# 定義一個股票價格字典
prices = {"A": 2.0, "B": 1.0}

# 使用 zip() 將「值」和「鍵」打包成配對
# 語法：zip(可疊代物件1, 可疊代物件2, ...)
# 注意：zip() 回傳的是「疊代器物件」，不是列表！
z = zip(prices.values(), prices.keys())
# z 是一個 zip 物件（疊代器），此時尚未產生任何元素
# 只有當你「訪問」z 時，才會逐一產生元素

# ===== 1. 第一次使用：成功 =====

# min(z) 會遍歷整個疊代器 z，找到最小的元素
# 在遍歷的過程中，z 會逐一產生元素：(2.0, 'A'), (1.0, 'B')
# 遍歷結束後，所有元素都已被取出，z 被「消耗完」
min(z)  # OK（消耗掉疊代器）
# 結果：(1.0, 'B')
# 代價：z 已經無法再使用了

# ===== 2. 第二次使用：失敗 =====

# max(z) 會嘗試再次遍歷 z
# 但此時 z 已經是「空的疊代器」，沒有任何元素可供遍歷
# 因此 max() 會在空序列上操作，拋出 ValueError
# max(z)  # 會失敗：因為 z 已經被消耗完
#
# 錯誤訊息：ValueError: max() arg is an empty sequence
# 原因：z 是一個已耗盡的疊代器，裡面沒有任何元素

# ===== 3. 為何 zip() 只回傳疊代器 =====

# zip() 的設計是一種「懶惰評估（Lazy Evaluation）」
# 優點：
# - 節省記憶體：不需要預先產生所有元素
# - 處理大型資料時更有效率
# - 多個 zip() 可以串在一起形成資料處理管線
#
# 缺點：
# - 只能遍歷一次（疊代器的限制）
# - 若需要多次使用，必須先轉換為列表

# ===== 4. 解決方案：轉換為列表 =====

# 若需要多次使用 zip() 的結果，可以先轉換為列表
prices = {"A": 2.0, "B": 1.0}
z_list = list(zip(prices.values(), prices.keys()))
# z_list = [(2.0, 'A'), (1.0, 'B')]

# 列表可以多次遍歷，不會耗盡
min(z_list)  # (1.0, 'B')
max(z_list)  # (2.0, 'A')

# ===== 5. 其他會回傳疊代器的函數 =====

# 許多 Python 內建函數和標準庫都會回傳疊代器：
# - map(function, iterable)
# - filter(function, iterable)
# - enumerate(iterable)
# - dict.items()、dict.keys()、dict.values()（在 Python 3 中）
# - file.readlines()（已耗盡）
#
# 這些都需要注意「只能遍歷一次」的特性

# ===== 6. 實用技巧 =====

# 技巧一：使用 itertools.tee() 複製疊代器
# from itertools import tee
# z1, z2 = tee(z)  # 建立兩個獨立的疊代器副本
# min(z1)
# max(z2)  # 這樣就能用兩次了

# 技巧二：使用 list() 立即轉換（最簡單的方式）
# z = list(zip(prices.values(), prices.keys()))

# 技巧三：使用 dict.items() 時先轉換
# items = list(d.items())  # 轉換為列表，可以多次迭代
