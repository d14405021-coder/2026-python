# R14. 物件排序 attrgetter（1.14）

from operator import attrgetter

class User:
    def __init__(self, user_id):
    # 每個 User 物件都有一個屬性 user_id
        self.user_id = user_id

# users 是「物件清單」，不是字典清單
users = [User(23), User(3), User(99)]

# attrgetter('user_id') 代表：排序時，從每個物件取 obj.user_id 當比較鍵。
# 等價概念：key=lambda u: u.user_id
#
# sorted 會回傳新的排序後清單，不會改動原本 users。
# 這裡結果順序會是 user_id: 3, 23, 99
sorted(users, key=attrgetter('user_id'))

# 閱讀重點：
# 1) 若資料是 dict，用 itemgetter；若資料是物件屬性，用 attrgetter
# 2) key 負責告訴 sorted「拿哪個欄位/屬性來比較」
# 3) sorted 預設升冪（小到大）；若要降冪可加 reverse=True
