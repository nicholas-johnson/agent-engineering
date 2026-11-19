# Run from the module folder: uv run python data/build_test_scripts.py
#
# Builds data/test-scripts.json, a library of 1,000 manual test scripts for Dormouse,
# a smart thermostat invented for this course. The 20 in test-scripts-small.json were
# written by hand; a model writes the other 980. Rerunning gives a different library.

import json
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

HERE = Path(__file__).parent
MODEL = "gpt-6-luna"
BATCH = 25
SEED = 5

# Each feature, the platforms it is tested on, and how many scripts per platform.
COMPONENTS = {
    "accounts": (["android", "ios", "web"], 30),
    "pairing": (["android", "ios", "device"], 30),
    "schedules": (["android", "ios", "web", "device"], 25),
    "heating": (["android", "ios", "web", "device"], 25),
    "away mode": (["android", "ios"], 30),
    "notifications": (["android", "ios", "web"], 25),
    "energy reports": (["android", "ios", "web"], 25),
    "firmware updates": (["android", "ios", "device"], 25),
    "zones": (["android", "ios", "web", "device"], 25),
    "household sharing": (["android", "ios", "web"], 25),
    "display and buttons": (["device"], 70),
    "sensors": (["device"], 70),
}

PLATFORM_NAMES = {
    "android": "Android app",
    "ios": "iOS app",
    "web": "web dashboard",
    "device": "thermostat itself",
}

INSTRUCTIONS = """You write manual test cases for Dormouse, a smart thermostat.

The product:
- The thermostat itself: a round display, a dial that turns and presses, a boost button, and a temperature and humidity sensor. It controls a gas boiler. Target temperatures run from 5 to 30 degrees in half-degree steps.
- Apps for Android and iOS, and a web dashboard.
- Features: accounts (email and password, two-step verification), pairing over 2.4 GHz Wi-Fi, schedules (up to six periods a day), heating control (target temperature, a one-hour boost, frost protection at 5 degrees), away mode with geofencing, notifications, monthly energy reports, overnight firmware updates between 02:00 and 04:00, zones (up to four thermostats in one home), and household sharing (an owner and up to eight members).
- Error codes shown on the thermostat's display:
  E-101 Wi-Fi network not found
  E-104 pairing timed out
  E-110 cannot reach the Dormouse cloud
  E-217 temperature sensor disconnected
  E-221 humidity sensor fault
  E-305 boiler not responding
  E-312 boiler reports a fault
  E-401 backup batteries low
  E-402 mains power interrupted
  E-510 firmware update failed

How to write a test case:
- A title of at most 12 words saying what is tested.
- Preconditions in one or two sentences.
- Two to six short steps, each an instruction.
- The expected result in one or two sentences, saying exactly what should happen.
- A priority (high, medium or low) and a realistic time to run it, from 2 to 45 minutes.
- British English and plain ASCII: write "degrees", not the symbol."""

SCHEMA = {
    "type": "object",
    "properties": {
        "scripts": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "priority": {"type": "string", "enum": ["high", "medium", "low"]},
                    "minutes": {"type": "integer"},
                    "preconditions": {"type": "string"},
                    "steps": {"type": "array", "items": {"type": "string"}},
                    "expected": {"type": "string"},
                },
                "required": ["title", "priority", "minutes", "preconditions", "steps", "expected"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["scripts"],
    "additionalProperties": False,
}

client = OpenAI()
small = json.loads((HERE / "test-scripts-small.json").read_text())


def write_batch(component, platform, count, avoid):
    prompt = (
        f"Write {count} different test cases for {component}, run on the {PLATFORM_NAMES[platform]}. "
        "Mix everyday use, edge cases, errors and accessibility."
    )
    if avoid:
        prompt += " These tests already exist, so don't repeat them:\n" + "\n".join(f"- {t}" for t in avoid)
    response = client.responses.create(
        model=MODEL,
        reasoning={"effort": "none"},
        instructions=INSTRUCTIONS,
        input=prompt,
        text={"format": {"type": "json_schema", "name": "test_scripts", "schema": SCHEMA, "strict": True}},
    )
    return json.loads(response.output_text)["scripts"]


def write_scripts(component, platform, count):
    avoid = [s["title"] for s in small if s["component"] == component and s["platform"] == platform]
    scripts = []
    while len(scripts) < count:
        batch = write_batch(component, platform, min(BATCH, count - len(scripts)), avoid)
        scripts += batch[: count - len(scripts)]
        avoid += [s["title"] for s in batch]
    return [
        {
            "title": s["title"],
            "platform": platform,
            "component": component,
            "priority": s["priority"],
            "minutes": s["minutes"],
            "preconditions": s["preconditions"],
            "steps": s["steps"],
            "expected": s["expected"],
        }
        for s in scripts
    ]


jobs = [(c, p, n) for c, (platforms, n) in COMPONENTS.items() for p in platforms]
written = []
with ThreadPoolExecutor(max_workers=8) as pool:
    futures = [pool.submit(write_scripts, *job) for job in jobs]
    for done, future in enumerate(as_completed(futures), 1):
        written += future.result()
        print(f"Written {len(written)} scripts ({done}/{len(jobs)} features and platforms)", end="\r")
print()

# Give the written scripts the IDs from TS-1000 to TS-1999 that the hand-written ones don't use.
random.seed(SEED)
written.sort(key=lambda s: (s["component"], s["platform"], s["title"]))
random.shuffle(written)
taken = {s["id"] for s in small}
free = [f"TS-{n}" for n in range(1000, 2000) if f"TS-{n}" not in taken]
library = small + [{"id": id, **s} for id, s in zip(free, written)]
library.sort(key=lambda s: s["id"])

(HERE / "test-scripts.json").write_text(json.dumps(library, indent=2) + "\n")
print(f"Wrote {len(library)} test scripts to data/test-scripts.json")
