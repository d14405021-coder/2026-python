# R13. 字典列表排序 itemgetter（1.13）

from operator import itemgetter

# rows 是「字典組成的清單」，每筆資料都有 fname 與 uid 欄位
rows = [{'fname': 'Brian', 'uid': 1003}, {'fname': 'John', 'uid': 1001}]

# 1) 依 fname（名字）排序
# key=itemgetter('fname') 代表每筆資料用 row['fname'] 當比較鍵
# sorted 會回傳新清單，不會改動原本 rows
sorted(rows, key=itemgetter('fname'))

# 2) 依 uid（數字 ID）排序
# 這行會按照 uid 由小到大排列
sorted(rows, key=itemgetter('uid'))

# 3) 多欄位排序（先 uid，再 fname）
# itemgetter('uid', 'fname') 會回傳 tuple： (row['uid'], row['fname'])
# Python 會先比 tuple 第 1 欄，若相同再比第 2 欄
sorted(rows, key=itemgetter('uid', 'fname'))

# 閱讀重點：
# 1) 先找 key= 後面指定哪個欄位
# 2) 若是多欄位，理解成「主排序鍵 + 次排序鍵」
# 3) sorted 是非原地排序；若要原地排序可用 rows.sort(...)
