# Stale copies — one fact changes. Find every chunk that still states the old one, by vector search and by plain text.
# Run from the module folder: uv run python playground/stale-copies/play.py
#                         or: source ../../.venv/bin/activate && python playground/stale-copies/play.py
#
# To play: change OLD_FACT and OLD_WORDINGS to another fact (the 48 hours of backup batteries, say),
# or change NEAREST. Vectors are kept in a ChromaDB store in output/chroma, so reruns are quick.

import hashlib
import json
import re
from pathlib import Path

import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

HERE = Path(__file__).parent
DATA = HERE.parent.parent / "data"
OUTPUT = HERE / "output"
OUTPUT.mkdir(exist_ok=True)

DATABASE = OUTPUT / "chroma"
EMBEDDING_MODEL = "text-embedding-3-small"
BATCH = 100
OLD_FACT = "A household invitation works for 7 days."  # what the documents say now
NEW_FACT = "A household invitation works for 14 days."  # what is true from today
OLD_WORDINGS = ["7 days", "seven days", "7-day", "seven-day"]  # every way of writing it you can think of
NEAREST = 20  # how many chunks the vector search returns

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
    # One chunk per section, starting with "Title > Heading", as in demo 3.
    chunks, path, lines = [], [], []

    def finish_section():
        content = "\n".join(lines).strip()
        if content:
            heading = " > ".join([document["title"], *path])
            id = f"{document['name']}#{slug(path[-1]) if path else 'top'}"
            while id in {c["id"] for c in chunks}:
                id += "-2"
            chunks.append({"id": id, "document": document["name"], "text": f"{heading}\n\n{content}"})

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


def embed(texts):
    vectors = []
    for start in range(0, len(texts), BATCH):
        response = client.embeddings.create(model=EMBEDDING_MODEL, input=texts[start : start + BATCH])
        vectors += [item.embedding for item in response.data]
        print(f"  Embedding: {len(vectors):,}/{len(texts):,}", end="\r")
    print(" " * 40, end="\r")
    return vectors


def open_collection():
    database = chromadb.PersistentClient(path=str(DATABASE), settings=Settings(anonymized_telemetry=False))
    # Compare by cosine similarity, and use our own embeddings rather than Chroma's built-in model.
    return database.get_or_create_collection(
        "chunks", configuration={"hnsw": {"space": "cosine"}}, embedding_function=None
    )


def update(collection, chunks):
    stored = collection.get(include=["metadatas"])
    stored = dict(zip(stored["ids"], (m["checksum"] for m in stored["metadatas"])))
    checksums = {c["id"]: hashlib.sha256(c["text"].encode()).hexdigest() for c in chunks}
    changed = [c for c in chunks if stored.get(c["id"]) != checksums[c["id"]]]
    removed = set(stored) - set(checksums)

    if removed:
        collection.delete(ids=list(removed))
    if changed:
        collection.upsert(
            ids=[c["id"] for c in changed],
            embeddings=embed([c["text"] for c in changed]),
            documents=[c["text"] for c in changed],
            metadatas=[{"document": c["document"], "checksum": checksums[c["id"]]} for c in changed],
        )


def vector_ranking(collection, text, k):
    # Every chunk's id, nearest to the text first.
    [vector] = embed([text])
    return collection.query(query_embeddings=[vector], n_results=k, include=[])["ids"][0]


def plain(text):
    text = text.lower().replace("→", ">").replace("->", ">").replace("°c", " degrees")
    return re.sub(r"\s*>\s*", ">", re.sub(r"\s+", " ", text))


def contains_facts(text, facts):
    return all(any(re.search(rf"\b{re.escape(plain(option))}\b", plain(text)) for option in fact.split("|")) for fact in facts)


def sentences_saying(text, wordings):
    # The sentences an editor would need to change.
    sentences = re.split(r"(?<=[.!?])\s+|\n+", text)
    return [s.strip() for s in sentences if contains_facts(s, ["|".join(wordings)])]


documents = {d["name"]: d for d in load_documents(DATA / "docs")}
chunks = [chunk for document in documents.values() for chunk in split_into_chunks(document)]
collection = open_collection()
update(collection, chunks)

# Plain text: every chunk that contains one of the wordings.
by_text = [c for c in chunks if contains_facts(c["text"], ["|".join(OLD_WORDINGS)])]
# Vectors: every chunk, nearest to the old fact first. A vector search would return the first NEAREST.
ranking = vector_ranking(collection, OLD_FACT, len(chunks))
rank = {id: n for n, id in enumerate(ranking, 1)}
in_nearest = sum(rank[c["id"]] <= NEAREST for c in by_text)
furthest = max(rank[c["id"]] for c in by_text)

found = {}
for chunk in by_text:
    found.setdefault(chunk["document"], []).append(chunk)

print(f'\nThe fact "{OLD_FACT}" is now "{NEW_FACT}"\n')
print(f"  Plain text search for {', '.join(OLD_WORDINGS)}: {len(by_text)} chunks in {len(found)} documents")
print(f"  Vector search for the old fact: {in_nearest} of them are in the nearest {NEAREST}")
print(f"  The furthest is number {furthest:,} of {len(chunks):,}")

print(f"\n  The documents to update, and where their chunks came in the vector search:\n")
print(f"  {'Vector rank':<20}{'Type':<17}{'Audience':<10}Document")
for name, its_chunks in sorted(found.items(), key=lambda item: min(rank[c["id"]] for c in item[1])):
    ranks = ", ".join(str(rank[c["id"]]) for c in sorted(its_chunks, key=lambda c: rank[c["id"]]))
    document = documents[name]
    print(f"  {ranks:<20}{document['type']:<17}{document['audience']:<10}{name}")

nearby = [id for id in ranking[:NEAREST] if id not in {c["id"] for c in by_text}]
if nearby:
    print(f"\n  In the nearest {NEAREST}, but not saying it:")
    for id in nearby:
        print(f"    {id}")

report = [
    {
        "document": name,
        "type": documents[name]["type"],
        "audience": documents[name]["audience"],
        "chunks": [
            {"id": c["id"], "vector_rank": rank[c["id"]], "sentences": sentences_saying(c["text"], OLD_WORDINGS)}
            for c in its_chunks
        ],
    }
    for name, its_chunks in sorted(found.items())
]
(OUTPUT / "stale-copies.json").write_text(
    json.dumps({"old": OLD_FACT, "new": NEW_FACT, "documents": report, "nearest_but_not_saying_it": nearby}, indent=2)
)
