# Run from the module folder: uv run python data/build_docs.py
#
# Builds data/docs/, the knowledge base for Dormouse, the smart thermostat invented for
# Module 5. The user guide and the internal note on the relay click were written by hand;
# a model writes everything else, using the user guide as its source of truth.
# Rerunning gives a different knowledge base.

import json
import random
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, timedelta
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

HERE = Path(__file__).parent
DOCS = HERE / "docs"
MODEL = "gpt-6-luna"
TITLES_PER_CALL = 30
SEED = 6
HAND_WRITTEN = {"user-guide.md", "internal-relay-click-revision-c.md"}

# Each kind of document: how many, who it is for, and what it is.
KINDS = {
    "support": (90, "customer", "help-centre articles, each explaining how to do one task or how one feature behaves"),
    "troubleshooting": (40, "customer", "troubleshooting guides, each working through the causes of one problem"),
    "installation": (25, "customer", "installation and wiring guides for installers and confident customers"),
    "app": (30, "customer", "guides to the screens of the Android app, the iOS app and the web dashboard"),
    "specification": (8, "customer", "technical specifications and data sheets for each product"),
    "integration": (
        12,
        "customer",
        "guides to connecting Dormouse with other systems: home automation, voice assistants, smart plugs and the like, never naming a brand",
    ),
    "policy": (
        10,
        "customer",
        "policies: warranty, returns, privacy, data retention, accessibility, safety and recycling",
    ),
    "internal": (
        40,
        "internal",
        "internal documents: engineering notes, support playbooks, QA reports, firmware rollout plans and known issues",
    ),
}

ERROR_CODES = {
    "E-101": "Wi-Fi network not found",
    "E-104": "Pairing timed out",
    "E-110": "Cannot reach the Dormouse cloud",
    "E-217": "Temperature sensor disconnected",
    "E-221": "Humidity sensor fault",
    "E-305": "Boiler not responding",
    "E-312": "Boiler reports a fault",
    "E-401": "Backup batteries low",
    "E-402": "Mains power interrupted",
    "E-510": "Firmware update failed",
}

RELEASES = {
    "3.0": ("2025-01-20", "Two-step verification for accounts. A home can now have four thermostats (it was two)."),
    "3.1": (
        "2025-03-17",
        "Geofencing for away mode. The away temperature can be changed in Settings > Away > Away temperature.",
    ),
    "3.2": (
        "2025-05-26",
        "Monthly energy reports in the new Energy tab. E-110 now appears when the Dormouse cloud cannot be reached (before, the Wi-Fi symbol flashed).",
    ),
    "3.3": (
        "2025-08-11",
        "Household sharing now allows eight members (it was five). Invitations now expire after 7 days.",
    ),
    "3.4": (
        "2025-10-06",
        "Support for the Dormouse Radiator Valve. Firmware updates now install between 02:00 and 04:00 (it was 01:00 to 05:00).",
    ),
    "3.5": (
        "2025-12-01",
        "A failed update (E-510) is now retried the next night. E-401 now appears a month before the backup batteries run out.",
    ),
    "4.0": (
        "2026-03-09",
        "New: Warm Wake. New display symbols, including the sunrise symbol for Warm Wake. Support for the Dormouse Room Sensor.",
    ),
    "4.1": (
        "2026-08-17",
        "The boost temperature can be changed in Settings > Heating > Boost temperature (it was always 21 degrees). Password reset links now work for 30 minutes (it was 24 hours).",
    ),
}

# Only the 4.0 release notes and the user guide say this.
WARM_WAKE = (
    " Warm Wake starts the heating up to 90 minutes early, so the home is warm when a schedule period starts."
    " It can be turned off in Settings > Heating > Warm Wake."
)

PRODUCTS = ["thermostat", "radiator valve", "room sensor", "app", "all"]

