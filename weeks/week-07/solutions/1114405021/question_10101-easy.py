# 題目：UVA 10101 (移動火柴棒) - 簡易版
# 說明：這個版本使用更直觀的方式窮舉所有可能的變化。
import sys

# 將每個數字的火柴棒轉為二進位遮罩
# 例如：0 有 6 根火柴
STICKS = {
    '0': 0x3f, '1': 0x06, '2': 0x5b, '3': 0x4f, 
    '4': 0x66, '5': 0x6d, '6': 0x7d, '7': 0x07, 
    '8': 0x7f, '9': 0x6f
}

def can_change(c_from, c_to):
    """
    判斷數字從 c_from 變成 c_to 會發生什麼事
    回傳 (需要增加的火柴數量, 需要減少的火柴數量)
    """
    s1, s2 = STICKS[c_from], STICKS[c_to]
    # 增加的火柴就是目標有但原本沒有的
    added = bin(~s1 & s2).count('1')
    # 減少的火柴就是原本有但目標沒有的
    removed = bin(s1 & ~s2).count('1')
    return added, removed

def check(eq_str):
    try:
        left, right = eq_str.split('=')
        return eval(left) == eval(right)
    except:
        return False

def solve():
    raw_data = sys.stdin.read().strip()
    if not raw_data:
        return
        
    eq = raw_data.split('#')[0]
    
    # 嘗試：從某個數字拿走一根火柴，放到另一個數字上 (或同一個數字)
    chars = list(eq)
    
    # i 是被拿走火柴的數字
    for i in range(len(chars)):
        if chars[i].isdigit():
            original_i = chars[i]
            for target_i in '0123456789':
                add1, rem1 = can_change(original_i, target_i)
                
                # 如果是內部移動一根 (自己拿走又自己加上去)
                if add1 == 1 and rem1 == 1:
                    chars[i] = target_i
                    if check("".join(chars)):
                        print("".join(chars) + '#')
                        return
                    chars[i] = original_i # 復原
                    
                # 如果只是拿走一根
                elif add1 == 0 and rem1 == 1:
                    chars[i] = target_i
                    
                    # 尋找可以放火柴的地方 j
                    for j in range(len(chars)):
                        if i != j and chars[j].isdigit():
                            original_j = chars[j]
                            for target_j in '0123456789':
                                add2, rem2 = can_change(original_j, target_j)
                                
                                # 必須是只能增加一根火柴
                                if add2 == 1 and rem2 == 0:
                                    chars[j] = target_j
                                    if check("".join(chars)):
                                        print("".join(chars) + '#')
                                        return
                                    chars[j] = original_j # 復原
                    
                    chars[i] = original_i # 復原
                    
    print("No")

if __name__ == '__main__':
    solve()
