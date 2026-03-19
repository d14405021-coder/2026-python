# R19. 轉換+聚合：生成器表達式（1.19）
# 說明：本程式示範如何結合「生成器表達式」與 Python 內建的聚合函數
# 生成器表達式可以即時做資料轉換，再傳給 sum()、min()、max() 等函數進行聚合
# 這種寫法比先建立列表再處理更節省記憶體

# ===== 1. sum() + 生成器表達式 =====

# 定義一個數字列表
nums = [1, 2, 3]

# 使用 sum() 搭配生成器表達式，計算每個數字的平方和
# 語法：sum(表達式 for 變數 in 可疊代物件)
# 生成器表達式會對每個元素進行計算（x * x），sum() 再把結果相加
# 相較於 [x * x for x in nums] 需要先建立完整列表，生成器更有效率
sum(x * x for x in nums)  # 結果：1 + 4 + 9 = 14

# ===== 2. str.join() + 生成器表達式 =====

# 定義一個元組，包含公司名稱（字串）、股數（整數）、價格（浮點數）
s = ("ACME", 50, 123.45)

# 使用 str.join() 將元組中的所有元素用逗號連接成一個字串
# 語法：'連接符'.join(可疊代物件)
# 由於 join() 需要字串元素，但元組中包含數字（50, 123.45）
# 因此用生成器表達式先將每個元素轉換為字串：str(x) for x in s
# 這裡的生成器扮演「轉換器」的角色
",".join(str(x) for x in s)  # 結果：'ACME,50,123.45'

# ===== 3. min() / max() + 生成器表達式 =====

# 定義一個股票投資組合列表，每個元素是字典
portfolio = [{"name": "AOL", "shares": 20}, {"name": "YHOO", "shares": 75}]

# 方法一：使用生成器表達式，找出 shares 最小的股票
# 語法：min(表達式 for 變數 in 可疊代物件)
# 這裡的表達式是 s['shares']，會取出每個字典的 shares 值
# min() 會比較這些值，回傳「最小的那個值」（而不是整個字典）
min(s["shares"] for s in portfolio)  # 結果：20

# 方法二：使用 key 參數，找出 shares 最少的「整筆資料」
# 語法：min(可疊代物件, key=比較函數)
# key 參數用來指定比較的依據（這裡用 lambda 函數取得 shares 值）
# min() 會回傳「使 key 函數結果最小」的「原始元素」
# 注意：回傳的是整個字典 {'name': 'AOL', 'shares': 20}，不只是 shares 的值
min(portfolio, key=lambda s: s["shares"])  # 結果：{'name': 'AOL', 'shares': 20}

# ===== 兩種寫法的差異 =====
# - min(s['shares'] for s in portfolio)：回傳「shares 的值」（20）
# - min(portfolio, key=lambda s: s['shares'])：回傳「shares 最小的字典」
# 根據需求選擇適合的寫法
