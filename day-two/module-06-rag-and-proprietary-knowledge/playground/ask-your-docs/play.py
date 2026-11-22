# Ask your docs — chat with the Dormouse knowledge base, and check every quote the answer relies on.
# Run from the module folder: uv run python playground/ask-your-docs/play.py
#                         or: source ../../.venv/bin/activate && python playground/ask-your-docs/play.py
#
# To play: ask your own questions (an empty line stops), or point DOCS at a folder of your own Markdown.
# Vectors are kept in a ChromaDB store in output/chroma, so only new or changed chunks are embedded.

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
DOCS = HERE.parent.parent / "data" / "docs"  # any folder of Markdown files will do
OUTPUT = HERE / "output"
OUTPUT.mkdir(exist_ok=True)

DATABASE = OUTPUT / "chroma"
MODEL = "gpt-6-luna"
EMBEDDING_MODEL = "text-embedding-3-small"
BATCH = 100
UPSERT = 5000  # Chroma stores at most about 5,000 chunks in one call
TOP = 5  # chunks the model is given for each question

# Demo 5's instructions. Change the first line if you point DOCS at your own documents.
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
    # Front matter is optional, so any Markdown will do. Without a title, the file name stands in.
    documents = []
    for path in sorted(folder.rglob("*.md")):
        text = path.read_text()
        fields = {"title": path.stem.replace("-", " ")}
        if text.startswith("---"):
            _, front, text = text.split("---", 2)
            fields.update(line.split(": ", 1) for line in front.strip().splitlines() if ": " in line)
        documents.append({"name": path.relative_to(folder).as_posix(), **fields, "body": text})
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
    # Embed new and changed chunks, and remove chunks that are no longer in DOCS.
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
            metadatas=[{"document": c["document"], "checksum": checksums[c["id"]]} for c in batch],
        )


def search(collection, question):
    [vector] = embed([question])
    results = collection.query(query_embeddings=[vector], n_results=TOP, include=["distances", "documents"])
    return [
        {"id": id, "similarity": round(1 - distance, 3), "text": text}
        for id, distance, text in zip(results["ids"][0], results["distances"][0], results["documents"][0])
    ]


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


documents = load_documents(DOCS)
chunks = [chunk for document in documents for chunk in split_into_chunks(document)]
collection = open_collection()
update(collection, chunks)
print(f"{len(documents):,} documents, {len(chunks):,} chunks. Ask a question; an empty line stops.\n")

transcript = []
while True:
    question = input("You: ")
    if not question:
        break

    found = search(collection, question)
    reply = answer(question, found)
    reply["citations"] = check(reply["citations"], found)

    print(f"Dormouse: {reply['answer']}")
    for citation in reply["citations"]:
        mark = "quote checked" if citation["checked"] else "NOT IN THAT CHUNK"
        print(f'   [{citation["chunk"]}] "{citation["quote"]}" ({mark})')
    if not reply["answered"]:
        print("   (answered: false)")
    print("   Searched:")
    for chunk in found:
        print(f"     {chunk['similarity']:.3f}  {chunk['id']}")
    print()

    chunks_found = [{"id": c["id"], "similarity": c["similarity"]} for c in found]
    transcript.append({"question": question, **reply, "chunks": chunks_found})
    (OUTPUT / "transcript.json").write_text(json.dumps(transcript, indent=2, ensure_ascii=False))
