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

WINDOW = 8
LENGTH = 400

python_code = "".join(Path(m.__file__).read_text() for m in [argparse, calendar, shutil, textwrap])

corpora = {
    "alice": ((MODULE / "data" / "alice.txt").read_text(), "Alice was "),
    "looking-glass": ((HERE / "looking-glass.txt").read_text(), "Alice was "),
    "python": (python_code, "    def "),
}


def build_model(text):
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


for name, (text, start) in corpora.items():
    model = build_model(text)
    samples = [generate(model, start) for _ in range(3)]
    (OUTPUT / f"{name}.txt").write_text("\n\n----------\n\n".join(samples) + "\n")

    print(f"=== {name} ===")
    print(samples[0])
    print()
