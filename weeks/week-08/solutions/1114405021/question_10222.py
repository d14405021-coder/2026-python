# 題目：UVA 10222 (Decode the Mad man)
# 說明：
# 此題是著名的鍵盤解碼問題。瘋狂打字員將手向右偏移了 2 個按鍵（UVA 標準測資為偏移 2 鍵）。
# （註：Markdown 中描述為偏移 3 鍵且 r 變 e，但 r 變 e 實際上只差 1 鍵。根據 UVA 10222 原題，
# 標準解法是將每個字元對應到 QWERTY 鍵盤上，並「向左移動 2 個按鍵」來解碼。）
# 輸入的字元可能包含大寫，需先轉換為小寫。空格及換行保持原樣。

import sys

def solve():
    # 建立一個標準 QWERTY 鍵盤的字串對應表
    # 注意反斜線 \ 必須跳脫寫成 \
    kb = "`1234567890-=qwertyuiop[]\asdfghjkl;'zxcvbnm,./"
    
    # 讀取全部輸入
    input_data = sys.stdin.read()
    if not input_data:
        return
        
    # 將輸入轉換為小寫
    input_data = input_data.lower()
    
    result = []
    # 針對每一個字元進行解碼
    for char in input_data:
        # 如果字元在鍵盤字串中，就找出它的索引
        idx = kb.find(char)
        if idx != -1:
            # 向左偏移 2 個按鍵
            result.append(kb[idx - 2])
        else:
            # 如果不在鍵盤字串中 (例如空白、換行等)，就保持原樣
            result.append(char)
            
    # 將解碼後的字元陣列合併成字串並輸出，不加多餘的換行
    sys.stdout.write("".join(result))

if __name__ == '__main__':
    solve()
