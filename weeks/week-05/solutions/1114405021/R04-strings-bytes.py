# R04. 位元組字串操作（2.20）
# -----------------------------------------------------------------------------
# 這份程式的目標：
# 1) 讓你看懂 bytes 與 str 在 Python 中的核心差異。
# 2) 熟悉 bytes 常見操作（切片、前綴檢查、切割、取代）。
# 3) 理解 bytes 與正規表達式搭配時的寫法。
#
# 先建立一個重要觀念：
# - str：文字字串，內容是 Unicode 字元（偏向「人看的文字」）。
# - bytes：位元組序列，元素是 0~255 的整數（偏向「機器處理的原始資料」）。
#
# 因為 bytes 的本質是「數字序列」，所以索引、格式化、編碼解碼等行為會和 str 不同。

import re

# ===== 1. 基本操作 =====
# 在字串前面加上 b，代表這是一個 bytes 常值（位元組字串）
# 這裡的 Hello World 會以 ASCII 可表示的位元組儲存。
data = b"Hello World"

# 切片操作 (Slicing)：和一般字串很像，切完之後型別仍是 bytes
# data[0:5] 代表取索引 0 到 4（不含 5）
print(data[0:5])  # 結果：b'Hello'

# startswith() 檢查前綴：
# 注意比對對象也必須是 bytes（不能直接用一般字串 "Hello"）
# 因為 bytes 與 str 是不同型別，Python 不會自動混用。
print(data.startswith(b"Hello"))  # 結果：True

# split() 切割：預設用空白分割
# 回傳 list，且每個元素仍是 bytes（不是 str）
print(data.split())  # 結果：[b'Hello', b'World']

# replace() 取代內容：
# 尋找片段與替換片段都必須用 bytes
# 這行會把 b"Hello" 換成 b"Hello Cruel"
print(data.replace(b"Hello", b"Hello Cruel"))  # 結果：b'Hello Cruel World'

# ===== 2. 結合正規表達式 =====
# 正規表達式可處理 bytes，但規則字串也要是 bytes 型別。
# 所以通常會使用 rb"..."：
# - r：raw string，反斜線不做一般跳脫（正規表示式常用）
# - b：bytes literal
raw = b"FOO:BAR,SPAM"

# rb"[:,]" 的意思是「匹配一個字元，該字元可為冒號或逗號」
# 因為 raw 是 bytes，所以 split 結果也會是 bytes 清單。
print(re.split(rb"[:,]", raw))  # 結果：[b'FOO', b'BAR', b'SPAM']

# ===== 3. 與一般字串的重要差異 =====

# 差異 1：索引取值 (Indexing) 會回傳整數，而不是字元！
a = "Hello"  # str：一般的 Unicode 字串
b = b"Hello"  # bytes：位元組字串

print(a[0])  # 結果：'H'（回傳長度為 1 的字元）
print(b[0])  # 結果：72（回傳 ASCII 編碼的整數值，即 ord('H') 的結果）
# 說明：
# - str 的單一索引是「字元」
# - bytes 的單一索引是「整數位元組值」
# 若你要拿到 bytes 形式的一個字元，請用切片 b[0:1]，結果會是 b'H'。

# 差異 2：沒有內建的字串格式化功能 (format)
# 位元組字串不支援 str 的 .format() 與 f-string。
# 正確流程：
# 1) 先用 str 完成格式化
# 2) 再用 encode() 轉成 bytes
# 這是實務上最常見、也最安全的做法。
formatted = "{:10s} {:10d}".format("ACME", 100).encode("ascii")
print(formatted)  # 結果：b'ACME            100'
# 說明：
# - "{:10s}"：字串欄位寬 10
# - "{:10d}"：整數欄位寬 10
# 最後 encode("ascii") 後，才會得到可用於網路封包或檔案位元組寫入的 bytes。
