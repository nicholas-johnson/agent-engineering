# Run from the module folder: uv run python demo/01_keyword_search.py

import json
import math
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
DOCS = HERE.parent / "data" / "docs"
OUTPUT = HERE / "output"
OUTPUT.mkdir(exist_ok=True)

QUESTION = "Why is the heating already on before my alarm goes off?"
K1 = 1.5
B = 0.75


def read_documents():
    documents = []
    for path in sorted(DOCS.glob("*.md")):
        _, header, text = path.read_text().split("---", 2)
        title = re.search(r"^title: (.+)$", header, re.MULTILINE)[1]
        documents.append({"id": path.stem, "title": title, "text": text.strip()})
    return documents


def user_guide_sections(documents):
    # The small library: the user guide, one entry per section that has text of its own.
    guide = next(d for d in documents if d["id"] == "user-guide")["text"]
    sections = []
    for part in re.split(r"\n(?=#{2,3} )", guide)[1:]:
        title, _, body = part.partition("\n")
        if body.strip():
            sections.append({"id": "user-guide", "title": title.lstrip("# "), "text": part})
    return sections


def words(text):
    return re.findall(r"[a-z0-9]+", text.lower())


def build_index(documents):
    # Ahead of time: each word → {document number: how many times}, and each document's length.
    index = {}
    lengths = []
    for number, document in enumerate(documents):
        text = words(document["text"])
        lengths.append(len(text))
        for word, count in Counter(text).items():
            index.setdefault(word, {})[number] = count
    return index, lengths


def search(question, documents, index, lengths):
    # For each question: score only the documents listed under the question's words.
    average_length = sum(lengths) / len(lengths)
    scores = Counter()
    for word in set(words(question)):
        entry = index.get(word, {})
        # len(entry) is how many documents contain the word: rare words count for more.
        rarity = math.log(1 + (len(documents) - len(entry) + 0.5) / (len(entry) + 0.5))
        for number, count in entry.items():
            scores[number] += rarity * count * (K1 + 1) / (count + K1 * (1 - B + B * lengths[number] / average_length))
    return [(score, documents[number]) for number, score in scores.most_common()]


documents = read_documents()
libraries = {"The user guide": user_guide_sections(documents), "All the documentation": documents}

found = {}
for name, library in libraries.items():
    index, lengths = build_index(library)
    results = search(QUESTION, library, index, lengths)
    print(f"\n=== {name}: {len(library):,} {'sections' if library[0]['id'] == 'user-guide' else 'documents'} ===")
    print(f"Q: {QUESTION}")
    for score, document in results[:3]:
        print(f"  {score:5.2f}  {document['title']}")
    found[name] = [{"score": round(s, 3), "id": d["id"], "title": d["title"]} for s, d in results]

(OUTPUT / "01_keyword_search.json").write_text(json.dumps({"question": QUESTION, "found": found}, indent=2))

# The last index built is the one for all 275 documents. Save it, most mentions first.
readable = {
    word: {documents[number]["id"]: count for number, count in sorted(entry.items(), key=lambda e: -e[1])}
    for word, entry in sorted(index.items())
}
(OUTPUT / "01_index.json").write_text(json.dumps(readable, indent=2))
