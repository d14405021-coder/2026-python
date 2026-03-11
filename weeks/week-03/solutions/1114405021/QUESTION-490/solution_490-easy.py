"""簡易版本：UVA 490 旋轉句子

簡單寫法，只用一個迴圈結構，沒有額外函式。
概念：讀完所有行，求最大寬度，然後逐列輸出。
"""

import sys

lines = [line.rstrip("\n") for line in sys.stdin]
if not lines:
    sys.exit(0)

max_len = max(len(l) for l in lines)
for i in range(max_len):
    row = []
    for j in range(len(lines) - 1, -1, -1):
        ch = lines[j][i] if i < len(lines[j]) else ' '
        row.append(ch)
    sys.stdout.write(''.join(row) + '\n')
