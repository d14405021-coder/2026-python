# 題目：UVA 10101 (移動火柴棒) - 手動版
# 說明：這個版本使用基礎 input() 和 while True 來讀取輸入。

def get_sticks(digit):
    # 手動定義每一個數字對應的二進位火柴棒
    sticks = {
        '0': 63, '1': 6, '2': 91, '3': 79, '4': 102,
        '5': 109, '6': 125, '7': 7, '8': 127, '9': 111
    }
    return sticks[digit]

def diff(old, new):
    s1, s2 = get_sticks(old), get_sticks(new)
    add = bin(~s1 & s2).count('1')
    rem = bin(s1 & ~s2).count('1')
    return add, rem

def eval_eq(eq):
    try:
        if '=' not in eq: return False
        l, r = eq.split('=')
        return eval(l) == eval(r)
    except:
        return False

def solve():
    while True:
        try:
            line = input().strip()
            if not line:
                continue
            
            eq = line.split('#')[0]
            if not eq: continue
            
            chars = list(eq)
            solved = False
            
            for i in range(len(chars)):
                if not chars[i].isdigit(): continue
                for target1 in '0123456789':
                    add1, rem1 = diff(chars[i], target1)
                    if add1 == 1 and rem1 == 1:
                        old = chars[i]
                        chars[i] = target1
                        if eval_eq("".join(chars)):
                            print("".join(chars) + '#')
                            solved = True
                            break
                        chars[i] = old
                    elif add1 == 0 and rem1 == 1:
                        old_i = chars[i]
                        chars[i] = target1
                        for j in range(len(chars)):
                            if i == j or not chars[j].isdigit(): continue
                            for target2 in '0123456789':
                                add2, rem2 = diff(chars[j], target2)
                                if add2 == 1 and rem2 == 0:
                                    old_j = chars[j]
                                    chars[j] = target2
                                    if eval_eq("".join(chars)):
                                        print("".join(chars) + '#')
                                        solved = True
                                        break
                                    chars[j] = old_j
                            if solved: break
                        chars[i] = old_i
                if solved: break
            
            if not solved:
                print("No")
                
        except EOFError:
            break

if __name__ == '__main__':
    solve()
