# 題目：UVA 10190 (Divide, But Not Quite Conquer!)
# 說明：這題要求將數字 n 持續除以 m，直到 n 變成 1 為止，途中必須每一階段都能整除。
# 注意事項：在 Markdown 中題目敘述誤植為「自動傘」問題，但 UVA 10190 與 ZeroJudge a183
# 皆為「連除問題 (Divide, But Not Quite Conquer!)」，因此在此實作連除演算法。
# 標準版使用 sys.stdin.read().split() 來快速讀入並處理所有輸入。

import sys

def solve():
    # 一次讀取所有輸入資料，自動過濾掉換行與多餘空白
    input_data = sys.stdin.read().split()
    if not input_data:
        return
        
    # 每兩個數字一組進行處理
    for i in range(0, len(input_data), 2):
        # 避免輸入的資料數量不是偶數個
        if i + 1 >= len(input_data):
            break
            
        n = int(input_data[i])
        m = int(input_data[i+1])
        
        # 邊界條件：n 和 m 必須 >= 2，若 m=1 會造成無窮迴圈，n=0/1 也不符合規定
        if n < 2 or m < 2:
            print("Boring!")
            continue
            
        # 用來儲存連除的數列
        seq = []
        temp = n
        is_boring = False
        
        # 持續除以 m
        while temp > 1:
            # 如果發現除下去會有餘數，代表不能整除
            if temp % m != 0:
                is_boring = True
                break
            
            # 加入當前的數字
            seq.append(temp)
            # 整除更新 temp
            temp //= m
            
        # 如果無法一路除到 1，就輸出 Boring!
        if is_boring:
            print("Boring!")
        else:
            # 成功除到 1 時，將最後的 1 也放進去
            seq.append(1)
            # 將數列中的數字轉成字串並用空格串接印出
            print(" ".join(map(str, seq)))

if __name__ == '__main__':
    solve()
