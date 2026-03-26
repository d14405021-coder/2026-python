# R08. 日期範圍與字串轉換（3.14–3.15）
# calendar.monthrange / strptime / strftime

from datetime import datetime, date, timedelta
from calendar import monthrange


# ── 3.14 當月日期範圍 ─────────────────────────────────
def get_month_range(start: date | None = None) -> tuple[date, date]:
    # 若未傳入 start，預設取「今天所在月份的第一天」。
    # replace(day=1) 常用來快速對齊到月初。
    if start is None:
        start = date.today().replace(day=1)

    # monthrange(year, month) 回傳 (weekday_of_first_day, days_in_month)
    # 例如 2012/8 會得到 (2, 31)，表示該月有 31 天。
    _, days = monthrange(start.year, start.month)

    # 這裡回傳的是半開區間 [start, end)：
    # - start 為月初
    # - end 為「下個月月初」
    # 這種表示法很適合做迴圈與區間判斷，邏輯通常更乾淨。
    return start, start + timedelta(days=days)


first, last = get_month_range(date(2012, 8, 1))
# 因為 last 是「下個月月初」，所以若要顯示本月最後一天，
# 需再減去 1 天。
print(first, "~", last - timedelta(days=1))  # 2012-08-01 ~ 2012-08-31


# 通用日期迭代生成器
def date_range(start: datetime, stop: datetime, step: timedelta):
    # 這是「逐步遞增」的時間序列產生器：
    # 每次產生目前 start，然後往前加上 step。
    # 條件採用 start < stop，因此 stop 本身不會被包含（半開區間）。
    while start < stop:
        yield start
        start += step


for d in date_range(datetime(2012, 9, 1), datetime(2012, 9, 2), timedelta(hours=6)):
    print(d)
# 2012-09-01 00:00:00 / 06:00 / 12:00 / 18:00

# ── 3.15 字串轉換為日期 ───────────────────────────────
text = "2012-09-20"

# strptime: string parse time
# 依照格式樣板把字串解析成 datetime。
# %Y=四位年、%m=兩位月、%d=兩位日。
dt = datetime.strptime(text, "%Y-%m-%d")
print(dt)  # 2012-09-20 00:00:00

# strftime: string format time
# 把 datetime 格式化成可讀字串。
# %A=星期全名、%B=月份全名、%d=日、%Y=四位年。
print(datetime.strftime(dt, "%A %B %d, %Y"))  # 'Thursday September 20, 2012'


# 手動解析（比 strptime 快 7 倍）
def parse_ymd(s: str) -> datetime:
    # 對固定格式 YYYY-MM-DD，手動 split + int 轉型通常更快。
    # 但可讀性與彈性較低，僅建議在高頻解析、已知格式固定時使用。
    y, m, d = s.split("-")
    return datetime(int(y), int(m), int(d))


print(parse_ymd("2012-09-20"))  # 2012-09-20 00:00:00
