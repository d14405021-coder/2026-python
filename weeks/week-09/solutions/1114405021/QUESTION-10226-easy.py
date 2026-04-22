# UVA 10226 / a219 - AI 簡單版（中文註解）
# 目標：列出所有合法排列，且只輸出和上一筆不同的區段。


def solve():
    first_case = True

    while True:
        try:
            line = input().strip()
            if not line:
                continue

            n = int(line)
            hates = []

            # 讀入每個人的禁位，0 表示該人的輸入結束
            for _ in range(n):
                bad = []
                while True:
                    parts = input().strip().split()
                    if not parts:
                        continue
                    done = False
                    for p in parts:
                        v = int(p)
                        if v == 0:
                            done = True
                            break
                        bad.append(v)
                    if done:
                        break
                hates.append(bad)

            if not first_case:
                print()
            first_case = False

            used = [False] * n
            perm = [0] * n
            prev = [""]

            def dfs(pos):
                if pos == n:
                    cur = ""
                    for x in perm:
                        cur += chr(65 + x)

                    if prev[0] == "":
                        print(cur)
                    else:
                        i = 0
                        while i < n and cur[i] == prev[0][i]:
                            i += 1
                        j = n - 1
                        while j > i and cur[j] == prev[0][j]:
                            j -= 1
                        print(cur[i:j + 1])

                    prev[0] = cur
                    return

                for person in range(n):
                    if used[person]:
                        continue
                    if (pos + 1) in hates[person]:
                        continue
                    used[person] = True
                    perm[pos] = person
                    dfs(pos + 1)
                    used[person] = False

            dfs(0)

        except EOFError:
            break


if __name__ == "__main__":
    solve()
