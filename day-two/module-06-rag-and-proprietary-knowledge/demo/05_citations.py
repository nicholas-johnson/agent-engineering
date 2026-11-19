# Run from the module folder: uv run python demo/05_citations.py

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
QUESTIONS = [
    "Why does my Dormouse turn the heating on before the time I set?",
    "How much does a Dormouse thermostat cost?",
]

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
    for id in (set(stored) - set(current)) | {c["id"] for c in changed}:
        db.execute("delete from chunks where id = ?", (id,))
    for chunk, vector in zip(changed, embed([c["text"] for c in changed])):
        db.execute(
            "insert into chunks (id, embedding, document, text, checksum) values (?, ?, ?, ?, ?)",
            (chunk["id"], sqlite_vec.serialize_float32(vector), chunk["document"], chunk["text"], current[chunk["id"]]),
        )
    db.commit()


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


def plain(text):
    text = text.lower().replace("→", ">").replace("->", ">").replace("°c", " degrees")
    return re.sub(r"\s*>\s*", ">", re.sub(r"\s+", " ", text))


def contains_facts(text, facts):
    return all(any(re.search(rf"\b{re.escape(plain(option))}\b", plain(text)) for option in fact.split("|")) for fact in facts)


documents = load_documents(DATA / "docs")
db = open_database()
update(db, [chunk for document in documents for chunk in split_into_chunks(document)])

shown = []
for question, vector in zip(QUESTIONS, embed(QUESTIONS)):
    found = search(db, vector)
    reply = answer(question, found)
    reply["citations"] = check(reply["citations"], found)
    print(f"\nQ: {question}\nA: {reply['answer']}")
    for citation in reply["citations"]:
        mark = "quote checked" if citation["checked"] else "NOT IN THAT CHUNK"
        print(f'   [{citation["chunk"]}] "{citation["quote"]}" ({mark})')
    shown.append({"question": question, **reply})

# Every question in the set: right, refused, or wrong?
tally = {"answered right": 0, "answered wrong": 0, "said it didn't know": 0}
refused = quoted = checked = 0
results = []
questions = json.loads((DATA / "questions.json").read_text())
for n, (q, vector) in enumerate(zip(questions, embed([q["question"] for q in questions])), 1):
    print(f"  Asking {n}/{len(questions)}", end="\r")
    found = search(db, vector)
    reply = answer(q["question"], found)
    reply["citations"] = check(reply["citations"], found)
    quoted += len(reply["citations"])
    checked += sum(c["checked"] for c in reply["citations"])
    if q["kind"] in ("everyday", "error code"):
        if not reply["answered"]:
            outcome = "said it didn't know"
        elif contains_facts(reply["answer"], q["facts"]):
            outcome = "answered right"
        else:
            outcome = "answered wrong"
        tally[outcome] += 1
    elif q["kind"] == "not covered":
        outcome = "said it didn't know" if not reply["answered"] else "made something up"
        refused += not reply["answered"]
    else:
        outcome = "quoted an internal document" if contains_facts(reply["answer"], q["facts"]) else "kept it internal"
    results.append({"id": q["id"], "kind": q["kind"], "question": q["question"], "outcome": outcome, **reply})
print(" " * 40, end="\r")

answerable = sum(tally.values())
covered = sum(q["kind"] == "not covered" for q in questions)
print(f"\nOf {answerable} questions the documentation answers: " + ", ".join(f"{k} {v}" for k, v in tally.items()))
print(f"Of {covered} questions it doesn't: said it didn't know {refused}")
print(f"Quotes found in the chunk they cite: {checked} of {quoted}")

(OUTPUT / "05_citations.json").write_text(
    json.dumps({"shown": shown, "tally": tally, "refused": refused, "quotes": [checked, quoted], "results": results}, indent=2)
)
