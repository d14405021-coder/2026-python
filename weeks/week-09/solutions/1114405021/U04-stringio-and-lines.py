# U04. 類檔案物件 StringIO 與逐行處理（5.6 / 5.1 逐行）
# Bloom: Understand — 知道 file-like 是鴨子型別，能把記憶體當檔案用

import io
from pathlib import Path

# 這支範例主要示範兩個觀念：
# 1. StringIO 可以讓你把記憶體中的字串當成檔案來讀寫
# 2. 真正讀文字檔時，逐行處理可以降低記憶體使用量，適合大檔案

# ── 5.6 StringIO：記憶體裡的「假檔案」 ─────────────────
# StringIO 是一個存在記憶體中的檔案物件，不會真的建立實體檔案。
# 它很適合拿來做測試、暫存文字、或是給那些只接受 file-like 物件的 API 使用。
buf = io.StringIO()
# print(..., file=buf) 代表把輸出寫到 buf，而不是螢幕。
print("第一行", file=buf)
print("第二行", file=buf)
print("第三行", file=buf)

# 取出整段字串
# getvalue() 會把目前 StringIO 裡累積的所有內容一次取出。
text = buf.getvalue()
print("---StringIO 內容---")
print(text)

# 也能當讀檔用：seek 回開頭再逐行讀
# StringIO 也是可迭代的檔案物件；若要重新從頭讀，先用 seek(0) 把游標移回開頭。
buf.seek(0)
for i, line in enumerate(buf, 1):
    # enumerate(..., 1) 讓行號從 1 開始，更符合人類閱讀習慣。
    # rstrip() 把換行拿掉，避免輸出時多出空白行。
    print(i, line.rstrip())

# 為什麼有用？任何收 file-like 的 API（csv、json、logging）
# 都能塞 StringIO，不必真的寫到磁碟、方便測試。
import csv
# 再建立一個記憶體中的檔案，交給 csv.writer 使用。
# 這種做法常用在單元測試：不用建立真實檔案，也能檢查輸出格式。
mem = io.StringIO()
writer = csv.writer(mem)
# writer.writerow() 每次寫入一列 CSV。
writer.writerow(["name", "score"])
writer.writerow(["alice", 90])
print("---CSV in memory---")
# 直接把記憶體中的 CSV 內容印出來，確認 writer 寫入的結果。
print(mem.getvalue())

# ── 5.1 延伸：逐行處理檔案（大檔友善） ─────────────────
# 先造一個多行檔
# 這裡先建立範例來源檔 poem.txt，內容包含空行，方便後面示範過濾與加行號。
src = Path("poem.txt")
# write_text() 會直接把整段文字寫入檔案。
# 其中的空行是刻意保留，讓後面的篩選邏輯有東西可處理。
src.write_text("床前明月光\n\n疑是地上霜\n\n舉頭望明月\n低頭思故鄉\n", encoding="utf-8")

# 任務：過濾空行、加上行號、寫到新檔
# dst 是輸出檔，會存放加上行號後的結果。
dst = Path("poem_numbered.txt")
# 以文字模式同時開啟來源檔與目的檔。
# 來源檔用來讀，目的檔用來寫；with 可以確保離開區塊後自動關閉檔案。
with open(src, "rt", encoding="utf-8") as fin, \
     open(dst, "wt", encoding="utf-8") as fout:
    # n 用來記錄非空行的行號，初始為 0。
    n = 0
    for line in fin:               # 逐行：一次只讀一行到記憶體
        # rstrip() 去掉行尾換行字元，這樣後面判斷空行比較方便。
        line = line.rstrip()
        # 如果去掉換行後變成空字串，表示這一行原本是空行，直接跳過。
        if not line:
            continue               # 跳過空行
        # 只有真正保留下來的內容才計入行號。
        n += 1
        # 使用兩位數格式化 {n:02d}，讓輸出更整齊。
        print(f"{n:02d}. {line}", file=fout)

print("---加行號後---")
# 讀回目的檔內容，確認寫出的結果是否符合預期。
print(dst.read_text(encoding="utf-8"))
