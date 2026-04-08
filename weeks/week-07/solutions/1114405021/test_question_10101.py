import unittest
import sys
from io import StringIO
import importlib.util

def run_test(module_name, file_name, input_data):
    original_stdin = sys.stdin
    original_stdout = sys.stdout
    sys.stdin = StringIO(input_data)
    fake_stdout = StringIO()
    sys.stdout = fake_stdout
    
    try:
        spec = importlib.util.spec_from_file_location(module_name, file_name)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        module.solve()
        output = fake_stdout.getvalue().strip()
        return output
    finally:
        sys.stdin = original_stdin
        sys.stdout = original_stdout

class TestQuestion10101(unittest.TestCase):
    def test_std(self):
        self.assertEqual(run_test("q_std", "question_10101.py", "1+1=3#"), "1+1=2#")
        
    def test_easy(self):
        self.assertEqual(run_test("q_easy", "question_10101-easy.py", "7-1=8#"), "7-1=6#")
        
    def test_manual(self):
        self.assertEqual(run_test("q_man", "question_10101-manual.py", "1+2=3#"), "No")

if __name__ == '__main__':
    unittest.main()
