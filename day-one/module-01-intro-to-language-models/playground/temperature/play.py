# Temperature — reshape next-word probabilities before picking a word.
# Run from the module folder: uv run python playground/temperature/play.py
#                         or: python3 playground/temperature/play.py
#
# To play: change TEMPERATURES or START below, or edit apply_temperature()
# to try greedy (temperature 0), top-k or top-p sampling (see README.md).

import json
import random
import re
from collections import Counter, defaultdict
from pathlib import Path

MODULE = Path(__file__).parent.parent.parent
OUTPUT = Path(__file__).parent / "output"
OUTPUT.mkdir(exist_ok=True)

# < 1 sharpens toward the most likely words; 1 leaves probabilities alone; > 1 flattens them.
TEMPERATURES = [0.1, 0.5, 1.0, 2.0, 5.0]
START = "alice was beginning to get"


def split_into_words(text):
    return re.findall(r"[a-z']+|[.,!?;:]", text.lower())


# Build a word-pair model from Alice: model[word] -> {next_word: probability}.
words = split_into_words((MODULE / "data" / "alice.txt").read_text())
counts = defaultdict(Counter)
for word, next_word in zip(words, words[1:]):
    counts[word][next_word] += 1
model = {
    word: {w: c / sum(next_words.values()) for w, c in next_words.most_common()}
    for word, next_words in counts.items()
}


def apply_temperature(next_words, temperature):
    # Raise every probability to 1 / temperature, then rescale so they add up to 1.
    weights = {word: p ** (1 / temperature) for word, p in next_words.items()}
    total = sum(weights.values())
    return {word: weight / total for word, weight in weights.items()}


def complete_sentence(start, temperature):
    words = split_into_words(start)
    while len(words) < 30 and words[-1] not in {".", "!", "?"} and words[-1] in model:
        next_words = apply_temperature(model[words[-1]], temperature)
        words += random.choices(list(next_words), weights=list(next_words.values()))
    return " ".join(words)


# Save the top 10 words after "the" at each temperature so you can inspect the numbers.
after_the = {}
for temperature in TEMPERATURES:
    reshaped = apply_temperature(model["the"], temperature)
    top_ten = sorted(reshaped.items(), key=lambda item: item[1], reverse=True)[:10]
    after_the[temperature] = {word: round(p, 4) for word, p in top_ten}
(OUTPUT / "after_the.json").write_text(json.dumps(after_the, indent=2))

# Complete the same prompt three times at each temperature.
for temperature in TEMPERATURES:
    print(f"=== temperature {temperature} ===")
    for _ in range(3):
        print(complete_sentence(START, temperature))
    print()
