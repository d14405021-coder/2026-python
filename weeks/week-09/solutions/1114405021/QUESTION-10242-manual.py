# UVA 10242 - 手打程式
# 手打重點：用 DFS + 記憶化，狀態為 (目前節點, 已搶集合)


def solve():
    while True:
        try:
            n, m = map(int, input().split())
        except EOFError:
            break

        if n == 0 and m == 0:
            break

        g = [[] for _ in range(n + 1)]
        for _ in range(m):
            u, v = map(int, input().split())
            g[u].append(v)

        atm = [0] * (n + 1)
        for i in range(1, n + 1):
            atm[i] = int(input().strip())

        s, p = map(int, input().split())
        bars = set(map(int, input().split()))

        memo = {}

        def dfs(u, robbed, visiting):
            key = (u, frozenset(robbed))
            if key in memo:
                return memo[key]
            if key in visiting:
                return 0

            nxt_visiting = visiting | {key}
            best = 0 if u in bars else 0

            for v in g[u]:
                gain = 0
                new_robbed = robbed.copy()
                if v not in robbed:
                    gain = atm[v]
                    new_robbed.add(v)
                cand = gain + dfs(v, new_robbed, nxt_visiting)
                if cand > best:
                    best = cand

            memo[key] = best
            return best

        start_robbed = {s}
        print(atm[s] + dfs(s, start_robbed, set()))


if __name__ == "__main__":
    solve()
