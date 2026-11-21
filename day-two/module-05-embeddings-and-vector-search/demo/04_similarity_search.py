# Run from the module folder: uv run python demo/04_similarity_search.py

import json
import math
import re
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

HERE = Path(__file__).parent
DOCS = HERE.parent / "data" / "docs"
OUTPUT = HERE / "output"
OUTPUT.mkdir(exist_ok=True)

EMBEDDING_MODEL = "text-embedding-3-small"
BATCH = 100
QUESTION = "Why is the heating already on before my alarm goes off?"

client = OpenAI()


def read_documents():
    documents = []
    for path in sorted(DOCS.glob("*.md")):
        _, header, text = path.read_text().split("---", 2)
        title = re.search(r"^title: (.+)$", header, re.MULTILINE)[1]
        audience = re.search(r"^audience: (.+)$", header, re.MULTILINE)[1]
        documents.append({"id": path.stem, "title": title, "audience": audience, "text": text.strip()})
    return documents


def user_guide_sections(documents):
    # The small library: the user guide, one entry per section that has text of its own.
    guide = next(d for d in documents if d["id"] == "user-guide")
    sections = []
    for part in re.split(r"\n(?=#{2,3} )", guide["text"])[1:]:
        title, _, body = part.partition("\n")
        if body.strip():
            sections.append({"id": "user-guide", "title": title.lstrip("# "), "audience": guide["audience"], "text": part})
    return sections


def embed(texts):
    vectors = []
    for start in range(0, len(texts), BATCH):
        response = client.embeddings.create(model=EMBEDDING_MODEL, input=texts[start : start + BATCH])
        vectors += [item.embedding for item in response.data]
        print(f"  Embedding: {len(vectors):,}/{len(texts):,}", end="\r")
    print(" " * 40, end="\r")
    return vectors


def cosine_similarity(a, b):
    # 1 when two vectors point the same way, 0 when they have nothing in common.
    dot = sum(x * y for x, y in zip(a, b))
    length_a = math.sqrt(sum(x * x for x in a))
    length_b = math.sqrt(sum(y * y for y in b))
    return dot / (length_a * length_b)


documents = read_documents()
libraries = {"The user guide": user_guide_sections(documents), "All the documentation": documents}
[question_vector] = embed([QUESTION])

found = {}
for name, library in libraries.items():
    print(f"\n=== {name}: {len(library):,} {'sections' if library[0]['id'] == 'user-guide' else 'documents'} ===")
    print(f"Q: {QUESTION}")
    vectors = embed([d["text"] for d in library])
    results = sorted(
        ((cosine_similarity(question_vector, v), d) for v, d in zip(vectors, library)),
        key=lambda r: r[0],
        reverse=True,
    )
    for similarity, document in results[:3]:
        print(f"  {similarity:.3f}  {document['audience']:<8}  {document['title']}")
    found[name] = [
        {"similarity": round(s, 4), "id": d["id"], "audience": d["audience"], "title": d["title"]} for s, d in results
    ]

(OUTPUT / "04_similarity_search.json").write_text(json.dumps({"question": QUESTION, "found": found}, indent=2))
