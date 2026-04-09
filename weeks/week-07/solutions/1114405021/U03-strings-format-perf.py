# U03. 字串格式化效能與陷阱（2.14–2.20）
#
# 這份範例主要在示範三個常見重點：
# 1. 大量串接字串時，使用 join() 通常比反覆用 + 更有效率。
# 2. format_map() 搭配 __missing__ 可以在資料缺欄位時保留占位符，不會直接報錯。
# 3. bytes 與 str 的索引結果不同，這是處理文字與位元資料時很容易踩到的差異。

import timeit

# ── join 效能優於 + （2.14）──────────────────────────
#
# 這段是在比較兩種組字串的方式：
# 1. 在迴圈裡一直做 s += p。
# 2. 先把所有片段放進列表，再用 "".join(parts) 一次接起來。
#
# 第一種寫法每次都會建立新的字串物件，資料量一大時會反覆複製內容，成本很高。
# 第二種寫法由 join() 一次完成配置與合併，通常會明顯比較快，也更適合大量片段。
parts = [f"item{i}" for i in range(1000)]


def bad_concat():
    # 這是刻意示範的「較差」寫法：每次迴圈都產生新字串。
    # 字串是不可變物件，所以 s += p 不是原地修改，而是建立一個新結果再指回 s。
    s = ""
    for p in parts:
        s += p  # 每次建立新字串，資料越多越慢，整體接近 O(n²)
    return s


def good_join():
    # 這是建議寫法：先準備好片段，再交給 join() 統一串接。
    # join() 會先估算總長度，再一次完成輸出，通常是線性時間 O(n)。
    return "".join(parts)  # 一次分配，O(n)


t1 = timeit.timeit(bad_concat, number=500)
t2 = timeit.timeit(good_join, number=500)
# 印出兩種方法的執行時間，方便觀察差距。
print(f"+串接: {t1:.3f}s  join: {t2:.3f}s")


# ── format_map 處理缺失鍵（2.15）─────────────────────
#
# format_map() 的好處是它能直接接受映射物件，例如 dict 或其子類別。
# 如果模板字串裡用了某個鍵，但資料沒有提供，預設情況下會拋出 KeyError。
# 這裡透過 __missing__ 自訂缺失鍵行為：當欄位不存在時，不報錯，改回傳原本的 {key}。
class SafeSub(dict):
    def __missing__(self, key: str) -> str:
        # 把找不到的欄位原樣保留下來，方便你之後再補值或做除錯。
        return "{" + key + "}"  # 缺失時保留佔位符


name = "Guido"
s = "{name} has {n} messages."
# vars() 會回傳目前區域變數組成的字典，因此 SafeSub(vars()) 可以同時讀到 name 等變數。
# 由於 n 不存在，__missing__ 會介入並保留 {n}，所以整個格式化過程不會失敗。
print(s.format_map(SafeSub(vars())))  # 'Guido has {n} messages.'（n 不存在也不報錯）

# ── bytes 索引回傳整數（2.20）────────────────────────
#
# 這段要強調 str 與 bytes 的索引結果不同：
# 1. str[0] 取到的是字元字串。
# 2. bytes[0] 取到的是整數，代表對應位元組的數值。
#
# 這個差異在處理檔案、網路封包、編碼轉換時非常重要，因為 bytes 比較接近原始資料。
a = "Hello"
b = b"Hello"
print(a[0])  # 'H'（字元）
print(b[0])  # 72（整數 = ord('H')）

# bytes 不能直接 format，通常要先對字串完成格式化，再轉成 bytes。
# 也就是先處理文字排版，再 encode 成 ASCII 或 UTF-8 等編碼。
print("{:10s} {:5d}".format("ACME", 100).encode("ascii"))
# b'ACME            100'
