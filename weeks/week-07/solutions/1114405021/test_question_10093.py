import unittest
from io import StringIO
import sys
import importlib.util


def load_module_from_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


class TestQuestion10093(unittest.TestCase):
    def run_test_with_input(self, module_name, file_name, input_data):
        original_stdin = sys.stdin
        original_stdout = sys.stdout

        sys.stdin = StringIO(input_data)
        fake_stdout = StringIO()
        sys.stdout = fake_stdout

        try:
            module = load_module_from_path(module_name, file_name)
            module.solve()
            output = fake_stdout.getvalue().strip()
            return output
        finally:
            sys.stdin = original_stdin
            sys.stdout = original_stdout

    def test_standard_solution(self):
        input_data = "5 4\nPHPP\nPPHH\nPPPP\nPHPP\nPHHP"
        expected_output = "6"
        output = self.run_test_with_input("q_std", "question_10093.py", input_data)
        self.assertEqual(output, expected_output)

    def test_easy_solution(self):
        input_data = "5 4\nPHPP\nPPHH\nPPPP\nPHPP\nPHHP"
        expected_output = "6"
        output = self.run_test_with_input(
            "q_easy", "question_10093-easy.py", input_data
        )
        self.assertEqual(output, expected_output)

    def test_manual_solution(self):
        input_data = "5 4\nPHPP\nPPHH\nPPPP\nPHPP\nPHHP"
        expected_output = "6"
        output = self.run_test_with_input(
            "q_man", "question_10093-manual.py", input_data
        )
        self.assertEqual(output, expected_output)

    def test_edge_case_all_plains(self):
        input_data = "3 3\nPPP\nPPP\nPPP"
        expected_output = "4"
        output = self.run_test_with_input("q_std", "question_10093.py", input_data)
        self.assertEqual(output, expected_output)

    def test_edge_case_all_hills(self):
        input_data = "3 3\nHHH\nHHH\nHHH"
        expected_output = "0"
        output = self.run_test_with_input("q_std", "question_10093.py", input_data)
        self.assertEqual(output, expected_output)


if __name__ == "__main__":
    unittest.main()
