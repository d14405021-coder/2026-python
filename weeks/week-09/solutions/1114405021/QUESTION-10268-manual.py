# UVA 10268 - 手打程式
# 手打重點：反向 DP，計算「t 次測試最多可測幾層」。


def min_trials(k, n):
    if k == 1:
        return n

    max_trials = 63
    prev = [0] * (k + 1)

    for t in range(1, max_trials + 1):
        curr = [0] * (k + 1)
        curr[1] = t
        for e in range(2, k + 1):
            curr[e] = prev[e - 1] + 1 + prev[e]

        if curr[k] >= n:
            return t

        prev = curr

    return 64


def solve():
    while True:
        line = input().strip()
        if not line:
            continue

        parts = line.split()
        if len(parts) == 1 and parts[0] == "0":
            break
        
        k, n = map(int, parts)

        ans = min_trials(k, n)
        if ans > 63:
            print("More than 63 trials needed.")
        else:
            print(ans)


if __name__ == "__main__":
    solve()
