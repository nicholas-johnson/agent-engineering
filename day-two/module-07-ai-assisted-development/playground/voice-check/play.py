# Voice check — check customer copy against the Dormouse voice twice: with rules in code, and with a model.
# Run from the module folder: uv run python playground/voice-check/play.py
#                         or: source ../../.venv/bin/activate && python playground/voice-check/play.py
#
# To play: paste in some copy (an empty line ends it), or press Enter straight away to check SAMPLE.
# Then add a rule to rule_problems() for something only the model caught, and run it again.

import json
import re
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

HERE = Path(__file__).parent
VOICE = HERE.parent.parent / "data" / "brain" / "voice.md"
OUTPUT = HERE / "output"
OUTPUT.mkdir(exist_ok=True)

MODEL = "gpt-6-luna"
# Copy that breaks the voice in as many ways as we could fit in.
SAMPLE = """Introducing the all-new Warm Wake: a revolutionary, seamless way to wake up to a cosy home!
Our smart AI now lets you choose exactly when your heating kicks in, so you could save up to 20% on your gas bill.
Want it 21°C by 6:30 AM? Just head to Settings → Heating → Warm Wake and Unlock Your Perfect Morning."""
JUDGE = """You check customer copy for Dormouse against our voice guide, below.
List every place the copy breaks the guide: quote the words, say which rule they break, and suggest a fix.
Then rewrite the whole copy so it follows the guide. If nothing breaks it, list no problems and return the copy unchanged."""

SCHEMA = {
    "type": "object",
    "properties": {
        "problems": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {"quote": {"type": "string"}, "rule": {"type": "string"}, "fix": {"type": "string"}},
                "required": ["quote", "rule", "fix"],
                "additionalProperties": False,
            },
        },
        "rewrite": {"type": "string"},
    },
    "required": ["problems", "rewrite"],
    "additionalProperties": False,
}

client = OpenAI()


def banned_words(voice):
    """The list under "Words we don't use" in the brand voice."""
    section = voice.split("## Words we don't use", 1)[1]
    return [line[2:].strip() for line in section.splitlines() if line.startswith("- ")]


def rule_problems(copy, voice):
    """The rules simple enough to check in code. Fast, free, and the same every time."""
    words = [word for word in banned_words(voice) if re.search(rf"\b{re.escape(word)}\b", copy, re.IGNORECASE)]
    problems = [f'"{word}" is on the list of words we don\'t use' for word in words]
    problems += [f'"{m}" is a savings figure' for m in re.findall(r"\d+ ?%|\d+ per ?cent", copy, re.IGNORECASE)]
    # 6:30 AM, 7am, 7 p.m.
    times = re.findall(r"\b\d{1,2}(?:[:.]\d{2})? ?(?:[ap]\.m\.|[ap]m\b)", copy, re.IGNORECASE)
    problems += [f'"{m}" uses the 12-hour clock' for m in times]
    problems += [f'"{m}" uses the degree symbol' for m in re.findall(r"\d+ ?°[CF]?", copy)]
    return problems


def model_problems(copy, voice):
    """A model reads the whole voice guide, including the rules code can't check."""
    response = client.responses.create(
        model=MODEL,
        reasoning={"effort": "none"},
        instructions=f"{JUDGE}\n\n{voice}",
        input=copy,
        text={"format": {"type": "json_schema", "name": "voice_check", "schema": SCHEMA, "strict": True}},
    )
    return json.loads(response.output_text)


print("Paste the copy to check, then press Enter on an empty line. Press Enter straight away to check the sample.\n")
lines = []
while line := input():
    lines.append(line)
copy = "\n".join(lines) or SAMPLE
voice = VOICE.read_text()

if not lines:
    print(f"The sample:\n\n{SAMPLE}\n")

rules = rule_problems(copy, voice)
print(f"Rules in code found {len(rules)}:")
for problem in rules:
    print(f"  - {problem}")

print("\nAsking the model...", end="\r")
judged = model_problems(copy, voice)
print(f"The model found {len(judged['problems'])}:")
for problem in judged["problems"]:
    print(f'  - "{problem["quote"]}": {problem["rule"]}\n      Fix: {problem["fix"]}')
print(f"\nRewritten:\n\n{judged['rewrite']}")

(OUTPUT / "check.json").write_text(json.dumps({"copy": copy, "rules": rules, **judged}, indent=2, ensure_ascii=False))