# Characters models like to use, and their plain ASCII versions.
PLAIN = {
    "\u2018": "'",
    "\u2019": "'",
    "\u201c": '"',
    "\u201d": '"',
    "\u2013": "-",
    "\u2014": "-",
    "\u2026": "...",
    "\u00d7": "x",
    "\u00a0": " ",
    "\u2192": ">",
    "\u00b0C": " degrees",
    "\u00b0": " degrees",
    "\u00b1": "+/-",
}

guide = (DOCS / "user-guide.md").read_text().split("---", 2)[2].strip()
# Only the user guide and the release notes describe Warm Wake, so a change to it is a change in one place.
guide = re.sub(
    r"### Warm Wake\n.*?(?=\n## )",
    "### Warm Wake\n\nWarm Wake starts the heating before a schedule period. The display shows the sunrise symbol while it does.\n",
    guide,
    flags=re.DOTALL,
)

# Phrases that break the rules below. A document that uses one is written again.
FORBIDDEN = re.compile(r"minutes early|90 minutes|> Warm Wake|\$\d|\bprices?\b", re.IGNORECASE)

INSTRUCTIONS = f"""You write documentation for Dormouse, a company that makes a smart thermostat.

The user guide below is the source of truth. Never contradict it.

<user_guide>
{guide}
</user_guide>

Facts that are not in the user guide:
- Products: the Dormouse Thermostat; the Dormouse Radiator Valve (fits M30 x 1.5 valve bodies, with adapters in the box for other common valves, runs on two AA batteries that last about two years); the Dormouse Room Sensor (temperature and humidity, one CR2032 coin cell that lasts about a year, up to three per zone). Valves and sensors talk to their zone's thermostat over a low-power 868 MHz radio link; only the thermostat uses Wi-Fi.
- The thermostat: 84 mm across and 24 mm deep, a 2.4-inch round colour display, powered by mains through its wall plate, accurate to 0.3 degrees, for use indoors between 0 and 40 degrees. Hardware revisions A (2024), B (2025) and C (2026); serial numbers start DMA, DMB or DMC.
- Current firmware: 4.1. Release history: {"; ".join(f"{v} ({d}): {c}" for v, (d, c) in RELEASES.items())}
- Support is contacted in the app, under Help > Contact support.
- Warranty: 2 years. Returns: within 30 days. Heating history is kept for 2 years. Phone locations are never stored, only whether each member is home or away.
- Internal only (mention these only in internal documents): support has three levels (1: app chat agents, 2: product specialists, 3: engineering); firmware is rolled out to 1%, then 10%, then every thermostat over a week; every release is tested against the manual test-script library before rollout.

How to write:
- Markdown. Start with "# " and the title, then 6 to 12 sections with "## " headings. Use "### " inside a section only if it really helps.
- 1,000 to 1,500 words. Keep each section under 250 words. Use tables or numbered steps where they help.
- Write as the company's engineers and technical writers do: say what the product does, in the product's own terms.
- No questions and answers, and no FAQ sections.
- You may name Warm Wake, but never describe how it works, how early it starts, or where its setting is.
- Never mention prices, discounts, people's names, the company's history or founders, its offices or locations, future products, phone numbers, email addresses, web addresses, or other companies' brands.
- Menu paths look like Settings > Heating > Boost temperature.
- British English and plain ASCII: write "degrees", not the symbol."""

