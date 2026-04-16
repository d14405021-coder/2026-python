# Understand（理解）- 生成器概念

# 這個檔案示範的是「生成器（generator）」的核心觀念。
# 生成器的重點不是一次把所有資料都算好，而是「需要時才產生下一筆資料」。
# 這樣可以節省記憶體，也很適合處理無限序列、逐步遍歷與遞迴資料結構。


def frange(start, stop, step):
    # frange() 的功能類似內建的 range()，但可以支援小數。
    # 這裡不用 return 一整串結果，而是每次用 yield 送出一個值。
    # yield 的意思是：先把目前的值交給呼叫端，之後保留函式狀態，下一次再繼續執行。
    x = start
    while x < stop:
        yield x
        x += step


# 把生成器轉成 list，方便一次看完整輸出。
# 注意：這只是為了示範；實務上如果資料很多，通常不會急著全部轉成 list。
result = list(frange(0, 2, 0.5))
print(f"frange(0, 2, 0.5): {result}")


def countdown(n):
    # 這個函式示範生成器「可暫停、可恢復」的特性。
    # 執行到 yield 時會先回傳目前值，等下一次 next() 才會從下一行繼續。
    print(f"Starting countdown from {n}")
    while n > 0:
        yield n
        n -= 1
    # 當迴圈結束後，代表所有值都已經送出，生成器也就結束。
    print("Done!")


print("\n--- 建立生成器 ---")
# 呼叫 countdown(3) 不會立刻執行完整函式，只會建立一個 generator 物件。
# 真正的內容會等到 next(c) 或 for 迴圈取值時才開始跑。
c = countdown(3)
print(f"生成器物件: {c}")

print("\n--- 逐步迭代 ---")
# next() 每呼叫一次，就向生成器要下一個值。
# 這裡會看到值依序被吐出來，而不是一次全部算完。
print(f"next(c): {next(c)}")
print(f"next(c): {next(c)}")
print(f"next(c): {next(c)}")

# 當生成器內容全部取完後，再呼叫 next() 就會丟出 StopIteration。
# 這是 Python 用來表示「沒有下一筆資料了」的標準方式。
try:
    next(c)
except StopIteration:
    print("StopIteration!")


def fibonacci():
    # 這是一個「無限生成器」的典型範例。
    # 它永遠不會自己結束，而是持續產生費氏數列：0, 1, 1, 2, 3, 5, ...
    # 這種寫法適合在只想要前幾項時，避免先算出整個無限序列。
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


print("\n--- Fibonacci 生成器 ---")
# 這裡只取前 10 個值，避免無限迴圈。
fib = fibonacci()
for i in range(10):
    print(next(fib), end=" ")
print()


def chain_iter(*iterables):
    # yield from 是很常見也很漂亮的寫法，意思是：
    # 「把內層可迭代物件的每個元素，逐一轉交給外層生成器」。
    # 下面這個函式會把多個序列接在一起，依序吐出所有元素。
    for it in iterables:
        yield from it


print("\n--- yield from 用法 ---")
# 把多個 list 串接成一個連續的串流。
# 這樣不用手動寫雙層迴圈，程式會更乾淨。
result = list(chain_iter([1, 2], [3, 4], [5, 6]))
print(f"chain_iter: {result}")


class Node:
    # Node 用來示範樹狀結構。
    # 每個節點都可以有自己的子節點，形成一棵樹。
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, node):
        # 將子節點加入 children 清單，建立父子關係。
        self.children.append(node)

    def __iter__(self):
        # 讓 Node 本身可以被迭代，也就是 for child in node 時會跑到 children。
        # 這樣 depth_first() 裡面就能直接用 for child in self。
        return iter(self.children)

    def depth_first(self):
        # 深度優先遍歷（DFS）的核心概念：
        # 1. 先拜訪自己
        # 2. 再遞迴拜訪每個子節點
        yield self
        for child in self:
            yield from child.depth_first()


print("\n--- 樹的深度優先遍歷 ---")
# 建立一棵簡單的樹：
# 0
# ├─ 1
# │  ├─ 3
# │  └─ 4
# └─ 2
root = Node(0)
root.add_child(Node(1))
root.add_child(Node(2))
root.children[0].add_child(Node(3))
root.children[0].add_child(Node(4))

# 透過 depth_first()，我們會依照 DFS 順序拿到所有節點。
for node in root.depth_first():
    print(node.value, end=" ")
print()


def flatten(items):
    # flatten() 用來把巢狀序列攤平成一條平面序列。
    # 如果遇到可迭代物件，就遞迴往下展開；如果是單一值，就直接 yield 出去。
    # 這個技巧在處理多層 list、tuple、集合時很實用。
    for x in items:
        # 字串雖然也是可迭代物件，但通常不希望被拆成一個個字元。
        # 所以這裡特別排除 str。
        if hasattr(x, "__iter__") and not isinstance(x, str):
            yield from flatten(x)
        else:
            yield x


print("\n--- 巢狀序列攤平 ---")
# 巢狀清單示範：外層裡面還包著內層清單。
# flatten() 會把它變成單一層級的資料結構。
nested = [1, [2, [3, 4]], 5]
print(f"展開: {list(flatten(nested))}")
