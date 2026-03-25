# question_10041.py
# 說明：UVA 10041 Vito's Family (Vito 家族) 解答
#
# 解題思路：
# 1. 這是一個經典的「找中位數」問題。
# 2. 假設你在數線上要找一個點，讓這個點到所有其他給定點的「距離總和」最小，
#    那麼這個點必然是這些點的「中位數」。
# 3. 實作上，只要將輸入的親戚門牌號碼排序，取中間的元素當作 Vito 的家，
#    然後把每個親戚家到這個中位數的距離加起來，就是最小總距離。

import sys


def find_min_distance(relatives):
    """
    計算 Vito 到所有親戚家的最小總距離
    :param relatives: 親戚們的門牌號碼列表 (list of integers)
    :return: 最小的距離總和 (integer)
    """
    if not relatives:
        return 0

    # 步驟 1：將所有親戚的門牌號碼由小到大排序
    sorted_relatives = sorted(relatives)

    # 步驟 2：找出中位數的索引
    # 即使長度是偶數，取中間靠左的點作為中位數一樣能得到最小距離總和
    mid_index = len(sorted_relatives) // 2
    median = sorted_relatives[mid_index]

    # 步驟 3：計算所有親戚家到中位數的絕對值距離並加總
    total_distance = sum(abs(x - median) for x in sorted_relatives)

    return total_distance


def main():
    # 讀取標準輸入 (stdin) 的所有資料，並以空白或換行符號分割
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    # 第一個數字為測資筆數
    num_test_cases = int(input_data[0])
    idx = 1

    # 處理每一筆測試資料
    for _ in range(num_test_cases):
        if idx >= len(input_data):
            break

        # 第一個數字是親戚的數量
        r = int(input_data[idx])

        # 接下來的 r 個數字是親戚的門牌號碼
        relatives = [int(x) for x in input_data[idx + 1 : idx + 1 + r]]

        # 計算並輸出這筆測資的結果
        print(find_min_distance(relatives))

        # 更新指標，跳到下一筆測資的位置
        idx += r + 1


if __name__ == "__main__":
    main()
