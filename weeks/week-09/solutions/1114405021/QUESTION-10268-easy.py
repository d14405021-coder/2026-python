"""
QUESTION-10268 簡化版本（Easy版本）
雞蛋掉落問題 - 簡單易懂的方式
"""

def min_trials(k, n):
    """
    用簡單方式理解：
    我們想知道：有k個雞蛋，最多進行多少次試驗，就能涵蓋n層樓？
    
    反轉思考：有k個雞蛋，進行t次試驗，最多能測試多少層樓？
    """
    if k == 1:
        # 只有1個雞蛋 → 只能從下往上逐層測試
        return n
    
    max_trials = 63
    
    # 用陣列記錄：prev[e] = 上一次試驗用 e 個雞蛋能測多少層
    # curr[e] = 這一次試驗用 e 個雞蛋能測多少層
    prev = [0] * (max_trials + 1)
    curr = [0] * (max_trials + 1)
    
    for trials in range(1, max_trials + 1):
        for eggs in range(1, k + 1):
            if eggs == 1:
                # 1個雞蛋：每試驗一次只能多測一層
                curr[eggs] = trials
            else:
                # 多個雞蛋：在某層試驗
                # - 破了 → 下面用(eggs-1)個雞蛋可測 prev[eggs-1] 層
                # - 沒破 → 上面用 eggs 個雞蛋可測 prev[eggs] 層
                # - 這一層 + 下層 + 上層 = 總共可測的層數
                curr[eggs] = prev[eggs - 1] + 1 + prev[eggs]
        
        # 如果能涵蓋 n 層，找到答案了！
        if curr[k] >= n:
            return trials
        
        prev = curr[:]
    
    return -1

def solve():
    """讀取輸入並輸出答案"""
    while True:
        line = input().strip()
        if not line:
            continue
        
        parts = line.split()
        if len(parts) == 1 and parts[0] == "0":
            break
        
        k, n = map(int, parts)
        
        result = min_trials(k, n)
        
        if result > 63:
            print("More than 63 trials needed.")
        else:
            print(result)


if __name__ == "__main__":
    solve()
