# 測試程式：QUESTION-10242
# 比對 easy 與 manual 的輸出

from io import StringIO
import importlib.util
import sys


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_solve(mod, data, func_name):
    old_in = sys.stdin
    old_out = sys.stdout
    sys.stdin = StringIO(data)
    buf = StringIO()
    sys.stdout = buf
    try:
        getattr(mod, func_name)()
        return buf.getvalue().strip()
    finally:
        sys.stdin = old_in
        sys.stdout = old_out


def main():
    # 使用無環測資，避免遞迴循環問題
    data = (
        "4 4\n"
        "1 2\n"
        "2 3\n"
        "3 4\n"
        "1 4\n"
        "5\n"
        "4\n"
        "3\n"
        "2\n"
        "1 1\n"
        "4\n"
        "0 0\n"
    )

    easy = load_module("QUESTION-10242-easy.py", "q10242_easy")
    manual = load_module("QUESTION-10242-manual.py", "q10242_manual")

    out_easy = run_solve(easy, data, "solve_atm_robbery")
    out_manual = run_solve(manual, data, "solve")

    print("PASS" if out_easy == out_manual else "FAIL")


if __name__ == "__main__":
    main()
