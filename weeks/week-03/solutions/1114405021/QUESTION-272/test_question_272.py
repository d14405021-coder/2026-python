#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
UVA 272 TeX 引號轉換 - 簡易版本測試

直接測試轉換函數是否正常工作
"""

def convert_quote_to_tex(text):
    """轉換雙引號為 TeX 格式"""
    result = []
    in_quote = False

    for char in text:
        if char == '"':
            if in_quote:
                result.append("''")
                in_quote = False
            else:
                result.append("``")
                in_quote = True
        else:
            result.append(char)

    return ''.join(result)

# 測試案例
test_cases = [
    ('He said "Hello"', 'He said ``Hello\'\''),
    ('"To be or not to be," quoth the bard, "that is the question."', 
     '``To be or not to be,\'\' quoth the bard, ``that is the question.\'\''),
    ('A "quick" "brown" fox', 'A ``quick\'\' ``brown\'\' fox'),
    ('No quotes here', 'No quotes here'),
    ('""', '``\'\''),
]

# 執行測試
print("UVA 272 TeX 引號轉換測試")
print("=" * 50)

passed = 0
failed = 0

for i, (input_text, expected) in enumerate(test_cases, 1):
    result = convert_quote_to_tex(input_text)
    if result == expected:
        print(f"✓ 測試 {i} 通過")
        passed += 1
    else:
        print(f"✗ 測試 {i} 失敗")
        print(f"  輸入:  {input_text}")
        print(f"  預期:  {expected}")
        print(f"  結果:  {result}")
        failed += 1

print("=" * 50)
print(f"總計: {passed} 通過, {failed} 失敗")
