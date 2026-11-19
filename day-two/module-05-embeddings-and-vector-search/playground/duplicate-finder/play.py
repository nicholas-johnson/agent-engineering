# Duplicate finder — find pairs of test scripts on the same platform that say almost the same thing.
# Run from the module folder: uv run python playground/duplicate-finder/play.py
#                         or: source ../../.venv/bin/activate && python playground/duplicate-finder/play.py
#
# To play: raise or lower THRESHOLD, show more pairs with SHOW, or compare across platforms
# too (see README.md). Vectors are cached in output/, so reruns are quick.

import json
import math
import sqlite3
import struct
from itertools import combinations
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
THRESHOLD = 0.90  # pairs at least this similar count as possible duplicates
SHOW = 5  # how many of the closest pairs to print

client = OpenAI()


def what_it_tests(script):
    return f"{script['title']}. {script['expected']}"


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


scripts = json.loads((DATA / "test-scripts.json").read_text())
vectors = embed([what_it_tests(s) for s in scripts])

# Compare every script with every other script on the same platform: about 128,000 pairs.
pairs = []
for (a, vector_a), (b, vector_b) in combinations(zip(scripts, vectors), 2):
    if a["platform"] != b["platform"]:
        continue
    similarity = cosine_similarity(vector_a, vector_b)
    if similarity >= THRESHOLD:
        pairs.append((similarity, a, b))
pairs.sort(key=lambda pair: pair[0], reverse=True)

print(f"\n{len(pairs)} pairs of scripts on the same platform are at least {THRESHOLD} similar. The closest:")
for similarity, a, b in pairs[:SHOW]:
    print(f"\n  {similarity:.3f}  {a['platform']}")
    print(f"    {a['id']}  {a['title']}")
    print(f"    {b['id']}  {b['title']}")

(OUTPUT / "duplicates.json").write_text(
    json.dumps(
        [
            {
                "similarity": round(similarity, 4),
                "platform": a["platform"],
                "scripts": [{key: s[key] for key in ["id", "title", "expected"]} for s in [a, b]],
            }
            for similarity, a, b in pairs
        ],
        indent=2,
    )
)
