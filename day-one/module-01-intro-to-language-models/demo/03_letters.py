# Run from the module folder: uv run python demo/03_letters.py

import json
import random
from collections import Counter, defaultdict
from pathlib import Path

DATA = Path(__file__).parent.parent / "data"
OUTPUT = Path(__file__).parent / "output"
OUTPUT.mkdir(exist_ok=True)

WINDOW = 8


def build_model(text):
    counts = defaultdict(Counter)
    for i in range(len(text) - WINDOW):
        counts[text[i : i + WINDOW]][text[i + WINDOW]] += 1

    model = {}
    for context, next_letters in counts.items():
        total = sum(next_letters.values())
        model[context] = {l: round(c / total, 4) for l, c in next_letters.most_common()}
    return model


def complete_sentence(model, start):
    text = start
    while len(text) < 300 and text[-1] not in ".!?" and text[-WINDOW:] in model:
        next_letters = model[text[-WINDOW:]]
        text += random.choices(list(next_letters), weights=list(next_letters.values()))[0]
    return text


for name in ["alice-chapter-1", "alice"]:
    text = " ".join((DATA / f"{name}.txt").read_text().lower().split())
    model = build_model(text)
    (OUTPUT / f"03_letters_{name}.json").write_text(json.dumps(model, indent=2))

    print(f"=== {name} ===")
    for _ in range(3):
        print(complete_sentence(model, "alice was beginning to get"))
    print()
