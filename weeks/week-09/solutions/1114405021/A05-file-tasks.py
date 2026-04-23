# A05. 綜合應用：僅寫新檔 + 目錄統計（5.5 / 5.13 / 5.1）
# Bloom: Apply — 把前面學到的 API 組起來解小任務

from pathlib import Path
from datetime import date

# 這支範例示範兩個常見的小任務：
# 1. 用 'x' 模式建立只能寫一次的日記檔
# 2. 遞迴走訪某個資料夾，統計所有 .py 檔的行數與 def 數量

# ── 任務一：日記小工具（5.5 的 'x' 模式） ──────────────
# 規則：每天只能建一次；同一天重複執行要提示「已存在」。
# date.today() 取得今天日期，isoformat() 轉成 YYYY-MM-DD 格式。
today = date.today().isoformat()          # 例如 2026-04-23
# 檔名使用今天日期，方便每天產生一份獨立日記。
diary = Path(f"diary-{today}.txt")

try:
    # 'x' 模式代表 exclusive create：
    # 只有在檔案不存在時才能建立；如果檔案已存在，會直接丟出 FileExistsError。
    with open(diary, "x", encoding="utf-8") as f:   # 'x' = exclusive create
        # 寫入日記標題與第一段內容。
        f.write(f"# {today} 日記\n")
        f.write("今天學了檔案 I/O。\n")
    # 建立成功後，印出提示訊息。
    print(f"已建立 {diary}")
except FileExistsError:
    # 如果今天的日記已經存在，就不要覆蓋原檔，改為提醒使用者。
    print(f"{diary} 今天已寫過，保留原內容不覆蓋")

# ── 任務二：統計某資料夾裡 .py 檔的行數 ────────────────
# 走訪目錄 → 逐檔逐行讀 → 累計三個數字
def count_py(folder: Path):
    # total：總行數
    # nonblank：非空白行數
    # defs：以 def 開頭的函式定義行數
    total, nonblank, defs = 0, 0, 0
    # rglob("*.py") 會遞迴搜尋 folder 底下所有 .py 檔案。
    for p in folder.rglob("*.py"):
        # errors="replace" 的意思是：如果遇到無法解碼的字元，就用替代字元處理，避免整個程式中斷。
        with open(p, "rt", encoding="utf-8", errors="replace") as f:
            # 逐行讀取，避免一次把整個檔案載入記憶體。
            for line in f:
                # 每讀到一行就累計總行數。
                total += 1
                # strip() 去掉前後空白與換行，方便判斷這行是否真的有內容。
                s = line.strip()
                if s:
                    # 不是空字串就算非空白行。
                    nonblank += 1
                # 只要這行是以 def 開頭，就視為函式定義。
                if s.startswith("def "):
                    defs += 1
    return total, nonblank, defs

# 指定要統計的目錄位置。
# 這裡用相對路徑組合，代表目前檔案所在位置往上再進入 week-04/in-class。
target = Path("..") / ".." / "week-04" / "in-class"
# 先檢查目錄是否存在，再進行統計，避免路徑錯誤。
if target.exists():
    total, nonblank, defs = count_py(target)
    # 依序印出統計結果，方便閱讀。
    print(f"{target}")
    print(f"  總行數       : {total}")
    print(f"  非空白行     : {nonblank}")
    print(f"  def 起頭行數 : {defs}")
else:
    # 如果示範目錄不存在，就輸出提示訊息。
    print(f"示範目錄不存在：{target}")

# ── 課堂延伸挑戰（自行嘗試） ───────────────────────────
# 1) 把日記工具改成「附加」模式 'a'：同一天可多次追寫一行時間戳。
# 2) count_py 再多算一個「註解行（以 # 開頭）」的數字。
# 3) 把統計結果用 print(..., sep='\t', file=f) 寫到 stats.tsv。
