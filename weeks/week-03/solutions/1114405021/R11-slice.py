# R11. 命名切片 slice（1.11）

# 這是一筆固定欄寬（fixed-width）的文字紀錄。
# 不同欄位位在字串中的固定位置。
record = '....................100 .......513.25 ..........'

# slice(start, stop) 代表索引範圍 [start:stop]：
# - 包含 start
# - 不包含 stop
#
# 把切片命名成 SHARES、PRICE 的好處：
# 1) 可讀性高（看到名稱就知道意義）
# 2) 之後欄位位置改動時，只需改這裡，不用全檔找魔法數字
SHARES = slice(20, 23)
PRICE = slice(31, 37)

# record[SHARES] 等價於 record[20:23]
# record[PRICE]  等價於 record[31:37]
#
# 這裡先把股數轉 int，再把價格轉 float，最後算總成本。
# 數學意義：cost = shares * price
cost = int(record[SHARES]) * float(record[PRICE])

# 閱讀這段程式的口訣：
# 1) 先確認資料是固定欄寬字串
# 2) 再看每個 slice 名稱對應哪一段索引
# 3) 最後看切出來的字串如何轉型（int/float）並參與運算
