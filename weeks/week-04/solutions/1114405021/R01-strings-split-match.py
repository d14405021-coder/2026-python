# R01. 字串分割與匹配（2.1–2.3）
# 說明：本程式示範 Python 中常用的「字串分割」與「模式匹配」技巧
# 包含：re.split() 多分隔符分割、startswith/endswith 前後綴匹配、fnmatch 通配符匹配

# 匯入 re 模組：Python 標準的正規表達式模組
# re.split() 可用正規表達式作為分隔符，支援多種分隔符同時使用
import re

# 匯入 fnmatch 模組：用於「Shell 風格」的簡單萬用字元匹配
# fnmatch：會根據作業系統的語言設定決定是否區分大小寫
# fnmatchcase：強制區分大小寫
from fnmatch import fnmatch, fnmatchcase

# ═══════════════════════════════════════════════════════════
# 2.1 多界定符分割
# ═══════════════════════════════════════════════════════════

# 定義一個包含多種分隔符的字串
# 分隔符包括：分號(;)、逗號(,)、空白字元(\s)
line = "asdf fjdk; afed, fjek,asdf, foo"

# 使用 re.split() 搭配正規表達式分割字串
# 正規表達式：[;,\s]\s*
# - [;,\s]：匹配分號、逗號、或任何空白字元（空格、Tab 等）
# - \s*：匹配分隔符後面零或多個空白字元（用來去除多餘空格）
print(re.split(r"[;,\s]\s*", line))
# 結果：['asdf', 'fjdk', 'afed', 'fjek', 'asdf', 'foo']

# ── 非捕獲分組：分組但不保留分隔符 ──

# 使用「非捕獲分組 (?:...)」的寫法
# 正規表達式：(?:,|;|\s)\s*
# - (?:...)：非捕獲分組，不會將這部分作為單獨的群組捕獲
# - ,|;|\s：匹配逗號、分號、或空白字元（豎線 | 表示「或」）
# 結果與上一行相同，但語義更明確
print(re.split(r"(?:,|;|\s)\s*", line))
# 結果：['asdf', 'fjdk', 'afed', 'fjek', 'asdf', 'foo']

# ═══════════════════════════════════════════════════════════
# 2.2 開頭/結尾匹配
# ═══════════════════════════════════════════════════════════

# 定義檔案名稱
filename = "spam.txt"

# 使用 endswith() 檢查字串是否以指定後綴結尾
print(filename.endswith(".txt"))  # True
# 說明：spam.txt 是否以 ".txt" 結尾 → 是 → True

# 使用 startswith() 檢查字串是否以指定前綴開頭
print(filename.startswith("file:"))  # False
# 說明：spam.txt 是否以 "file:" 開頭 → 否 → False

# ── 同時檢查多種後綴 → 傳入 tuple（不能傳 list）─

# 定義多個檔案名稱列表
filenames = ["Makefile", "foo.c", "bar.py", "spam.c", "spam.h"]

# 使用列表推導式過濾出特定後綴的檔案
# endswith() 接受一個「tuple」作為參數，可以同時檢查多種後綴
# 注意：必須是 tuple，不能是 list！
print([name for name in filenames if name.endswith((".c", ".h"))])
# 結果：['foo.c', 'spam.c', 'spam.h']
# 說明：找出所有以 .c 或 .h 結尾的檔案

# 為何要用 tuple 而非 list？
# 因為 endswith() 內部會檢查參數型別，若傳入 list 可能導致意外行為
# tuple 是不可變的，更安全

# ═══════════════════════════════════════════════════════════
# 2.3 Shell 通配符匹配
# ═══════════════════════════════════════════════════════════

# 使用 fnmatch() 進行「Shell 風格」的簡單模式匹配
# fnmatch 支援以下萬用字元：
# - *：匹配任意字元（零個或多個）
# - ?：匹配任意單一字元
# - [seq]：匹配 seq 中的任意單一字元
# - [!seq]：匹配不在 seq 中的任意單一字元

print(fnmatch("foo.txt", "*.txt"))  # True
# 說明："foo.txt" 是否符合 "*.txt"（任意字元 + .txt）→ 是 → True

print(fnmatch("Dat45.csv", "Dat[0-9]*"))  # True
# 說明："Dat45.csv" 是否符合 "Dat[0-9]*"
# - Dat：必須以 "Dat" 開頭
# - [0-9]：第二位是數字（0-9）
# - *：後面可以是任意字元
# → "Dat45.csv" 符合條件 → True

# ── fnmatchcase 強制區分大小寫 ──

# fnmatch 會根據作業系統的語言設定決定是否區分大小寫
# fnmatchcase 會嚴格區分大小寫

print(fnmatchcase("foo.txt", "*.TXT"))  # False
# 說明："foo.txt" 是否符合 "*.TXT"（嚴格大小寫）
# .txt 與 .TXT 不同 → False

# 若在 Windows 上，fnmatch 可能也會回傳 True（不區分大小寫）
# fnmatchcase 可確保跨平台一致性

# ── 實際應用：地址篩選 ──

# 定義一個地址列表
addresses = ["5412 N CLARK ST", "1060 W ADDISON ST", "1039 W GRANVILLE AVE"]

# 使用 fnmatchcase 篩選以 " ST" 結尾的地址（結尾是空白 + ST）
print([a for a in addresses if fnmatchcase(a, "* ST")])
# 結果：['5412 N CLARK ST', '1060 W ADDISON ST']
# 說明：第三個地址 "1039 W GRANVILLE AVE" 不以 " ST" 結尾，被過濾掉
