# Run from the module folder: uv run python demo/07_docs_server.py
# You don't need to run it yourself: demo/07_agent.py starts it.

import hashlib
import json
import re
import sqlite3
from pathlib import Path

import sqlite_vec
from dotenv import load_dotenv
from mcp.server.mcpserver import MCPServer
from openai import OpenAI

load_dotenv()

HERE = Path(__file__).parent
DATA = HERE.parent / "data"
OUTPUT = HERE / "output"
OUTPUT.mkdir(exist_ok=True)

DATABASE = OUTPUT / "knowledge.db"
EMBEDDING_MODEL = "text-embedding-3-small"
BATCH = 100
TOP = 5

# Log warnings only, so every search isn't reported on the agent's terminal.
server = MCPServer("dormouse-docs", log_level="WARNING")


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
    # No progress line here: a server's stdout carries its messages to the agent.
    client = OpenAI()
    vectors = []
    for start in range(0, len(texts), BATCH):
        response = client.embeddings.create(model=EMBEDDING_MODEL, input=texts[start : start + BATCH])
        vectors += [item.embedding for item in response.data]
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


@server.tool()
def search_docs(query: str) -> str:
    """Search Dormouse's documentation by meaning: the user guide, and support, troubleshooting,
    installation, specification, policy, error-code and release-note articles. Describe what to
    look for in `query`, in the words the documentation would use. Returns the five closest
    sections as JSON, closest first, each with an id to cite and its text."""
    db = open_database()
    # Always the documents as they are now: only new or changed chunks are embedded.
    update(db, [chunk for document in load_documents(DATA / "docs") for chunk in split_into_chunks(document)])
    [vector] = embed([query])
    rows = db.execute(
        "select id, 1 - distance, text from chunks where embedding match ? and k = ? order by distance",
        (sqlite_vec.serialize_float32(vector), TOP),
    )
    return json.dumps([{"id": id, "similarity": round(similarity, 3), "text": text} for id, similarity, text in rows])


server.run()
