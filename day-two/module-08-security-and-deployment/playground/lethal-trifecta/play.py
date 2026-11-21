# Lethal trifecta — check an agent's tools for private data, untrusted content and a way to send data out.
# Run from the module folder: uv run python playground/lethal-trifecta/play.py
#                         or: source ../../.venv/bin/activate && python playground/lethal-trifecta/play.py
#
# To play: add an agent you use or are building to AGENTS, label its tools, and see what the check says.
# Then argue with the labels: is a ticket written by a customer untrusted? No API key needed.

import json
from pathlib import Path

HERE = Path(__file__).parent
OUTPUT = HERE / "output"
OUTPUT.mkdir(exist_ok=True)

LEGS = {
    "private": "private data",
    "untrusted": "untrusted content",
    "outbound": "a way to send data out",
}
MISSING = {"private": "no private data", "untrusted": "no untrusted content", "outbound": "no way to send data out"}
# Each tool, and the legs it gives the agent. "confirmed" means a person approves every call.
AGENTS = {
    "Ask Dormouse, demo 3": {
        "get_my_home": {"legs": ["private", "untrusted"]},  # device names are written by household members
        "contact_support": {"legs": []},  # goes to our own support team
        "invite_member": {"legs": ["outbound"]},  # emails a link to any address
    },
    "Ask Dormouse, demo 4": {
        "get_my_home": {"legs": ["private", "untrusted"]},
        "contact_support": {"legs": []},
        "invite_member": {"legs": ["outbound"], "confirmed": True},
    },
    "Priya's assistant, demo 6": {
        "search_docs": {"legs": ["private"]},
        "get_customer": {"legs": ["private", "untrusted"]},  # tickets are written by customers
        "offer_replacement": {"legs": []},  # sends a thermostat to the customer's own address
    },
    "Module 7's coding agent": {
        "read_file": {"legs": ["private", "untrusted"]},  # the company's code, and files anyone could commit
        "write_file": {"legs": []},
        "run_tests": {"legs": ["outbound"]},  # runs code the agent wrote, which can reach the internet
    },
    "An email assistant": {
        "read_inbox": {"legs": ["private", "untrusted"]},  # anyone can email you
        "send_email": {"legs": ["outbound"]},
    },
    "A research agent": {
        "read_notes": {"legs": ["private"]},
        "fetch_page": {"legs": ["untrusted", "outbound"]},  # the address it fetches can carry data out
    },
}


def check(tools):
    found = {leg: [name for name, tool in tools.items() if leg in tool["legs"]] for leg in LEGS}
    guarded = [name for name in found["outbound"] if tools[name].get("confirmed")]
    if not all(found.values()):
        missing = [MISSING[leg] for leg, names in found.items() if not names]
        verdict = f"Safe from this attack: {' and '.join(missing)}."
    elif len(guarded) == len(found["outbound"]):
        verdict = "All three, but a person confirms every way out. As safe as the person reading the question."
    else:
        verdict = "At risk: all three. An injection can read private data and send it out."
        # A leg that only one tool gives is the cheapest one to remove.
        single = [names[0] for names in found.values() if len(names) == 1]
        if single:
            verdict += f" Taking away {' or '.join(sorted(set(single)))} would break it."
    return found, verdict


report = {}
for agent, tools in AGENTS.items():
    found, verdict = check(tools)
    report[agent] = {"legs": found, "verdict": verdict}
    print(agent)
    for leg, description in LEGS.items():
        print(f"  {description + ':':<24} {', '.join(found[leg]) or '-'}")
    print(f"  {verdict}\n")

(OUTPUT / "report.json").write_text(json.dumps(report, indent=2))
