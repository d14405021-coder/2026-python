import unittest

from robot_core import RobotState, run_commands, turn_left, turn_right


class TestRobotCore(unittest.TestCase):
    def test_turn_left_from_north(self):
        self.assertEqual(turn_left("N"), "W")

    def test_turn_right_from_north(self):
        self.assertEqual(turn_right("N"), "E")

    def test_turn_left_accepts_lowercase_direction(self):
        self.assertEqual(turn_left("n"), "W")

    def test_four_right_turns_back_to_origin_direction(self):
        direction = "N"
        for _ in range(4):
            direction = turn_right(direction)
        self.assertEqual(direction, "N")

    def test_move_inside_boundary_stays_alive(self):
        scents = set()
        result = run_commands(0, 0, "N", "F", 5, 3, scents)
        self.assertEqual((result.x, result.y, result.direction, result.lost), (0, 1, "N", False))

    def test_out_of_bounds_marks_lost(self):
        scents = set()
        result = run_commands(5, 3, "N", "F", 5, 3, scents)
        self.assertTrue(result.lost)

    def test_lost_robot_stops_following_commands(self):
        scents = set()
        result = run_commands(5, 3, "N", "FRFRF", 5, 3, scents)
        self.assertEqual((result.x, result.y, result.direction), (5, 3, "N"))
        self.assertTrue(result.lost)


if __name__ == "__main__":
    unittest.main()
