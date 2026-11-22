# Chunk sizes — cut the knowledge base at its headings, or every 50, 150 or 400 words, and see what retrieval finds.
# Run from the module folder: uv run python playground/chunk-sizes/play.py
#                         or: source ../../.venv/bin/activate && python playground/chunk-sizes/play.py
#
# To play: change SIZES or OVERLAP, or TOP, and rerun.
# Each way of chunking is kept in its own ChromaDB collection in output/chroma, so a rerun only embeds what's new.

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
MODEL = "gpt-6-luna"
EMBEDDING_MODEL = "text-embedding-3-small"
BATCH = 100
UPSERT = 5000  # Chroma stores at most about 5,000 chunks in one call
TOP = 5
SIZES = [50, 150, 400]  # words in each fixed window
OVERLAP = 0  # words each window repeats from the one before it (try 25)
INSTRUCTIONS = "You are the support assistant for Dormouse, a smart thermostat. Answer the customer in a short paragraph."

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
    # Demo 3's way: one chunk per section, starting with "Title > Heading".
    chunks, path, lines = [], [], []

    def finish_section():
        content = "\n".join(lines).strip()
        if content:
            heading = " > ".join([document["title"], *path])
            id = f"{document['name']}#{slug(path[-1]) if path else 'top'}"
            while id in {c["id"] for c in chunks}:
                id += "-2"
            chunks.append({"id": id, "text": f"{heading}\n\n{content}"})

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


def split_into_windows(document, size):
    # Every `size` words, wherever the cut falls. Headings are just more words.
    words = document["body"].split()
    step = size - OVERLAP
    return [
        {"id": f"{document['name']}#words-{start + 1}", "text": " ".join(words[start : start + size])}
        for start in range(0, max(len(words) - OVERLAP, 1), step)
    ]


def embed(texts):
    vectors = []
    for start in range(0, len(texts), BATCH):
        response = client.embeddings.create(model=EMBEDDING_MODEL, input=texts[start : start + BATCH])
        vectors += [item.embedding for item in response.data]
        print(f"  Embedding: {len(vectors):,}/{len(texts):,}", end="\r")
    print(" " * 40, end="\r")
    return vectors


def open_collection(database, way):
    # One collection per way of chunking, compared by cosine similarity, with our own embeddings.
    name = "chunks_" + slug(way).replace("-", "_")
    return database.get_or_create_collection(name, configuration={"hnsw": {"space": "cosine"}}, embedding_function=None)


def update(collection, chunks):
    # Embed new and changed chunks; remove the ones that have gone.
    stored = collection.get(include=["metadatas"])
    stored = dict(zip(stored["ids"], (m["checksum"] for m in stored["metadatas"])))
    checksums = {c["id"]: hashlib.sha256(c["text"].encode()).hexdigest() for c in chunks}
    changed = [c for c in chunks if stored.get(c["id"]) != checksums[c["id"]]]
    removed = set(stored) - set(checksums)

    if removed:
        collection.delete(ids=list(removed))
    vectors = embed([c["text"] for c in changed])
    for start in range(0, len(changed), UPSERT):
        batch = changed[start : start + UPSERT]
        collection.upsert(
            ids=[c["id"] for c in batch],
            embeddings=vectors[start : start + UPSERT],
            documents=[c["text"] for c in batch],
            metadatas=[{"checksum": checksums[c["id"]]} for c in batch],
        )


def search(collection, vector):
    results = collection.query(query_embeddings=[vector], n_results=TOP, include=["documents"])
    return [{"id": id, "text": text} for id, text in zip(results["ids"][0], results["documents"][0])]


def prompt(question, found):
    # What demo 3 sends the model: the instructions, the chunks, and the question.
    documentation = "\n\n".join(f'<chunk id="{c["id"]}">\n{c["text"]}\n</chunk>' for c in found)
    return f"{INSTRUCTIONS}\n\nUse our documentation:\n\n{documentation}\n\n{question}"


def count_tokens(text):
    # The API counts the tokens without running the model.
    return client.responses.input_tokens.count(model=MODEL, input=text).input_tokens


def plain(text):
    text = text.lower().replace("→", ">").replace("->", ">").replace("°c", " degrees")
    return re.sub(r"\s*>\s*", ">", re.sub(r"\s+", " ", text))


def contains_facts(text, facts):
    return all(any(re.search(rf"\b{re.escape(plain(option))}\b", plain(text)) for option in fact.split("|")) for fact in facts)


documents = load_documents(DATA / "docs")
ways = {"headings": [c for d in documents for c in split_into_chunks(d)]}
for size in SIZES:
    ways[f"{size} words"] = [c for d in documents for c in split_into_windows(d, size)]

database = chromadb.PersistentClient(path=str(DATABASE), settings=Settings(anonymized_telemetry=False))
collections = {way: open_collection(database, way) for way in ways}
for way, chunks in ways.items():
    update(collections[way], chunks)

questions = [q for q in json.loads((DATA / "questions.json").read_text()) if q["kind"] in ("everyday", "error code")]
vectors = embed([q["question"] for q in questions])

results = {}
for n, (way, chunks) in enumerate(ways.items(), 1):
    print(f"  Searching and counting tokens: {n}/{len(ways)}", end="\r")
    checks, prompts = [], []
    for q, vector in zip(questions, vectors):
        top = search(collections[way], vector)
        found = any(contains_facts(c["text"], q["facts"]) for c in top)
        checks.append({"id": q["id"], "found": found, "top": [c["id"] for c in top]})
        prompts.append(prompt(q["question"], top))
    results[way] = {
        "chunks": len(chunks),
        "words_per_chunk": round(sum(len(c["text"].split()) for c in chunks) / len(chunks)),
        # One count for all 24 prompts together, shared out: much quicker than 24 counts.
        "tokens_per_question": round(count_tokens("\n\n".join(prompts)) / len(questions)),
        "found": sum(c["found"] for c in checks),
        "checks": checks,
    }
print(" " * 50, end="\r")

print(f"\n  {'Chunking':<10}{'Chunks':>8}{'Words each':>12}{'Tokens sent':>13}   Facts in the top {TOP}, of {len(questions)}")
for way, r in results.items():
    print(f"  {way:<10}{r['chunks']:>8,}{r['words_per_chunk']:>12,}{r['tokens_per_question']:>13,}   {r['found']:>3}")

(OUTPUT / "results.json").write_text(json.dumps({"top": TOP, "overlap": OVERLAP, "ways": results}, indent=2))
