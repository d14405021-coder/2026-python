# 題目：UVA 10226 / ZeroJudge a219（手打版）
# 說明：
# 1) 以最直觀的 DFS 回溯法列舉所有合法排列
# 2) 按字典序輸出
# 3) 與上一個答案相比，只輸出不同區段


def solve():
    first_case = True

    while True:
        try:
            line = input().strip()
            if not line:
                continue

            n = int(line)
            hates = []

            # 讀每個人的「不想排的位置」清單，以 0 結束
            for _ in range(n):
                bad_positions = []
                while True:
                    parts = input().strip().split()
                    if not parts:
                        continue

                    finished = False
                    for token in parts:
                        value = int(token)
                        if value == 0:
                            finished = True
                            break
                        bad_positions.append(value)

                    if finished:
                        break

                hates.append(bad_positions)

            # 測資間要空一行
            if not first_case:
                print()
            first_case = False

            used = [False] * n
            perm = [0] * n
            prev_output = [""]

            def dfs(pos):
                # 若已排滿，組字串並輸出差異段
                if pos == n:
                    current = ""
                    for i in range(n):
                        current += chr(65 + perm[i])

                    last = prev_output[0]

                    if last == "":
                        print(current)
                    else:
                        # 找共同前綴終點
                        left = 0
                        while left < n and current[left] == last[left]:
                            left += 1

                        # 找共同後綴起點
                        right = n - 1
                        while right > left and current[right] == last[right]:
                            right -= 1

                        diff = ""
                        for k in range(left, right + 1):
                            diff += current[k]

                        print(diff)

                    prev_output[0] = current
                    return

                # 依人員編號（A, B, C...）順序嘗試，保證字典序
                for person in range(n):
                    if used[person]:
                        continue

                    dislike_here = False
                    for bad in hates[person]:
                        if bad == pos + 1:
                            dislike_here = True
                            break

                    if dislike_here:
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
