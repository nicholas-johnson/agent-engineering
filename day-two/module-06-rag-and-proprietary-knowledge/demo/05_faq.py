# Run from the module folder: uv run python demo/05_faq.py

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
DATA = HERE.parent / "data"
OUTPUT = HERE / "output"
OUTPUT.mkdir(exist_ok=True)

DATABASE = OUTPUT / "chroma"
MODEL = "gpt-6-luna"
EMBEDDING_MODEL = "text-embedding-3-small"
BATCH = 100
TOP = 5
STORE_BATCH = 5000  # ChromaDB takes at most 5,461 items in one call
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
            chunks.append({"id": id, "document": document["name"], "audience": document["audience"], "text": f"{heading}\n\n{content}"})

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


def open_collections():
    database = chromadb.PersistentClient(path=str(DATABASE), settings=Settings(anonymized_telemetry=False))
    # Compare by cosine similarity, and use our own embeddings rather than Chroma's built-in model.
    space = {"hnsw": {"space": "cosine"}}
    chunk_store = database.get_or_create_collection("chunks", configuration=space, embedding_function=None)
    # Each chunk's questions, pointing back to the chunk that answers them.
    question_store = database.get_or_create_collection("questions", configuration=space, embedding_function=None)
    return chunk_store, question_store


def update(chunk_store, chunks):
    stored = chunk_store.get(include=["metadatas"])
    stored = dict(zip(stored["ids"], (m["checksum"] for m in stored["metadatas"])))
    current = {c["id"]: checksum(c["text"]) for c in chunks}
    changed = [c for c in chunks if stored.get(c["id"]) != current[c["id"]]]
    removed = set(stored) - set(current)
    if removed:
        chunk_store.delete(ids=list(removed))
    if changed:
        chunk_store.upsert(
            ids=[c["id"] for c in changed],
            embeddings=embed([c["text"] for c in changed]),
            documents=[c["text"] for c in changed],
            metadatas=[{"document": c["document"], "audience": c["audience"], "checksum": current[c["id"]]} for c in changed],
        )


def update_questions(question_store, faq, chunks):
    # Embed the questions for chunks whose text or questions are new or have changed. data/build_faq.py wrote them.
    texts = {c["id"]: c["text"] for c in chunks}
    current = {
        id: checksum(texts[id] + "\n".join(entry["questions"]))
        for id, entry in faq.items()
        if id in texts and checksum(texts[id]) == entry["checksum"]
    }
    stored = question_store.get(include=["metadatas"])
    stale = [id for id, m in zip(stored["ids"], stored["metadatas"]) if current.get(m["chunk"]) != m["checksum"]]
    if stale:
        question_store.delete(ids=stale)
    done = {m["chunk"] for m in stored["metadatas"] if current.get(m["chunk"]) == m["checksum"]}
    todo = [(id, n, question) for id in current if id not in done for n, question in enumerate(faq[id]["questions"])]
    vectors = embed([q for _, _, q in todo])
    for start in range(0, len(todo), STORE_BATCH):
        batch = todo[start : start + STORE_BATCH]
        question_store.upsert(
            ids=[f"{id}?{n}" for id, n, _ in batch],
            embeddings=vectors[start : start + STORE_BATCH],
            documents=[question for _, _, question in batch],
            metadatas=[{"chunk": id, "checksum": current[id]} for id, _, _ in batch],
        )


def search(chunk_store, question_store, vector, by):
    # Search the chunks, their questions, or both, keeping each chunk's best match.
    best = {}
    if by in ("chunks", "both"):
        results = chunk_store.query(query_embeddings=[vector], n_results=TOP, include=["distances"])
        for id, distance in zip(results["ids"][0], results["distances"][0]):
            best[id] = max(best.get(id, (0, None)), (1 - distance, None), key=lambda b: b[0])
    if by in ("questions", "both"):
        results = question_store.query(
            query_embeddings=[vector], n_results=TOP * 4, include=["distances", "documents", "metadatas"]
        )
        for distance, matched, metadata in zip(results["distances"][0], results["documents"][0], results["metadatas"][0]):
            chunk = metadata["chunk"]
            best[chunk] = max(best.get(chunk, (0, None)), (1 - distance, matched), key=lambda b: b[0])
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
chunk_store, question_store = open_collections()
update(chunk_store, chunks)
update_questions(question_store, faq, chunks)
print(f"\n{len(chunks):,} chunks, and {sum(len(e['questions']) for e in faq.values()):,} questions they answer.")

warm_wake = "user-guide.md#warm-wake"
print(f"\nThe questions written for {warm_wake}:")
for question in faq[warm_wake]["questions"]:
    print(f"   {question}")

print(f"\nQ: {QUESTION}")
[question_vector] = embed([QUESTION])
found = search(chunk_store, question_store, question_vector, "both")
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
        top = search(chunk_store, question_store, vector, by)
        hit = any(contains_facts(chunks_by_id[c["id"]]["text"], q["facts"]) for c in top)
        hits += hit
        checks.append({"by": by, "id": q["id"], "question": q["question"], "found": hit, "top": top})
    scores[by] = hits
print(
    f"\nThe answer was in the top {TOP} chunks, for {len(questions)} questions: "
    + ", ".join(f"searching {by} {hits}" for by, hits in scores.items())
)

(OUTPUT / "05_faq.json").write_text(
    json.dumps({"question": QUESTION, "found": found, "answer": reply, "scores": scores, "checks": checks}, indent=2)
)
