# What to embed — embed the library four ways and see where the right document lands.
# Run from the module folder: uv run python playground/what-to-embed/play.py
#                         or: source ../../.venv/bin/activate && python playground/what-to-embed/play.py
#
# To play: add a way of your own to WAYS (the opening paragraph alone, or the text without its headings),
# or set CUSTOMERS_ONLY = True. Vectors are cached in output/, so reruns are quick.

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
TOP = 5  # a question is a hit if a right document is in the top 5
CUSTOMERS_ONLY = False  # True searches only the customer documents, as demo 6's filter does


def read_documents():
    documents = []
    for path in sorted((DATA / "docs").glob("*.md")):
        _, header, text = path.read_text().split("---", 2)
        fields = dict(re.findall(r"^(\w+): (.+)$", header, re.MULTILINE))
        documents.append({"id": path.stem, "text": text.strip(), **fields})
    return documents


def opening_paragraph(document):
    # The first block of text that isn't a heading.
    blocks = re.split(r"\n\s*\n", document["text"])
    return next(b.strip() for b in blocks if not b.strip().startswith("#"))


def whole_document(document):
    return document["text"]


def title(document):
    return document["title"]


def title_and_headings(document):
    headings = re.findall(r"^#{2,3} (.+)$", document["text"], re.MULTILINE)
    return "\n".join([document["title"], *headings])


def title_and_opening(document):
    return f"{document['title']}\n{opening_paragraph(document)}"


# Four ways to turn a document into the text we embed.
WAYS = {
    "whole document": whole_document,
    "title": title,
    "title + headings": title_and_headings,
    "title + opening": title_and_opening,
}

client = OpenAI()


def embed(texts):
    # Vectors are kept in output/vectors.db by their text, so a rerun only embeds new text.
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


def cosine_similarity(a, b):
    return math.sumprod(a, b) / (math.sqrt(math.sumprod(a, a)) * math.sqrt(math.sumprod(b, b)))


def rank_of_right_document(question, question_vector, vectors):
    similarities = {
        d["id"]: cosine_similarity(question_vector, v)
        for d, v in zip(documents, vectors)
        if d["audience"] == "customer" or not CUSTOMERS_ONLY
    }
    # 1 + how many documents are closer than the best right one, so an exact tie counts as a draw.
    best = max(similarities[id] for id in question["expected"])
    rank = 1 + sum(similarity > best for similarity in similarities.values())
    return rank, sorted(similarities, key=similarities.get, reverse=True)[:TOP]


def row(label, values):
    label = label if len(label) <= 50 else label[:47] + "..."
    return f"  {label:<52}" + "".join(f"{value:>18}" for value in values)


documents = read_documents()
questions = json.loads((DATA / "questions.json").read_text())

question_vectors = embed([q["question"] for q in questions])
library = {}
words = {}
for way, make_text in WAYS.items():
    texts = [make_text(d) for d in documents]
    library[way] = embed(texts)
    words[way] = sum(len(t.split()) for t in texts)

results = []
for q, question_vector in zip(questions, question_vectors):
    ways = {}
    for way, vectors in library.items():
        rank, top = rank_of_right_document(q, question_vector, vectors)
        ways[way] = {"rank": rank, "top": top}
    results.append({**q, "ways": ways})

hits = {way: sum(r["ways"][way]["rank"] <= TOP for r in results) for way in WAYS}
searched = "the customer documents" if CUSTOMERS_ONLY else f"all {len(documents):,} documents"
print(f"\nWhere the right document lands (1 = first), searching {searched}:\n")
print(row("Question", WAYS))
for r in results:
    print(row(r["question"], [r["ways"][way]["rank"] for way in WAYS]))
    if r is results[0]:
        print()  # the module's question first, then the other nineteen
print(f"\n{row(f'A right document in the top {TOP}, of {len(questions)}', hits.values())}")
print(row("Words embedded", [f"{n:,}" for n in words.values()]))

(OUTPUT / "ranks.json").write_text(json.dumps({"hits": hits, "words": words, "questions": results}, indent=2))
