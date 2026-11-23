# Debug hunt: a fresh copy of the Dormouse project with a customer's saved home that shows a bug, for you to find.
# Run from the module folder: uv run python playground/debug-hunt/play.py
#                         or: source ../../.venv/bin/activate && python playground/debug-hunt/play.py
#
# To play: open output/project in Cursor and use Debug mode on the bug report below, or try Claude Code.
# Run this script again to start from a clean copy.

import json
import shutil
from pathlib import Path

HERE = Path(__file__).parent
PROJECT = HERE.parent.parent / "data" / "project"
COPY = HERE / "output" / "project"

# A home whose settings were saved by an older version of the app.
HOME = {
    "name": "7 Orchard Close",
    "room": 16.5,
    "next_period": {"start": "2026-11-24T06:45", "target": 19.5},
    "heat_ups": [[2.0, 55], [3.0, 80]],
    "settings": {
        "boost_temperature": 21.0,
        "warm_wake": True,
        "week_starts_on": "sunday",
        "away_temperature": 16.0,
        "geofencing": False,
    },
}

REPORT = """Bug report from support:

  A customer at 7 Orchard Close chose Sunday for "Week starts on" in the app.
  On the web dashboard's settings page it shows Monday. They changed it back to
  Sunday in the app twice, and the dashboard still shows Monday.

  To reproduce, from the project folder:
    python -m dormouse homes/house-7.json
  then open homes/house-7.html in a browser."""

shutil.rmtree(COPY, ignore_errors=True)
shutil.copytree(PROJECT, COPY, ignore=shutil.ignore_patterns("__pycache__", "*.html"))
(COPY / "homes" / "house-7.json").write_text(json.dumps(HOME, indent=2) + "\n")

print(REPORT)
print(f"\nA fresh copy of the project is in playground/debug-hunt/output/project.")
print("Open it in Cursor, choose Debug mode, and paste the bug report.")
