# U06. 時區操作最佳實踐：UTC 優先（3.16）
#
# 這份範例要傳達的核心觀念是：
# 1. 只要涉及跨時區或長時間運算，內部資料最好都先轉成 UTC。
# 2. 本地時間可能遇到夏令時間（DST）跳轉，會出現不存在或重複的時刻。
# 3. 顯示給使用者時，再把 UTC 轉回目標時區即可。

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# UTC 用來做內部運算與儲存，因為它沒有夏令時間切換問題。
utc = ZoneInfo("UTC")
# 這裡選用美國中部時區，方便示範夏令時間開始時的跳時現象。
central = ZoneInfo("America/Chicago")

# 問題：直接在本地時間做加減，碰到夏令時間邊界時可能產生不存在的時間。
# 美國 2013-03-10 凌晨 2:00 時鐘會往前撥到 3:00，也就是 2:00 到 2:59 這段時間根本不存在。
local_dt = datetime(2013, 3, 10, 1, 45, tzinfo=central)
# 直接在本地時間上加 30 分鐘，表面上看起來合理，但結果會落到不存在的 2:15。
wrong = local_dt + timedelta(minutes=30)
print(f"錯誤結果：{wrong}")  # 2:15（不存在的時間！）

# 正確做法：先把時間轉成 UTC，再做加減，最後要顯示時再轉回本地時區。
# 這樣的流程可以避免在 DST 轉換點踩到不存在的時刻。
utc_dt = local_dt.astimezone(utc)
# 這裡先在 UTC 中加 30 分鐘，因為 UTC 沒有夏令時間跳動，所以結果是連續且穩定的。
correct = utc_dt + timedelta(minutes=30)
print(f"正確結果：{correct.astimezone(central)}")  # 3:15（跳過了 2:xx）

# 最佳實踐：輸入 → 轉成帶時區的時間 → 轉 UTC 儲存/計算 → 顯示時再轉回當地時區。
#
# 這個流程的好處是：
# 1. 資料庫或內部邏輯只需要處理一種標準時間格式。
# 2. 不同地區的使用者可以各自看到符合自己時區的時間。
# 3. 避免把「沒有時區資訊的字串」直接當成某個地點的真實時間而造成誤判。
user_input = "2012-12-21 09:30:00"
# strptime() 先把字串解析成 naive datetime，也就是「沒有時區」的時間物件。
# 這個時間本身只代表一個年月日時分秒，還不能確定它屬於哪個地區。
naive = datetime.strptime(user_input, "%Y-%m-%d %H:%M:%S")
# replace(tzinfo=...) 只是替這個時間「標記」它屬於某個時區，並不是做時區換算。
# 這一步適合在你已經知道原始時間是哪個地區時使用。
# 接著 astimezone(utc) 才是真正把它轉成 UTC。
aware = naive.replace(tzinfo=central).astimezone(utc)
print(f"存 UTC：{aware}")
# 顯示給使用者時，再轉回目標時區，例如台北時間。
# 這樣後端只存一份標準時間，前端或輸出層再依需求轉換即可。
print(f"顯示台北：{aware.astimezone(ZoneInfo('Asia/Taipei'))}")
