# R16. 過濾：推導式 / generator / filter / compress（1.16）
# 說明：本程式示範 Python 中常見的資料過濾技巧
# 包括：列表推導式、生成器表達式、filter 函數、以及 itertools.compress

# ===== 1. 列表推導式（List Comprehension）=====
# 定義一個包含正數、負數和零的列表
mylist = [1, 4, -5, 10]

# 使用列表推導式過濾出正數
# 語法：[表達式 for 元素 in 可疊代物件 if 條件]
# 會產生一個新列表，包含所有大於 0 的元素
[n for n in mylist if n > 0]  # 結果：[1, 4, 10]

# ===== 2. 生成器表達式（Generator Expression）=====
# 語法與列表推導式相同，但用小括號括起來
# 與列表推導式的差別：生成器是「懶惰疊代器」，只會在需要時才產生值
# 優點：節省記憶體，適合處理大量資料
pos = (n for n in mylist if n > 0)  # pos 是一個生成器物件，不是列表

# ===== 3. filter() 函數 =====

# 定義一個字串列表，包含數字和無法轉換為整數的字串
values = ["1", "2", "-3", "-", "N/A"]


# 定義一個輔助函數，用來判斷字串是否可以轉換為整數
def is_int(val):
    try:
        # 嘗試將值轉換為整數
        int(val)
        return True  # 轉換成功，回傳 True
    except ValueError:
        # 轉換失敗（發生 ValueError 例外），回傳 False
        return False


# 使用 filter() 函數過濾資料
# 語法：filter(過濾函數, 可疊代物件)
# filter 會對可疊代物件中的每個元素執行過濾函數
# 只保留使函數回傳 True 的元素
# 注意：filter 回傳的是疊代器，需要用 list() 轉換為列表
list(filter(is_int, values))  # 結果：['1', '2', '-3']

# ===== 4. itertools.compress() =====

# compress 是另一種過濾方式，根據「布林遮罩（boolean mask）」來篩選元素
# 優點：可以先獨立定義篩選條件，再應用到多個資料上

from itertools import compress

addresses = ["a1", "a2", "a3"]  # 地址列表（要過濾的目標）
counts = [0, 3, 10]  # 計數列表（用來產生篩選條件）

# 先用列表推導式產生布林遮罩：哪些 counts 大於 5
# counts[0]=0 不大於 5 → False
# counts[1]=3 不大於 5 → False
# counts[2]=10 大於 5 → True
more5 = [n > 5 for n in counts]  # 結果：[False, False, True]

# 使用 compress 根據布林遮罩過濾 addresses
# 語法：compress(資料列表, 布林遮罩列表)
# 會依序檢查布林遮罩，只保留對應位置為 True 的元素
list(compress(addresses, more5))  # 結果：['a3']
