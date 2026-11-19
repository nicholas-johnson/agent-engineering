# What to embed — embed the library three ways and see where the right script lands.
# Run from the module folder: uv run python playground/what-to-embed/play.py
#                         or: source ../../.venv/bin/activate && python playground/what-to-embed/play.py
#
# To play: add a way of your own to WAYS (the steps alone, or the component plus the title),
# or set FILTER_BY_PLATFORM = True. Vectors are cached in output/, so reruns are quick.

import json
import math
import sqlite3
import struct
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

HERE = Path(__file__).parent
DATA = HERE.parent.parent / "data"
OUTPUT = HERE / "output"
OUTPUT.mkdir(exist_ok=True)

EMBEDDING_MODEL = "text-embedding-3-small"
BATCH = 100
TOP = 5  # a request is a hit if a right script is in the top 5
FILTER_BY_PLATFORM = False  # True searches only the request's platform, as demo 4 does
FIRST = {
    "request": "Customers can't sign in after resetting their password",
    "platform": "android",
    "expected": ["TS-1042"],
}


def full_text(script):
    return " ".join([script["title"], script["preconditions"], *script["steps"], script["expected"]])


def title(script):
    return script["title"]


def title_and_expected(script):
    return f"{script['title']}. {script['expected']}"


# Three ways to turn a script into the text we embed.
WAYS = {"full text": full_text, "title": title, "title + expected": title_and_expected}

client = OpenAI()


def embed(texts):
    # Vectors are kept in output/vectors.db by their text, so a rerun only embeds new text.
    cache = sqlite3.connect(OUTPUT / "vectors.db")
    cache.execute("create table if not exists vectors (text text primary key, vector blob)")
    stored = dict(cache.execute("select text, vector from vectors"))
    missing = list(dict.fromkeys(t for t in texts if t not in stored))
    for start in range(0, len(missing), BATCH):
        batch = missing[start : start + BATCH]
        response = client.embeddings.create(model=EMBEDDING_MODEL, input=batch)
        for text, item in zip(batch, response.data):
            stored[text] = struct.pack(f"{len(item.embedding)}f", *item.embedding)
            cache.execute("insert into vectors values (?, ?)", (text, stored[text]))
        cache.commit()
        print(f"  Embedding: {start + len(batch):,}/{len(missing):,}", end="\r")
    print(" " * 40, end="\r")
    return [struct.unpack(f"{len(stored[t]) // 4}f", stored[t]) for t in texts]


def cosine_similarity(a, b):
    return math.sumprod(a, b) / (math.sqrt(math.sumprod(a, a)) * math.sqrt(math.sumprod(b, b)))


def rank_of_right_script(request, request_vector, vectors):
    similarities = {
        s["id"]: cosine_similarity(request_vector, v)
        for s, v in zip(scripts, vectors)
        if s["platform"] == request["platform"] or not FILTER_BY_PLATFORM
    }
    # 1 + how many scripts are closer than the best right one, so an exact tie counts as a draw.
    best = max(similarities[id] for id in request["expected"])
    rank = 1 + sum(similarity > best for similarity in similarities.values())
    return rank, sorted(similarities, key=similarities.get, reverse=True)[:TOP]


def row(label, values):
    label = label if len(label) <= 50 else label[:47] + "..."
    return f"  {label:<52}" + "".join(f"{value:>18}" for value in values)


scripts = json.loads((DATA / "test-scripts.json").read_text())
requests = json.loads((DATA / "requests.json").read_text())
all_requests = [FIRST, *requests]

request_vectors = embed([r["request"] for r in all_requests])
library = {}
for way, make_text in WAYS.items():
    library[way] = embed([make_text(s) for s in scripts])

results = []
for r, request_vector in zip(all_requests, request_vectors):
    ways = {}
    for way, vectors in library.items():
        rank, top = rank_of_right_script(r, request_vector, vectors)
        ways[way] = {"rank": rank, "top": top}
    results.append({**r, "ways": ways})


hits = {way: sum(r["ways"][way]["rank"] <= TOP for r in results[1:]) for way in WAYS}
searched = "the request's platform" if FILTER_BY_PLATFORM else f"all {len(scripts):,} scripts"
print(f"\nWhere the right script lands (1 = first), searching {searched}:\n")
print(row("Request", WAYS))
for r in results:
    print(row(r["request"], [r["ways"][way]["rank"] for way in WAYS]))
    if r["request"] == FIRST["request"]:
        print()  # the module's request first, then the twenty
print(f"\n{row(f'A right script in the top {TOP}, of {len(requests)}', hits.values())}")

(OUTPUT / "ranks.json").write_text(json.dumps({"hits": hits, "requests": results}, indent=2))
