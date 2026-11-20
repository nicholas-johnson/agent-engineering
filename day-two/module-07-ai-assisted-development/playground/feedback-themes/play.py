# Feedback themes — group two months of customer feedback into themes, and count them. Where does DOR-231 come from?
# Run from the module folder: uv run python playground/feedback-themes/play.py
#                         or: source ../../.venv/bin/activate && python playground/feedback-themes/play.py
#
# To play: reword INSTRUCTIONS (fewer themes, our names instead of the customer's), or add feedback of your own.
# The model must reply in the shape of SCHEMA, so the counts and ids can be checked in code.

import json
from collections import Counter
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

HERE = Path(__file__).parent
DATA = HERE.parent.parent / "data"
OUTPUT = HERE / "output"
OUTPUT.mkdir(exist_ok=True)

MODEL = "gpt-6-luna"
INSTRUCTIONS = """You are a product manager at Dormouse. Group the customer feedback below into themes.
A theme is one problem or request that a single piece of work could address.
Name each theme in a few plain words, as the customer would see it ("Heating comes on before the schedule"), not with our feature names.
Put every piece of feedback in exactly one theme. Praise, and one-off questions, can have themes of their own."""

feedback = json.loads((DATA / "feedback.json").read_text())
ids = [f["id"] for f in feedback]

# Strict structured output: the reply must match this, and every id must be one of the real ones.
SCHEMA = {
    "type": "object",
    "properties": {
        "themes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "A few plain words, from the customer's side"},
                    "summary": {"type": "string", "description": "One sentence: what these customers want"},
                    "feedback_ids": {"type": "array", "items": {"type": "string", "enum": ids}},
                },
                "required": ["name", "summary", "feedback_ids"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["themes"],
    "additionalProperties": False,
}

client = OpenAI()

print(f"Grouping {len(feedback)} pieces of feedback...", end="\r")
response = client.responses.create(
    model=MODEL,
    reasoning={"effort": "none"},
    instructions=INSTRUCTIONS,
    input="\n".join(f"- {f['id']} ({f['channel']}, {f['date']}): {f['text']}" for f in feedback),
    text={"format": {"type": "json_schema", "name": "themes", "schema": SCHEMA, "strict": True}},
)
themes = json.loads(response.output_text)["themes"]
(OUTPUT / "themes.json").write_text(json.dumps(themes, indent=2, ensure_ascii=False))

# Count in code, not by asking the model: a count it writes itself can be wrong.
themes.sort(key=lambda theme: -len(theme["feedback_ids"]))
print(f"{len(feedback)} pieces of feedback, {len(themes)} themes, biggest first:\n")
for theme in themes:
    print(f"  {len(theme['feedback_ids']):>2}  {theme['name']}")
    print(f"      {' '.join(sorted(theme['feedback_ids']))}")

# The schema makes every id a real one. It can't stop one being left out, or used twice.
used = Counter(id for theme in themes for id in theme["feedback_ids"])
missing = [id for id in ids if id not in used]
twice = [id for id, count in used.items() if count > 1]
print(f"\nIn no theme: {' '.join(missing) or 'none'}. In more than one: {' '.join(sorted(twice)) or 'none'}.")
