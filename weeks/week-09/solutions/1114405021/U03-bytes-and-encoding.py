# U03. 文字 vs 位元組、編碼觀念（5.1 encoding / 5.4）
# Bloom: Understand — 能解釋什麼時候用 'rb'、為什麼要指定 encoding

from pathlib import Path

# 這支範例主要在示範三件事：
# 1. 什麼是 bytes，以及為什麼非文字檔要用二進位模式開啟
# 2. str 和 bytes 之間如何互相轉換
# 3. 為什麼讀寫文字檔時一定要明確指定 encoding

# ── 5.4 二進位讀寫：圖片、zip、任何非文字 ───────────────
# 先造一個「假 PNG」：只寫前 8 bytes 的 magic number
# PNG 檔案開頭有固定的 magic number，用來辨識檔案類型。
# 這裡用 bytes([...]) 直接建立一串位元組資料，模擬 PNG 檔頭。
magic = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])
# write_bytes() 會把 bytes 直接寫入檔案，適合圖片、壓縮檔、音訊等二進位資料。
Path("fake.png").write_bytes(magic)

# 讀回前 8 bytes，對照 PNG 檔頭
# 'rb' 代表以二進位模式讀取，不會做文字解碼。
# 對於圖片或其他非文字內容，這是正確的讀法。
with open("fake.png", "rb") as f:
    head = f.read(8)
# 讀回來的結果會是 bytes 物件，不是一般字串。
print(head)           # b'\x89PNG\r\n\x1a\n'
# 比對讀回的前 8 bytes 是否和原本的 magic number 一樣。
print(head == magic)  # True

# bytes 可逐位元組迭代（拿到 int，不是 str）
# bytes 物件可以直接被迭代，每次拿到的是 0~255 的整數值。
for b in head[:4]:
    # hex(b) 可以把整數轉成十六進位字串，方便觀察位元組內容。
    print(b, hex(b))

# ── 文字 vs 位元組的型別差 ─────────────────────────────
# s 是一般字串（str），b 是把字串用 UTF-8 編碼後得到的 bytes。
s = "你好"
# encode() 會把字串轉成位元組序列；這裡明確指定 utf-8，避免不同環境出現差異。
b = s.encode("utf-8")   # str → bytes
print(s, type(s))       # <class 'str'>
print(b, type(b))       # <class 'bytes'>
# decode() 則是反過來，把 bytes 依照指定編碼還原成字串。
print(b.decode("utf-8"))  # bytes → str

# ── 5.1 encoding 參數：寫錯會爛掉 ──────────────────────
# write_text() 會直接幫你用指定 encoding 寫入純文字檔。
# 這裡寫入中文內容，後面會示範用不同編碼讀取時可能出錯。
Path("zh.txt").write_text("中文測試\n", encoding="utf-8")

# 正常：用 utf-8 讀 utf-8 寫的檔
# 讀取時用相同的 utf-8 編碼，才能正確還原原本的中文字。
print(Path("zh.txt").read_text(encoding="utf-8"))

# 故意弄錯：用 big5 解 utf-8 → UnicodeDecodeError
# 如果讀檔時指定錯誤的編碼，Python 會無法把位元組正確解碼成字串。
# 這裡故意用 big5 去讀 utf-8 檔案，示範實際會拋出的解碼錯誤。
try:
    print(Path("zh.txt").read_text(encoding="big5"))
except UnicodeDecodeError as e:
    # 捕捉錯誤後印出訊息，方便理解「編碼不一致」會造成什麼結果。
    print("解碼錯誤:", e)

# 小結：
# - 文字檔 → 'rt'/'wt'，一律明示 encoding='utf-8'
# - 非文字（png/zip/pickle）→ 'rb'/'wb'，不談 encoding
