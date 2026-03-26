# R07. 日期時間基本運算（3.12–3.13）
# timedelta 加減 / weekday() 計算指定星期

from datetime import datetime, timedelta

# ── 3.12 timedelta 基本運算 ───────────────────────────
# timedelta 代表「時間差」，可用天、小時、分鐘等組成。
# 這裡 a = 2 天 6 小時。
a = timedelta(days=2, hours=6)

# 這裡 b = 4.5 小時（也就是 4 小時 30 分）。
b = timedelta(hours=4.5)

# 兩個 timedelta 可以直接相加，得到新的時間差物件。
c = a + b

# c.days 只會回傳「整天數」部分，不含剩餘小時。
print(c.days)  # 2

# total_seconds() 會回傳完整秒數（含天數），
# 除以 3600 可換算成總小時數，這通常比只看 days 更完整。
print(c.total_seconds() / 3600)  # 58.5

dt = datetime(2012, 9, 23)

# datetime + timedelta 可得到「往後推算」的日期時間。
print(dt + timedelta(days=10))  # 2012-10-03 00:00:00

d1, d2 = datetime(2012, 9, 23), datetime(2012, 12, 21)

# 兩個 datetime 相減會得到 timedelta，
# 取 .days 可得相差天數（整天）。
print((d2 - d1).days)  # 89

# 閏年自動處理
# datetime 的日期運算會自動處理閏年規則：
# - 2012 是閏年，2 月有 29 天
# - 2013 是平年，2 月有 28 天
print((datetime(2012, 3, 1) - datetime(2012, 2, 28)).days)  # 2（閏年）
print((datetime(2013, 3, 1) - datetime(2013, 2, 28)).days)  # 1（平年）

# ── 3.13 計算指定星期日期 ─────────────────────────────
# Python 的 weekday() 規則：
# Monday=0, Tuesday=1, ..., Sunday=6
# 下面用對照表把英文星期名稱轉成索引值。
WEEKDAYS = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]


def get_previous_byday(dayname: str, start: datetime | None = None) -> datetime:
    # 若未提供起始日期，預設使用今天。
    if start is None:
        start = datetime.today()

    # start 的星期索引（0~6）
    day_num = start.weekday()

    # 目標星期索引（例如 "Monday" -> 0）
    target = WEEKDAYS.index(dayname)

    # 核心公式：
    # (7 + day_num - target) % 7 會得到「往回幾天可到目標星期」。
    # 但若剛好是同一天（結果為 0），題意通常要「上一個」而非「今天」，
    # 所以用 `or 7` 把 0 轉成 7，代表往前一週。
    days_ago = (7 + day_num - target) % 7 or 7

    # 從 start 往回減去對應天數，即可得到上一個指定星期。
    return start - timedelta(days=days_ago)


base = datetime(2012, 8, 28)  # 週二
# 2012-08-28 是星期二，上一個星期一是 2012-08-27。
print(get_previous_byday("Monday", base))  # 2012-08-27
# 同理，上一個星期五是 2012-08-24。
print(get_previous_byday("Friday", base))  # 2012-08-24
