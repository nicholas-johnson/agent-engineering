# Other books — train the character model on prose, a sequel, and Python source code.
# Run from the module folder: uv run python playground/other-books/play.py
#                         or: python3 playground/other-books/play.py
#
# To play: change WINDOW or LENGTH below, or add your own text/code to `corpora`
# (try combining Alice + Python into one corpus; see README.md).

import argparse
import calendar
import random
import shutil
import textwrap
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).parent
MODULE = HERE.parent.parent
OUTPUT = HERE / "output"
OUTPUT.mkdir(exist_ok=True)

# Number of characters of context, and how many characters to generate per sample.
WINDOW = 8
LENGTH = 400

# Read four standard-library modules directly from your Python installation.
python_code = "".join(Path(m.__file__).read_text() for m in [argparse, calendar, shutil, textwrap])

# Each entry maps corpus name -> (training text, starting prompt).
corpora = {
    "alice": ((MODULE / "data" / "alice.txt").read_text(), "Alice was "),
    "looking-glass": ((HERE / "looking-glass.txt").read_text(), "Alice was "),
    "python": (python_code, "    def "),
}


def build_model(text):
    # Keep case, newlines and indentation intact so generated code looks like code.
    model = defaultdict(Counter)
    for i in range(len(text) - WINDOW):
        model[text[i : i + WINDOW]][text[i + WINDOW]] += 1
    return model


def generate(model, start):
    text = start
    while len(text) < LENGTH and text[-WINDOW:] in model:
        next_letters = model[text[-WINDOW:]]
        text += random.choices(list(next_letters), weights=list(next_letters.values()))[0]
    return text


# Train on each corpus, save three samples to output/<name>.txt, and print the first.
for name, (text, start) in corpora.items():
    model = build_model(text)
    samples = [generate(model, start) for _ in range(3)]
    (OUTPUT / f"{name}.txt").write_text("\n\n----------\n\n".join(samples) + "\n")

    print(f"=== {name} ===")
    print(samples[0])
    print()
