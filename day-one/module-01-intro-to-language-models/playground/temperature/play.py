import json
import random
from pathlib import Path

MODULE = Path(__file__).parent.parent.parent
OUTPUT = Path(__file__).parent / "output"
OUTPUT.mkdir(exist_ok=True)

TEMPERATURES = [0.1, 0.5, 1.0, 2.0, 5.0]

model = json.loads((MODULE / "demo" / "output" / "01_word_pairs_alice.json").read_text())


def apply_temperature(next_words, temperature):
    weights = {word: p ** (1 / temperature) for word, p in next_words.items()}
    total = sum(weights.values())
    return {word: weight / total for word, weight in weights.items()}


def complete_sentence(start, temperature):
    words = start.split()
    while len(words) < 30 and words[-1] not in {".", "!", "?"} and words[-1] in model:
        next_words = apply_temperature(model[words[-1]], temperature)
        words += random.choices(list(next_words), weights=list(next_words.values()))
    return " ".join(words)


after_the = {}
for temperature in TEMPERATURES:
    reshaped = apply_temperature(model["the"], temperature)
    top_ten = sorted(reshaped.items(), key=lambda item: item[1], reverse=True)[:10]
    after_the[temperature] = {word: round(p, 4) for word, p in top_ten}
(OUTPUT / "after_the.json").write_text(json.dumps(after_the, indent=2))

for temperature in TEMPERATURES:
    print(f"=== temperature {temperature} ===")
    for _ in range(3):
        print(complete_sentence("alice was beginning to get", temperature))
    print()
