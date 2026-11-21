# Run from the module folder: uv run python demo/02_word_vectors.py

import math
import random
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
GUIDE = HERE.parent / "data" / "docs" / "user-guide.md"
OUTPUT = HERE / "output"
OUTPUT.mkdir(exist_ok=True)

SIZE = 20
WINDOW = 3
NEGATIVES = 5
MIN_COUNT = 2
EPOCHS = 30
LEARNING_RATE = 0.05
SEED = 1
WORDS = ["warm", "password", "heating", "alarm"]

random.seed(SEED)


def sigmoid(x):
    return 1 / (1 + math.exp(-max(-30, min(30, x))))


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

# Two sets of numbers per word: one for the word itself, one for when it is a neighbour.
vectors = [[random.uniform(-0.5, 0.5) / SIZE for _ in range(SIZE)] for _ in vocabulary]
neighbours = [[0.0] * SIZE for _ in vocabulary]
# Random "not a neighbour" words, picked more often the more often they appear.
noise = [index[w] for w in vocabulary for _ in range(round(counts[w] ** 0.75))]

for epoch in range(EPOCHS):
    rate = LEARNING_RATE * (1 - epoch / EPOCHS)
    for i, word in enumerate(tokens):
        for j in range(max(0, i - WINDOW), min(len(tokens), i + WINDOW + 1)):
            if j == i:
                continue
            vector = vectors[word]
            change = [0.0] * SIZE
            # Pull the real neighbour closer and push the random ones away.
            samples = [(tokens[j], 1)] + [(random.choice(noise), 0) for _ in range(NEGATIVES)]
            for other, is_neighbour in samples:
                neighbour = neighbours[other]
                guess = sigmoid(sum(a * b for a, b in zip(vector, neighbour)))
                error = is_neighbour - guess
                for k in range(SIZE):
                    change[k] += rate * error * neighbour[k]
                    neighbour[k] += rate * error * vector[k]
            for k in range(SIZE):
                vector[k] += change[k]
    print(f"  Training: epoch {epoch + 1}/{EPOCHS}", end="\r")
print(" " * 40, end="\r")

print(f"\n=== Trained on the user guide: {len(words):,} words, {len(vocabulary)} different words ===")
for word in WORDS:
    if word not in index:
        print(f"  {word:<10} never seen")
        continue
    closest = sorted(
        ((cosine_similarity(vectors[index[word]], vectors[i]), other) for other, i in index.items() if other != word),
        reverse=True,
    )
    print(f"  {word:<10} {', '.join(other for _, other in closest[:5])}")

with open(OUTPUT / "02_word_vectors.txt", "w") as file:
    for word, i in index.items():
        file.write(f"{word} {' '.join(f'{x:.4f}' for x in vectors[i])}\n")
