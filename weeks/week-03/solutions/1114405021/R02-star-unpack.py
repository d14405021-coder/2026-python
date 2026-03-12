# R2. 解包數量不固定：星號解包（1.2）

def drop_first_last(grades):
    # 星號解包：當序列長度不固定時，用 * 接住「剩餘多個值」。
    # 這行代表：
    # first  取得第一個成績
    # last   取得最後一個成績
    # middle 取得中間所有成績（型別一定是 list）
    first, *middle, last = grades

    # 回傳「去頭去尾」後的平均。
    # sum(middle)：中間分數總和
    # len(middle)：中間分數個數
    # 注意：若 middle 為空（例如只給 2 筆資料），會發生除以 0 的錯誤。
    return sum(middle) / len(middle)

record = ('Dave', 'dave@example.com', '773-555-1212', '847-555-1212')
# 這裡示範前面固定欄位 + 後面不固定欄位。
# name 與 email 接前兩格，剩下全部電話都丟進 phone_numbers(list)。
name, email, *phone_numbers = record

# * 也可以放在最前面：
# current 會拿到最後一個值；
# trailing 會拿到前面所有值（list）。
*trailing, current = [10, 8, 7, 1, 9, 5, 10, 3]

# 閱讀這類程式的快速口訣：
# 1) 先找 * 在哪裡（它接住「可變長度」那一段）
# 2) 再看其餘變數固定拿哪幾格
# 3) 最後確認資料量是否足夠，避免解包失敗或後續運算錯誤
