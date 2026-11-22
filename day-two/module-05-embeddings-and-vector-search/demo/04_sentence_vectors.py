# Run from the module folder: uv run python demo/04_sentence_vectors.py

import json
import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
DOCS = HERE.parent / "data" / "docs"
OUTPUT = HERE / "output"
OUTPUT.mkdir(exist_ok=True)

WORD_MAP = OUTPUT / "03_word_map.json"
QUESTION = "Why is the heating already on before my alarm goes off?"
PAIRS = [
    ("Warm Wake starts the heating early", "Frost protection turns the heating on"),
    ("Warm Wake starts the heating early", "Reset your password by email"),
    ("The heating is off and frost protection is on", "The heating is on and frost protection is off"),
]


def words(text):
    return re.findall(r"[a-z0-9]+", text.lower())


def sentence_vector(text, word_vectors):
    # Add up the vectors of the words the model knows. A word it has never seen adds nothing.
    known = [word_vectors[w] for w in words(text) if w in word_vectors]
    return [sum(column) for column in zip(*known)]


def cosine_similarity(a, b):
    # 1 when two vectors point the same way, 0 when they have nothing in common.
    dot = sum(x * y for x, y in zip(a, b))
    length_a = math.sqrt(sum(x * x for x in a))
    length_b = math.sqrt(sum(y * y for y in b))
    return dot / (length_a * length_b)


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


if not WORD_MAP.exists():
    sys.exit("Run demo/03_word_map.py first: this demo adds up the two numbers it gives each word.")
# Every word's two numbers, from demo 3's map of all 235 words.
word_vectors = {w: [p["x"], p["y"]] for w, p in json.loads(WORD_MAP.read_text())["all"].items()}

written = {"pairs": [], "question": {}, "libraries": {}}

print("\n=== Two sentences at a time ===")
for a, b in PAIRS:
    similarity = cosine_similarity(sentence_vector(a, word_vectors), sentence_vector(b, word_vectors))
    print(f"  {similarity:6.3f}  {a}\n          {b}")
    written["pairs"].append({"a": a, "b": b, "similarity": round(similarity, 4)})

question_vector = sentence_vector(QUESTION, word_vectors)
written["question"] = {
    "text": QUESTION,
    "left_out": [w for w in words(QUESTION) if w not in word_vectors],
    "vector": question_vector,
}

documents = read_documents()
libraries = {"The user guide": user_guide_sections(documents), "All the documentation": documents}
for name, library in libraries.items():
    print(f"\n=== {name}: {len(library):,} {'sections' if library[0]['id'] == 'user-guide' else 'documents'} ===")
    print(f"Q: {QUESTION}")
    results = sorted(
        ((cosine_similarity(question_vector, sentence_vector(d["text"], word_vectors)), d) for d in library),
        key=lambda r: r[0],
        reverse=True,
    )
    for similarity, document in results[:3]:
        print(f"  {similarity:.3f}  {document['audience']:<8}  {document['title']}")
    written["libraries"][name] = [
        {"rank": rank, "similarity": round(similarity, 4), "id": d["id"], "title": d["title"]}
        for rank, (similarity, d) in enumerate(results, start=1)
    ]

(OUTPUT / "04_sentence_vectors.json").write_text(json.dumps(written, indent=2))
