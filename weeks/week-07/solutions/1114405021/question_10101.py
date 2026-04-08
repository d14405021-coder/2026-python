# 題目：UVA 10101 / ZeroJudge a094 (移動火柴棒)
# 說明：這是一個經典的火柴棒算式修正問題

import sys

# 0-9 數字的火柴棒表示法 (七段顯示器)
# a=0, b=1, c=2, d=3, e=4, f=5, g=6
# 對應的二進位：0b_gfedcba
sticks = {
    '0': 0b0111111,
    '1': 0b0000110,
    '2': 0b1011011,
    '3': 0b1001111,
    '4': 0b1100110,
    '5': 0b1101101,
    '6': 0b1111101,
    '7': 0b0000111,
    '8': 0b1111111,
    '9': 0b1101111
}

# 取得將字元轉換成特定字元所需的變化
# 傳回：(增加的棒數, 減少的棒數)
def get_diff(c1, c2):
    s1 = sticks[c1]
    s2 = sticks[c2]
    # 需要增加的棒子
    add = bin(~s1 & s2).count('1')
    # 需要減少的棒子
    remove = bin(s1 & ~s2).count('1')
    return add, remove

def check_equation(eq_str):
    if '=' not in eq_str: return False
    left, right = eq_str.split('=')
    try:
        # 安全評估運算式
        return eval(left) == eval(right)
    except:
        return False

def solve():
    input_str = sys.stdin.read().strip()
    if not input_str:
        return
        
    # 擷取到 # 為止的算式
    eq = ""
    for char in input_str:
        eq += char
        if char == '#':
            break
            
    if not eq or eq[-1] != '#':
        return
        
    eq = eq[:-1] # 移除 #
    
    # 嘗試修改算式中的每一個數字
    for i in range(len(eq)):
        if eq[i].isdigit():
            for target in '0123456789':
                if target != eq[i]:
                    add, remove = get_diff(eq[i], target)
                    # 內部移動一根火柴
                    if add == 1 and remove == 1:
                        new_eq = eq[:i] + target + eq[i+1:]
                        if check_equation(new_eq):
                            print(new_eq + '#')
                            return
                            
                    # 取走一根火柴
                    elif add == 0 and remove == 1:
                        # 需要在別的地方加上一根火柴
                        for j in range(len(eq)):
                            if i != j and eq[j].isdigit():
                                for target2 in '0123456789':
                                    if target2 != eq[j]:
                                        add2, remove2 = get_diff(eq[j], target2)
                                        if add2 == 1 and remove2 == 0:
                                            # 找到可以加上火柴的地方
                                            new_eq = list(eq)
                                            new_eq[i] = target
                                            new_eq[j] = target2
                                            if check_equation("".join(new_eq)):
                                                print("".join(new_eq) + '#')
                                                return
                                                
    print("No")

if __name__ == '__main__':
    solve()
