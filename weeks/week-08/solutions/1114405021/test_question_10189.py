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

class TestQuestion10189(unittest.TestCase):
    
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
        input_data = """4 4\n*...\n....\n.*..\n....\n3 5\n**...\n.....\n.*...\n0 0"""
        expected_output = """Field #1:\n*100\n2210\n1*10\n1110\n\nField #2:\n**100\n33200\n1*100"""
        output = self.run_test_case("q10189_std", "question_10189.py", input_data)
        self.assertEqual(output, expected_output)

    def test_easy_solution(self):
        input_data = """4 4\n*...\n....\n.*..\n....\n3 5\n**...\n.....\n.*...\n0 0"""
        expected_output = """Field #1:\n*100\n2210\n1*10\n1110\n\nField #2:\n**100\n33200\n1*100"""
        output = self.run_test_case("q10189_easy", "question_10189-easy.py", input_data)
        self.assertEqual(output, expected_output)
        
    def test_manual_solution(self):
        input_data = """4 4\n*...\n....\n.*..\n....\n3 5\n**...\n.....\n.*...\n0 0"""
        expected_output = """Field #1:\n*100\n2210\n1*10\n1110\n\nField #2:\n**100\n33200\n1*100"""
        output = self.run_test_case("q10189_manual", "question_10189-manual.py", input_data)
        self.assertEqual(output, expected_output)
        
    def test_single_field(self):
        input_data = """3 3\n...\n.*.\n...\n0 0"""
        expected_output = """Field #1:\n111\n1*1\n111"""
        output = self.run_test_case("q10189_std", "question_10189.py", input_data)
        self.assertEqual(output, expected_output)

if __name__ == '__main__':
    unittest.main()
