# Fusion knobs — demo 4's hybrid search, with every setting of the merge left for you to change.
# Run from the module folder: uv run python playground/fusion-knobs/play.py
#                         or: source ../../.venv/bin/activate && python playground/fusion-knobs/play.py
#
# To play: change FUSION, RRF_K, CANDIDATES or KEYWORD_WEIGHT below and rerun.
# The library's vectors are kept in output/test-scripts.db, so later runs only embed the 20 requests.

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
DATA = HERE.parent.parent / "data"
OUTPUT = HERE / "output"
OUTPUT.mkdir(exist_ok=True)

DATABASE = OUTPUT / "test-scripts.db"
EMBEDDING_MODEL = "text-embedding-3-small"
BATCH = 100
TOP = 5

# The knobs. Demo 4 is FUSION = "rank", RRF_K = 60, CANDIDATES = 20, KEYWORD_WEIGHT = 1.0.
FUSION = "rank"  # "rank": reciprocal rank fusion. "score": rescale both lists' scores to 0-1 and add them
RRF_K = 60  # rank fusion only: a small k rewards first place much more than tenth; a big k barely does
CANDIDATES = 20  # how many results each search hands to the merge
KEYWORD_WEIGHT = 1.0  # how much the keyword list counts, against 1.0 for the vector list (try 0.5 or 2)

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
    db.execute("drop table if exists script_words")
    db.execute("create virtual table script_words using fts5(id unindexed, platform unindexed, text)")
    db.executemany(
        "insert into script_words values (?, ?, ?)", [(s["id"], s["platform"], script_text(s)) for s in scripts]
    )

    # Only embed scripts that are new or have changed since the last run.
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
    # bm25() is lower for better matches, so flip its sign: a higher score is a better match.
    query = " OR ".join(f'"{word}"' for word in words(request))
    return db.execute(
        "select id, -bm25(script_words) from script_words where script_words match ? and platform = ?"
        " order by bm25(script_words) limit ?",
        (query, platform, CANDIDATES),
    ).fetchall()


def vector_search(db, vector, platform):
    return db.execute(
        "select id, 1 - distance from scripts where embedding match ? and k = ? and platform = ? order by distance",
        (sqlite_vec.serialize_float32(vector), CANDIDATES, platform),
    ).fetchall()


def rank_fusion(keyword, vector):
    # Each list gives a script weight / (k + its rank). Only the order counts, not the scores.
    scores = Counter()
    for weight, results in [(KEYWORD_WEIGHT, keyword), (1.0, vector)]:
        for rank, (id, _) in enumerate(results, 1):
            scores[id] += weight / (RRF_K + rank)
    return [id for id, _ in scores.most_common()]


def score_fusion(keyword, vector):
    # Rescale each list so its best score is 1 and its worst is 0, then add them up.
    scores = Counter()
    for weight, results in [(KEYWORD_WEIGHT, keyword), (1.0, vector)]:
        if not results:
            continue
        high = max(score for _, score in results)
        low = min(score for _, score in results)
        for id, score in results:
            scores[id] += weight * (score - low) / ((high - low) or 1)
    return [id for id, _ in scores.most_common()]


scripts = json.loads((DATA / "test-scripts.json").read_text())
db = open_database(scripts)
requests = json.loads((DATA / "requests.json").read_text())
vectors = embed([r["request"] for r in requests])

hits = Counter()
results = []
for r, vector in zip(requests, vectors):
    keyword = keyword_search(db, r["request"], r["platform"])
    found = vector_search(db, vector, r["platform"])
    rankings = {
        "keyword": [id for id, _ in keyword],
        "vector": [id for id, _ in found],
        "hybrid": rank_fusion(keyword, found) if FUSION == "rank" else score_fusion(keyword, found),
    }
    for method, ranking in rankings.items():
        hits[method] += any(id in r["expected"] for id in ranking[:TOP])
    results.append({**r, **{method: ranking[:TOP] for method, ranking in rankings.items()}})

settings = f"rank fusion, k = {RRF_K}" if FUSION == "rank" else "score fusion"
settings += f", {CANDIDATES} candidates each, keyword weight {KEYWORD_WEIGHT}"
print(f"\n{settings}")
print(f"A right script in the top {TOP}, for {len(requests)} requests:")
print(f"  keyword {hits['keyword']}, vector {hits['vector']}, hybrid {hits['hybrid']}")

(OUTPUT / "results.json").write_text(json.dumps({"settings": settings, "hits": hits, "requests": results}, indent=2))
