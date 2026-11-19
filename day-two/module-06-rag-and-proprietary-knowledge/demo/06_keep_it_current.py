# Run from the module folder: uv run python demo/06_keep_it_current.py

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
DATA = HERE.parent / "data"
OUTPUT = HERE / "output"
OUTPUT.mkdir(exist_ok=True)

DATABASE = OUTPUT / "knowledge.db"
MODEL = "gpt-6-luna"
EMBEDDING_MODEL = "text-embedding-3-small"
BATCH = 100
TOP = 5
QUESTION = "Why does my Dormouse turn the heating on before the time I set?"

INSTRUCTIONS = """You are the support assistant for Dormouse, a smart thermostat. Answer the customer in a short paragraph.
Use only the documentation below, never what you know from elsewhere.
Quote, word for word, each sentence you rely on, with the id of the chunk it comes from.
If the documentation does not answer the question, set answered to false and say so. Do not guess."""

SCHEMA = {
    "type": "object",
    "properties": {
        "answered": {"type": "boolean"},
        "answer": {"type": "string"},
        "citations": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {"chunk": {"type": "string"}, "quote": {"type": "string"}},
                "required": ["chunk", "quote"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["answered", "answer", "citations"],
    "additionalProperties": False,
}

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
    stored = dict(db.execute("select id, checksum from chunks"))
    current = {c["id"]: hashlib.sha256(c["text"].encode()).hexdigest() for c in chunks}
    changed = [c for c in chunks if stored.get(c["id"]) != current[c["id"]]]
    removed = set(stored) - set(current)
    for id in removed | {c["id"] for c in changed}:
        db.execute("delete from chunks where id = ?", (id,))
    for chunk, vector in zip(changed, embed([c["text"] for c in changed])):
        db.execute(
            "insert into chunks (id, embedding, document, text, checksum) values (?, ?, ?, ?, ?)",
            (chunk["id"], sqlite_vec.serialize_float32(vector), chunk["document"], chunk["text"], current[chunk["id"]]),
        )
    db.commit()
    return len(changed), len(removed)


def search(db, vector):
    rows = db.execute(
        "select id, text from chunks where embedding match ? and k = ? order by distance",
        (sqlite_vec.serialize_float32(vector), TOP),
    )
    return [{"id": id, "text": text} for id, text in rows]


def answer(question, found):
    documentation = "\n\n".join(f'<chunk id="{c["id"]}">\n{c["text"]}\n</chunk>' for c in found)
    response = client.responses.create(
        model=MODEL,
        reasoning={"effort": "none"},
        instructions=f"{INSTRUCTIONS}\n\n{documentation}",
        input=question,
        text={"format": {"type": "json_schema", "name": "answer", "schema": SCHEMA, "strict": True}},
    )
    return json.loads(response.output_text)


def words(text):
    return " ".join(re.sub(r"[*`|]", " ", text).split()).lower()


def check(citations, found):
    # A quote counts only if it really is in the chunk it cites.
    texts = {c["id"]: words(c["text"]) for c in found}
    return [{**c, "checked": words(c["quote"]) in texts.get(c["chunk"], "")} for c in citations]


def ask(db):
    found = search(db, embed([QUESTION])[0])
    reply = answer(QUESTION, found)
    reply["citations"] = check(reply["citations"], found)
    print(f"Q: {QUESTION}\nA: {reply['answer']}")
    for citation in reply["citations"]:
        mark = "quote checked" if citation["checked"] else "NOT IN THAT CHUNK"
        print(f'   [{citation["chunk"]}] "{citation["quote"]}" ({mark})')
    return reply


def chunks_of(documents):
    return [chunk for document in documents for chunk in split_into_chunks(document)]


db = open_database()
documents = {d["name"]: d for d in load_documents(DATA / "docs")}
update(db, chunks_of(documents.values()))
print("\n=== The knowledge base for firmware 4.1 ===")
before = ask(db)

# Firmware 4.2 ships: a new release note, and a new version of the user guide.
updates = load_documents(DATA / "updates")
documents.update({d["name"]: d for d in updates})
chunks = chunks_of(documents.values())
changed, removed = update(db, chunks)
print(f"\n=== Firmware 4.2: {len(updates)} documents changed ===")
print(f"Re-embedded {changed} of {len(chunks):,} chunks and removed {removed}. No retraining.\n")
after = ask(db)

(OUTPUT / "06_keep_it_current.json").write_text(
    json.dumps({"question": QUESTION, "before": before, "changed": changed, "removed": removed, "after": after}, indent=2)
)
