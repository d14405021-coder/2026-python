# R09. 時區操作（3.16）
# zoneinfo（Python 3.9+）取代 pytz

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo, available_timezones

# ZoneInfo 使用 IANA 時區資料庫名稱（例如 "Asia/Taipei"）。
# 這些名稱可正確涵蓋各地歷史時區規則與夏令時間（DST）變化。
utc = ZoneInfo("UTC")
central = ZoneInfo("America/Chicago")
taipei = ZoneInfo("Asia/Taipei")

# 建立帶時區的 datetime
# 這種有 tzinfo 的 datetime 稱為 aware datetime（具時區意識）。
# 與之相對的是 naive datetime（無時區資訊），
# 在跨時區系統中，建議盡量使用 aware datetime。
d = datetime(2012, 12, 21, 9, 30, 0, tzinfo=central)
print(d)  # 2012-12-21 09:30:00-06:00

# 轉換時區
# astimezone() 會把「同一個絕對時間點」轉成目標時區顯示。
# 注意：改變的是顯示用的本地時間，不是事件本身發生時刻。
print(d.astimezone(ZoneInfo("Asia/Kolkata")))  # 2012-12-21 21:00:00+05:30
print(d.astimezone(taipei))  # 2012-12-21 23:30:00+08:00

# 取得當前 UTC 時間
# datetime.now(tz=utc) 直接產生 UTC aware datetime。
# 在後端服務、資料庫儲存、跨地區系統整合中很常見。
now_utc = datetime.now(tz=utc)
print(now_utc)

# 最佳實踐：內部用 UTC，輸出再轉本地
# 實務上常見流程：
# 1) 內部儲存/計算全部用 UTC，避免 DST 與地區差異造成混亂
# 2) 顯示給使用者時再轉成使用者時區
utc_dt = datetime(2013, 3, 10, 7, 45, 0, tzinfo=utc)
print(utc_dt.astimezone(central))  # 2013-03-10 01:45:00-06:00

# 查詢國家時區

# available_timezones() 會回傳可用時區名稱集合。
# 這裡用包含字串篩選，示範如何找出台北相關時區名稱。
tw_zones = [z for z in available_timezones() if "Taipei" in z]
print(tw_zones)  # ['Asia/Taipei']
