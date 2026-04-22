# UVA 10252 - 手打程式
# 手打版採用直觀暴力法：枚舉整數座標，計算距離和。

import math


def solve():
    t = int(input().strip())

    for _ in range(t):
        n = int(input().strip())
        points = []
        for _ in range(n):
            x, y = map(int, input().split())
            points.append((x, y))

        xs = [x for x, _ in points]
        ys = [y for _, y in points]

        min_x = min(xs) - 10
        max_x = max(xs) + 10
        min_y = min(ys) - 10
        max_y = max(ys) + 10

        best = float("inf")
        cnt = 0

        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                total = 0.0
                for px, py in points:
                    total += math.sqrt((x - px) ** 2 + (y - py) ** 2)

                if total < best:
                    best = total
                    cnt = 1
                elif abs(total - best) < 1e-9:
                    cnt += 1

        print(int(best), cnt)


if __name__ == "__main__":
    solve()
