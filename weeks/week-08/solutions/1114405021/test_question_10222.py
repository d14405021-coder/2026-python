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

class TestQuestion10222(unittest.TestCase):
    
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
        input_data = """k[r d o\nvnxdt"""
        expected_output = """how a r\nthere"""
        output = self.run_test_case("q10222_std", "question_10222.py", input_data)
        self.assertEqual(output, expected_output)

    def test_easy_solution(self):
        input_data = """k[r d o\nvnxdt"""
        expected_output = """how a r\nthere"""
        output = self.run_test_case("q10222_easy", "question_10222-easy.py", input_data)
        self.assertEqual(output, expected_output)
        
    def test_manual_solution(self):
        input_data = """k[r d o\nvnxdt"""
        expected_output = """how a r\nthere"""
        output = self.run_test_case("q10222_manual", "question_10222-manual.py", input_data)
        self.assertEqual(output, expected_output)
        
    def test_capital_letters(self):
        input_data = """K[R D O"""
        expected_output = """how a r"""
        output = self.run_test_case("q10222_std", "question_10222.py", input_data)
        self.assertEqual(output, expected_output)

if __name__ == '__main__':
    unittest.main()
