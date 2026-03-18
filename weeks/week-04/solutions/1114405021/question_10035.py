"""
UVA 10035 - Primary Arithmetic

題意：
- 逐行讀入兩個非負整數 a, b。
- 計算做直式加法時，一共發生幾次進位（carry）。
- 讀到 "0 0" 結束，不輸出該行結果。

本檔提供：
1. 核心函式 count_carries（回傳進位次數）
2. 輸出格式函式 format_carry_message
3. solve（可供單元測試與主程式共用）
"""

from __future__ import annotations


def count_carries(a: int, b: int) -> int:
    """
    計算 a + b 的直式加法過程中，總共有幾次進位。

    教學理解：
    - 從個位數開始往左位數前進。
    - 每次都把「當前位數 + 前一位進位」相加。
    - 若結果 >= 10，代表此位會產生進位到下一位，carry_count + 1。
    """

    # carry 只會是 0 或 1，代表「前一位是否有進位」。
    carry = 0
    # carry_count 用來累計整個直式加法過程的進位總次數。
    carry_count = 0

    # 只要其中一個數還有位數沒處理，就繼續。
    # 每次迴圈處理一個十進位位數。
    while a > 0 or b > 0:
        da = a % 10
        db = b % 10

        if da + db + carry >= 10:
            carry = 1
            carry_count += 1
        else:
            carry = 0

        a //= 10
        b //= 10

    return carry_count


def format_carry_message(carry_count: int) -> str:
    """
    把進位次數轉成題目要求句型。

    規則：
    - 0 次：No carry operation.
    - 1 次：1 carry operation.
    - 2 次以上：N carry operations.
    """

    if carry_count == 0:
        return "No carry operation."
    if carry_count == 1:
        return "1 carry operation."
    return f"{carry_count} carry operations."


def solve(raw_input: str) -> str:
    """
    解析整份輸入並回傳輸出字串。

    輸入格式：
    - 每行兩個整數
    - 遇到 "0 0" 代表結束
    """

    # outputs 每個元素都是一行最終輸出句子。
    outputs = []

    for line in raw_input.splitlines():
        line = line.strip()
        if not line:
            continue

        a_str, b_str = line.split()
        a = int(a_str)
        b = int(b_str)

        # 題目規定 0 0 是結束標記，不是要計算的資料。
        if a == 0 and b == 0:
            break

        outputs.append(format_carry_message(count_carries(a, b)))

    return "\n".join(outputs)


def main() -> None:
    """OJ 入口：讀 stdin，寫 stdout。"""

    import sys

    raw_input = sys.stdin.read()
    result = solve(raw_input)
    if result:
        print(result)


if __name__ == "__main__":
    main()
