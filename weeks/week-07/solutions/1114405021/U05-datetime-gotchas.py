# U05. 日期時間的陷阱（3.12–3.15）
#
# 這份範例主要在示範兩個常見問題：
# 1. timedelta 只能表示固定長度的時間差，不能直接用「月份」這種不固定長度的單位。
# 2. datetime.strptime() 很方便，但在大量解析日期字串時，手動拆字串通常會更快。

import timeit
import calendar
from datetime import datetime, timedelta

# ── timedelta 不支援月份（3.12）──────────────────────
#
# timedelta 的設計是給「天數、秒數、微秒」這種固定長度的時間差使用。
# 但月份長度不固定，有 28、29、30、31 天，因此它無法直接接受 months=1。
# 這也是為什麼把「加一個月」交給 timedelta 會失敗。
dt = datetime(2012, 9, 23)
try:
    dt + timedelta(months=1)  # type: ignore[call-arg]
except TypeError as e:
    # 這裡刻意示範錯誤，讓你看到 months 不是 timedelta 支援的參數。
    print(f"TypeError: {e}")  # 'months' is an invalid keyword argument


# 正確做法：如果你真的要「加一個月」，就必須自己處理月份進位與天數邊界。
#
# 做法是：
# 1. 先算出目標年份與月份。
# 2. 用 calendar.monthrange() 查出那個月有幾天。
# 3. 如果原本日期超過該月最大天數，就把日期壓到最後一天。
#
# 這個「壓到合法範圍」的動作通常稱為 clamp。
def add_one_month(dt: datetime) -> datetime:
    # 先把年月拆開，準備往下一個月前進。
    year = dt.year
    month = dt.month + 1
    # 如果 12 月再往後加一個月，就要進到下一年 1 月。
    if month == 13:
        year += 1
        month = 1

    # monthrange() 會回傳該月的星期資訊與天數，這裡只需要天數。
    # 例如 2012-02 會回傳 29 天，因為 2012 是閏年。
    _, days_in_target_month = calendar.monthrange(year, month)
    # 如果原日期是 31 號，但目標月份只有 30 天或 28 天，就要調整到最後一天。
    day = min(dt.day, days_in_target_month)

    # 用 replace() 建立新的日期物件，只改年月日，不改原本的時分秒。
    return dt.replace(year=year, month=month, day=day)


# 2012-01-31 加一個月後應該變成 2012-02-29，而不是不存在的 2012-02-31。
# 2012-09-23 加一個月後則是 2012-10-23。
print(add_one_month(datetime(2012, 1, 31)))  # 2012-02-29
print(add_one_month(datetime(2012, 9, 23)))  # 2012-10-23

# ── strptime 效能問題（3.15）─────────────────────────
#
# strptime() 的優點是語意清楚，格式驗證也完整；缺點是它做了不少解析與格式檢查工作，
# 因此在大量資料重複轉換時，速度可能不如你自己先把固定格式拆開再建構 datetime。
dates = [f"2012-{m:02d}-{d:02d}" for m in range(1, 13) for d in range(1, 29)]


def use_strptime(s: str) -> datetime:
    # 直接交給標準庫解析，最簡潔，但通常不是最快。
    return datetime.strptime(s, "%Y-%m-%d")


def use_manual(s: str) -> datetime:
    # 如果輸入格式固定且可控，手動 split 後轉成整數，通常會比 strptime 更快。
    # 這種方法犧牲了一點通用性，換來更高的效能。
    y, m, d = s.split("-")
    return datetime(int(y), int(m), int(d))


# 先確認兩種方法對同一筆資料會產生相同結果，避免只是跑得快但結果不一樣。
assert use_strptime("2012-09-20") == use_manual("2012-09-20")

# 用 timeit 跑大量樣本，觀察兩種做法的速度差距。
# 這裡的重點不是絕對數字，而是讓你看到固定格式資料常常可以用更簡單的方式加速。
t1 = timeit.timeit(lambda: [use_strptime(d) for d in dates], number=100)
t2 = timeit.timeit(lambda: [use_manual(d) for d in dates], number=100)
# 印出比較結果，方便直觀看出手動解析通常更快。
print(f"strptime: {t1:.3f}s  手動解析: {t2:.3f}s（快 {t1 / t2:.1f} 倍）")
