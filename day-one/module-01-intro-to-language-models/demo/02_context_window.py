# Run from the module folder: uv run python demo/02_context_window.py

import json
import random
import re
from collections import Counter, defaultdict
from pathlib import Path

DATA = Path(__file__).parent.parent / "data"
OUTPUT = Path(__file__).parent / "output"
OUTPUT.mkdir(exist_ok=True)

WINDOW = 5


def split_into_words(text):
    return re.findall(r"[a-z']+|[.,!?;:]", text.lower())


def build_model(words):
    counts = defaultdict(Counter)
    for i in range(len(words) - WINDOW):
        context = " ".join(words[i : i + WINDOW])
        counts[context][words[i + WINDOW]] += 1

    model = {}
    for context, next_words in counts.items():
        total = sum(next_words.values())
        model[context] = {w: round(c / total, 4) for w, c in next_words.most_common()}
    return model


def complete_sentence(model, start):
    words = split_into_words(start)
    while (
        len(words) < 100
        and words[-1] not in {".", "!", "?"}
        and " ".join(words[-WINDOW:]) in model
    ):
        next_words = model[" ".join(words[-WINDOW:])]
        words += random.choices(list(next_words), weights=list(next_words.values()))
    return " ".join(words)


for name in ["alice-chapter-1", "alice"]:
    words = split_into_words((DATA / f"{name}.txt").read_text())
    model = build_model(words)
    (OUTPUT / f"02_context_window_{name}.json").write_text(json.dumps(model, indent=2))

    print(f"=== {name} ===")
    for _ in range(3):
        print(complete_sentence(model, "alice was beginning to get"))
    print()
