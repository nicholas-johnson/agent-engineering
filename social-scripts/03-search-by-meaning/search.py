"""Clip 3's searches: Alice in Wonderland, searched by keyword and by meaning.

Cuts the book into passages, finds each question's words with Ctrl+F and with
keyword search (BM25), then embeds every passage and finds the closest by
meaning. Prints what the clip shows, and writes map.js: every passage squashed
from 1,536 numbers to 2 with PCA, for the map on the stage.

Needs OPENAI_API_KEY in .env. Embedding the book costs well under a tenth of a cent.

Run with: uv run python social-scripts/03-search-by-meaning/search.py
"""

import json
import math
import random
import re
from collections import Counter
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

HERE = Path(__file__).parent
BOOK = HERE / "../../day-one/module-01-intro-to-language-models/data/alice.txt"
PASSAGE_WORDS = 120  # paragraphs are joined until a passage has at least this many words
MODEL = "text-embedding-3-small"
QUESTIONS = {"angry": ("the angry queen", "angry"), "pipe": ("the creature with a pipe", "pipe")}
K1, B = 1.5, 0.75  # BM25's usual settings, as in Module 5
# Who each passage is mostly about, to colour the map
GROUPS = {
    "royals": ["Queen", "King"],
    "caterpillar": ["Caterpillar"],
    "turtle": ["Mock Turtle", "Gryphon"],
    "tea": ["Hatter", "March Hare", "Dormouse"],
}


def cut_into_passages(text):
    passages, current = [], []
    for paragraph in re.split(r"\n\s*\n", text):
        if paragraph.strip():
            current.append(" ".join(paragraph.split()))
        if sum(len(p.split()) for p in current) >= PASSAGE_WORDS:
            passages.append(" ".join(current))
            current = []
    return passages + [" ".join(current)] if current else passages


def words(text):
    return re.findall(r"[a-z]+", text.lower())


def keyword_search(question, passages):
    documents = [words(p) for p in passages]
    average = sum(map(len, documents)) / len(documents)
    appears_in = Counter(w for d in documents for w in set(d))
    scores = []
    for document in documents:
        counts, score = Counter(document), 0
        for word in set(words(question)):
            if counts[word]:
                rarity = math.log(1 + (len(documents) - appears_in[word] + 0.5) / (appears_in[word] + 0.5))
                score += rarity * counts[word] * (K1 + 1) / (counts[word] + K1 * (1 - B + B * len(document) / average))
        scores.append(score)
    return max(range(len(passages)), key=lambda i: scores[i])


def embed(client, texts):
    vectors = []
    for start in range(0, len(texts), 100):
        response = client.embeddings.create(model=MODEL, input=texts[start : start + 100])
        vectors += [item.embedding for item in response.data]
    return vectors


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def cosine_similarity(a, b):
    return dot(a, b) / math.sqrt(dot(a, a) * dot(b, b))


# PCA: the two directions in which the passages differ most, found by power iteration.
def squash_to_2d(vectors, others):
    mean = [sum(column) / len(vectors) for column in zip(*vectors)]
    centred = [[x - m for x, m in zip(v, mean)] for v in vectors]
    gram = [[dot(a, b) for b in centred] for a in centred]
    rng = random.Random(0)
    directions = []
    for _ in range(2):
        weights = [rng.random() for _ in centred]
        for _ in range(200):
            weights = [dot(row, weights) for row in gram]
            for found in directions:
                overlap = dot(weights, found)
                weights = [w - overlap * f for w, f in zip(weights, found)]
            length = math.sqrt(dot(weights, weights))
            weights = [w / length for w in weights]
        directions.append(weights)
    axes = []
    for weights in directions:
        axis = [sum(w * v[k] for w, v in zip(weights, centred)) for k in range(len(mean))]
        length = math.sqrt(dot(axis, axis))
        axes.append([a / length for a in axis])
    project = lambda v: [round(dot([x - m for x, m in zip(v, mean)], axis), 4) for axis in axes]
    return [project(v) for v in vectors], [project(v) for v in others]


def group_of(passage):
    counts = {group: sum(len(re.findall(rf"\b{name}\b", passage)) for name in names) for group, names in GROUPS.items()}
    best = max(counts, key=counts.get)
    return best if counts[best] >= 2 else ""


def short(passage, length=110):
    return passage if len(passage) <= length else passage[:length] + "…"


load_dotenv()
text = BOOK.read_text()
passages = cut_into_passages(text)
print(f"Alice in Wonderland, cut into {len(passages)} passages of about {PASSAGE_WORDS} words")

client = OpenAI()
passage_vectors = embed(client, passages)
question_vectors = embed(client, [question for question, _ in QUESTIONS.values()])
points, question_points = squash_to_2d(passage_vectors, question_vectors)

questions = {}
for (name, (question, word)), vector, point in zip(QUESTIONS.items(), question_vectors, question_points):
    print(f"\nQuestion: {question}")
    hits = [m.start() for m in re.finditer(word, text, re.IGNORECASE)]
    print(f'  Ctrl+F "{word}": {len(hits)} matches')
    for at in hits:
        print(f"    …{' '.join(text[max(0, at - 50) : at + 40].split())}…")
    keyword = keyword_search(question, passages)
    print(f"  Best keyword match: [{keyword}] {short(passages[keyword])}")
    similarities = [cosine_similarity(vector, v) for v in passage_vectors]
    closest = sorted(range(len(passages)), key=lambda i: -similarities[i])
    print("  Closest by meaning:")
    for i in closest[:3]:
        print(f"    {similarities[i]:.3f} [{i}] {short(passages[i])}")
    print(f"  The closest passage as numbers: [{', '.join(f'{x:.3f}' for x in passage_vectors[closest[0]][:4])}, …]")
    questions[name] = {"text": question, "point": point, "nearest": closest[0], "keyword": keyword}

map_data = {"points": [[x, y, group_of(p)] for (x, y), p in zip(points, passages)], "questions": questions}
(HERE / "map.js").write_text(
    "// Written by search.py: every passage of Alice in Wonderland, squashed from 1,536 numbers to 2\n"
    "// with PCA, with its group, and where each question lands.\n"
    f"window.MAP = {json.dumps(map_data, separators=(',', ':'))};\n"
)
print(f"\nWrote map.js: {len(points)} passages and {len(questions)} questions")
