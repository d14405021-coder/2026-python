"""
UVA 490 - Rotating Sentences

題目要求將一組多行文字以順時針方向旋轉 90 度。輸入最多 100 行，
每行最多 100 個字元，包含可見字元、空白或標點，但不包括 tab。

輸出時需將所有行視為矩陣的行，短行以空白補齊至最寬行，
然後將矩陣順時針旋轉 90 度再列印。

例如：
HELLO
WORLD

對應矩陣為：
H E L L O
W O R L D

旋轉 90 度後變成：
W H
O E
R L
L L
D O

本檔案提供完整可執行的解答，包含主函數與輔助函式，
並以繁體中文詳細註解每個步驟。
"""

import sys


def rotate_sentences(lines):
    """
    將輸入的多行文字列表旋轉 90 度並返回結果列表

    參數:
        lines (List[str]): 原始每行的字串（末尾不含換行符）
    返回:
        List[str]: 旋轉後每行需要輸出的字串
    """
    if not lines:
        # 沒有任何輸入行時，直接返回空列表
        return []

    # 先找出最長的行長，短行在右側用空白補齊
    max_len = max(len(l) for l in lines)

    # 將所有行填充到相同的長度（左對齊）
    padded = [l.ljust(max_len) for l in lines]

    # 旋轉矩陣：新矩陣的行數等於原行的最大長度
    # 例如原 padded 是 m 行 n 列，結果會是 n 行 m 列
    result = []
    for col in range(max_len):
        # 對於每個輸出行（即原來的列），從最後一行開始往上讀
        row_chars = []
        for row in range(len(padded) - 1, -1, -1):
            row_chars.append(padded[row][col])
        result.append(''.join(row_chars))

    return result


def main():
    """
    主程式：從標準輸入讀取所有資料，處理並輸出旋轉結果。

    執行步驟：
    1. 讀取所有行，去除末尾換行符但保留行內空白
    2. 呼叫 rotate_sentences 取得旋轉後的每行字串
    3. 將結果逐行列印
    """
    # 使用 sys.stdin.read 可同時支援 EOF 偵測
    data = sys.stdin.read().splitlines()
    # splitlines() 已經去掉換行符

    rotated = rotate_sentences(data)

    # 輸出每一行，print 自動加上換行
    for line in rotated:
        print(line)


if __name__ == '__main__':
    main()
