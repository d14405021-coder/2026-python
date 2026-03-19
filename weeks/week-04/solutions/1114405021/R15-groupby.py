# R15. 分組 groupby（1.15）
# 說明：本程式示範如何使用 itertools 模組中的 groupby 函數
# groupby 可以將可疊代物件（iterable）中的相鄰元素根據指定的鍵值（key）進行分組

# 匯入 itertools 模組中的 groupby 函數
# groupby 是 Python 內建的分組工具，能將序列中相鄰且具有相同鍵值的元素收集在一起
from itertools import groupby

# 匯入 operator 模組中的 itemgetter 函數
# itemgetter 用來定義分組的鍵值（key），比 lambda 更簡潔高效
from operator import itemgetter

# 定義要分組的資料列表，每個元素是一個字典（dict）
# 包含日期（date）和地址（address）兩個欄位
rows = [
    {"date": "07/01/2012", "address": "..."},
    {"date": "07/02/2012", "address": "..."},
]

# 在使用 groupby 之前，必須先對資料依照分組鍵值進行「排序」
# 重要：groupby 只會將「相鄰的」相同鍵值分在一起，若未排序會導致分組錯誤
rows.sort(key=itemgetter("date"))

# 使用 groupby 進行分組
# 語法：groupby(資料, key=分組鍵值函數)
# - rows：要分組的資料列表
# - key=itemgetter('date')：以 'date' 欄位的值作為分組依據
# groupby 會返回一個疊代器（iterator），每個元素是 (鍵值, 該組的疊代器)
for date, items in groupby(rows, key=itemgetter("date")):
    # date：當前分組的鍵值（即日期值）
    # items：該組內所有元素的疊代器，可以用 for 迴圈逐一取出
    for i in items:
        # 在這裡可以對同一組內的每個元素進行處理
        # 例如：列印、計算、或進行其他操作
        pass  # 此處為範例，因此使用 pass 不做任何事
