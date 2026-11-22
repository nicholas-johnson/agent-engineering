# Word vectors — train demo 5's word2vec model yourself, with every setting exposed.
# Run from the module folder: uv run python playground/word-vectors/play.py
#                         or: source ../../.venv/bin/activate && python playground/word-vectors/play.py
#
# To play: add document ids to DOCUMENTS, or change SIZE, WINDOW or EPOCHS, then type words to see their
# closest words. An empty line stops. The user guide alone takes about ten seconds; more text takes longer.

import json
import math
import random
import re
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
DOCS = HERE.parent.parent / "data" / "docs"
OUTPUT = HERE / "output"
OUTPUT.mkdir(exist_ok=True)

DOCUMENTS = ["user-guide"]  # file names in data/docs, without .md
SIZE = 20  # numbers per word
WINDOW = 3  # how many words either side count as neighbours
NEGATIVES = 5  # random "not a neighbour" words for each real one
MIN_COUNT = 2  # words seen fewer times than this get no vector
EPOCHS = 30  # passes over the text
LEARNING_RATE = 0.05
SEED = 1
WORDS = ["warm", "boost", "schedule", "password", "heating", "alarm"]  # shown after training
CLOSEST = 5

random.seed(SEED)


def sigmoid(x):
    return 1 / (1 + math.exp(-max(-30, min(30, x))))


def cosine_similarity(a, b):
    return math.sumprod(a, b) / (math.sqrt(math.sumprod(a, a)) * math.sqrt(math.sumprod(b, b)))


def read_words(name):
    text = (DOCS / f"{name}.md").read_text().split("---", 2)[2]
    return re.findall(r"[a-z0-9]+", text.lower())


def show(word):
    # One line for a word, and the same answer kept in `closest` for output/closest.json.
    if word not in index:
        seen = counts[word]
        closest[word] = f"too rare: seen {seen}, needs MIN_COUNT = {MIN_COUNT}" if seen else "never seen"
        return closest[word]
    found = sorted(
        ((cosine_similarity(vectors[index[word]], vectors[i]), other) for other, i in index.items() if other != word),
        reverse=True,
    )[:CLOSEST]
    closest[word] = [{"word": other, "similarity": round(s, 3)} for s, other in found]
    return ", ".join(other for _, other in found)


def save():
    # The settings go in too, so you can compare runs.
    settings = {
        "DOCUMENTS": DOCUMENTS,
        "SIZE": SIZE,
        "WINDOW": WINDOW,
        "NEGATIVES": NEGATIVES,
        "MIN_COUNT": MIN_COUNT,
        "EPOCHS": EPOCHS,
        "LEARNING_RATE": LEARNING_RATE,
        "SEED": SEED,
    }
    (OUTPUT / "closest.json").write_text(json.dumps({"settings": settings, "closest": closest}, indent=2))


texts = [read_words(name) for name in DOCUMENTS]
counts = Counter(word for words in texts for word in words)
vocabulary = sorted(w for w, c in counts.items() if c >= MIN_COUNT)
index = {w: i for i, w in enumerate(vocabulary)}
documents = [[index[w] for w in words if w in index] for words in texts]

# Two sets of numbers per word: one for the word itself, one for when it is a neighbour.
vectors = [[random.uniform(-0.5, 0.5) / SIZE for _ in range(SIZE)] for _ in vocabulary]
neighbours = [[0.0] * SIZE for _ in vocabulary]
# Random "not a neighbour" words, picked more often the more often they appear.
noise = [index[w] for w in vocabulary for _ in range(round(counts[w] ** 0.75))]

start = time.perf_counter()
for epoch in range(EPOCHS):
    rate = LEARNING_RATE * (1 - epoch / EPOCHS)
    for number, tokens in enumerate(documents, 1):
        # Each document is its own text, so a window never runs from one into the next.
        for i, word in enumerate(tokens):
            for j in range(max(0, i - WINDOW), min(len(tokens), i + WINDOW + 1)):
                if j == i:
                    continue
                vector = vectors[word]
                change = [0.0] * SIZE
                # Pull the real neighbour closer and push the random ones away.
                for other, is_neighbour in [(tokens[j], 1)] + [(random.choice(noise), 0) for _ in range(NEGATIVES)]:
                    neighbour = neighbours[other]
                    step = rate * (is_neighbour - sigmoid(math.sumprod(vector, neighbour)))
                    change = [c + step * n for c, n in zip(change, neighbour)]
                    neighbours[other] = [n + step * v for n, v in zip(neighbour, vector)]
                vectors[word] = [v + c for v, c in zip(vector, change)]
        print(f"  Training: epoch {epoch + 1}/{EPOCHS}, document {number}/{len(documents)}", end="\r")
seconds = time.perf_counter() - start
print(" " * 60, end="\r")

total = sum(len(words) for words in texts)
print(
    f"\n=== Trained on {len(DOCUMENTS)} document{'s' if len(DOCUMENTS) != 1 else ''} in {seconds:.0f} seconds:"
    f" {total:,} words, {len(vocabulary):,} different words ==="
)
closest = {}
for word in WORDS:
    print(f"  {word:<10} {show(word)}")

with open(OUTPUT / "vectors.txt", "w") as file:
    for word, i in index.items():
        file.write(f"{word} {' '.join(f'{x:.4f}' for x in vectors[i])}\n")
save()

# Your own words. An empty line stops.
print()
while word := input("Word: ").strip().lower():
    print(f"  {show(word)}")
    save()
