# Run from the module folder: uv run python demo/03_retrieve_and_answer.py

import hashlib
import json
import re
import sqlite3
import time
from pathlib import Path

import sqlite_vec
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

HERE = Path(__file__).parent
DATA = HERE.parent / "data"
OUTPUT = HERE / "output"
OUTPUT.mkdir(exist_ok=True)

DATABASE = OUTPUT / "knowledge.db"
MODEL = "gpt-6-luna"
EMBEDDING_MODEL = "text-embedding-3-small"
BATCH = 100
TOP = 5
INPUT_PRICE = 0.10
OUTPUT_PRICE = 0.50
INSTRUCTIONS = "You are the support assistant for Dormouse, a smart thermostat. Answer the customer in a short paragraph."
QUESTION = "Why does my Dormouse turn the heating on before the time I set?"

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
    # One chunk per section: everything under a heading, down to the next heading.
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


def open_database():
    db = sqlite3.connect(DATABASE)
    db.enable_load_extension(True)
    sqlite_vec.load(db)
    db.enable_load_extension(False)
    db.execute(
        "create virtual table if not exists chunks using vec0("
        "id text primary key, embedding float[1536] distance_metric=cosine,"
        "document text, +text text, +checksum text)"
    )
    return db


def update(db, chunks):
    # Embed new and changed chunks, and remove chunks that are no longer in the documents.
    stored = dict(db.execute("select id, checksum from chunks"))
    checksums = {c["id"]: hashlib.sha256(c["text"].encode()).hexdigest() for c in chunks}
    changed = [c for c in chunks if stored.get(c["id"]) != checksums[c["id"]]]
    removed = set(stored) - set(checksums)

    for id in removed | {c["id"] for c in changed}:
        db.execute("delete from chunks where id = ?", (id,))
    for chunk, vector in zip(changed, embed([c["text"] for c in changed])):
        db.execute(
            "insert into chunks (id, embedding, document, text, checksum) values (?, ?, ?, ?, ?)",
            (chunk["id"], sqlite_vec.serialize_float32(vector), chunk["document"], chunk["text"], checksums[chunk["id"]]),
        )
    db.commit()
    return len(changed), len(removed)


def search(db, vector, only_document=None):
    where, parameters = ("and document = ?", (only_document,)) if only_document else ("", ())
    rows = db.execute(
        f"select id, 1 - distance, text from chunks where embedding match ? and k = ? {where} order by distance",
        (sqlite_vec.serialize_float32(vector), TOP, *parameters),
    )
    return [{"id": id, "similarity": round(similarity, 3), "text": text} for id, similarity, text in rows]


def answer(question, found):
    documentation = "\n\n".join(f'<chunk id="{c["id"]}">\n{c["text"]}\n</chunk>' for c in found)
    start = time.perf_counter()
    response = client.responses.create(
        model=MODEL,
        reasoning={"effort": "none"},
        instructions=f"{INSTRUCTIONS}\n\nUse our documentation:\n\n{documentation}",
        input=question,
    )
    usage = response.usage
    return {
        "answer": response.output_text,
        "input_tokens": usage.input_tokens,
        "cost_dollars": round((usage.input_tokens * INPUT_PRICE + usage.output_tokens * OUTPUT_PRICE) / 1_000_000, 5),
        "seconds": round(time.perf_counter() - start, 1),
    }


def plain(text):
    # Lower case, one way of writing menu paths and degrees, single spaces.
    text = text.lower().replace("→", ">").replace("->", ">").replace("°c", " degrees")
    return re.sub(r"\s*>\s*", ">", re.sub(r"\s+", " ", text))


def contains_facts(text, facts):
    # Every fact must appear; "a|b" means either will do.
    return all(any(re.search(rf"\b{re.escape(plain(option))}\b", plain(text)) for option in fact.split("|")) for fact in facts)


documents = load_documents(DATA / "docs")
chunks = [chunk for document in documents for chunk in split_into_chunks(document)]
db = open_database()
changed, removed = update(db, chunks)
print(f"\n{len(documents):,} documents, {len(chunks):,} chunks. Embedded {changed:,} new or changed chunks.")
(OUTPUT / "chunks.json").write_text(json.dumps(chunks, indent=2))

print(f"\nQ: {QUESTION}")
[question_vector] = embed([QUESTION])
found = search(db, question_vector)
for chunk in found:
    print(f"   {chunk['similarity']:.3f}  {chunk['id']}")
result = answer(QUESTION, found)
print(f"A: {result['answer']}")
print(f"   {result['input_tokens']:,} tokens in, ${result['cost_dollars']:.4f}, {result['seconds']} seconds")

# How often does the top 5 contain the facts a right answer needs?
questions = [q for q in json.loads((DATA / "questions.json").read_text()) if q["kind"] in ("everyday", "error code")]
vectors = embed([q["question"] for q in questions])
scores, checks = {}, []
for name, only in [("user guide", "user-guide.md"), ("knowledge base", None)]:
    hits = 0
    for q, vector in zip(questions, vectors):
        top = search(db, vector, only)
        hit = any(contains_facts(c["text"], q["facts"]) for c in top)
        hits += hit
        checks.append({"library": name, "id": q["id"], "question": q["question"], "found": hit, "top": [c["id"] for c in top]})
    scores[name] = hits
print(
    f"\nThe answer was in the top {TOP} chunks, for {len(questions)} questions: "
    + ", ".join(f"{name} {hits}" for name, hits in scores.items())
)

(OUTPUT / "03_retrieve_and_answer.json").write_text(
    json.dumps({"question": QUESTION, "found": found, **result, "scores": scores, "checks": checks}, indent=2)
)
