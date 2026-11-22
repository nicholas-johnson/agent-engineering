# Run from the module folder: uv run python demo/05_word_vectors.py

import json
import math
import random
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
DOCS = HERE.parent / "data" / "docs"
GUIDE = DOCS / "user-guide.md"
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
QUESTION = "Why is the heating already on before my alarm goes off?"

random.seed(SEED)


def sigmoid(x):
    return 1 / (1 + math.exp(-max(-30, min(30, x))))


def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    length_a = math.sqrt(sum(x * x for x in a))
    length_b = math.sqrt(sum(y * y for y in b))
    return dot / (length_a * length_b)


def words(text):
    return re.findall(r"[a-z0-9]+", text.lower())


def sentence_vector(text, word_vectors):
    # Add up the vectors of the words the model knows, as demo 4 does.
    known = [word_vectors[w] for w in words(text) if w in word_vectors]
    return [sum(column) for column in zip(*known)]


def read_documents():
    documents = []
    for path in sorted(DOCS.glob("*.md")):
        _, header, text = path.read_text().split("---", 2)
        title = re.search(r"^title: (.+)$", header, re.MULTILINE)[1]
        audience = re.search(r"^audience: (.+)$", header, re.MULTILINE)[1]
        documents.append({"id": path.stem, "title": title, "audience": audience, "text": text.strip()})
    return documents


def user_guide_sections(documents):
    # The small library: the user guide, one entry per section that has text of its own.
    guide = next(d for d in documents if d["id"] == "user-guide")
    sections = []
    for part in re.split(r"\n(?=#{2,3} )", guide["text"])[1:]:
        title, _, body = part.partition("\n")
        if body.strip():
            sections.append({"id": "user-guide", "title": title.lstrip("# "), "audience": guide["audience"], "text": part})
    return sections


guide_words = words(GUIDE.read_text().split("---", 2)[2])
counts = Counter(guide_words)
vocabulary = sorted(w for w, c in counts.items() if c >= MIN_COUNT)
index = {w: i for i, w in enumerate(vocabulary)}
tokens = [index[w] for w in guide_words if w in index]

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

print(f"\n=== Trained on the user guide: {len(guide_words):,} words, {len(vocabulary)} different words ===")
for word in WORDS:
    if word not in index:
        print(f"  {word:<10} never seen")
        continue
    closest = sorted(
        ((cosine_similarity(vectors[index[word]], vectors[i]), other) for other, i in index.items() if other != word),
        reverse=True,
    )
    print(f"  {word:<10} {', '.join(other for _, other in closest[:5])}")

with open(OUTPUT / "05_word_vectors.txt", "w") as file:
    for word, i in index.items():
        file.write(f"{word} {' '.join(f'{x:.4f}' for x in vectors[i])}\n")

# The question again, adding up 20 numbers per word instead of demo 4's two.
word_vectors = {word: vectors[i] for word, i in index.items()}
question_vector = sentence_vector(QUESTION, word_vectors)
written = {}
documents = read_documents()
libraries = {"The user guide": user_guide_sections(documents), "All the documentation": documents}
for name, library in libraries.items():
    print(f"\n=== {name}: {len(library):,} {'sections' if library[0]['id'] == 'user-guide' else 'documents'} ===")
    print(f"Q: {QUESTION}")
    results = sorted(
        ((cosine_similarity(question_vector, sentence_vector(d["text"], word_vectors)), d) for d in library),
        key=lambda r: r[0],
        reverse=True,
    )
    for similarity, document in results[:3]:
        print(f"  {similarity:.3f}  {document['audience']:<8}  {document['title']}")
    written[name] = [
        {"rank": rank, "similarity": round(similarity, 4), "id": d["id"], "title": d["title"]}
        for rank, (similarity, d) in enumerate(results, start=1)
    ]

(OUTPUT / "05_question.json").write_text(json.dumps(written, indent=2))
