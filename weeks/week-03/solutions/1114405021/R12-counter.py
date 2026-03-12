# R12. Counter 統計 + most_common（1.12）

from collections import Counter

# Counter 是專門做「元素次數統計」的字典子類別。
# 可以把它想成：元素 -> 出現次數。
words = ['look', 'into', 'my', 'eyes', 'look']

# 建立統計結果。
# 這裡會得到類似：{'look': 2, 'into': 1, 'my': 1, 'eyes': 1}
word_counts = Counter(words)

# most_common(n)：回傳前 n 個最常出現元素。
# 回傳型別是 list，元素是 (元素, 次數) tuple。
# 例如可能是：[('look', 2), ('into', 1), ('my', 1)]
word_counts.most_common(3)

# update(iterable)：把新資料加進既有 Counter，次數會累加。
# 這裡多加入兩個 'eyes'，所以 'eyes' 計數會 +2。
word_counts.update(['eyes', 'eyes'])

# 閱讀重點：
# 1) 先看原始資料有哪些元素
# 2) 再看 Counter 轉換後每個元素的頻率
# 3) most_common 是查詢，不會重設計數
# 4) update 是累加，不是覆蓋
