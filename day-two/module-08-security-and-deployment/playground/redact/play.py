# Redact — take the personal data out of support messages before you log them, and count what gets through.
# Run from the module folder: uv run python playground/redact/play.py
#                         or: source ../../.venv/bin/activate && python playground/redact/play.py
#
# To play: add a pattern to PATTERNS for something that got through, and run it again.
# Then add a message of your own to MESSAGES that beats every pattern. No API key needed.

import json
import re
from pathlib import Path

HERE = Path(__file__).parent
OUTPUT = HERE / "output"
OUTPUT.mkdir(exist_ok=True)

# Each message, and the personal data in it that should come out.
MESSAGES = [
    ("Call me on 07700 900123 if you need to.", ["07700 900123"]),
    ("My email is sam.taylor@example.com.", ["sam.taylor@example.com"]),
    ("We're at 14 Elm Grove, Leeds LS6 2AB.", ["14 Elm Grove", "LS6 2AB"]),
    ("Postcode ls62ab, if that helps.", ["ls62ab"]),
    ("My mobile is +44 7700 900123.", ["+44 7700 900123"]),
    ("It's sam dot taylor at example dot com.", ["sam dot taylor at example dot com"]),
    ("Ring me on oh seven seven double oh, nine double oh one two three.", ["oh seven seven double oh, nine double oh one two three"]),
    ("This is Sam Taylor, the owner.", ["Sam Taylor"]),
    ("Jo's phone is the one ending 124.", ["Jo", "ending 124"]),
    ("We're away until the 30th, the house is empty.", ["away until the 30th"]),
]
# The patterns, in order. Each match is replaced by its label.
PATTERNS = [
    ("[EMAIL]", r"[\w.+-]+@[\w-]+(\.[\w-]+)+"),
    ("[PHONE]", r"(\+44 ?|\b0)7\d{3} ?\d{6}\b"),
    ("[POSTCODE]", r"\b[A-Z]{1,2}\d[A-Z\d]? ?\d[A-Z]{2}\b"),
]


def redact(text):
    for label, pattern in PATTERNS:
        text = re.sub(pattern, label, text)
    return text


results, caught, total = [], 0, 0
for message, personal in MESSAGES:
    redacted = redact(message)
    missed = [p for p in personal if p in redacted]
    caught += len(personal) - len(missed)
    total += len(personal)
    results.append({"message": message, "redacted": redacted, "missed": missed})
    print(f"{'  ' if not missed else '! '}{redacted}")
    for p in missed:
        print(f"    missed: {p}")

print(f"\nTook out {caught} of {total} pieces of personal data.")
(OUTPUT / "redacted.json").write_text(json.dumps(results, indent=2))
