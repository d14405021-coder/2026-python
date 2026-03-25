# question_10056-manual.py
# 說明：UVA 10056 What is the Probability 的「手打基礎版 (Manual)」解答
# 針對不熟悉快速讀寫和串列操作的初學者設計，
# 使用最傳統的 input().split() 與浮點數運算來解題。


def solve():
    try:
        # 第一行通常是測試資料的筆數 S
        line = input().strip()
        if not line:
            return

        test_cases = int(line)

        # 針對每一組測試資料進行迴圈處理
        for _ in range(test_cases):
            # 讀取一行，並用空白切開
            # 格式：N (玩家數) p (成功機率) i (目標玩家編號)
            data = input().strip().split()

            # 若遇到空行，就繼續讀下一行
            while not data:
                data = input().strip().split()

            n = int(data[0])  # 轉換為整數
            p = float(data[1])  # 轉換為浮點數
            i = int(data[2])  # 轉換為整數

            # 如果成功機率是 0，表示沒有人會贏
            if p == 0.0:
                print("0.0000")
                continue

            # q 為失敗的機率
            q = 1.0 - p

            # 使用無窮等比級數公式求總機率：S = a / (1 - r)
            # 1. 首項 a：第 i 個人在「第一輪」就贏的機率
            #    也就是前 i-1 個人都失敗，然後他成功
            a = (q ** (i - 1)) * p

            # 2. 公比 r：一整輪 N 個人全部都失敗的機率
            r = q**n

            # 3. 如果 r == 1 (大家永遠失敗)，這在 p>0 時理論上不會發生，但做個防呆
            if r == 1.0:
                print("0.0000")
                continue

            # 4. 計算最終獲勝機率
            probability = a / (1.0 - r)

            # 輸出格式化字串，限制在小數點後 4 位
            print(f"{probability:.4f}")

    except EOFError:
        # 當所有資料都讀取完畢，會觸發 EOFError，安全結束
        pass


if __name__ == "__main__":
    solve()
