# 測試程式：QUESTION-10226
# 測試 easy 與 manual 版本輸出是否一致

from io import StringIO
import importlib.util
import sys


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_solve(module, data):
    old_in = sys.stdin
    old_out = sys.stdout
    sys.stdin = StringIO(data)
    buf = StringIO()
    sys.stdout = buf
    try:
        module.solve()
        return buf.getvalue().strip()
    finally:
        sys.stdin = old_in
        sys.stdout = old_out


def main():
    data = "3\n0\n0\n0\n3\n1 0\n3 0\n0"
    easy = load_module("QUESTION-10226-easy.py", "q10226_easy")
    manual = load_module("QUESTION-10226-manual.py", "q10226_manual")

    out_easy = run_solve(easy, data)
    out_manual = run_solve(manual, data)

    print("PASS" if out_easy == out_manual else "FAIL")


if __name__ == "__main__":
    main()
