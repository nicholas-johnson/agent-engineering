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


def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    length_a = math.sqrt(sum(x * x for x in a))
    length_b = math.sqrt(sum(y * y for y in b))
    return dot / (length_a * length_b)


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

# Each word's vector, with the zeros left out: its neighbours, most frequent first.
written = {
    word: {vocabulary[j]: count for count, j in sorted(((c, j) for j, c in enumerate(vectors[i]) if c), reverse=True)}
    for word, i in index.items()
}
(OUTPUT / "02_count_vectors.json").write_text(json.dumps(written, indent=2))
