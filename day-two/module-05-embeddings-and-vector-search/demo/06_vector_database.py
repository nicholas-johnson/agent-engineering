# Run from the module folder: uv run python demo/06_vector_database.py

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
DOCS = HERE.parent / "data" / "docs"
OUTPUT = HERE / "output"
OUTPUT.mkdir(exist_ok=True)

DATABASE = OUTPUT / "chroma"
EMBEDDING_MODEL = "text-embedding-3-small"
BATCH = 100
QUESTION = "Why is the heating already on before my alarm goes off?"
CLICK_QUESTION = "My thermostat makes a clicking noise"
CUSTOMERS = {"audience": "customer"}

client = OpenAI()


def read_documents():
    documents = []
    for path in sorted(DOCS.glob("*.md")):
        _, header, text = path.read_text().split("---", 2)
        fields = dict(re.findall(r"^(\w+): (.+)$", header, re.MULTILINE))
        documents.append({"id": path.stem, "text": text.strip(), **fields})
    return documents


def embed(texts):
    vectors = []
    for start in range(0, len(texts), BATCH):
        response = client.embeddings.create(model=EMBEDDING_MODEL, input=texts[start : start + BATCH])
        vectors += [item.embedding for item in response.data]
        print(f"  Embedding: {len(vectors):,}/{len(texts):,}", end="\r")
    print(" " * 40, end="\r")
    return vectors


def update(collection, documents):
    # Only embed documents that are new or have changed since the last run.
    stored = collection.get(include=["metadatas"])
    checksums = dict(zip(stored["ids"], (m["checksum"] for m in stored["metadatas"])))
    changed = [d for d in documents if checksums.get(d["id"]) != hashlib.sha256(d["text"].encode()).hexdigest()]
    if changed:
        collection.upsert(
            ids=[d["id"] for d in changed],
            embeddings=embed([d["text"] for d in changed]),
            documents=[d["text"] for d in changed],
            metadatas=[
                {
                    "title": d["title"],
                    "type": d["type"],
                    "audience": d["audience"],
                    "checksum": hashlib.sha256(d["text"].encode()).hexdigest(),
                }
                for d in changed
            ],
        )
    return len(changed)


def search(collection, question, where=None):
    [vector] = embed([question])
    results = collection.query(query_embeddings=[vector], n_results=3, where=where, include=["distances", "metadatas"])
    return [
        {"id": id, "similarity": round(1 - distance, 4), **metadata}
        for id, distance, metadata in zip(results["ids"][0], results["distances"][0], results["metadatas"][0])
    ]


def show(found):
    for document in found:
        print(f"  {document['similarity']:.3f}  {document['audience']:<8}  {document['title']}")


database = chromadb.PersistentClient(path=str(DATABASE), settings=Settings(anonymized_telemetry=False))
# Compare by cosine similarity, and use our own embeddings rather than Chroma's built-in model.
collection = database.get_or_create_collection(
    "dormouse-docs", configuration={"hnsw": {"space": "cosine"}}, embedding_function=None
)
documents = read_documents()
print(f"\nStored {update(collection, documents):,} new or changed documents in {DATABASE.name}/")

searches = [
    (QUESTION, "customers only", CUSTOMERS),
    (CLICK_QUESTION, "every document", None),
    (CLICK_QUESTION, "customers only", CUSTOMERS),
]
found = []
for question, label, where in searches:
    print(f"\nQ: {question}  ({label})")
    results = search(collection, question, where)
    show(results)
    found.append({"question": question, "where": where, "found": results})

(OUTPUT / "06_vector_database.json").write_text(json.dumps(found, indent=2))
