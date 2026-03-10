"""
Test cases for Task 2: Student Ranking
Using Test-Driven Development approach
"""
import unittest
import sys
from pathlib import Path

# Add parent directory to path to import task modules
sys.path.insert(0, str(Path(__file__).parent.parent))
from task2_student_ranking import rank_students


class TestRankStudentsNormalCase(unittest.TestCase):
    """Test rank_students with normal cases"""
    
    def test_normal_case_with_tie_breaks(self):
        """Normal case: ranking with score, age, and name tiebreakers"""
        students = [
            ("amy", 88, 20),
            ("bob", 88, 19),
            ("zoe", 92, 21),
            ("ian", 88, 19),
            ("leo", 75, 20),
            ("eva", 92, 20)
        ]
        k = 3
        expected = [
            ("eva", 92, 20),
            ("zoe", 92, 21),
            ("bob", 88, 19)
        ]
        result = rank_students(students, k)
        self.assertEqual(result, expected)
    
    def test_return_top_k_only(self):
        """Normal case: return exactly k students"""
        students = [
            ("alice", 90, 20),
            ("bob", 85, 19),
            ("charlie", 88, 21)
        ]
        k = 2
        expected = [
            ("alice", 90, 20),
            ("charlie", 88, 21)
        ]
        result = rank_students(students, k)
        self.assertEqual(result, expected)
    
    def test_all_different_scores(self):
        """Normal case: all students have different scores"""
        students = [
            ("alice", 95, 20),
            ("bob", 85, 19),
            ("charlie", 90, 21)
        ]
        k = 2
        expected = [
            ("alice", 95, 20),
            ("charlie", 90, 21)
        ]
        result = rank_students(students, k)
        self.assertEqual(result, expected)


class TestRankStudentsBoundaryCase(unittest.TestCase):
    """Test rank_students with boundary cases"""
    
    def test_k_equals_one(self):
        """Boundary case: k=1, return only top student"""
        students = [
            ("alice", 90, 20),
            ("bob", 85, 19),
            ("charlie", 90, 19)
        ]
        k = 1
        expected = [("bob", 85, 19)] if [("bob", 85, 19)] else []
        result = rank_students(students, k)
        self.assertEqual(len(result), 1)
    
    def test_k_equals_n(self):
        """Boundary case: k equals total number of students"""
        students = [
            ("alice", 90, 20),
            ("bob", 85, 19)
        ]
        k = 2
        expected = [
            ("alice", 90, 20),
            ("bob", 85, 19)
        ]
        result = rank_students(students, k)
        self.assertEqual(result, expected)
    
    def test_single_student(self):
        """Boundary case: only one student"""
        students = [("alice", 90, 20)]
        k = 1
        expected = [("alice", 90, 20)]
        result = rank_students(students, k)
        self.assertEqual(result, expected)


class TestRankStudentsTieBreaker(unittest.TestCase):
    """Test rank_students with various tiebreaker scenarios"""
    
    def test_same_score_different_age(self):
        """Tiebreaker: same score differs by age (younger first)"""
        students = [
            ("alice", 88, 22),
            ("bob", 88, 19),
            ("charlie", 88, 20)
        ]
        k = 3
        expected = [
            ("bob", 88, 19),
            ("charlie", 88, 20),
            ("alice", 88, 22)
        ]
        result = rank_students(students, k)
        self.assertEqual(result, expected)
    
    def test_same_score_same_age_different_name(self):
        """Tiebreaker: same score and age differs by name (alphabetical)"""
        students = [
            ("zoe", 88, 19),
            ("alice", 88, 19),
            ("bob", 88, 19)
        ]
        k = 3
        expected = [
            ("alice", 88, 19),
            ("bob", 88, 19),
            ("zoe", 88, 19)
        ]
        result = rank_students(students, k)
        self.assertEqual(result, expected)
    
    def test_complex_tiebreaker_chain(self):
        """Tiebreaker: score → age → name chain"""
        students = [
            ("zoe", 85, 20),
            ("alice", 85, 19),
            ("bob", 85, 19),
            ("charlie", 90, 21)
        ]
        k = 4
        expected = [
            ("charlie", 90, 21),
            ("alice", 85, 19),
            ("bob", 85, 19),
            ("zoe", 85, 20)
        ]
        result = rank_students(students, k)
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main(verbosity=2)
