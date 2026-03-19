# R18. namedtuple（1.18）
# 說明：本程式示範如何使用 collections 模組中的 namedtuple
# namedtuple（命名元組）是一種特殊的数据結構
# 結合了「元組（tuple）」的不可變特性，與「字典（dict）」的命名訪問特性
# 優點：比普通類別更輕量、比元組更具可讀性、比字典更節省記憶體

# 匯入 collections 模組中的 namedtuple 函數
from collections import namedtuple

# ===== 1. 建立命名元組類別 =====

# 使用 namedtuple() 建立一個命名元組類別
# 語法：namedtuple('類別名稱', ['欄位1', '欄位2', ...])
# - 第一個參數：類別名稱（字串）
# - 第二個參數：欄位名稱列表（可用串列或字串）
Subscriber = namedtuple("Subscriber", ["addr", "joined"])
# 建立了一個名為 Subscriber 的類別，有兩個欄位：addr（地址）和 joined（加入日期）

# ===== 2. 建立命名元組實例 =====

# 使用建立的 Subscriber 類別，來建立具體的實例（物件）
# 就像呼叫普通函數一樣，傳入各個欄位的值
sub = Subscriber("jonesy@example.com", "2012-10-19")
# sub.addr   → 'jonesy@example.com'
# sub.joined → '2012-10-19'

# ===== 3. 存取欄位的方式 =====

# namedtuple 有兩種存取方式：
# 方式一：使用欄位名稱（像物件屬性一样直觀）
sub.addr  # 結果：'jonesy@example.com'
# 方式二：使用索引（像普通元組一样，可用位置索引）
# sub[0]   # 結果：'jonesy@example.com'

# ===== 4. 命名元組的不可變性 =====

# namedtuple 建立的物件是不可變的（immutable）
# 一旦建立後，無法直接修改欄位的值
# 例如：sub.addr = 'new@example.com' 會發生錯誤（AttributeError）

# 若要「修改」值，需要使用 _replace() 方法
# _replace() 會建立一個新的命名元組，取代指定欄位的值

# 建立一個 Stock 類別，包含三個欄位：name（股票名稱）、shares（股數）、price（價格）
Stock = namedtuple("Stock", ["name", "shares", "price"])

# 建立一個 Stock 實例
s = Stock("ACME", 100, 123.45)

# 使用 _replace() 方法建立新的命名元組（不改變原本的物件）
# 語法：命名元組._replace(欄位名稱=新值)
# _replace() 會回傳一個全新的命名元組，原本的 s 保持不變
s = s._replace(shares=75)  # 將 shares 從 100 改為 75
# 結果：Stock(name='ACME', shares=75, price=123.45)

# ===== 實用情境 =====
# namedtuple 很適合用於：
# - 函數的傳回值（比元組更具可讀性）
# - 替代簡單的資料類別（比自訂類別更簡潔）
# - 處理固定結構的資料（如座標、日期、記錄等）
