import json
import random
from collections import Counter, defaultdict
from pathlib import Path

DATA = Path(__file__).parent.parent / "data"
OUTPUT = Path(__file__).parent / "output"
OUTPUT.mkdir(exist_ok=True)

WINDOW = 4

vocabulary = set(json.loads((DATA / "tokens.json").read_text()))
longest = max(len(token) for token in vocabulary)


def split_into_tokens(text):
    tokens = []
    i = 0
    while i < len(text):
        for size in range(longest, 0, -1):
            if text[i : i + size] in vocabulary:
                tokens.append(text[i : i + size])
                i += size
                break
    return tokens


def build_model(tokens):
    counts = defaultdict(Counter)
    for i in range(len(tokens) - WINDOW):
        context = "|".join(tokens[i : i + WINDOW])
        counts[context][tokens[i + WINDOW]] += 1

    model = {}
    for context, next_tokens in counts.items():
        total = sum(next_tokens.values())
        model[context] = {t: round(c / total, 4) for t, c in next_tokens.most_common()}
    return model


def complete_sentence(model, start):
    tokens = split_into_tokens(start)
    while (
        len(tokens) < 80
        and not any(mark in tokens[-1] for mark in ".!?")
        and "|".join(tokens[-WINDOW:]) in model
    ):
        next_tokens = model["|".join(tokens[-WINDOW:])]
        tokens += random.choices(list(next_tokens), weights=list(next_tokens.values()))
    return "".join(tokens)


for name in ["alice-chapter-1", "alice"]:
    text = " ".join((DATA / f"{name}.txt").read_text().lower().split())
    tokens = split_into_tokens(text)
    model = build_model(tokens)
    (OUTPUT / f"04_tokens_{name}.json").write_text(json.dumps(model, indent=2))

    print(f"=== {name} ===")
    for _ in range(3):
        print(complete_sentence(model, "alice was beginning to get"))
    print()
