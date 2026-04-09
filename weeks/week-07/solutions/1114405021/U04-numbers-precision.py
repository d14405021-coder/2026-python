# U04. 數字精度的陷阱與選擇（3.1–3.7）
#
# 這份範例主要在示範三個重點：
# 1. Python 內建 round() 並不是一般人直覺上的四捨五入，而是銀行家捨入。
# 2. NaN 不是任何值的「相等對象」，所以不能用 == 來判斷是否為 NaN。
# 3. float 較快但會有二進位浮點誤差；Decimal 較精確但通常比較慢，適合金融與會計場景。

import math
import timeit
from decimal import Decimal, ROUND_HALF_UP

# ── 銀行家捨入（3.1）─────────────────────────────────
#
# round() 的行為很常讓人誤會。很多人以為 0.5 會進位成 1，2.5 會進位成 3，
# 但 Python 預設採用的是「四捨六入五取偶」，也就是遇到剛好一半時，會往最接近的偶數靠。
# 這樣做的目的，是在大量統計時減少長期偏差。
print(round(0.5))  # 0（不是 1！）
print(round(2.5))  # 2（不是 3！）
print(round(3.5))  # 4


# 如果你要的是日常最常見的「四捨五入」，不要直接依賴 round()。
# 比較穩定的作法是搭配 Decimal 與 ROUND_HALF_UP，明確指定捨入規則。
def trad_round(x: float, n: int = 0) -> Decimal:
    # 先把 float 轉成字串，再交給 Decimal。
    # 這樣可以避免直接用 Decimal(0.1) 時，吃進二進位浮點本身的表示誤差。
    d = Decimal(str(x))
    # quantize() 需要一個目標格式，n=0 代表整數，n>0 代表小數點後保留 n 位。
    fmt = Decimal("1") if n == 0 else Decimal("0." + "0" * n)
    # ROUND_HALF_UP 就是一般人熟悉的四捨五入規則。
    return d.quantize(fmt, rounding=ROUND_HALF_UP)


print(trad_round(0.5))  # 1
print(trad_round(2.5))  # 3

# ── NaN 無法用 == 比較（3.7）─────────────────────────
#
# NaN 的意思是「Not a Number」，通常代表無效的數值結果，例如除以零或未定義的運算。
# 這種值有一個特殊規則：它不等於任何東西，甚至連它自己也不等於自己。
# 所以你不能用 x == x 來判斷 NaN，而應該用 math.isnan(x)。
c = float("nan")
print(c == c)  # False（自己不等於自己！）
print(c == float("nan"))  # False
# math.isnan() 才是檢查 NaN 的正確方式。
print(math.isnan(c))  # True（唯一正確的檢測方式）

# 當資料裡可能夾雜 NaN 時，先過濾再運算通常比較安全。
# 這裡用串列生成式把所有不是 NaN 的值留下來。
data = [1.0, float("nan"), 3.0, float("nan"), 5.0]
clean = [x for x in data if not math.isnan(x)]
print(clean)  # [1.0, 3.0, 5.0]

# ── float vs Decimal 選擇（3.2）──────────────────────
#
# float 的優點是速度快、記憶體占用小，適合科學運算、圖形處理、工程計算等情境。
# 它的缺點是很多十進位小數無法被二進位浮點完全精準表示，所以會出現看似奇怪的尾數誤差。
print(0.1 + 0.2)  # 0.30000000000000004
print(0.1 + 0.2 == 0.3)  # False

# Decimal 則是用十進位方式表示數字，適合需要金額精度的場景，例如金融、會計、報表。
# 它通常比 float 慢，但換來的是可預期、可控的精確度。
print(Decimal("0.1") + Decimal("0.2"))  # 0.3
print(Decimal("0.1") + Decimal("0.2") == Decimal("0.3"))  # True

# 用 timeit 比較兩種型別在大量運算時的速度差異。
# 這裡不是要證明哪個「絕對比較好」，而是要強調：
# 選擇資料型別時，應該依照你更需要「速度」還是「精確度」來決定。
t1 = timeit.timeit(lambda: 0.1 * 999, number=100_000)
t2 = timeit.timeit(lambda: Decimal("0.1") * 999, number=100_000)
# 直接印出比較結果，讓讀者可以觀察 Decimal 通常會慢多少。
print(f"float: {t1:.3f}s  Decimal: {t2:.3f}s（Decimal 約慢 {t2 / t1:.0f} 倍）")
