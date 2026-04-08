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

class TestQuestion10170(unittest.TestCase):
    def test_std(self):
        self.assertEqual(run_test("q_std", "question_10170.py", "1 6\n3 10\n3 14"), "3\n5\n6")
        
    def test_easy(self):
        self.assertEqual(run_test("q_easy", "question_10170-easy.py", "1 6\n3 10\n3 14"), "3\n5\n6")
        
    def test_manual(self):
        self.assertEqual(run_test("q_man", "question_10170-manual.py", "1 6\n3 10\n3 14"), "3\n5\n6")

if __name__ == '__main__':
    unittest.main()
