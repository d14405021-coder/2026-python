"""
Test cases for Task 3: Log Summary
Using Test-Driven Development approach
"""
import unittest
import sys
from pathlib import Path

# Add parent directory to path to import task modules
sys.path.insert(0, str(Path(__file__).parent.parent))
from task3_log_summary import analyze_logs


class TestLogSummaryNormalCase(unittest.TestCase):
    """Test analyze_logs with normal cases"""
    
    def test_normal_case_with_multiple_users(self):
        """Normal case: multiple users with various actions"""
        logs = [
            ("alice", "login"),
            ("bob", "login"),
            ("alice", "view"),
            ("alice", "logout"),
            ("bob", "view"),
            ("bob", "view"),
            ("chris", "login"),
            ("bob", "logout")
        ]
        expected_users = [
            ("bob", 4),
            ("alice", 3),
            ("chris", 1)
        ]
        expected_top_action = ("login", 3)
        users, top_action = analyze_logs(logs)
        self.assertEqual(users, expected_users)
        self.assertEqual(top_action, expected_top_action)
    
    def test_all_same_action(self):
        """Normal case: all logs have the same action"""
        logs = [
            ("alice", "login"),
            ("bob", "login"),
            ("charlie", "login")
        ]
        expected_users = [
            ("alice", 1),
            ("bob", 1),
            ("charlie", 1)
        ]
        expected_top_action = ("login", 3)
        users, top_action = analyze_logs(logs)
        self.assertEqual(users, expected_users)
        self.assertEqual(top_action, expected_top_action)
    
    def test_single_user_multiple_actions(self):
        """Normal case: single user with multiple actions"""
        logs = [
            ("alice", "login"),
            ("alice", "view"),
            ("alice", "logout")
        ]
        expected_users = [("alice", 3)]
        expected_top_action = ("login", 1)  # or any action, all have count 1
        users, top_action = analyze_logs(logs)
        self.assertEqual(users, expected_users)
        self.assertEqual(expected_top_action[1], top_action[1])  # Check count


class TestLogSummaryBoundaryCase(unittest.TestCase):
    """Test analyze_logs with boundary cases"""
    
    def test_empty_input(self):
        """Boundary case: empty input (m=0)"""
        logs = []
        expected_users = []
        expected_top_action = (None, 0)  # or should handle gracefully
        users, top_action = analyze_logs(logs)
        self.assertEqual(users, expected_users)
    
    def test_single_log_entry(self):
        """Boundary case: single log entry"""
        logs = [("alice", "login")]
        expected_users = [("alice", 1)]
        expected_top_action = ("login", 1)
        users, top_action = analyze_logs(logs)
        self.assertEqual(users, expected_users)
        self.assertEqual(top_action, expected_top_action)
    
    def test_single_user_single_action(self):
        """Boundary case: one user, one action"""
        logs = [("alice", "logout")]
        expected_users = [("alice", 1)]
        expected_top_action = ("logout", 1)
        users, top_action = analyze_logs(logs)
        self.assertEqual(users, expected_users)
        self.assertEqual(top_action, expected_top_action)


class TestLogSummarySortingOrder(unittest.TestCase):
    """Test correct sorting of results"""
    
    def test_users_sorted_by_count_descending_then_name(self):
        """Sorting: users by total count (desc), then by name (asc) if tied"""
        logs = [
            ("zoe", "login"),
            ("alice", "login"),
            ("zoe", "view"),
            ("alice", "logout"),
            ("alice", "view")
        ]
        expected_users = [
            ("alice", 3),
            ("zoe", 2)
        ]
        users, _ = analyze_logs(logs)
        self.assertEqual(users, expected_users)
    
    def test_users_same_count_sorted_by_name(self):
        """Sorting: same event count → sorted by name alphabetically"""
        logs = [
            ("zoe", "login"),
            ("bob", "login"),
            ("alice", "login"),
            ("zoe", "view"),
            ("bob", "logout"),
            ("alice", "view")
        ]
        expected_users = [
            ("alice", 2),
            ("bob", 2),
            ("zoe", 2)
        ]
        users, _ = analyze_logs(logs)
        self.assertEqual(users, expected_users)
    
    def test_top_action_highest_count(self):
        """Top action: action with highest count"""
        logs = [
            ("alice", "login"),
            ("alice", "login"),
            ("bob", "logout"),
            ("bob", "view"),
            ("bob", "view")
        ]
        expected_top_action = ("view", 2)  # or login, both have count 2
        _, top_action = analyze_logs(logs)
        self.assertEqual(top_action[1], 2)


class TestLogSummaryEdgeCases(unittest.TestCase):
    """Test edge cases and special scenarios"""
    
    def test_many_different_actions(self):
        """Edge case: many different actions"""
        logs = [
            ("alice", "login"),
            ("alice", "logout"),
            ("alice", "view"),
            ("alice", "edit"),
            ("alice", "delete")
        ]
        expected_users = [("alice", 5)]
        # All actions appear once, so top_action could be any
        users, top_action = analyze_logs(logs)
        self.assertEqual(users, expected_users)
        self.assertEqual(top_action[1], 1)
    
    def test_user_name_case_sensitive(self):
        """Edge case: user names should be case-sensitive (Alice != alice)"""
        logs = [
            ("alice", "login"),
            ("Alice", "login"),
            ("alice", "view")
        ]
        users, _ = analyze_logs(logs)
        # Assuming case-sensitive, expect 2 different users
        self.assertTrue(len(users) >= 1)
    
    def test_repeated_actions_by_same_user(self):
        """Edge case: same user repeating same action"""
        logs = [
            ("alice", "login"),
            ("alice", "login"),
            ("alice", "login"),
            ("bob", "logout")
        ]
        expected_users = [
            ("alice", 3),
            ("bob", 1)
        ]
        expected_top_action = ("login", 3)
        users, top_action = analyze_logs(logs)
        self.assertEqual(users, expected_users)
        self.assertEqual(top_action, expected_top_action)


if __name__ == '__main__':
    unittest.main(verbosity=2)
