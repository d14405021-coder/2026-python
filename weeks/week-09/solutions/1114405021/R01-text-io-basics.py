# R01. 文本 I/O 基本式（5.1 / 5.2 / 5.3 / 5.17）
# Bloom: Remember — 會叫出 open/print 的基本參數

from pathlib import Path

# 這個範例主要示範 Python 文字檔 I/O 的基本操作：
# 1. 如何建立與寫入文字檔
# 2. 如何把文字檔讀回來
# 3. 如何把 print 的輸出直接導向檔案
# 4. 如何控制分隔符號與結尾字元
# 5. 文字模式與位元組模式的差異，以及常見錯誤

# ── 5.1 讀寫文本檔 ─────────────────────────────────────
# 寫入：mode='wt'（預設 't'），一定要指定 encoding
# Path("hello.txt") 代表目前工作目錄下的 hello.txt 檔案。
# 使用文字模式 "wt" 開檔，表示要寫入文字內容；encoding='utf-8' 可避免中文亂碼。
path = Path("hello.txt")
with open(path, "wt", encoding="utf-8") as f:
    # write() 會把字串直接寫進檔案。
    # 這裡寫入兩行文字，第二行的 \n 代表換行。
    f.write("你好，Python\n")
    f.write("第二行\n")

# 讀回：一次讀完 vs 逐行讀
# 這裡用 "rt" 讀回剛剛寫好的 hello.txt。
# read() 適合小檔案；如果檔案很大，整個讀進記憶體可能會太耗資源。
with open(path, "rt", encoding="utf-8") as f:
    print(f.read())  # 一次讀完（小檔才適合）

# 再開一次同一個檔案，用逐行方式處理。
# 檔案物件本身就是可迭代的，所以可以直接用 for line in f 逐行讀取。
with open(path, "rt", encoding="utf-8") as f:
    for line in f:  # 大檔必備：逐行迭代
        # rstrip() 會把每一行右側的換行字元去掉，讓輸出更乾淨。
        print(line.rstrip())

# ── 5.2 print 導向檔案 ─────────────────────────────────
# print() 不一定只能印到螢幕，只要指定 file= 就可以把輸出寫進檔案。
with open("log.txt", "wt", encoding="utf-8") as f:
    # 這兩行會被寫入 log.txt，而不是顯示在終端機。
    print("登入成功", file=f)
    print("使用者:", "alice", file=f)

# ── 5.3 調整分隔符與行終止符 ───────────────────────────
fruits = ["apple", "banana", "cherry"]
# print(*fruits, sep=",") 會把串列展開後，用逗號串接成 CSV 格式。
# end="\n" 表示這次 print 結束時加上換行，這也是預設值。
with open("fruits.csv", "wt", encoding="utf-8") as f:
    print(*fruits, sep=",", end="\n", file=f)

# end='' 可避免多一個換行
# 這裡用附加模式 "at"，代表不覆蓋原檔，而是把內容接到檔案最後面。
# 第一個 print 的 end="," 讓 "date" 後面不先換行，方便下一個 print 接著補上日期。
with open("fruits.csv", "at", encoding="utf-8") as f:
    print("date", end=",", file=f)
    print("2026-04-23", file=f)

# 把 fruits.csv 的完整內容讀出來並印到螢幕上，方便檢查檔案結果。
print(Path("fruits.csv").read_text(encoding="utf-8"))
# apple,banana,cherry
# date,2026-04-23

# ── 5.17 文字模式 vs 位元組模式提醒 ────────────────────
# 文字模式 'wt' 只能寫入 str；如果要寫入 bytes，必須改用 'wb'。
# 這段 try/except 是刻意示範錯誤：把 bytes 寫進文字模式會引發 TypeError。
# 'wt' 寫 str、'wb' 寫 bytes；寫錯型別會 TypeError
try:
    with open("bad.txt", "wt", encoding="utf-8") as f:
        # 這裡故意傳入 bytes，讓 Python 拋出錯誤，示範型別不符的情況。
        f.write(b"bytes in text mode")  # ← 會錯
except TypeError as e:
    # 捕捉錯誤後把訊息印出來，方便學習者看到實際例外內容。
    print("錯誤示範:", e)
