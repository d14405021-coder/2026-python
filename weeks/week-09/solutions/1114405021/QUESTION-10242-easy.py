"""
UVA 10242 - ATM 搶劫問題 (Easy版本)
簡化的解法 - 使用集合表示已搶 ATM
"""

def solve_atm_robbery():
    """讀取輸入並求解"""
    while True:
        try:
            n, m = map(int, input().split())
            if n == 0 and m == 0:
                break
            
            # 建立鄰接表
            graph = [[] for _ in range(n + 1)]
            for _ in range(m):
                u, v = map(int, input().split())
                graph[u].append(v)
            
            # 讀取 ATM 金額
            atm = [0] * (n + 1)
            for i in range(1, n + 1):
                atm[i] = int(input())
            
            # 讀取起點和酒吧
            s, p = map(int, input().split())
            bars = set(map(int, input().split()))
            
            # DFS - 用集合表示已搶 ATM
            memo = {}
            
            def dfs(node, robbed):
                """
                從 node 開始，已搶過 robbed 中的 ATM
                返回能搶到的最大金額
                """
                key = (node, frozenset(robbed))
                if key in memo:
                    return memo[key]
                
                result = 0
                
                # 嘗試去每個相鄰路口
                for next_node in graph[node]:
                    money = 0
                    new_robbed = robbed.copy()
                    
                    # 如果這個路口的 ATM 還沒搶過，搶它
                    if next_node not in robbed:
                        money = atm[next_node]
                        new_robbed.add(next_node)
                    
                    # 繼續搜尋
                    total = money + dfs(next_node, new_robbed)
                    result = max(result, total)
                
                memo[key] = result
                return result
            
            # 開始時搶起點的 ATM
            robbed = {s}
            answer = atm[s] + dfs(s, robbed)
            print(answer)
            
        except EOFError:
            break

if __name__ == "__main__":
    solve_atm_robbery()
