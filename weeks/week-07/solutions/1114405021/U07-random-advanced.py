# U07. 隨機種子與安全亂數（3.11）
#
# 這份範例主要在示範兩個概念：
# 1. random 模組產生的是「偽隨機」，只要種子相同，輸出序列就會完全一樣。
# 2. 如果用途涉及密碼、token、session key 等安全需求，應改用 secrets，而不是 random。

import random
import secrets

# 相同種子 → 相同序列（可重現）
#
# random.seed() 會把亂數生成器設定到固定起點。
# 這代表之後生成的數字序列會完全可重現，這對測試、模擬、教學都很有用。
# 但也正因為可預測，所以不適合拿來做安全用途。
random.seed(42)
seq1 = [random.randint(1, 100) for _ in range(5)]
# 再次設成同一個種子後，接下來產生的數字序列會和 seq1 一模一樣。
random.seed(42)
seq2 = [random.randint(1, 100) for _ in range(5)]
# 這裡比較兩次結果是否相同，用來驗證種子控制的是整段亂數流。
print(seq1 == seq2)  # True

# 不同 Random 實例各自獨立
#
# random.Random() 可以建立獨立的亂數生成器實例。
# 這表示每個物件都有自己的狀態，不會互相干擾。
# 當你需要多組彼此隔離的隨機序列時，這種寫法比共用全域 random 狀態更清楚。
rng1 = random.Random(1)
rng2 = random.Random(2)
# 兩個實例使用不同種子，所以一開始產生的數字也不同。
print(rng1.random(), rng2.random())  # 各自的隨機流

# 密碼學安全亂數（不可預測，不能設種子）
#
# secrets 模組是專門為安全用途設計的。
# 它背後使用的來源目標是「不可預測」，因此不能像 random 一樣靠 seed 重現。
# 如果你要產生驗證碼、重設密碼 token、登入 session、一次性連結等資料，應該優先用 secrets。
print(secrets.randbelow(100))  # 密碼學安全整數
# token_hex() 會回傳指定長度的十六進位字串，常用在 token 或識別碼。
print(secrets.token_hex(16))  # 密碼學安全 hex 字串
# token_bytes() 會回傳原始位元組資料，適合需要 bytes 形式金鑰或隨機資料的場景。
print(secrets.token_bytes(16))  # 密碼學安全 bytes

# 重要：random 模組不適合密碼、token、session key 等安全場景。
# 它適合的是遊戲、抽樣、模擬、測試資料生成這類「需要可重現」或「不要求安全性」的用途。
