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

class TestQuestion10190(unittest.TestCase):
    
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
        input_data = """125 5\n30 3\n80 2\n81 3"""
        expected_output = """125 25 5 1\nBoring!\nBoring!\n81 27 9 3 1"""
        output = self.run_test_case("q10190_std", "question_10190.py", input_data)
        self.assertEqual(output, expected_output)

    def test_easy_solution(self):
        input_data = """125 5\n30 3\n80 2\n81 3"""
        expected_output = """125 25 5 1\nBoring!\nBoring!\n81 27 9 3 1"""
        output = self.run_test_case("q10190_easy", "question_10190-easy.py", input_data)
        self.assertEqual(output, expected_output)
        
    def test_manual_solution(self):
        input_data = """125 5\n30 3\n80 2\n81 3"""
        expected_output = """125 25 5 1\nBoring!\nBoring!\n81 27 9 3 1"""
        output = self.run_test_case("q10190_manual", "question_10190-manual.py", input_data)
        self.assertEqual(output, expected_output)
        
    def test_edge_cases(self):
        input_data = """1 5\n10 1\n0 0"""
        expected_output = """Boring!\nBoring!\nBoring!"""
        output = self.run_test_case("q10190_std", "question_10190.py", input_data)
        self.assertEqual(output, expected_output)

if __name__ == '__main__':
    unittest.main()
