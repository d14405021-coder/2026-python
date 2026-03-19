# U8. 字典最值為何常用 zip(values, keys)（1.8）
# 說明：本程式說明在 Python 中查找字典的「最大/最小值」時
# 為何常常需要使用 zip() 來同時取得「值」和「對應的鍵」
# 關鍵問題：min()/max() 直接用於字典時，只會比較鍵，不會比較值

# 定義一個股票價格字典：鍵是股票代碼，值是價格
prices = {"A": 2.0, "B": 1.0}

# ===== 1. 直接使用 min()/max() 在字典上的問題 =====

# min(prices) 會找到「鍵」的最小值
# 由於 min() 會作用於字典本身，遍歷的是 key（鍵）
# 比較的是字串的大小（依字母順序）
min(prices)  # 結果：'A'
# 說明：比較 'A' 和 'B' 的字母順序，'A' < 'B'，所以回傳 'A'
# 注意：這不是我們想要的！我們想要的是「價格最低」的股票

# ===== 2. 使用 .values() 只取得值 =====

# min(prices.values()) 會找到「值」的最小值
# 遍歷的是字典的所有值（prices），比較的是數值大小
min(prices.values())  # 結果：1.0
# 說明：比較 2.0 和 1.0，1.0 較小，所以回傳 1.0
# 缺點：只知道最小值是 1.0，但不知道是哪個鍵（股票代碼）

# ===== 3. 解決方案：使用 zip() 同時取得值和鍵 =====

# 使用 zip() 將「值」和「鍵」打包成配對
# 語法：zip(可疊代物件1, 可疊代物件2)
# 會將 prices.values() 和 prices.keys() 的元素一一配對
# 結果是一連串的 tuple：(值, 鍵)

min(zip(prices.values(), prices.keys()))
# 說明：
# - zip(prices.values(), prices.keys()) → [(2.0, 'A'), (1.0, 'B')]
# - min() 比較第一個元素（值）：2.0 和 1.0
# - 1.0 較小，回傳整個 tuple：(1.0, 'B')
# 回傳 (最小value, 對應key)，一次拿到兩者

# ===== 4. 為何 zip(values, keys) 比 zip(keys, values) 更常見 =====

# 注意：min(zip(prices.values(), prices.keys()))
#       是「值在前面、鍵在後面」的順序
# 原因：min()/max() 預設「先比較第一個元素」
#       若有多個相同值時，才會比較第二個元素
# 因此將「要比較的值」放在前面，「要回傳的鍵」放在後面

# ===== 5. 應用場景 =====

# 場景一：找出價格最低的股票
min(zip(prices.values(), prices.keys()))  # ('B', 1.0)

# 場景二：取得鍵（不使用 index）
min_price_key = min(prices, key=lambda k: prices[k])
# 這也是常見寫法：用 key 參數指定比較依據

# 場景三：同時取得最大/最小的鍵和值
min_item = min(zip(prices.values(), prices.keys()))
max_item = max(zip(prices.values(), prices.keys()))
# min_item = (1.0, 'B')
# max_item = (2.0, 'A')

# ===== 6. zip() 的其他用法 =====

# zip() 可以同時處理多個列表
# names = ['Alice', 'Bob', 'Charlie']
# scores = [85, 92, 78]
# for name, score in zip(names, scores):
#     print(f'{name}: {score}')

# 注意：zip() 會在最短的列表用完時停止
# 若列表長度不同，會截斷到最短的長度
