# Run from the module folder: uv run python demo/04_faq.py

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


def checksum(text):
    return hashlib.sha256(text.encode()).hexdigest()


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
    # Each chunk's questions, pointing back to the chunk that answers them.
    db.execute(
        "create virtual table if not exists questions using vec0("
        "id text primary key, embedding float[1536] distance_metric=cosine,"
        "+chunk text, +question text, +checksum text)"
    )
    return db


def update(db, chunks):
    stored = dict(db.execute("select id, checksum from chunks"))
    current = {c["id"]: checksum(c["text"]) for c in chunks}
    changed = [c for c in chunks if stored.get(c["id"]) != current[c["id"]]]
    for id in (set(stored) - set(current)) | {c["id"] for c in changed}:
        db.execute("delete from chunks where id = ?", (id,))
    for chunk, vector in zip(changed, embed([c["text"] for c in changed])):
        db.execute(
            "insert into chunks (id, embedding, document, text, checksum) values (?, ?, ?, ?, ?)",
            (chunk["id"], sqlite_vec.serialize_float32(vector), chunk["document"], chunk["text"], current[chunk["id"]]),
        )
    db.commit()


def update_questions(db, faq, chunks):
    # Embed the questions for chunks that are new or have changed. data/build_faq.py wrote them.
    current = {c["id"]: checksum(c["text"]) for c in chunks}
    stored = list(db.execute("select id, chunk, checksum from questions"))
    for id, chunk, written_for in stored:
        if current.get(chunk) != written_for:
            db.execute("delete from questions where id = ?", (id,))
    done = {chunk for _, chunk, written_for in stored if current.get(chunk) == written_for}
    todo = [
        (id, n, question)
        for id, entry in faq.items()
        if id not in done and current.get(id) == entry["checksum"]
        for n, question in enumerate(entry["questions"])
    ]
    for (id, n, question), vector in zip(todo, embed([q for _, _, q in todo])):
        db.execute(
            "insert into questions (id, embedding, chunk, question, checksum) values (?, ?, ?, ?, ?)",
            (f"{id}?{n}", sqlite_vec.serialize_float32(vector), id, question, current[id]),
        )
    db.commit()


def search(db, vector, by):
    # Search the chunks, their questions, or both, keeping each chunk's best match.
    best = {}
    if by in ("chunks", "both"):
        for id, similarity in db.execute(
            "select id, 1 - distance from chunks where embedding match ? and k = ?",
            (sqlite_vec.serialize_float32(vector), TOP),
        ):
            best[id] = max(best.get(id, (0, None)), (similarity, None), key=lambda b: b[0])
    if by in ("questions", "both"):
        for chunk, similarity, matched in db.execute(
            "select chunk, 1 - distance, question from questions where embedding match ? and k = ?",
            (sqlite_vec.serialize_float32(vector), TOP * 4),
        ):
            best[chunk] = max(best.get(chunk, (0, None)), (similarity, matched), key=lambda b: b[0])
    ranked = sorted(best.items(), key=lambda item: item[1][0], reverse=True)[:TOP]
    return [{"id": id, "similarity": round(sim, 3), "matched_question": matched} for id, (sim, matched) in ranked]


def answer(question, found, chunks_by_id):
    documentation = "\n\n".join(f'<chunk id="{c["id"]}">\n{chunks_by_id[c["id"]]["text"]}\n</chunk>' for c in found)
    response = client.responses.create(
        model=MODEL,
        reasoning={"effort": "none"},
        instructions=f"{INSTRUCTIONS}\n\nUse our documentation:\n\n{documentation}",
        input=question,
    )
    return response.output_text


def plain(text):
    text = text.lower().replace("→", ">").replace("->", ">").replace("°c", " degrees")
    return re.sub(r"\s*>\s*", ">", re.sub(r"\s+", " ", text))


def contains_facts(text, facts):
    return all(any(re.search(rf"\b{re.escape(plain(option))}\b", plain(text)) for option in fact.split("|")) for fact in facts)


documents = load_documents(DATA / "docs")
chunks = [chunk for document in documents for chunk in split_into_chunks(document)]
chunks_by_id = {c["id"]: c for c in chunks}
faq = json.loads((DATA / "faq.json").read_text())
db = open_database()
update(db, chunks)
update_questions(db, faq, chunks)
print(f"\n{len(chunks):,} chunks, and {sum(len(e['questions']) for e in faq.values()):,} questions they answer.")

warm_wake = "user-guide.md#warm-wake"
print(f"\nThe questions written for {warm_wake}:")
for question in faq[warm_wake]["questions"]:
    print(f"   {question}")

print(f"\nQ: {QUESTION}")
[question_vector] = embed([QUESTION])
found = search(db, question_vector, "both")
for chunk in found:
    via = f'  via "{chunk["matched_question"]}"' if chunk["matched_question"] else ""
    print(f"   {chunk['similarity']:.3f}  {chunk['id']}{via}")
reply = answer(QUESTION, found, chunks_by_id)
print(f"A: {reply}")

questions = [q for q in json.loads((DATA / "questions.json").read_text()) if q["kind"] in ("everyday", "error code")]
vectors = embed([q["question"] for q in questions])
scores, checks = {}, []
for by in ("chunks", "questions", "both"):
    hits = 0
    for q, vector in zip(questions, vectors):
        top = search(db, vector, by)
        hit = any(contains_facts(chunks_by_id[c["id"]]["text"], q["facts"]) for c in top)
        hits += hit
        checks.append({"by": by, "id": q["id"], "question": q["question"], "found": hit, "top": top})
    scores[by] = hits
print(
    f"\nThe answer was in the top {TOP} chunks, for {len(questions)} questions: "
    + ", ".join(f"searching {by} {hits}" for by, hits in scores.items())
)

(OUTPUT / "04_faq.json").write_text(
    json.dumps({"question": QUESTION, "found": found, "answer": reply, "scores": scores, "checks": checks}, indent=2)
)
