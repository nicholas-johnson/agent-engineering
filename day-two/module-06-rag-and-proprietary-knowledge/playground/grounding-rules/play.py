# Grounding rules — the same chunks, three sets of instructions. Which one stops the model making things up?
# Run from the module folder: uv run python playground/grounding-rules/play.py
#                         or: source ../../.venv/bin/activate && python playground/grounding-rules/play.py
#
# To play: reword the RULES, or add a fourth, and rerun. Answers vary from run to run, so run it twice.
# Vectors are kept in a ChromaDB store in output/chroma, so after the first run only the questions are embedded.

import hashlib
import json
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
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
TOP = 5
INSTRUCTIONS = "You are the support assistant for Dormouse, a smart thermostat. Answer the customer in a short paragraph."

# What comes between INSTRUCTIONS and the chunks. "plain" is demo 3's.
RULES = {
    "plain": "Use our documentation:",
    "only the docs": "Use only the documentation below, never what you know from elsewhere.",
    "only, and say so": "Use only the documentation below, never what you know from elsewhere.\n"
    "If the documentation does not answer the question, say so. Do not guess.",
}

# A second model call reads each reply and says whether it answered the question.
JUDGE = """You read a support assistant's reply to a customer's question.
Say true if the reply gives the customer the information they asked for, even if it is hedged or a guess.
Say false if it says it doesn't know, or that the information isn't available, even if it then suggests where to look."""

JUDGE_SCHEMA = {
    "type": "object",
    "properties": {"gave_an_answer": {"type": "boolean"}},
    "required": ["gave_an_answer"],
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
    stored = collection.get(include=["metadatas"])
    stored = dict(zip(stored["ids"], (m["checksum"] for m in stored["metadatas"])))
    checksums = {c["id"]: hashlib.sha256(c["text"].encode()).hexdigest() for c in chunks}
    changed = [c for c in chunks if stored.get(c["id"]) != checksums[c["id"]]]
    removed = set(stored) - set(checksums)

    if removed:
        collection.delete(ids=list(removed))
    if changed:
        collection.upsert(
            ids=[c["id"] for c in changed],
            embeddings=embed([c["text"] for c in changed]),
            documents=[c["text"] for c in changed],
            metadatas=[{"document": c["document"], "checksum": checksums[c["id"]]} for c in changed],
        )


def search(collection, vector):
    results = collection.query(query_embeddings=[vector], n_results=TOP, include=["documents"])
    return [{"id": id, "text": text} for id, text in zip(results["ids"][0], results["documents"][0])]


def answer(question, found, rule):
    documentation = "\n\n".join(f'<chunk id="{c["id"]}">\n{c["text"]}\n</chunk>' for c in found)
    response = client.responses.create(
        model=MODEL,
        reasoning={"effort": "none"},
        instructions=f"{INSTRUCTIONS}\n\n{RULES[rule]}\n\n{documentation}",
        input=question,
    )
    return response.output_text


def gave_an_answer(question, reply):
    response = client.responses.create(
        model=MODEL,
        reasoning={"effort": "none"},
        instructions=JUDGE,
        input=f"Question: {question}\n\nReply: {reply}",
        text={"format": {"type": "json_schema", "name": "judgement", "schema": JUDGE_SCHEMA, "strict": True}},
    )
    return json.loads(response.output_text)["gave_an_answer"]


def plain(text):
    text = text.lower().replace("→", ">").replace("->", ">").replace("°c", " degrees")
    return re.sub(r"\s*>\s*", ">", re.sub(r"\s+", " ", text))


def contains_facts(text, facts):
    return all(any(re.search(rf"\b{re.escape(plain(option))}\b", plain(text)) for option in fact.split("|")) for fact in facts)


def run(rule, q, found):
    reply = answer(q["question"], found, rule)
    answered = gave_an_answer(q["question"], reply)
    if q["kind"] == "not covered":
        outcome = "made something up" if answered else "said it didn't know"
    elif not answered:
        outcome = "said it didn't know"
    else:
        outcome = "answered right" if contains_facts(reply, q["facts"]) else "answered wrong"
    return {"rule": rule, "id": q["id"], "kind": q["kind"], "question": q["question"], "outcome": outcome, "reply": reply}


documents = load_documents(DATA / "docs")
collection = open_collection()
update(collection, [chunk for document in documents for chunk in split_into_chunks(document)])

# The 24 questions the documentation answers, and the 5 it doesn't. Every rule gets the same chunks.
questions = [q for q in json.loads((DATA / "questions.json").read_text()) if q["kind"] != "internal"]
found = [search(collection, vector) for vector in embed([q["question"] for q in questions])]

results = []
with ThreadPoolExecutor(max_workers=8) as pool:
    jobs = [pool.submit(run, rule, q, top) for rule in RULES for q, top in zip(questions, found)]
    for job in as_completed(jobs):
        results.append(job.result())
        print(f"  Asking and judging: {len(results)}/{len(jobs)}", end="\r")
print(" " * 50, end="\r")
results.sort(key=lambda r: (list(RULES).index(r["rule"]), r["id"]))


def count(rule, covered, outcome):
    return sum(r["rule"] == rule and (r["kind"] != "not covered") == covered and r["outcome"] == outcome for r in results)


answerable = sum(q["kind"] != "not covered" for q in questions)
print(f"\n  {'':<26}" + "".join(f"{rule:>18}" for rule in RULES))
print(f"  Of the {answerable} the documentation answers:")
for outcome in ("answered right", "answered wrong", "said it didn't know"):
    print(f"    {outcome:<24}" + "".join(f"{count(rule, True, outcome):>18}" for rule in RULES))
print(f"  Of the {len(questions) - answerable} it doesn't:")
for outcome in ("made something up", "said it didn't know"):
    print(f"    {outcome:<24}" + "".join(f"{count(rule, False, outcome):>18}" for rule in RULES))

(OUTPUT / "results.json").write_text(json.dumps({"rules": RULES, "results": results}, indent=2, ensure_ascii=False))
