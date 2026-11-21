# Shrink the vectors — ask for shorter embeddings and see what search loses.
# Run from the module folder: uv run python playground/shrink-the-vectors/play.py
#                         or: source ../../.venv/bin/activate && python playground/shrink-the-vectors/play.py
#
# To play: add sizes to DIMENSIONS (try 128, 32 or 16), or change TOP.
# Vectors are cached in output/, so a rerun only embeds what it hasn't seen.

import json
import math
import re
import sqlite3
import struct
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

HERE = Path(__file__).parent
DATA = HERE.parent.parent / "data"
OUTPUT = HERE / "output"
OUTPUT.mkdir(exist_ok=True)

EMBEDDING_MODEL = "text-embedding-3-small"
BATCH = 100
DIMENSIONS = [1536, 512, 256, 64]  # 1536 is the full length; the API cuts it down for us
TOP = 5
BYTES_PER_NUMBER = 4  # each number is stored as a 32-bit float, as ChromaDB does

client = OpenAI()


def read_documents():
    documents = []
    for path in sorted((DATA / "docs").glob("*.md")):
        _, header, text = path.read_text().split("---", 2)
        fields = dict(re.findall(r"^(\w+): (.+)$", header, re.MULTILINE))
        documents.append({"id": path.stem, "text": text.strip(), **fields})
    return documents


def embed(texts, dimensions):
    # Vectors are kept in output/vectors.db by size and text, so a rerun only embeds new text.
    cache = sqlite3.connect(OUTPUT / "vectors.db")
    cache.execute(
        "create table if not exists vectors"
        " (dimensions integer, text text, vector blob, primary key (dimensions, text))"
    )
    stored = dict(cache.execute("select text, vector from vectors where dimensions = ?", (dimensions,)))
    missing = list(dict.fromkeys(t for t in texts if t not in stored))
    for start in range(0, len(missing), BATCH):
        batch = missing[start : start + BATCH]
        response = client.embeddings.create(model=EMBEDDING_MODEL, input=batch, dimensions=dimensions)
        for text, item in zip(batch, response.data):
            stored[text] = struct.pack(f"{len(item.embedding)}f", *item.embedding)
            cache.execute("insert into vectors values (?, ?, ?)", (dimensions, text, stored[text]))
        cache.commit()
        print(f"  Embedding at {dimensions}: {start + len(batch):,}/{len(missing):,}", end="\r")
    print(" " * 40, end="\r")
    return [struct.unpack(f"{len(stored[t]) // 4}f", stored[t]) for t in texts]


def cosine_similarity(a, b):
    return math.sumprod(a, b) / (math.sqrt(math.sumprod(a, a)) * math.sqrt(math.sumprod(b, b)))


def rank_of_right_document(question, question_vector, vectors):
    # Search every document, as demo 4 does. 1 + how many documents beat the best right one.
    similarities = {d["id"]: cosine_similarity(question_vector, v) for d, v in zip(documents, vectors)}
    best = max(similarities[id] for id in question["expected"])
    return 1 + sum(similarity > best for similarity in similarities.values())


documents = read_documents()
questions = json.loads((DATA / "questions.json").read_text())

results = []
for dimensions in DIMENSIONS:
    vectors = embed([d["text"] for d in documents], dimensions)
    question_vectors = embed([q["question"] for q in questions], dimensions)
    ranks = [rank_of_right_document(q, v, vectors) for q, v in zip(questions, question_vectors)]
    results.append(
        {
            "dimensions": dimensions,
            "bytes_per_vector": dimensions * BYTES_PER_NUMBER,
            "first": sum(rank == 1 for rank in ranks),
            "top": sum(rank <= TOP for rank in ranks),
            "ranks": {q["question"]: rank for q, rank in zip(questions, ranks)},
        }
    )

print(f"\nThe {len(questions)} questions, searched at each size:\n")
print(f"  Dimensions  Bytes per vector  A million vectors  Right document first  In the top {TOP}")
for r in results:
    # A million vectors of n bytes each take n megabytes.
    print(
        f"  {r['dimensions']:>10,}  {r['bytes_per_vector']:>16,}  {r['bytes_per_vector']:>14,} MB"
        f"  {r['first']:>20}  {r['top']:>12}"
    )

(OUTPUT / "results.json").write_text(json.dumps(results, indent=2))