TITLES_SCHEMA = {
    "type": "object",
    "properties": {
        "documents": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "product": {"type": "string", "enum": PRODUCTS},
                    "brief": {"type": "string"},
                },
                "required": ["title", "product", "brief"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["documents"],
    "additionalProperties": False,
}

client = OpenAI(timeout=180)  # so a dropped connection fails and is retried, rather than hanging


def ask(prompt, schema=None):
    structured = {"text": {"format": {"type": "json_schema", "name": "documents", "schema": schema, "strict": True}}}
    response = client.responses.create(
        model=MODEL,
        reasoning={"effort": "none"},
        instructions=INSTRUCTIONS,
        input=prompt,
        **(structured if schema else {}),
    )
    return response.output_text


def plain_ascii(text):
    for fancy, plain in PLAIN.items():
        text = text.replace(fancy, plain)
    return text.encode("ascii", "ignore").decode()


def plan_kind(kind, count, description):
    planned = []
    while len(planned) < count:
        prompt = (
            f"List {min(TITLES_PER_CALL, count - len(planned))} different {description}. "
            "For each, give a title, the product it is about, and a one-sentence brief of what it covers."
        )
        if planned:
            prompt += " These already exist, so don't repeat them:\n" + "\n".join(f"- {p['title']}" for p in planned)
        # Occasionally the reply has a second JSON object after the first, so read only the first.
        reply, _ = json.JSONDecoder().raw_decode(ask(prompt, TITLES_SCHEMA))
        planned += [{key: plain_ascii(value) for key, value in p.items()} for p in reply["documents"]]
    return [{**p, "kind": kind, "description": description} for p in planned[:count]]


def write_document(doc):
    prompt = f'Write the document "{doc["title"]}", one of our {doc["description"]}. It covers {doc["brief"]}'
    for attempt in range(3):
        body = plain_ascii(ask(prompt)).strip().removeprefix("```markdown").removesuffix("```").strip()
        body = re.sub(r"\A# .*\n", "", body).strip()
        if doc["kind"] == "release notes" or not FORBIDDEN.search(body):
            break
    else:
        print(f"\nStill breaks the rules after three tries: {doc['title']}")
    return doc, f"# {doc['title']}\n\n{body}\n"


def slug(title):
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


# 1. Decide what to write.
plans = []
with ThreadPoolExecutor(max_workers=8) as pool:
    for done, future in enumerate(as_completed([pool.submit(plan_kind, k, n, d) for k, (n, _, d) in KINDS.items()]), 1):
        plans += future.result()
        print(f"Planned {len(plans)} documents ({done}/{len(KINDS)} kinds)", end="\r")
print()
plans.sort(key=lambda p: (p["kind"], p["title"]))
for code, meaning in ERROR_CODES.items():
    plans.append(
        {
            "kind": "error code",
            "description": "articles on the error codes",
            "title": f"{code}: {meaning}",
            "product": "thermostat",
            "brief": f"what {code} means, what causes it, and what to do, step by step.",
        }
    )
for version, (_, changes) in RELEASES.items():
    if version == "4.0":
        changes += WARM_WAKE
    plans.append(
        {
            "kind": "release notes",
            "description": "firmware release notes",
            "title": f"Firmware {version} release notes",
            "product": "thermostat",
            "brief": f"exactly these changes and no others: {changes} Keep it under 300 words.",
        }
    )

# Every document gets an audience, the firmware it describes, and the date it was last updated.
random.seed(SEED)
for plan in plans:
    plan["audience"] = KINDS[plan["kind"]][1] if plan["kind"] in KINDS else "customer"
    if plan["kind"] == "release notes":
        plan["firmware"] = plan["title"].split()[1]
        plan["updated"] = RELEASES[plan["firmware"]][0]
    else:
        plan["firmware"] = "4.1"
        plan["updated"] = (date(2025, 1, 6) + timedelta(days=random.randrange(665))).isoformat()

# 2. Write them, replacing the previous generated documents.
for old in DOCS.glob("*.md"):
    if old.name not in HAND_WRITTEN:
        old.unlink()
written = 0
with ThreadPoolExecutor(max_workers=8) as pool:
    for future in as_completed([pool.submit(write_document, p) for p in plans]):
        doc, text = future.result()
        name = f"{slug(doc['title'])}.md"
        while (DOCS / name).exists():
            name = name.removesuffix(".md") + "-2.md"
        front = (
            f"---\ntitle: {doc['title']}\nproduct: {doc['product']}\ntype: {doc['kind']}\n"
            f"audience: {doc['audience']}\nfirmware: {doc['firmware']}\nupdated: {doc['updated']}\n---\n\n"
        )
        (DOCS / name).write_text(front + text)
        written += 1
        print(f"Written {written}/{len(plans)} documents", end="\r")
print()
print(f"data/docs/ now holds {len(list(DOCS.glob('*.md')))} documents")
