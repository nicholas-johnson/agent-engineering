import re
import unittest

from dormouse.pages import settings_page
from dormouse.settings import DEFAULTS


def section(html, heading):
    """The part of the page under one section heading."""
    match = re.search(rf"<h2>{heading}</h2>(.*?)(?=<h2>|$)", html, re.DOTALL)
    return match[1] if match else ""


class TestSettingsPage(unittest.TestCase):
    def test_every_setting_has_a_control(self):
        html = settings_page(DEFAULTS)
        for name in DEFAULTS:
            self.assertIn(f'name="{name}"', html)

    def test_sections_are_in_order(self):
        headings = re.findall(r"<h2>(.*?)</h2>", settings_page(DEFAULTS))
        self.assertEqual(headings, ["Heating", "Schedule", "Away"])

    def test_warm_wake_is_under_heating(self):
        self.assertIn("Warm Wake", section(settings_page(DEFAULTS), "Heating"))

    def test_switches_show_their_state(self):
        html = settings_page({**DEFAULTS, "geofencing": True})
        self.assertIn('name="geofencing" checked', html)


if __name__ == "__main__":
    unittest.main()
