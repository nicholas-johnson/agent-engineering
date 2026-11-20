import unittest

from dormouse.settings import DEFAULTS, check, update


class TestSettings(unittest.TestCase):
    def test_every_default_is_allowed(self):
        for name, value in DEFAULTS.items():
            check(name, value)

    def test_unknown_setting_is_rejected(self):
        with self.assertRaises(ValueError):
            check("turbo_mode", True)

    def test_boost_temperature_goes_in_half_degrees(self):
        check("boost_temperature", 21.5)
        with self.assertRaises(ValueError):
            check("boost_temperature", 21.3)

    def test_boost_temperature_has_a_range(self):
        with self.assertRaises(ValueError):
            check("boost_temperature", 30)

    def test_switches_are_on_or_off(self):
        with self.assertRaises(ValueError):
            check("warm_wake", "yes")

    def test_update_returns_a_new_copy(self):
        settings = dict(DEFAULTS)
        changed = update(settings, {"geofencing": True})
        self.assertTrue(changed["geofencing"])
        self.assertFalse(settings["geofencing"])

    def test_update_checks_every_change(self):
        with self.assertRaises(ValueError):
            update(DEFAULTS, {"week_starts_on": "Friday"})


if __name__ == "__main__":
    unittest.main()
