# R10. 去重且保序（1.10）

def dedupe(items):
    # seen 用來記錄「已看過」的值。
    # 用 set 的原因：查詢 item 是否存在的平均時間複雜度接近 O(1)。
    seen = set()

    # 逐一掃描原始序列，保持原本出現順序。
    for item in items:
        # 只要是第一次出現，就輸出；重複值略過。
        if item not in seen:
            # yield 代表這是一個生成器（generator）函式：
            # 不會一次建立完整清單，而是邊迭代邊產生結果，節省記憶體。
            yield item

            # 記得在輸出後把 item 標記為已出現。
            seen.add(item)

def dedupe2(items, key=None):
    # 進階版：支援「自訂比較鍵」。
    # 適合 items 是 dict、物件、tuple 等複合資料時，
    # 你可以指定只依某些欄位判斷是否重複。
    seen = set()

    for item in items:
        # 若沒有提供 key，就直接用 item 本身判重；
        # 若有 key，則用 key(item) 的結果判重。
        val = item if key is None else key(item)

        # 注意：放進 set 的 val 必須是可雜湊（hashable）型別。
        # 例如 list/dict 不能直接當 set 元素，通常需轉 tuple 或取可雜湊欄位。
        if val not in seen:
            # 即使是用 val 判重，輸出仍是原始 item，方便保留完整資料。
            yield item
            seen.add(val)

# 閱讀這段程式的口訣：
# 1) 先看「判重用什麼」：item 本身或 key(item)
# 2) 再看「第一次出現就 yield，之後略過」
# 3) 最後記住它是生成器，要用 list(...) 或 for 迴圈消耗結果
