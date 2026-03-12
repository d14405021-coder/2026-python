# R7. OrderedDict（1.7）

from collections import OrderedDict
import json

# OrderedDict 會記住「鍵值插入的順序」。
# 在較舊 Python 版本中，一般 dict 不保證順序時，OrderedDict 特別有用。
# 在現代 Python（3.7+）一般 dict 也會保留插入順序，
# 但 OrderedDict 仍可用於表達「我就是要有序映射」這個語意。
d = OrderedDict()

# 依序插入兩個鍵：foo 再 bar
d['foo'] = 1; d['bar'] = 2

# 轉成 JSON 字串時，會依照目前字典的鍵順序輸出。
# 這裡預期結果類似：{"foo": 1, "bar": 2}
# （是否有空白取決於 dumps 的參數設定）
json.dumps(d)

# 閱讀這段程式的重點：
# 1) 先看資料型別是不是 OrderedDict
# 2) 再追蹤鍵被加入的先後順序
# 3) 最後觀察序列化（如 JSON）是否需要維持此順序
