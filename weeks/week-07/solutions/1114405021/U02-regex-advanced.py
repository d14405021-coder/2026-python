# U02. 正則表達式進階技巧（2.4–2.6）
#
# 這份範例主要示範三件事：
# 1. 正則表達式如果會重複使用，先 compile() 預編譯通常比較有效率。
# 2. re.sub() 不一定只能接字串，也可以接回呼函數，讓替換邏輯更彈性。
# 3. 如果你要替換的文字需要保留原本的大小寫風格，可以用自訂函數判斷後再輸出。

import re
import timeit
from calendar import month_abbr

# ── 預編譯效能（2.4）──────────────────────────────────
#
# 這段是在比較兩種寫法：
# 1. 每次都直接呼叫 re.findall()，讓 re 每次重新處理樣式。
# 2. 先用 re.compile() 把樣式編譯成 regex 物件，之後重複使用。
#
# 當你在迴圈、服務請求、或大量資料處理中反覆使用同一個模式時，
# 預編譯通常能減少額外開銷。差距不一定在每個場景都很大，但在大量重複呼叫時會更明顯。
text = "Today is 11/27/2012. PyCon starts 3/13/2013."
datepat = re.compile(r"(\d+)/(\d+)/(\d+)")


def using_module():
    # 直接使用 re.findall()：每次呼叫時，模組都要再處理一次模式字串。
    return re.findall(r"(\d+)/(\d+)/(\d+)", text)


def using_compiled():
    # 使用預先編譯好的 regex 物件：模式已經準備好，可以直接拿來找資料。
    return datepat.findall(text)


t1 = timeit.timeit(using_module, number=50_000)
t2 = timeit.timeit(using_compiled, number=50_000)
# 這裡印出兩種寫法的時間，方便你觀察預編譯是否真的更快。
print(f"直接呼叫: {t1:.3f}s  預編譯: {t2:.3f}s")


# ── sub 回呼函數（2.5）────────────────────────────────
#
# re.sub() 的第二個參數不一定要是固定字串。
# 如果替換內容要根據「每次匹配到的文字」動態生成，就可以傳入函數。
# 函數會收到 match 物件，讓你能讀取每個群組，並組出想要的結果。
def change_date(m: re.Match) -> str:
    # month_abbr 是月份縮寫表，索引 1 對應 Jan、2 對應 Feb，以此類推。
    # m.group(1) 是月份、m.group(2) 是日期、m.group(3) 是年份。
    mon_name = month_abbr[int(m.group(1))]
    return f"{m.group(2)} {mon_name} {m.group(3)}"


# 將 mm/dd/yyyy 轉成 dd Mon yyyy。
# 例如 11/27/2012 會變成 27 Nov 2012。
print(datepat.sub(change_date, text))
# 'Today is 27 Nov 2012. PyCon starts 13 Mar 2013.'


# ── 保持大小寫一致的替換（2.6）───────────────────────
#
# 這個技巧的核心是：先定義一個工廠函數 matchcase()，
# 它會回傳真正給 re.sub() 使用的 replace()。
# replace() 每次拿到匹配結果後，先觀察原字串的大小寫型態，
# 再把新字串轉成對應形式，這樣就能保留原本文字的視覺風格。
def matchcase(word: str):
    def replace(m: re.Match) -> str:
        # m.group() 會拿到實際匹配到的文字，例如 "PYTHON"、"python" 或 "Python"。
        t = m.group()
        # 如果原文是全大寫，就把替換字也轉成全大寫。
        if t.isupper():
            return word.upper()
        # 如果原文是全小寫，就把替換字也轉成全小寫。
        if t.islower():
            return word.lower()
        # 如果第一個字母是大寫，通常代表這是一個首字大寫的專有名詞風格。
        if t[0].isupper():
            return word.capitalize()
        # 其他情況就維持原本傳入的樣子，不額外更動。
        return word

    return replace


s = "UPPER PYTHON, lower python, Mixed Python"
# IGNORECASE 讓正則不分大小寫地找出 python。
# matchcase("snake") 會依照每次匹配到的原文大小寫，動態回傳 snake / SNAKE / Snake。
print(re.sub("python", matchcase("snake"), s, flags=re.IGNORECASE))
# 'UPPER SNAKE, lower snake, Mixed Snake'
