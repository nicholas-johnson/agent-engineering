import json
import random
import re
from collections import Counter, defaultdict
from pathlib import Path

DATA = Path(__file__).parent.parent / "data"
OUTPUT = Path(__file__).parent / "output"
OUTPUT.mkdir(exist_ok=True)


def split_into_words(text):
    return re.findall(r"[a-z']+|[.,!?;:]", text.lower())


def build_model(words):
    counts = defaultdict(Counter)
    for word, next_word in zip(words, words[1:]):
        counts[word][next_word] += 1

    model = {}
    for word, next_words in counts.items():
        total = sum(next_words.values())
        model[word] = {w: round(c / total, 4) for w, c in next_words.most_common()}
    return model


def complete_sentence(model, start):
    words = split_into_words(start)
    while len(words) < 100 and words[-1] not in {".", "!", "?"} and words[-1] in model:
        next_words = model[words[-1]]
        words += random.choices(list(next_words), weights=list(next_words.values()))
    return " ".join(words)


for name in ["alice-chapter-1", "alice"]:
    words = split_into_words((DATA / f"{name}.txt").read_text())
    model = build_model(words)
    (OUTPUT / f"01_word_pairs_{name}.json").write_text(json.dumps(model, indent=2))

    print(f"=== {name} ===")
    for _ in range(3):
        print(complete_sentence(model, "alice was beginning to get"))
    print()
