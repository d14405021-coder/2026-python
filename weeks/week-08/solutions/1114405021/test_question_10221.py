import unittest
from io import StringIO
import sys
import importlib.util

def load_module(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

class TestQuestion10221(unittest.TestCase):
    
    def run_test_case(self, module_name, file_name, input_data):
        original_stdin = sys.stdin
        original_stdout = sys.stdout
        
        sys.stdin = StringIO(input_data)
        fake_stdout = StringIO()
        sys.stdout = fake_stdout
        
        try:
            module = load_module(module_name, file_name)
            module.solve()
            output = fake_stdout.getvalue().strip()
            return output
        finally:
            sys.stdin = original_stdin
            sys.stdout = original_stdout

    def test_standard_solution(self):
        input_data = """500 30 deg\n700 60 min\n200 45 deg"""
        expected_output = """3633.775503 3592.408346\n124.616509 124.614927\n5215.043805 5082.035982"""
        output = self.run_test_case("q10221_std", "question_10221.py", input_data)
        self.assertEqual(output, expected_output)

    def test_easy_solution(self):
        input_data = """500 30 deg\n700 60 min\n200 45 deg"""
        expected_output = """3633.775503 3592.408346\n124.616509 124.614927\n5215.043805 5082.035982"""
        output = self.run_test_case("q10221_easy", "question_10221-easy.py", input_data)
        self.assertEqual(output, expected_output)
        
    def test_manual_solution(self):
        input_data = """500 30 deg\n700 60 min\n200 45 deg"""
        expected_output = """3633.775503 3592.408346\n124.616509 124.614927\n5215.043805 5082.035982"""
        output = self.run_test_case("q10221_manual", "question_10221-manual.py", input_data)
        self.assertEqual(output, expected_output)
        
    def test_large_angle(self):
        # 測試角度 > 180 以及 >= 360 的情況
        # 390 度等同於 30 度
        # 330 度等同於 30 度 (因為 > 180 取 360 - a)
        input_data = """500 390 deg\n500 330 deg"""
        expected_output = """3633.775503 3592.408346\n3633.775503 3592.408346"""
        output = self.run_test_case("q10221_std", "question_10221.py", input_data)
        self.assertEqual(output, expected_output)

if __name__ == '__main__':
    unittest.main()
