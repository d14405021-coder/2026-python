"""
UVA 490 簡易測試版本

不使用 unittest，只使用函式呼叫和簡單輸出。
註解以繁體中文解釋每個測試案例。
"""

from solution_490 import rotate_sentences


def run_case(input_lines):
    """給定多行輸入，回傳旋轉後的結果串接"""
    return "\n".join(rotate_sentences(input_lines)) + ("\n" if input_lines else "")


def test_basic():
    """測試標準範例"""
    inp = ["HELLO", "WORLD"]
    expected = "WH\nOE\nRL\nLL\nDO\n"
    assert run_case(inp) == expected


def test_single():
    """單行測試"""
    assert run_case(["ABC"]) == "A\nB\nC\n"


def test_empty():
    """空輸入應無輸出"""
    assert run_case([]) == ""


def test_diff_len():
    """行長度不一"""
    inp = ["A", "BC", "DEF"]
    expected = "DBA\nEC \nF  \n"
    assert run_case(inp) == expected


def test_spaces():
    """包含空格和標點"""
    assert run_case(["Hi, there!", "123"]) == "1H\n2i\n3,\n  \n t\n h\n e\n r\n e\n !\n"


def run_easy_tests():
    """執行所有簡易測試並輸出結果"""
    tests = [
        test_basic,
        test_single,
        test_empty,
        test_diff_len,
        test_spaces,
    ]
    passed = 0
    for t in tests:
        try:
            t()
            print(f"{t.__name__}: PASS")
            passed += 1
        except AssertionError:
            print(f"{t.__name__}: FAIL")
    print(f"passed {passed}/{len(tests)}")


if __name__ == '__main__':
    run_easy_tests()
