# R8. 字典運算：min/max/sorted + zip（1.8）

prices = {'ACME': 45.23, 'AAPL': 612.78, 'FB': 10.75}

# 1) 用 zip(value, key) 建立 (價格, 股票代號) 的配對
# zip(prices.values(), prices.keys()) 會產生像這樣的序列：
# (45.23, 'ACME'), (612.78, 'AAPL'), (10.75, 'FB')
#
# min 會先比 tuple 第 1 格（價格），因此得到「最便宜」那組。
min(zip(prices.values(), prices.keys()))

# max 同理，會得到「最貴」那組 (價格, 代號)。
max(zip(prices.values(), prices.keys()))

# sorted 會依 tuple 規則排序：先按價格，再按代號。
# 結果是由小到大的 (價格, 代號) 清單。
sorted(zip(prices.values(), prices.keys()))

# 2) 另一種更直覺寫法：在 key 集合上找最小值
# min(prices, key=...) 的回傳值是「字典的 key」，不是 value。
# 這裡 key 函式告訴 min：請用 prices[k] 當比較依據。
min(prices, key=lambda k: prices[k])  # 回傳 key

# 閱讀重點：
# 1) 先確認你要的結果是「(value, key) 配對」還是「只要 key」
# 2) zip 技巧適合一次拿到值與鍵；key= 寫法語意更直觀
# 3) 若價格相同，tuple 比較會再比第二欄（代號），這會影響最終結果
