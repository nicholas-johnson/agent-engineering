"""When Warm Wake will switch the heating on for one saved home, and that home's settings page.

From the project folder: python -m dormouse homes/flat-3b.json
"""

import json
import sys
from datetime import datetime
from pathlib import Path

from dormouse.pages import settings_page
from dormouse.warm_wake import heating_start, learned_rate

path = Path(sys.argv[1])
home = json.loads(path.read_text())
period = datetime.fromisoformat(home["next_period"]["start"])
target = home["next_period"]["target"]

rate = learned_rate(home["heat_ups"])
start = heating_start(period, home["room"], target, rate, home["settings"])
minutes = round((period - start).total_seconds() / 60)

print(f"{home['name']}: the room is at {home['room']:g} degrees. The next period starts at {period:%H:%M}, at {target:g} degrees.")
print(f"Warm Wake switches the heating on at {start:%H:%M}, {minutes} minutes early.")

page = path.with_suffix(".html")
page.write_text(settings_page(home["settings"]))
print(f"Settings page: {page}")
