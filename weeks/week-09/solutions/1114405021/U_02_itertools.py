# Understand（理解）- itertools 工具函數

# 從 itertools 匯入常見的迭代器工具：
# - islice：對迭代器做切片，不需要先把全部資料轉成 list
# - dropwhile：只要條件為 True 就持續丟棄，直到第一次 False 才開始保留
# - takewhile：只要條件為 True 就持續取值，遇到第一次 False 就停止
# - chain：把多個可迭代物件串成一個連續序列
# - permutations：產生有順序的排列
# - combinations：產生沒有順序差異的組合
from itertools import islice, dropwhile, takewhile, chain, permutations, combinations

print("--- islice() 切片 ---")


def count(n):
    # 這是一個無限生成器：從 n 開始，不斷往上加 1 並 yield 出去。
    # 因為資料無限，所以不能直接把它完整轉成 list。
    i = n
    while True:
        yield i
        i += 1


# 建立一個從 0 開始的無限數列：0, 1, 2, 3, ...
c = count(0)
# islice(c, 5, 10) 代表取出第 5 個到第 9 個元素，end 不包含 10。
# 對這個無限數列來說，結果會是 [5, 6, 7, 8, 9]。
result = list(islice(c, 5, 10))
print(f"islice(c, 5, 10): {result}")

print("\n--- dropwhile() 條件跳過 ---")
# 測試資料：前段有小於 5 的值，後面也有大於與小於 5 的混合。
nums = [1, 3, 5, 2, 4, 6]
# dropwhile(lambda x: x < 5, nums)
# 會先跳過前面所有符合 x < 5 的元素：1、3。
# 一旦遇到第一個不符合條件的元素 5，就開始把後面所有元素都保留下來。
# 所以結果會是 [5, 2, 4, 6]。
result = list(dropwhile(lambda x: x < 5, nums))
print(f"dropwhile(x<5, {nums}): {result}")

print("\n--- takewhile() 條件取用 ---")
# takewhile(lambda x: x < 5, nums)
# 會從頭開始取值，直到第一次遇到不符合條件的元素 5 為止。
# 因此只會取到 [1, 3]。
result = list(takewhile(lambda x: x < 5, nums))
print(f"takewhile(x<5, {nums}): {result}")

print("\n--- chain() 串聯 ---")
# 三個獨立的串列，等一下會用 chain 把它們接成一條連續序列。
a = [1, 2]
b = [3, 4]
c = [5]
# chain(a, b, c) 會依序讀取 a、b、c 中的元素，看起來就像把三個串列接在一起。
print(f"chain(a, b, c): {list(chain(a, b, c))}")

print("\n--- permutations() 排列 ---")
items = ["a", "b", "c"]
print(f"permutations(items):")
# permutations(items) 預設會把全部元素都拿去排列。
# 因為排列強調「順序」，所以 ('a', 'b', 'c') 與 ('b', 'a', 'c') 會被視為不同結果。
for p in permutations(items):
    print(f"  {p}")

print(f"permutations(items, 2):")
# permutations(items, 2) 表示從 3 個元素中挑 2 個，並列出所有有順序的排列組合。
# 例如 ('a', 'b') 和 ('b', 'a') 都會出現，因為順序不同。
for p in permutations(items, 2):
    print(f"  {p}")

print("\n--- combinations() 組合 ---")
print(f"combinations(items, 2):")
# combinations(items, 2) 是「組合」而不是「排列」，所以不看順序。
# 例如 ('a', 'b') 會出現，但 ('b', 'a') 不會重複出現。
for c in combinations(items, 2):
    print(f"  {c}")

print("\n--- 組合應用：密碼窮舉 ---")
chars = ["A", "B", "1"]
print("2位數密碼:")
# 使用 permutations(chars, 2) 產生兩個字元的密碼排列。
# 因為是排列，所以 AB、BA 都會出現，而且不會重複使用同一個位置的元素。
for p in permutations(chars, 2):
    print(f"  {''.join(p)}")

print("2位數密碼（可重複）:")
from itertools import combinations_with_replacement

# combinations_with_replacement 允許重複選同一個元素，
# 但它仍然屬於「組合」，也就是不看順序，所以 AB 與 BA 只會視為同一種。
# 如果你要的是「可重複且順序有差異」的密碼，通常要改用 product(chars, repeat=2)。
for p in combinations_with_replacement(chars, 2):
    print(f"  {''.join(p)}")
