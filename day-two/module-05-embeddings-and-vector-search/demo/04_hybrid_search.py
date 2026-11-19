# Run from the module folder: uv run python demo/04_hybrid_search.py

import hashlib
import json
import re
import sqlite3
from collections import Counter
from pathlib import Path

import sqlite_vec
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

HERE = Path(__file__).parent
DATA = HERE.parent / "data"
OUTPUT = HERE / "output"
OUTPUT.mkdir(exist_ok=True)

DATABASE = OUTPUT / "test-scripts.db"
EMBEDDING_MODEL = "text-embedding-3-small"
BATCH = 100
CANDIDATES = 20
RRF_K = 60
TOP = 5
REQUESTS = [
    ("Customers can't sign in after resetting their password", "android"),
    ("The thermostat's display shows E-104", "device"),
]

client = OpenAI()


def what_it_tests(script):
    return f"{script['title']}. {script['expected']}"


def script_text(script):
    return " ".join([script["title"], script["preconditions"], *script["steps"], script["expected"]])


def words(text):
    return re.findall(r"[a-z0-9]+", text.lower())


def embed(texts):
    vectors = []
    for start in range(0, len(texts), BATCH):
        response = client.embeddings.create(model=EMBEDDING_MODEL, input=texts[start : start + BATCH])
        vectors += [item.embedding for item in response.data]
        print(f"  Embedding: {len(vectors):,}/{len(texts):,}", end="\r")
    print(" " * 40, end="\r")
    return vectors


def open_database(scripts):
    db = sqlite3.connect(DATABASE)
    db.enable_load_extension(True)
    sqlite_vec.load(db)
    db.enable_load_extension(False)
    db.execute(
        "create virtual table if not exists scripts using vec0("
        "id text primary key, embedding float[1536] distance_metric=cosine,"
        "platform text, minutes integer, +title text, +checksum text)"
    )
    # SQLite's built-in full-text search ranks with BM25, like demo 1. It needs no API, so rebuild it.
    db.execute("drop table if exists script_words")
    db.execute("create virtual table script_words using fts5(id unindexed, platform unindexed, text)")
    db.executemany(
        "insert into script_words values (?, ?, ?)", [(s["id"], s["platform"], script_text(s)) for s in scripts]
    )

    stored = dict(db.execute("select id, checksum from scripts"))
    checksums = {s["id"]: hashlib.sha256(what_it_tests(s).encode()).hexdigest() for s in scripts}
    changed = [s for s in scripts if stored.get(s["id"]) != checksums[s["id"]]]
    for script, vector in zip(changed, embed([what_it_tests(s) for s in changed])):
        db.execute("delete from scripts where id = ?", (script["id"],))
        db.execute(
            "insert into scripts (id, embedding, platform, minutes, title, checksum) values (?, ?, ?, ?, ?, ?)",
            (
                script["id"],
                sqlite_vec.serialize_float32(vector),
                script["platform"],
                script["minutes"],
                script["title"],
                checksums[script["id"]],
            ),
        )
    db.commit()
    return db


def keyword_search(db, request, platform):
    query = " OR ".join(f'"{word}"' for word in words(request))
    return [
        id
        for (id,) in db.execute(
            "select id from script_words where script_words match ? and platform = ? order by bm25(script_words) limit ?",
            (query, platform, CANDIDATES),
        )
    ]


def vector_search(db, vector, platform):
    return [
        id
        for (id,) in db.execute(
            "select id from scripts where embedding match ? and k = ? and platform = ? order by distance",
            (sqlite_vec.serialize_float32(vector), CANDIDATES, platform),
        )
    ]


def hybrid(*rankings):
    # Reciprocal rank fusion: a script scores 1 / (60 + its rank) in each list it appears in.
    scores = Counter()
    for ranking in rankings:
        for rank, id in enumerate(ranking, 1):
            scores[id] += 1 / (RRF_K + rank)
    return [id for id, _ in scores.most_common()]


scripts = json.loads((DATA / "test-scripts.json").read_text())
titles = {s["id"]: s["title"] for s in scripts}
db = open_database(scripts)

found = []
for request, platform in REQUESTS:
    [vector] = embed([request])
    ranking = hybrid(keyword_search(db, request, platform), vector_search(db, vector, platform))
    print(f"\nRequest: {request} ({platform})")
    for id in ranking[:TOP]:
        print(f"  {id}  {titles[id]}")
    found.append({"request": request, "platform": platform, "found": ranking[:TOP]})

# Twenty requests with known answers: is a right script in the top five?
requests = json.loads((DATA / "requests.json").read_text())
vectors = embed([r["request"] for r in requests])
hits = Counter()
results = []
for r, vector in zip(requests, vectors):
    rankings = {
        "keyword": keyword_search(db, r["request"], r["platform"]),
        "vector": vector_search(db, vector, r["platform"]),
    }
    rankings["hybrid"] = hybrid(rankings["keyword"], rankings["vector"])
    for method, ranking in rankings.items():
        hits[method] += any(id in r["expected"] for id in ranking[:TOP])
    results.append({**r, **{method: ranking[:TOP] for method, ranking in rankings.items()}})

print(f"\nA right script in the top {TOP}, for {len(requests)} requests:")
print(f"  keyword {hits['keyword']}, vector {hits['vector']}, hybrid {hits['hybrid']}")

(OUTPUT / "04_hybrid_search.json").write_text(
    json.dumps({"found": found, "hits": hits, "requests": results}, indent=2)
)
