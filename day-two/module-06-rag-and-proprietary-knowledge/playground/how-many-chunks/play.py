# How many chunks — send the model the top 1, 2, ... 20 chunks: what each extra chunk finds, and what it costs.
# Run from the module folder: uv run python playground/how-many-chunks/play.py
#                         or: source ../../.venv/bin/activate && python playground/how-many-chunks/play.py
#
# To play: change MAX_TOP or the prices, and rerun.
# Vectors are kept in a ChromaDB store in output/chroma, so after the first run only the 24 questions are embedded.

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
MAX_TOP = 20  # try every TOP from 1 to this
# Dollars per million tokens, from Module 4's price list (checked 10 November 2026).
INPUT_PRICE = 0.10  # gpt-6-luna input
EMBEDDING_PRICE = 0.02  # text-embedding-3-small
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
    vectors, tokens = [], 0
    for start in range(0, len(texts), BATCH):
        response = client.embeddings.create(model=EMBEDDING_MODEL, input=texts[start : start + BATCH])
        vectors += [item.embedding for item in response.data]
        tokens += response.usage.prompt_tokens
        print(f"  Embedding: {len(vectors):,}/{len(texts):,}", end="\r")
    print(" " * 40, end="\r")
    return vectors, tokens


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
        vectors, _ = embed([c["text"] for c in changed])
        collection.upsert(
            ids=[c["id"] for c in changed],
            embeddings=vectors,
            documents=[c["text"] for c in changed],
            metadatas=[{"document": c["document"], "checksum": checksums[c["id"]]} for c in changed],
        )


def search(collection, vector):
    results = collection.query(query_embeddings=[vector], n_results=MAX_TOP, include=["documents"])
    return [{"id": id, "text": text} for id, text in zip(results["ids"][0], results["documents"][0])]


def wrap(chunk):
    # How demo 3 puts a chunk in the prompt.
    return f'<chunk id="{chunk["id"]}">\n{chunk["text"]}\n</chunk>'


def count_tokens(text):
    # The API counts the tokens without running the model.
    return client.responses.input_tokens.count(model=MODEL, input=text).input_tokens


def plain(text):
    text = text.lower().replace("→", ">").replace("->", ">").replace("°c", " degrees")
    return re.sub(r"\s*>\s*", ">", re.sub(r"\s+", " ", text))


def contains_facts(text, facts):
    return all(any(re.search(rf"\b{re.escape(plain(option))}\b", plain(text)) for option in fact.split("|")) for fact in facts)


documents = load_documents(DATA / "docs")
collection = open_collection()
update(collection, [chunk for document in documents for chunk in split_into_chunks(document)])

questions = [q for q in json.loads((DATA / "questions.json").read_text()) if q["kind"] in ("everyday", "error code")]
vectors, question_tokens = embed([q["question"] for q in questions])
tops = [search(collection, vector) for vector in vectors]

# The rank of the first chunk that holds each question's facts (None if it isn't in the top MAX_TOP).
ranks = [
    next((n for n, c in enumerate(top, 1) if contains_facts(c["text"], q["facts"])), None) for q, top in zip(questions, tops)
]

# Tokens per question with no chunks, then what the 1st chunks add, the 2nd chunks, and so on.
# Counting all 24 questions' 1st chunks together, then their 2nd, is quicker than counting every prompt.
base = count_tokens("\n\n".join(f"{INSTRUCTIONS}\n\nUse our documentation:\n\n{q['question']}" for q in questions))
added = []
for n in range(MAX_TOP):
    print(f"  Counting tokens: {n + 1}/{MAX_TOP}", end="\r")
    added.append(count_tokens("\n\n".join(wrap(top[n]) for top in tops)))
print(" " * 40, end="\r")

rows = []
for top in range(1, MAX_TOP + 1):
    tokens = (base + sum(added[:top])) / len(questions)
    found = sum(rank is not None and rank <= top for rank in ranks)
    rows.append({"top": top, "found": found, "tokens": round(tokens), "dollars": tokens * INPUT_PRICE / 1_000_000})

embedding_dollars = question_tokens / len(questions) * EMBEDDING_PRICE / 1_000_000
print(f"\n  {'TOP':>4}  {'Facts in the top TOP, of ' + str(len(questions)):<28}{'Tokens in':>10}{'Per question':>15}")
for r in rows:
    print(f"  {r['top']:>4}  {r['found']:>3}  {'#' * r['found']:<24}{r['tokens']:>10,}{'$' + format(r['dollars'], '.6f'):>15}")
print(f"\n  Embedding each question costs ${embedding_dollars:.8f}, whatever TOP is.")

(OUTPUT / "results.json").write_text(
    json.dumps(
        {
            "rows": rows,
            "embedding_dollars_per_question": embedding_dollars,
            "questions": [{"id": q["id"], "question": q["question"], "rank": rank} for q, rank in zip(questions, ranks)],
        },
        indent=2,
    )
)
