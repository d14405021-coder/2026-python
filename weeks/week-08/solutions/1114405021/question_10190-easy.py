# 題目：UVA 10190 (Divide, But Not Quite Conquer!) - 簡易版
# 說明：因為原 Markdown 題目描述誤植為「自動傘」問題，但根據標題 (UVA 10190) 與連結 (ZeroJudge a183)，
# 此處實作正牌的「Divide, But Not Quite Conquer!」解答。
# 這個版本使用 while True 與 input() 的方式讀取，對初學者來說較好理解。

def solve():
    while True:
        try:
            # 讀取一行，並將兩個數字分別存入 n 和 m
            line = input().strip()
            if not line:
                continue
                
            parts = line.split()
            n = int(parts[0])
            m = int(parts[1])
            
            # 如果 n 或是 m 有小於 2 的，代表無法一直除下去或是會無窮迴圈 (例如除以 1)
            if n < 2 or m < 2:
                print("Boring!")
                continue
                
            seq = []
            current = n
            
            # 當數字還大於 1，就一直嘗試除以 m
            while current > 1:
                # 若發現無法被 m 整除，提早結束
                if current % m != 0:
                    break
                    
                # 可以整除的話，先把數字存起來
                seq.append(current)
                # 將數字除以 m 繼續下一輪
                current = current // m
                
            # 迴圈結束後，檢查是不是剛好除到變成 1
            if current == 1:
                seq.append(1)
                # 將陣列內的數字轉換為字串並用空白連接
                print(" ".join(map(str, seq)))
            else:
                # 若不是 1，代表中途有無法整除的情況發生
                print("Boring!")
                
        except EOFError:
            # 當讀取到檔案結尾時跳出迴圈
            break

if __name__ == '__main__':
    solve()
