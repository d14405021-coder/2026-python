# 題目：UVA 10222 (Decode the Mad man) - 手動版
# 說明：這個版本完全不用 find 函式，而是自己寫迴圈去對照陣列找位置。
# 非常適合在嚴格不能用字串內建函數的考試中默寫。

def solve():
    # 建立一個陣列，儲存鍵盤上的每一個字元
    kb = list("`1234567890-=qwertyuiop[]\asdfghjkl;'zxcvbnm,./")
    
    while True:
        try:
            line = input()
            
            # 手動將大寫轉小寫 (不用 lower)
            new_line = ""
            for char in line:
                if 'A' <= char <= 'Z':
                    # A 的 ASCII 是 65，a 是 97，差 32
                    new_line += chr(ord(char) + 32)
                else:
                    new_line += char
            
            decoded = ""
            # 對於每個字元，手動找尋其在 kb 陣列中的索引
            for char in new_line:
                found = False
                for i in range(len(kb)):
                    if char == kb[i]:
                        # 找到字元了，就把它的索引減 2 (左移 2 個鍵)
                        decoded += kb[i - 2]
                        found = True
                        break
                        
                # 如果沒有在 kb 中找到 (例如空白鍵)，就直接保持原樣加進去
                if not found:
                    decoded += char
                    
            print(decoded)
            
        except EOFError:
            break

if __name__ == '__main__':
    solve()
