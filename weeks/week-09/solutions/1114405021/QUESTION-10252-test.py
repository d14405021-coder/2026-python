# 測試程式：QUESTION-10252
# 比對 easy 與 manual 的輸出

from io import StringIO
import importlib.util
import sys


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_solve(mod, data):
    old_in = sys.stdin
    old_out = sys.stdout
    sys.stdin = StringIO(data)
    buf = StringIO()
    sys.stdout = buf
    try:
        mod.solve()
        return buf.getvalue().strip()
    finally:
        sys.stdin = old_in
        sys.stdout = old_out


def main():
    data = "1\n3\n0 0\n1 1\n2 2\n"
    easy = load_module("QUESTION-10252-easy.py", "q10252_easy")
    manual = load_module("QUESTION-10252-manual.py", "q10252_manual")

    out_easy = run_solve(easy, data)
    out_manual = run_solve(manual, data)

    print("PASS" if out_easy == out_manual else "FAIL")


if __name__ == "__main__":
    main()
