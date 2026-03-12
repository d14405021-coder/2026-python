import unittest

from robot_core import run_commands


class TestRobotScent(unittest.TestCase):
    def test_first_lost_robot_leaves_scent(self):
        scents = set()
        run_commands(5, 3, "N", "F", 5, 3, scents)
        self.assertIn((5, 3, "N"), scents)

    def test_second_robot_ignores_dangerous_forward_with_same_scent(self):
        scents = set()
        first = run_commands(5, 3, "N", "F", 5, 3, scents)
        second = run_commands(5, 3, "N", "F", 5, 3, scents)

        self.assertTrue(first.lost)
        self.assertFalse(second.lost)
        self.assertEqual((second.x, second.y, second.direction), (5, 3, "N"))

    def test_same_position_but_different_direction_should_not_share_scent(self):
        scents = set()
        run_commands(5, 3, "N", "F", 5, 3, scents)
        second = run_commands(5, 3, "E", "F", 5, 3, scents)

        self.assertTrue(second.lost)
        self.assertIn((5, 3, "E"), scents)

    def test_invalid_command_raises_error(self):
        scents = set()
        with self.assertRaises(ValueError):
            run_commands(0, 0, "N", "X", 5, 3, scents)


if __name__ == "__main__":
    unittest.main()
