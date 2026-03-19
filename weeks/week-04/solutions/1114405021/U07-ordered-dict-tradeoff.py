# U7. OrderedDict 的取捨：保序但更吃記憶體（1.7）
# 說明：本程式說明 collections 模組中 OrderedDict 的特性
# 以及它與普通 dict 的差異
# 核心概念：OrderedDict 能「記住」元素的插入順序
# 代價：由於需要額外的資料結構來維護順序，因此會消耗更多記憶體

# 匯入 collections 模組中的 OrderedDict 類別
from collections import OrderedDict

# ===== 1. 建立 OrderedDict =====

# 建立一個空的 OrderedDict
d = OrderedDict()

# 使用普通的方式加入鍵值對
d["foo"] = 1  # 第一個插入：foo
d["bar"] = 2  # 第二個插入：bar

# 遍歷 OrderedDict 時，會按照「插入順序」回傳元素
# 結果：foo, bar（永遠是這個順序，即使 foo < bar 字母順序在前面）

# ===== 2. 為何需要額外結構 =====

# 你能解釋：為了維持插入順序，它需要額外結構（因此更耗記憶體）
#
# 普通 dict 的內部結構（Python 3.7+）：
# - 底層使用「雜湊表（Hash Table）」
# - 虽然在 Python 3.7+ 中已經「保序」，但沒有明確記錄順序
# - 每個 bucket 只存 key 的雜湊值和指標
#
# OrderedDict 的內部結構：
# - 除了普通的雜湊表，還有一個「雙向連結串列（Doubly Linked List）」
# - 這個串列明確記錄每個 key 的「前一個」和「下一個」key
# - 插入時：將新 key 加到串列末端
# - 刪除時：從串列中移除該 key
# - 遍歷時：沿著串列走訪，而非雜湊表
#
# 記憶體代價：
# - 普通 dict：每個元素額外儲存一個指標（約 8 bytes）
# - OrderedDict：每個元素額外儲存兩個指標（前、後）+ 串列維護成本
# - 根據 Python 官方測試，OrderedDict 比普通 dict 多消耗約 20-30% 記憶體

# ===== 3. 何時使用 OrderedDict =====

# 適合使用 OrderedDict 的情境：
# - 舊版 Python（< 3.7）：需要明確依賴插入順序時
# - 需要「最近使用」（LRU）快取時：OrderedDict.move_to_end()
# - 需要反覆移動元素到開頭或結尾時
# - 序列化後需要保序時（如 JSON、CSV 等格式）
#
# 現代 Python（3.7+）的建議：
# - 大多數情況使用普通 dict 即可（已內建保序）
# - 只有在需要「有序操作」（如 move_to_end）時才用 OrderedDict

# ===== 4. OrderedDict 特有方法 =====

# d.move_to_end(key)：將指定 key 移到開頭或結尾
# d.popitem(last=True)：移除並回傳最後一個（或第一個）元素
# d.move_to_end('foo', last=True) → 移到結尾
# d.move_to_end('foo', last=False) → 移到開頭

# ===== 5. 總結 =====

# OrderedDict 的「取捨」：
# - 獲得：明確的有序操作能力
# - 付出：更高的記憶體消耗
# - 建議：在 Python 3.7+ 時代，除非有特殊需求，否則優先使用普通 dict
