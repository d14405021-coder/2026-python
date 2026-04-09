# U01. 字串分割與匹配的陷阱（2.1–2.11）
#
# 這份範例主要在示範三個常見重點：
# 1. 使用 re.split() 時，若正則裡有「捕獲分組」，分隔符也會被保留下來。
# 2. startswith() 可以接受多個前綴，但參數必須是 tuple，而不是 list。
# 3. strip() 只會清掉字串頭尾的空白，不會處理字串中間的空白。

import re

# ── 捕獲分組保留分隔符（2.1）─────────────────────────
#
# re.split() 的特性：
# 當分割用的模式包含「捕獲分組」時，分隔符本身會一併出現在結果列表中。
# 這個行為很實用，因為我們可以把原字串拆開後，再把值與分隔符交錯接回去，
# 做到「分割後又能保留原本的標點或空白結構」。
line = "asdf fjdk; afed, fjek,asdf, foo"
fields = re.split(r"(;|,|\s)\s*", line)
# 偶數索引放的是原本的資料片段，奇數索引放的是對應的分隔符。
values = fields[::2]
# 把最後一個值後面補上一個空字串，方便 zip() 逐一配對時不會漏掉尾端。
delimiters = fields[1::2] + [""]
# 交錯把值與分隔符重新接回去，這樣就能重建成去除多餘空白後的版本。
rebuilt = "".join(v + d for v, d in zip(values, delimiters))
print(rebuilt)  # 'asdf fjdk;afed,fjek,asdf,foo'

# ── startswith 必須傳 tuple（2.2）────────────────────
#
# startswith() 可以一次檢查多個可能的前綴，概念上像是：
# 「只要是這些前綴中的任一個，就視為符合」。
# 但它不接受 list，因為這個 API 期待的是 tuple 這種不可變序列。
# 如果直接傳 list，Python 會拋出 TypeError。
url = "http://www.python.org"
choices = ["http:", "ftp:"]
try:
    url.startswith(choices)  # type: ignore[arg-type]
except TypeError as e:
    # 這裡刻意示範錯誤情況，讓讀者知道為什麼必須轉成 tuple。
    print(f"TypeError: {e}")
# 將 list 轉成 tuple 後，再交給 startswith() 就是合法用法。
print(url.startswith(tuple(choices)))  # True（轉成 tuple 才行）

# ── strip 只處理頭尾，不處理中間（2.11）──────────────
#
# strip()、lstrip()、rstrip() 的核心概念都是「只處理邊界」。
# 它們會移除字串前後指定的字元，但不會碰到字串中央的內容。
# 這也是很多人清理文字時最容易誤判的地方：
# 你以為 strip() 會把所有空白都刪掉，但其實它只會清頭尾。
s = "  hello     world  "
# 先用 strip() 去掉頭尾空白，觀察中間的多個空白仍然被保留。
print(repr(s.strip()))  # 'hello     world'（中間多餘空白還在）
# 如果直接把所有空白都拿掉，雖然乾淨，但會連單字間的分隔都消失。
print(repr(s.replace(" ", "")))  # 'helloworld'（過頭，連詞間空白也消）
# 正確做法通常是：先 strip()，再用正則把連續空白壓成單一空白。
print(repr(re.sub(r"\s+", " ", s.strip())))  # 'hello world'（正確）

# 生成器逐行清理（高效，不預載入記憶體）
#
# 這裡示範另一種常見寫法：用生成器表達式逐行 strip。
# 好處是可以邊讀邊處理，不需要先把所有資料一次載入到記憶體中。
# 當資料量大時，這種寫法通常比先建立完整清單更省資源。
lines = ["  apple  \n", "  banana  \n"]
for line in (l.strip() for l in lines):
    print(line)
