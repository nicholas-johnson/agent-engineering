# Run from the module folder: uv run python demo/02_count_vectors.py

import json
import math
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
GUIDE = HERE.parent / "data" / "docs" / "user-guide.md"
OUTPUT = HERE / "output"
OUTPUT.mkdir(exist_ok=True)

WINDOW = 3
MIN_COUNT = 2
WORDS = ["warm", "password", "heating", "alarm"]
PICKED = [
    "sunrise", "wake", "warm", "early", "heat", "frost", "temperature", "schedule",
    "boiler", "radiator", "router", "app", "phone", "email", "account", "password",
]
STEPS = 200


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def cosine_similarity(a, b):
    return dot(a, b) / math.sqrt(dot(a, a) * dot(b, b))


text = GUIDE.read_text().split("---", 2)[2]
words = re.findall(r"[a-z0-9]+", text.lower())
counts = Counter(words)
vocabulary = sorted(w for w, c in counts.items() if c >= MIN_COUNT)
index = {w: i for i, w in enumerate(vocabulary)}
tokens = [index[w] for w in words if w in index]

# One row per word: how often each word in the vocabulary appears up to WINDOW places away from it.
vectors = [[0] * len(vocabulary) for _ in vocabulary]
for i, word in enumerate(tokens):
    for j in range(max(0, i - WINDOW), min(len(tokens), i + WINDOW + 1)):
        if j != i:
            vectors[word][tokens[j]] += 1

print(f"\n=== Counted in the user guide: {len(words):,} words, {len(vocabulary)} different words ===")
for word in WORDS:
    if word not in index:
        print(f"  {word:<10} never seen")
        continue
    closest = sorted(
        ((cosine_similarity(vectors[index[word]], vectors[i]), other) for other, i in index.items() if other != word),
        reverse=True,
    )
    print(f"  {word:<10} {', '.join(other for _, other in closest[:5])}")

# 235 numbers are hard to picture. Squeeze 16 words we picked down to one number each, a place on a line.
rows = [vectors[index[w]] for w in PICKED]
similar = [[0 if i == j else cosine_similarity(a, b) for j, b in enumerate(rows)] for i, a in enumerate(rows)]
pull = [sum(row) for row in similar]
positions = [float(i) for i in range(len(PICKED))]  # Anywhere will do.
for _ in range(STEPS):
    # Move each word halfway towards the average position of the others, weighted by how alike they are.
    positions = [(p + dot(s, positions) / total) / 2 for p, s, total in zip(positions, similar, pull)]
    # Re-centre and stretch the line back out, or every word would end up at the same point.
    middle = dot(pull, positions) / sum(pull)
    positions = [p - middle for p in positions]
    length = math.sqrt(dot(positions, positions))
    positions = [p / length for p in positions]
if positions[PICKED.index("warm")] > 0:
    positions = [-p for p in positions]
line = sorted(zip(positions, PICKED))

print(f"\n=== {len(PICKED)} words we picked: one number each ===")
for position, word in line:
    print(f"  {position:5.2f}  {word}")

# Each word's vector, with the zeros left out: its neighbours, most frequent first.
written = {
    word: {vocabulary[j]: count for count, j in sorted(((c, j) for j, c in enumerate(vectors[i]) if c), reverse=True)}
    for word, i in index.items()
}
(OUTPUT / "02_count_vectors.json").write_text(json.dumps(written, indent=2))
(OUTPUT / "02_word_line.json").write_text(json.dumps({w: round(p, 2) for p, w in line}, indent=2))
