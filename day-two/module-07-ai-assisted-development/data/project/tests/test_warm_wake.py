import unittest
from datetime import datetime

from dormouse.settings import DEFAULTS
from dormouse.warm_wake import heating_start, minutes_to_heat

SEVEN = datetime(2026, 11, 20, 7, 0)


class TestWarmWake(unittest.TestCase):
    def test_minutes_to_heat(self):
        self.assertEqual(minutes_to_heat(17, 20, 4), 45)

    def test_a_warm_room_needs_no_time(self):
        self.assertEqual(minutes_to_heat(21, 20, 4), 0)

    def test_starts_early_by_the_time_the_home_takes_to_heat(self):
        start = heating_start(SEVEN, 17, 20, 4, dict(DEFAULTS))
        self.assertEqual(start, datetime(2026, 11, 20, 6, 15))

    def test_never_more_than_90_minutes_early(self):
        start = heating_start(SEVEN, 10, 21, 2, dict(DEFAULTS))
        self.assertEqual(start, datetime(2026, 11, 20, 5, 30))

    def test_when_warm_wake_is_off_the_heating_starts_on_time(self):
        settings = {**DEFAULTS, "warm_wake": False}
        self.assertEqual(heating_start(SEVEN, 10, 21, 2, settings), SEVEN)


if __name__ == "__main__":
    unittest.main()
