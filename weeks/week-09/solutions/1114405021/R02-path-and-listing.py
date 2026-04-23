# R02. 路徑操作與目錄列舉（5.11 / 5.12 / 5.13）
# Bloom: Remember — 會用 pathlib 組路徑、檢查存在、列出檔案

import os
from pathlib import Path

# 這支範例主要示範三件事：
# 1. 如何用 pathlib 和 os.path 組合路徑
# 2. 如何檢查檔案或資料夾是否存在
# 3. 如何列出資料夾內容，以及用 glob/rglob 篩選檔案

# ── 5.11 組路徑：pathlib 是現代寫法 ────────────────────
# Path("weeks") / "week-09" 會把路徑元件安全地串接起來，
# 不需要自己手動寫斜線或反斜線，跨平台也比較穩定。
base = Path("weeks") / "week-09"
# print(base) 直接顯示路徑物件的字串形式。
# 在 Windows 上顯示時通常會自動用反斜線；在其他系統上可能是正斜線。
print(base)              # weeks/week-09（Windows 會自動變成反斜線）
# name 取出最後一段名稱，也就是目前路徑的資料夾名稱。
print(base.name)         # week-09
# parent 取出上一層目錄，也就是 weeks。
print(base.parent)       # weeks
# suffix 取出副檔名；因為這裡是資料夾，所以沒有副檔名，結果是空字串。
print(base.suffix)       # ''（無副檔名）

# 這裡建立一個代表檔案的 Path 物件。
# 與資料夾不同，檔案通常會搭配 stem/suffix 來看檔名與副檔名。
f = Path("hello.txt")
# stem 是不含副檔名的檔名，suffix 則是副檔名本身。
print(f.stem, f.suffix)  # hello .txt

# 相容舊寫法：os.path.join
# os.path.join 是較舊但仍常見的路徑拼接方式。
# 它會依照作業系統自動使用正確的分隔符號。
print(os.path.join("weeks", "week-09", "README.md"))

# ── 5.12 存在判斷 ──────────────────────────────────────
# Path.exists() 可檢查目標是否存在。
# is_file() 和 is_dir() 則可進一步判斷它是檔案還是資料夾。
p = Path("hello.txt")
print(p.exists())    # 是否存在
print(p.is_file())   # 是否是檔案
print(p.is_dir())    # 是否是資料夾

# 這個路徑預期不存在，用來示範存在檢查的寫法。
missing = Path("no_such_file.txt")
# 先檢查再讀取，是避免 FileNotFoundError 的基本防呆做法。
if not missing.exists():
    print(f"{missing} 不存在，略過讀取")

# ── 5.13 列出資料夾內容 ────────────────────────────────
# here 代表目前工作目錄，也就是 "."。
here = Path(".")

# 只列當層
# os.listdir() 會回傳指定資料夾下的所有名稱，
# 只看目前這一層，不會自動深入子資料夾。
for name in os.listdir(here):
    print("listdir:", name)

# 只抓 .py（當層）
# glob("*.py") 會在目前資料夾中尋找符合樣式的檔案，這裡只找副檔名為 .py 的檔案。
for p in here.glob("*.py"):
    print("glob:", p)

# 遞迴抓所有 .py（含子資料夾）
# rglob("*.py") 會遞迴搜尋所有子資料夾裡的 .py 檔案。
# 這比 glob 更深入，適合用來一次掃描整個專案。
for p in Path("..").rglob("*.py"):
    print("rglob:", p)
    break  # 示範用，只印第一個
