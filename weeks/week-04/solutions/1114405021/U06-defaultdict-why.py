# U6. defaultdict 為何比手動初始化乾淨（1.6）
# 說明：本程式比較「手動檢查 key 是否存在」與「使用 defaultdict」
# 兩種方式來處理「將值群組到對應的 key」的情境
# defaultdict 的優點：省去重複的 if 判斷，程式碼更簡潔

# 匯入 collections 模組中的 defaultdict 類別
from collections import defaultdict

# 定義要分組的鍵值對列表
# 目標：將相同 key 的值收集在一起
# 例如：'a' 對應 [1, 2]，'b' 對應 [3]
pairs = [("a", 1), ("a", 2), ("b", 3)]

# ===== 1. 手動版本：一直判斷 key 是否存在 =====

# 建立一個空字典
d = {}

# 遍歷每一個鍵值對
for k, v in pairs:
    # 每次迭代都要檢查 key 是否已存在
    if k not in d:
        # 若 key 不存在，需要先初始化一個空列表
        d[k] = []
    # 然後再將值加入列表
    d[k].append(v)

# 結果：d = {'a': [1, 2], 'b': [3]}
# 缺點：
# - 需要寫 if 判斷（樣板程式碼）
# - 若有多個這樣的場景，需要重複相同的判斷邏輯
# - 程式碼較長，可讀性較差

# ===== 2. defaultdict 版本：省掉初始化分支 =====

# 建立一個 defaultdict，指定預設值型別為 list
# 語法：defaultdict(工廠函數)
# - 工廠函數：當訪問不存在的 key 時，會自動呼叫這個函數來產生預設值
# - list 是工廠函數，呼叫 list() 會產生空列表 []
d2 = defaultdict(list)

# 遍歷每一個鍵值對
for k, v in pairs:
    # 當 d2[k] 中的 k 不存在時，defaultdict 會自動：
    # 1. 呼叫 list() 產生空列表 []
    # 2. 將這個空列表 assign 給 d2[k]
    # 3. 然後再執行 append(v)
    # 因此不需要手動檢查 key 是否存在
    d2[k].append(v)

# 結果：d2 = {'a': [1, 2], 'b': [3]}
# 優點：
# - 不需要 if 判斷
# - 程式碼更簡潔、更易讀
# - 避免遺漏初始化導致的錯誤

# ===== 3. defaultdict 的運作原理 =====

# defaultdict 的關鍵在於「工廠函數」：
# - defaultdict(list)  → 預設值是空列表 []
# - defaultdict(int)  → 預設值是 0（常用於計數）
# - defaultdict(set)  → 預設值是空集合 set()

# 當訪問一個不存在的 key 時：
# 1. defaultdict 會呼叫工廠函數產生預設值
# 2. 將 key 和預設值加入字典
# 3. 回傳這個預設值

# ===== 4. defaultdict(int) 的常見應用 =====

# 計算每個單字出現的次數
# words = ['apple', 'banana', 'apple', 'orange', 'banana', 'apple']
# word_count = defaultdict(int)
# for word in words:
#     word_count[word] += 1
# 結果：{'apple': 3, 'banana': 2, 'orange': 1}
# 若使用普通字典需要：if word not in d: d[word] = 0; d[word] += 1
