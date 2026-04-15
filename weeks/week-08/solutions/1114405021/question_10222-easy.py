# 題目：UVA 10222 (Decode the Mad man) - 簡易版
# 說明：因為原題敘述混亂，此處提供標準的「往左移 2 個按鍵」的解碼實作。
# 這個版本使用 while True 與 input() 的方式讀取，對於初學者較為友善。

def solve():
    # 建立一個標準 QWERTY 鍵盤的字串，由上到下，由左到右排好
    # 使用原始字串 (raw string) 'r' 來避免處理反斜線的跳脫問題
    kb = r"`1234567890-=qwertyuiop[]\asdfghjkl;'zxcvbnm,./"
    
    # 建立一個無窮迴圈來讀取輸入，直到 EOFError
    while True:
        try:
            # 讀取一行文字
            line = input()
            
            # 將這一行的文字全部轉換為小寫，因為鍵盤解碼不分大小寫
            line = line.lower()
            
            # 準備一個空字串來存放解碼後的結果
            decoded_line = ""
            
            # 針對這行的每一個字元進行處理
            for char in line:
                # 尋找該字元在鍵盤字串中的位置 (索引值)
                idx = kb.find(char)
                
                # find() 找不到會回傳 -1。如果是空白或其他符號，保持原樣
                if idx == -1:
                    decoded_line += char
                else:
                    # 如果找到了，就拿索引值減 2 的字元 (向左移 2 格)
                    decoded_line += kb[idx - 2]
                    
            # 輸出解碼後的這一行文字
            print(decoded_line)
            
        except EOFError:
            # 當沒有輸入時跳出迴圈
            break

if __name__ == '__main__':
    solve()
