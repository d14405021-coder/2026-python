# R04. 位元組字串操作（2.20）
# bytes / bytearray 支援大部分字串方法，但有幾個重要差異

import re

# `b"..."` 代表 bytes（位元組序列），常見於：
# 1) 網路傳輸資料（socket）
# 2) 讀寫二進位檔案（圖片、壓縮檔、音訊）
# 3) 需要明確控制編碼的情境
#
# 與一般字串 `str` 不同的是：
# - `str` 儲存的是「文字語意」（Unicode 字元）
# - `bytes` 儲存的是「原始位元組資料」（0~255 的整數序列）
data = b"Hello World"

# 切片（slice）在 bytes 上與字串很像，回傳型別仍然是 bytes。
# data[0:5] 取出索引 0~4 的內容，因此得到 b'Hello'。
print(data[0:5])  # b'Hello'

# startswith() 可檢查 bytes 是否以指定 bytes 前綴開頭。
# 注意：bytes 與 str 不能混用，這裡一定要寫成 b"Hello"。
print(data.startswith(b"Hello"))  # True

# split() 預設依空白切割，bytes 版本回傳的是「bytes list」。
# 所以結果中的每個元素仍是 b'...'
print(data.split())  # [b'Hello', b'World']

# replace() 會建立新的 bytes 物件，不會原地修改原本資料。
# 這裡把 b"Hello" 替換成 b"Hello Cruel"。
print(data.replace(b"Hello", b"Hello Cruel"))  # b'Hello Cruel World'

# 正則表達式也必須使用 bytes 模式
raw = b"FOO:BAR,SPAM"

# 若比對目標是 bytes，正則樣式也必須是 bytes（使用 rb"..."）。
# `rb"[:,]"` 的意思是：以 ':' 或 ',' 任一符號做切割。
# 結果同樣是 bytes 組成的串列。
print(re.split(rb"[:,]", raw))  # [b'FOO', b'BAR', b'SPAM']

# 差異 1：索引回傳整數而非字元
a = "Hello"
b = b"Hello"

# str 索引：回傳單一「字元」
print(a[0])  # 'H'（字元）

# bytes 索引：回傳單一「位元組值」（整數）
# 72 即 ASCII 中 'H' 的編碼值，也就是 ord('H')。
print(b[0])  # 72（整數，即 ord('H')）

# 差異 2：不能直接用 format()，需先編碼
# format() 產生的是 str（文字），不是 bytes。
# 如果後續流程需要 bytes（例如寫入二進位介面），
# 必須再用 encode() 轉成指定編碼。
# 這裡使用 ASCII，是因為內容僅含英數字元。
formatted = "{:10s} {:10d}".format("ACME", 100).encode("ascii")

# 最終輸出會是 bytes 物件。
print(formatted)  # b'ACME            100'
