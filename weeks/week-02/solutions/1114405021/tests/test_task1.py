"""
Test cases for Task 1: Sequence Clean
Using Test-Driven Development approach
"""
import unittest
import sys
from pathlib import Path

# Add parent directory to path to import task modules
sys.path.insert(0, str(Path(__file__).parent.parent))
from task1_sequence_clean import (
    dedupe_preserve_order,
    sort_ascending,
    sort_descending,
    extract_evens
)


class TestDedupePreserveOrder(unittest.TestCase):
    """Test dedupe_preserve_order function"""
    
    def test_normal_case_with_duplicates(self):
        """Normal case: sequence with duplicates preserves first occurrence"""
        input_seq = [5, 3, 5, 2, 9, 2, 8, 3, 1]
        expected = [5, 3, 2, 9, 8, 1]
        self.assertEqual(dedupe_preserve_order(input_seq), expected)
    
    def test_boundary_single_element(self):
        """Boundary case: single element"""
        input_seq = [1]
        expected = [1]
        self.assertEqual(dedupe_preserve_order(input_seq), expected)
    
    def test_no_duplicates(self):
        """Edge case: sequence with no duplicates"""
        input_seq = [1, 2, 3, 4, 5]
        expected = [1, 2, 3, 4, 5]
        self.assertEqual(dedupe_preserve_order(input_seq), expected)


class TestSortAscending(unittest.TestCase):
    """Test sort_ascending function"""
    
    def test_normal_case_unsorted(self):
        """Normal case: unsorted sequence should be sorted ascending"""
        input_seq = [5, 3, 5, 2, 9, 2, 8, 3, 1]
        expected = [1, 2, 2, 3, 3, 5, 5, 8, 9]
        self.assertEqual(sort_ascending(input_seq), expected)
    
    def test_boundary_single_element(self):
        """Boundary case: single element"""
        input_seq = [5]
        expected = [5]
        self.assertEqual(sort_ascending(input_seq), expected)
    
    def test_already_sorted(self):
        """Edge case: already sorted in ascending order"""
        input_seq = [1, 2, 3, 4, 5]
        expected = [1, 2, 3, 4, 5]
        self.assertEqual(sort_ascending(input_seq), expected)


class TestSortDescending(unittest.TestCase):
    """Test sort_descending function"""
    
    def test_normal_case_unsorted(self):
        """Normal case: unsorted sequence should be sorted descending"""
        input_seq = [5, 3, 5, 2, 9, 2, 8, 3, 1]
        expected = [9, 8, 5, 5, 3, 3, 2, 2, 1]
        self.assertEqual(sort_descending(input_seq), expected)
    
    def test_boundary_single_element(self):
        """Boundary case: single element"""
        input_seq = [5]
        expected = [5]
        self.assertEqual(sort_descending(input_seq), expected)
    
    def test_already_sorted_descending(self):
        """Edge case: already sorted in descending order"""
        input_seq = [5, 4, 3, 2, 1]
        expected = [5, 4, 3, 2, 1]
        self.assertEqual(sort_descending(input_seq), expected)


class TestExtractEvens(unittest.TestCase):
    """Test extract_evens function"""
    
    def test_normal_case_mixed_numbers(self):
        """Normal case: extract evens while maintaining original order"""
        input_seq = [5, 3, 5, 2, 9, 2, 8, 3, 1]
        expected = [2, 2, 8]
        self.assertEqual(extract_evens(input_seq), expected)
    
    def test_boundary_no_evens(self):
        """Boundary case: sequence with no even numbers"""
        input_seq = [1, 3, 5, 7, 9]
        expected = []
        self.assertEqual(extract_evens(input_seq), expected)
    
    def test_all_evens(self):
        """Edge case: all numbers are even"""
        input_seq = [2, 4, 6, 8, 10]
        expected = [2, 4, 6, 8, 10]
        self.assertEqual(extract_evens(input_seq), expected)


if __name__ == '__main__':
    unittest.main(verbosity=2)
