# Run from the module folder: uv run python demo/05_privacy.py

import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

import openai
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

HERE = Path(__file__).parent
DATA = HERE.parent / "data"
OUTPUT = HERE / "output"
OUTPUT.mkdir(exist_ok=True)

LOG = OUTPUT / "05_log.jsonl"
MODEL = "gpt-6-luna"
RETENTION_DAYS = 90
INSTRUCTIONS = "You are Ask Dormouse, the support assistant in the Dormouse app. Answer the customer in a short paragraph of plain text."
MESSAGE = (
    "Hi, it's Sam Taylor at 14 Elm Grove, Leeds LS6 2AB. My thermostat has started clicking loudly. "
    "Can I have a new one? Call me on 07700 900123 or email sam.taylor@example.com."
)

# Set by the app when Sam signs in.
SESSION = {"customer": "C-1001"}

client = OpenAI()
dormouse = json.loads((DATA / "dormouse.json").read_text())
providers = json.loads((DATA / "providers.json").read_text())
earlier = json.loads((DATA / "support_log.json").read_text())["records"]


def redact(text, customer, home):
    # First what we know about this customer, then anything else that looks like personal data.
    known = {
        customer["email"]: "[EMAIL]",
        customer["phone"]: "[PHONE]",
        home["address"]: "[ADDRESS]",
        customer["name"]: "[NAME]",
        customer["name"].split()[0]: "[NAME]",
    }
    for value, label in known.items():
        text = text.replace(value, label)
    text = re.sub(r"[\w.+-]+@[\w-]+(\.[\w-]+)+", "[EMAIL]", text)
    text = re.sub(r"\b07\d{3} ?\d{6}\b", "[PHONE]", text)
    text = re.sub(r"\b[A-Z]{1,2}\d[A-Z\d]? ?\d[A-Z]{2}\b", "[POSTCODE]", text)
    return text


customer = next(c for c in dormouse["customers"] if c["id"] == SESSION["customer"])
home = next(h for h in dormouse["homes"] if h["id"] == customer["home"])
now = datetime.now(timezone.utc)

print("1. What OpenAI keeps")
stored = client.responses.create(model=MODEL, reasoning={"effort": "none"}, instructions=INSTRUCTIONS, input=MESSAGE)
[kept] = client.responses.input_items.list(stored.id).data
print(f"   By default, OpenAI stores the response. Asking for {stored.id[:12]}... gives back:")
print(f'   "{kept.content[0].text[:70]}..."')
private = client.responses.create(model=MODEL, reasoning={"effort": "none"}, instructions=INSTRUCTIONS, input=MESSAGE, store=False)
try:
    client.responses.retrieve(private.id)
    print("   With store=False, it was still there.")
except openai.NotFoundError:
    print(f"   With store=False, asking for {private.id[:12]}... gives: not found.")
openai_facts = next(p for p in providers["providers"] if p["name"] == "OpenAI API")
print(f"   Either way: {openai_facts['abuse_monitoring']}")

print("\n2. What we keep")
record = {
    "time": now.isoformat(timespec="seconds"),
    "customer": customer["id"],
    "response_id": stored.id,
    "message": MESSAGE,
    "reply": stored.output_text,
}
safe = {**record, "message": redact(MESSAGE, customer, home), "reply": redact(stored.output_text, customer, home)}
print(f"   Before: {record['message']}")
print(f"   After:  {safe['message']}")

print("\n3. How long we keep it")
log = []
for r in earlier:
    when = now - timedelta(days=r["age_days"])
    log.append({"time": when.isoformat(timespec="seconds"), "customer": r["customer"], "message": r["message"], "reply": r["reply"]})
log.append(safe)
recent = [r for r in log if now - datetime.fromisoformat(r["time"]) <= timedelta(days=RETENTION_DAYS)]
print(f"   The log has {len(log)} conversations. Deleted {len(log) - len(recent)} older than {RETENTION_DAYS} days; kept {len(recent)}.")

print(f"\n4. {customer['name']} asks us to delete their data")
theirs = [r for r in recent if r["customer"] == customer["id"]]
for r in theirs:
    if "response_id" in r:
        client.responses.delete(r["response_id"])
recent = [r for r in recent if r["customer"] != customer["id"]]
stored_count = sum("response_id" in r for r in theirs)
print(f"   Deleted {len(theirs)} conversations from our log, and {stored_count} stored response at OpenAI.")
print(f"   What's left in the log: {len(recent)} conversation, from another customer.")

LOG.write_text("".join(json.dumps(r) + "\n" for r in recent))
