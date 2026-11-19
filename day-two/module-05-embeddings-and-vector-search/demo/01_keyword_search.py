# Run from the module folder: uv run python demo/01_keyword_search.py

import json
import math
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
DATA = HERE.parent / "data"
OUTPUT = HERE / "output"
OUTPUT.mkdir(exist_ok=True)

LIBRARIES = ["test-scripts-small.json", "test-scripts.json"]
REQUEST = "Customers can't sign in after resetting their password"
K1 = 1.5
B = 0.75


def script_text(script):
    return " ".join([script["title"], script["preconditions"], *script["steps"], script["expected"]])


def words(text):
    return re.findall(r"[a-z0-9]+", text.lower())


def bm25(request, scripts):
    documents = [words(script_text(s)) for s in scripts]
    average_length = sum(len(d) for d in documents) / len(documents)
    # How many scripts each word appears in: rare words count for more.
    appears_in = Counter(w for d in documents for w in set(d))

    results = []
    for script, document in zip(scripts, documents):
        counts = Counter(document)
        score = 0
        for word in set(words(request)):
            if word not in counts:
                continue
            rarity = math.log(1 + (len(documents) - appears_in[word] + 0.5) / (appears_in[word] + 0.5))
            count = counts[word]
            score += rarity * count * (K1 + 1) / (count + K1 * (1 - B + B * len(document) / average_length))
        results.append((score, script))
    return sorted(results, key=lambda r: r[0], reverse=True)


found = {}
for library in LIBRARIES:
    scripts = json.loads((DATA / library).read_text())
    results = bm25(REQUEST, scripts)

    print(f"\n=== {library}: {len(scripts):,} test scripts ===")
    print(f"Request: {REQUEST}")
    for score, script in results[:3]:
        print(f"  {score:5.2f}  {script['id']}  {script['platform']:<8} {script['title']}")

    found[library] = [
        {"score": round(score, 3), "id": s["id"], "platform": s["platform"], "title": s["title"]}
        for score, s in results[:10]
    ]

(OUTPUT / "01_keyword_search.json").write_text(json.dumps({"request": REQUEST, "found": found}, indent=2))
