# A06. 壓縮檔、臨時資料夾、物件序列化（5.7 / 5.19 / 5.21）
# Bloom: Apply — 能把標準庫工具組合起來解一個小任務

import gzip
import pickle
import tempfile
from pathlib import Path

# 這支範例主要示範三種常見的標準庫工具：
# 1. gzip：讀寫壓縮檔，介面和 open 很像
# 2. tempfile：建立臨時檔案或臨時資料夾，結束後可自動清理
# 3. pickle：把 Python 物件序列化成 bytes 存檔，再從 bytes 還原回物件

# ── 5.7 讀寫壓縮檔：gzip.open 幾乎和 open 一樣 ─────────
# 寫 .gz（文字模式要記得 encoding）
# gzip.open() 的用法和 open() 很接近，只是多了壓縮與解壓縮的處理。
# 當你用文字模式 "wt" 寫入時，仍然要指定 encoding，否則中文字可能出問題。
with gzip.open("notes.txt.gz", "wt", encoding="utf-8") as f:
    # 這裡寫入兩行文字，最後實際儲存在 .gz 壓縮檔中。
    f.write("第一行筆記\n")
    f.write("第二行筆記\n")

# 讀回：直接逐行迭代
# 以 "rt" 讀回時，gzip 會先解壓縮，再把內容當成文字串流來讀。
with gzip.open("notes.txt.gz", "rt", encoding="utf-8") as f:
    # 檔案物件本身可逐行迭代，所以可以直接 for line in f。
    for line in f:
        print("gz:", line.rstrip())

# 也能用 'wb'/'rb' 處理二進位資料
# 如果內容不是文字，而是原始位元組，就用二進位模式 'wb'/'rb'。
# 這樣不會發生文字編碼/解碼的問題。
with gzip.open("blob.bin.gz", "wb") as f:
    # 這裡寫入一小段 bytes，示範壓縮二進位資料的方式。
    f.write(b"\x00\x01\x02\x03")

# stat().st_size 可以查看檔案大小，幫助你確認壓縮檔確實有產生。
print("blob size:", Path("blob.bin.gz").stat().st_size, "bytes")

# ── 5.19 臨時檔案與資料夾：離開 with 自動清理 ──────────
# 場景：想跑個小實驗但不想在專案亂留檔
# TemporaryDirectory() 會建立一個暫時資料夾，離開 with 區塊後就會自動刪除。
with tempfile.TemporaryDirectory() as tmp:
    # 回傳值是字串路徑，先轉成 Path 方便後續做 / 串接。
    tmp = Path(tmp)
    print("暫存資料夾:", tmp)

    # 在裡面寫幾個檔
    # 這些檔案都存放在臨時資料夾中，不會污染專案目錄。
    (tmp / "a.txt").write_text("hello\n", encoding="utf-8")
    (tmp / "b.txt").write_text("world\n", encoding="utf-8")

    # 列出內容
    # iterdir() 會列出資料夾底下的直接子項目。
    for p in tmp.iterdir():
        # read_text() 直接讀回檔案內容，並用 rstrip() 去掉行尾換行。
        print("  ", p.name, "→", p.read_text(encoding="utf-8").rstrip())

# 離開 with 後，tmp 已自動刪除
# 離開 TemporaryDirectory 的 with 區塊後，資料夾已被清理掉。
print("離開後還存在嗎？", tmp.exists())  # False

# 單一臨時檔：NamedTemporaryFile
# NamedTemporaryFile 會建立一個有名字的臨時檔。
# delete=False 表示離開 with 時不要自動刪除，方便後續自己控制刪除時機。
with tempfile.NamedTemporaryFile("wt", delete=False, suffix=".log",
                                 encoding="utf-8") as f:
    # 這裡寫入一行暫存內容。
    f.write("暫存 log\n")
    # f.name 是這個臨時檔的實際路徑。
    log_path = f.name
print("暫存檔位置:", log_path)
# 用完之後手動刪除，避免留下不必要的暫存檔。
Path(log_path).unlink()  # 用完自己刪

# ── 5.21 pickle：把 Python 物件「原樣」存檔 ────────────
# 適用：dict/list/自訂類別；不適用：跨語言、長期存檔（用 json 更穩）
# pickle 可以把 Python 物件直接轉成二進位格式保存。
# 它很方便，但格式不是給人類閱讀的，也不適合跨語言使用。
scores = {
    "alice": [90, 85, 92],
    "bob":   [70, 75, 80],
    "carol": [88, 91, 95],
}

# 注意：pickle 是 bytes → 一定要 'wb'/'rb'
# 因為 pickle.dump 產生的是 bytes，所以檔案必須用二進位模式 'wb' 打開。
with open("scores.pkl", "wb") as f:
    pickle.dump(scores, f)

# 讀回時同樣要用二進位模式 'rb'，再交給 pickle.load 還原。
with open("scores.pkl", "rb") as f:
    loaded = pickle.load(f)

# 讀回後的 loaded 應該會和原本的 scores 完全相同。
print("讀回的物件:", loaded)
print("型別一致?", type(loaded) is dict)         # True
print("內容相等?", loaded == scores)              # True
# 直接對還原出的資料做運算，確認它真的還是原本的 Python 物件。
print("alice 平均:", sum(loaded["alice"]) / 3)   # 89.0

# ⚠️ 安全提醒：pickle.load 會執行內嵌指令，
# 絕對不要對「來路不明」的 .pkl 檔做 load。
# 這是因為 pickle 不是純資料格式，若載入惡意檔案可能有安全風險。

# ── 課堂延伸挑戰 ───────────────────────────────────────
# 1) 把 scores 存成 gzip 壓縮後的 pickle：gzip.open('scores.pkl.gz','wb')
# 2) 用 TemporaryDirectory 跑完整流程（寫→讀→比對），不在專案留任何檔
# 3) 試著 pickle 一個 lambda，觀察錯誤訊息（pickle 不能存 lambda）
