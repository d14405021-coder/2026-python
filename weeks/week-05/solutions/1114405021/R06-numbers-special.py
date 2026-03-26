# R06. 特殊數值：無窮大、NaN、分數、隨機（3.7–3.11）
# float inf/nan / fractions.Fraction / random

import math
import random
from fractions import Fraction

# ── 3.7 無窮大與 NaN ──────────────────────────────────
# float("inf")、float("-inf")、float("nan") 是 IEEE 754 常見特殊值：
# - inf：正無窮大
# - -inf：負無窮大
# - nan：Not a Number，通常來自未定義運算（例如 0/0）
a = float("inf")
b = float("-inf")
c = float("nan")
print(a, b, c)  # inf -inf nan

# 判斷特殊值時，請使用 math.isinf()/math.isnan()，
# 不要用一般比較運算直接判斷。
print(math.isinf(a))  # True
print(math.isnan(c))  # True

# 與無窮大運算的直覺：
# - inf + 有限數 = inf
# - 有限數 / inf = 0.0（趨近於 0）
print(a + 45, 10 / a)  # inf 0.0

# 某些涉及「無窮大互相抵銷」的運算是未定義，因此得到 nan。
print(a / a, a + b)  # nan nan（未定義）

# NaN 有一個很重要的特性：它不等於任何值，包含它自己。
# 因此 `c == c` 會是 False，實務上要用 math.isnan(c) 檢查。
print(c == c)  # False（NaN 不等於自己！）

# ── 3.8 分數運算 ──────────────────────────────────────
# Fraction 用「分子/分母」做精確有理數運算，
# 適合避免浮點誤差（例如金額比例、數學推導）。
p = Fraction(5, 4)
q = Fraction(7, 16)
r = p * q

# Fraction 之間加減乘除都會維持精確分數結果。
print(p + q)  # 27/16

# 可直接取得分子與分母，便於拆解或顯示。
print(r.numerator, r.denominator)  # 35 64

# 若要給一般 float API 使用，可再轉成 float。
print(float(r))  # 0.546875

# limit_denominator(max_denominator) 會尋找「最接近」的簡潔分數表示。
# 這裡把 35/64 近似成分母不超過 8 的分數，得到 4/7。
print(r.limit_denominator(8))  # 4/7

# float.as_integer_ratio() 可把浮點數拆成精確整數比值 (num, den)，
# 再交給 Fraction 建立，保留該浮點值在記憶體中的精確比例。
print(Fraction(*(3.75).as_integer_ratio()))  # 15/4

# ── 3.11 隨機選擇 ─────────────────────────────────────
values = [1, 2, 3, 4, 5, 6]

# choice(seq)：從序列中「隨機挑 1 個」元素。
print(random.choice(values))  # 隨機一個

# sample(seq, k)：抽 k 個「不重複」樣本，不改動原序列。
print(random.sample(values, 3))  # 3 個不重複樣本

# shuffle(list)：原地打亂（in-place），會直接改變 values 本身。
random.shuffle(values)
print(values)  # 打亂後的序列

# randint(a, b)：含頭含尾，會產生 [a, b] 之間的整數。
print(random.randint(0, 10))  # 0~10 整數

# 設定固定 seed 可讓亂數序列可重現，便於測試與除錯。
random.seed(42)
print(random.random())  # 固定種子：可重現
