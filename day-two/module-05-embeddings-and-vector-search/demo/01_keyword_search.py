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


def bm25(question, documents):
    texts = [words(d["text"]) for d in documents]
    average_length = sum(len(t) for t in texts) / len(texts)
    # How many documents each word appears in: rare words count for more.
    appears_in = Counter(w for t in texts for w in set(t))

    results = []
    for document, text in zip(documents, texts):
        counts = Counter(text)
        score = 0
        for word in set(words(question)):
            if word not in counts:
                continue
            rarity = math.log(1 + (len(texts) - appears_in[word] + 0.5) / (appears_in[word] + 0.5))
            count = counts[word]
            score += rarity * count * (K1 + 1) / (count + K1 * (1 - B + B * len(text) / average_length))
        results.append((score, document))
    return sorted(results, key=lambda r: r[0], reverse=True)


documents = read_documents()
libraries = {"The user guide": user_guide_sections(documents), "All the documentation": documents}

found = {}
for name, library in libraries.items():
    results = bm25(QUESTION, library)
    print(f"\n=== {name}: {len(library):,} {'sections' if library[0]['id'] == 'user-guide' else 'documents'} ===")
    print(f"Q: {QUESTION}")
    for score, document in results[:3]:
        print(f"  {score:5.2f}  {document['title']}")
    found[name] = [{"score": round(s, 3), "id": d["id"], "title": d["title"]} for s, d in results]

(OUTPUT / "01_keyword_search.json").write_text(json.dumps({"question": QUESTION, "found": found}, indent=2))
