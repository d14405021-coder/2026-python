# 題目：UVA 10190 (Divide, But Not Quite Conquer!) - 手動版
# 說明：這個版本完全不依賴高階語法（例如 map、join 或是 sys 模組）。
# 所有陣列轉換字串的過程都用最基礎的 for 迴圈來處理，非常適合在考試時手寫記憶。

def solve():
    # 建立一個無窮迴圈來讀取多組測試資料
    while True:
        try:
            # 讀取一行輸入
            line = input()
            # 如果讀到空行，就跳過這次迴圈
            if line == "":
                continue

            # 使用空白將字串切開，取得兩個部分
            parts = line.split()
            # 將字串轉換成整數
            n = int(parts[0])
            m = int(parts[1])

            # 邊界條件：如果 n 或 m 小於 2，不符合連除規則 (例如 m=1 會無窮迴圈)
            if n < 2 or m < 2:
                print("Boring!")
                continue

            # 建立一個列表來存儲除下來的數字
            seq = []
            current = n
            is_boring = False

            # 當數字大於 1，就一直除下去
            while current > 1:
                # 如果無法被 m 整除，代表不是完美的連除數列
                if current % m != 0:
                    is_boring = True
                    break
                
                # 把當前的數字存起來
                seq.append(current)
                # 將數字除以 m (使用整數除法)
                current = current // m

            # 判斷結果並輸出
            if is_boring:
                print("Boring!")
            else:
                # 如果完美除到最後，最後一個數字一定是 1，把它加進去
                seq.append(1)
                
                # 使用最基礎的迴圈來組合要印出的字串，不使用 join()
                result = ""
                for i in range(len(seq)):
                    # 把數字轉換成字串後接上去
                    result += str(seq[i])
                    # 如果不是最後一個數字，就在後面加上一個空白
                    if i < len(seq) - 1:
                        result += " "
                
                # 印出結果
                print(result)

        except EOFError:
            # 當讀取不到資料 (檔案結尾) 時，跳出迴圈
            break

if __name__ == '__main__':
    solve()
