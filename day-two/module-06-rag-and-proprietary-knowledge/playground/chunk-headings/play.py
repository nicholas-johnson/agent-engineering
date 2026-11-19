# Chunk headings — embed each chunk with and without its "Title > Heading" line, and see which retrieval finds more.
# Run from the module folder: uv run python playground/chunk-headings/play.py
#                         or: source ../../.venv/bin/activate && python playground/chunk-headings/play.py
#
# To play: add a way of your own to WAYS (the title alone, or the document's type and audience too).
# Vectors are kept in output/chunks.db, one table per way, so reruns are quick.

import hashlib
import json
import re
import sqlite3
from pathlib import Path

import sqlite_vec
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

HERE = Path(__file__).parent
DATA = HERE.parent.parent / "data"
OUTPUT = HERE / "output"
OUTPUT.mkdir(exist_ok=True)

DATABASE = OUTPUT / "chunks.db"
EMBEDDING_MODEL = "text-embedding-3-small"
BATCH = 100
TOP = 5  # a question is a hit if a chunk with its facts is in the top 5
DEPTH = 100  # how far down the list to look for the first right chunk

client = OpenAI()


def load_documents(folder):
    documents = []
    for path in sorted(folder.glob("*.md")):
        _, front, body = path.read_text().split("---", 2)
        fields = dict(line.split(": ", 1) for line in front.strip().splitlines())
        documents.append({"name": path.name, **fields, "body": body})
    return documents


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def split_into_chunks(document):
    # Demo 3's chunks, keeping the heading line and the section's own text apart.
    chunks, path, lines = [], [], []

    def finish_section():
        content = "\n".join(lines).strip()
        if content:
            heading = " > ".join([document["title"], *path])
            id = f"{document['name']}#{slug(path[-1]) if path else 'top'}"
            while id in {c["id"] for c in chunks}:
                id += "-2"
            chunks.append({"id": id, "heading": heading, "content": content, "text": f"{heading}\n\n{content}"})

    for line in document["body"].splitlines():
        heading = re.match(r"(#{1,3}) (.+)", line)
        if heading:
            finish_section()
            lines = []
            level = len(heading[1])
            path = path[: level - 2] + [heading[2].strip()] if level > 1 else []
        else:
            lines.append(line)
    finish_section()
    return chunks


# What we embed for each chunk. The model is always given the whole chunk, so only the search changes.
WAYS = {
    "without": lambda chunk: chunk["content"],
    "with": lambda chunk: chunk["text"],  # "Title > Heading", a blank line, then the section: demo 3
}


def embed(texts):
    vectors = []
    for start in range(0, len(texts), BATCH):
        response = client.embeddings.create(model=EMBEDDING_MODEL, input=texts[start : start + BATCH])
        vectors += [item.embedding for item in response.data]
        print(f"  Embedding: {len(vectors):,}/{len(texts):,}", end="\r")
    print(" " * 40, end="\r")
    return vectors


def open_database():
    db = sqlite3.connect(DATABASE)
    db.enable_load_extension(True)
    sqlite_vec.load(db)
    db.enable_load_extension(False)
    return db


def table_for(way):
    return "chunks_" + slug(way).replace("-", "_")


def update(db, table, chunks, make_text):
    # Embed make_text(chunk), but store the whole chunk, since that is what the model would read.
    db.execute(
        f"create virtual table if not exists {table} using vec0("
        "id text primary key, embedding float[1536] distance_metric=cosine, +text text, +checksum text)"
    )
    stored = dict(db.execute(f"select id, checksum from {table}"))
    current = {c["id"]: hashlib.sha256(make_text(c).encode()).hexdigest() for c in chunks}
    changed = [c for c in chunks if stored.get(c["id"]) != current[c["id"]]]
    for id in (set(stored) - set(current)) | {c["id"] for c in changed}:
        db.execute(f"delete from {table} where id = ?", (id,))
    for chunk, vector in zip(changed, embed([make_text(c) for c in changed])):
        db.execute(
            f"insert into {table} (id, embedding, text, checksum) values (?, ?, ?, ?)",
            (chunk["id"], sqlite_vec.serialize_float32(vector), chunk["text"], current[chunk["id"]]),
        )
    db.commit()


def rank_of_right_chunk(db, table, vector, facts):
    # 1 + how many chunks come before the first one that holds the facts.
    rows = db.execute(
        f"select id, text from {table} where embedding match ? and k = ? order by distance",
        (sqlite_vec.serialize_float32(vector), DEPTH),
    )
    ids = []
    for rank, (id, text) in enumerate(rows, 1):
        ids.append(id)
        if contains_facts(text, facts):
            return rank, ids[:TOP]
    return None, ids[:TOP]


def plain(text):
    text = text.lower().replace("→", ">").replace("->", ">").replace("°c", " degrees")
    return re.sub(r"\s*>\s*", ">", re.sub(r"\s+", " ", text))


def contains_facts(text, facts):
    return all(any(re.search(rf"\b{re.escape(plain(option))}\b", plain(text)) for option in fact.split("|")) for fact in facts)


def row(label, values):
    label = label if len(label) <= 55 else label[:52] + "..."
    return f"  {label:<57}" + "".join(f"{value:>10}" for value in values)


documents = load_documents(DATA / "docs")
chunks = [chunk for document in documents for chunk in split_into_chunks(document)]
db = open_database()
for way, make_text in WAYS.items():
    update(db, table_for(way), chunks, make_text)

questions = [q for q in json.loads((DATA / "questions.json").read_text()) if q["kind"] in ("everyday", "error code")]
vectors = embed([q["question"] for q in questions])

results = []
for q, vector in zip(questions, vectors):
    ways = {}
    for way in WAYS:
        rank, top = rank_of_right_chunk(db, table_for(way), vector, q["facts"])
        ways[way] = {"rank": rank, "top": top}
    results.append({"id": q["id"], "question": q["question"], "facts": q["facts"], "ways": ways})

hits = {way: sum((r["ways"][way]["rank"] or DEPTH + 1) <= TOP for r in results) for way in WAYS}
print(f"\nWhere the first chunk with the facts lands (1 = first), searching {len(chunks):,} chunks:\n")
print(row("Question", WAYS))
for r in results:
    print(row(r["question"], [r["ways"][way]["rank"] or f"{DEPTH}+" for way in WAYS]))
print(f"\n{row(f'Facts in the top {TOP}, of {len(questions)}', hits.values())}")

(OUTPUT / "results.json").write_text(json.dumps({"hits": hits, "questions": results}, indent=2))
