# Distance measures — cosine similarity, dot product and distance, on two kinds of vector.
# Run from the module folder: uv run python playground/distance-measures/play.py
#                         or: source ../../.venv/bin/activate && python playground/distance-measures/play.py
#
# To play: change QUESTION, or TOP to see further down each list.
# Embeddings are cached in output/vectors.db, so a rerun only embeds text it hasn't seen.

import json
import math
import re
import sqlite3
import struct
from collections import Counter
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

HERE = Path(__file__).parent
DOCS = HERE.parent.parent / "data" / "docs"
OUTPUT = HERE / "output"
OUTPUT.mkdir(exist_ok=True)

EMBEDDING_MODEL = "text-embedding-3-small"
BATCH = 100
QUESTION = "Why is the heating already on before my alarm goes off?"
TOP = 3

client = OpenAI()


def read_documents():
    documents = []
    for path in sorted(DOCS.glob("*.md")):
        _, header, text = path.read_text().split("---", 2)
        title = re.search(r"^title: (.+)$", header, re.MULTILINE)[1]
        documents.append({"id": path.stem, "title": title, "text": text.strip()})
    return documents


def words(text):
    return re.findall(r"[a-z0-9]+", text.lower())


def count_vector(text, vocabulary):
    # One number per vocabulary word: how many times it appears in the text.
    counts = Counter(words(text))
    return [counts[word] for word in vocabulary]


def embed(texts):
    # Vectors are kept in output/vectors.db by text, so a rerun only embeds new text.
    cache = sqlite3.connect(OUTPUT / "vectors.db")
    cache.execute("create table if not exists vectors (text text primary key, vector blob)")
    stored = dict(cache.execute("select text, vector from vectors"))
    missing = list(dict.fromkeys(t for t in texts if t not in stored))
    for start in range(0, len(missing), BATCH):
        batch = missing[start : start + BATCH]
        response = client.embeddings.create(model=EMBEDDING_MODEL, input=batch)
        for text, item in zip(batch, response.data):
            stored[text] = struct.pack(f"{len(item.embedding)}f", *item.embedding)
            cache.execute("insert into vectors values (?, ?)", (text, stored[text]))
        cache.commit()
        print(f"  Embedding: {start + len(batch):,}/{len(missing):,}", end="\r")
    print(" " * 40, end="\r")
    return [struct.unpack(f"{len(stored[t]) // 4}f", stored[t]) for t in texts]


def length(a):
    return math.sqrt(math.sumprod(a, a))


def cosine_similarity(a, b):
    # The angle between the vectors, ignoring their lengths. Higher is closer.
    return math.sumprod(a, b) / (length(a) * length(b))


def dot_product(a, b):
    # Like cosine similarity, but multiplied by both lengths. Higher is closer.
    return math.sumprod(a, b)


def distance(a, b):
    # Straight-line (Euclidean) distance between the two points. Lower is closer.
    return math.dist(a, b)


MEASURES = {
    "Cosine similarity": (cosine_similarity, "higher"),
    "Dot product": (dot_product, "higher"),
    "Distance": (distance, "lower"),
}

documents = read_documents()
# Every word the documents use, plus the question's ("my" and "alarm" are in no document).
vocabulary =sorted({word for d in documents for word in words(d["text"])} | set(words(QUESTION)))
kinds = {
    f"Word counts: one number for each of {len(vocabulary):,} words": (
        count_vector(QUESTION, vocabulary),
        [count_vector(d["text"], vocabulary) for d in documents],
    ),
    f"{EMBEDDING_MODEL}: 1,536 numbers, length 1": (
        embed([QUESTION])[0],
        embed([d["text"] for d in documents]),
    ),
}

results = {"question": QUESTION}
for kind, (question_vector, vectors) in kinds.items():
    print(f"\n=== {kind} ===")
    print(f"Q: {QUESTION}")
    results[kind] = {}
    for name, (measure, closer) in MEASURES.items():
        ranked = sorted(
            ((measure(question_vector, v), length(v), d) for v, d in zip(vectors, documents)),
            key=lambda r: r[0],
            reverse=closer == "higher",
        )
        # Each document's length in words, and its vector's length, beside the score.
        print(f"\n  {name} ({closer} is closer)\n        score  words   length")
        for score, size, d in ranked[:TOP]:
            print(f"    {score:>9.3f}  {len(words(d['text'])):>5}  {size:>7.3f}  {d['title']}")
        results[kind][name] = [
            {
                "rank": rank,
                "score": round(score, 4),
                "words": len(words(d["text"])),
                "length": round(size, 4),
                "id": d["id"],
                "title": d["title"],
            }
            for rank, (score, size, d) in enumerate(ranked, 1)
        ]

(OUTPUT / "results.json").write_text(json.dumps(results, indent=2))
