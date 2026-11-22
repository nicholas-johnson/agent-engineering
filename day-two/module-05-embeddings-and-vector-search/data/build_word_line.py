# Puts 16 words from the user guide on a line, for the "word line" slide. Each word starts anywhere,
# then moves again and again towards the words whose counts (as in demo 2) are most like its own.
# Run from the module folder: uv run python data/build_word_line.py

import json
import math
import re
from collections import Counter
from pathlib import Path

DATA = Path(__file__).parent
GUIDE = DATA / "docs" / "user-guide.md"

WINDOW = 3
MIN_COUNT = 2
WORDS = [
    "sunrise", "wake", "warm", "early", "heat", "frost", "temperature", "schedule",
    "boiler", "radiator", "router", "app", "phone", "email", "account", "password",
]
STEPS = 200


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def cosine_similarity(a, b):
    return dot(a, b) / math.sqrt(dot(a, a) * dot(b, b))


# Count every word's neighbours, exactly as demo 2 does.
text = GUIDE.read_text().split("---", 2)[2]
words = re.findall(r"[a-z0-9]+", text.lower())
counts = Counter(words)
vocabulary = sorted(w for w, c in counts.items() if c >= MIN_COUNT)
index = {w: i for i, w in enumerate(vocabulary)}
tokens = [index[w] for w in words if w in index]
vectors = [[0] * len(vocabulary) for _ in vocabulary]
for i, word in enumerate(tokens):
    for j in range(max(0, i - WINDOW), min(len(tokens), i + WINDOW + 1)):
        if j != i:
            vectors[word][tokens[j]] += 1

# How alike each pair of words is: the cosine similarity of their rows. A word isn't pulled by itself.
rows = [vectors[index[w]] for w in WORDS]
similar = [[0 if i == j else cosine_similarity(a, b) for j, b in enumerate(rows)] for i, a in enumerate(rows)]
pull = [sum(row) for row in similar]

positions = [float(i) for i in range(len(WORDS))]  # Anywhere will do.
for _ in range(STEPS):
    # Move each word halfway towards the average position of the others, weighted by how alike they are.
    positions = [(p + dot(s, positions) / total) / 2 for p, s, total in zip(positions, similar, pull)]
    # Re-centre and stretch the line back out, or every word would end up at the same point.
    middle = dot(pull, positions) / sum(pull)
    positions = [p - middle for p in positions]
    length = math.sqrt(dot(positions, positions))
    positions = [p / length for p in positions]

if positions[WORDS.index("warm")] > 0:
    positions = [-p for p in positions]

line = sorted(zip(positions, WORDS))
(DATA / "word_line.json").write_text(json.dumps({"positions": {w: round(p, 2) for p, w in line}}, indent=2) + "\n")
print("Each word pulled towards the words it is most like:")
for position, word in line:
    print(f"  {position:5.2f}  {word}")
