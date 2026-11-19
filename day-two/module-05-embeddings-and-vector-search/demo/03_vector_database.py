# Run from the module folder: uv run python demo/03_vector_database.py

import hashlib
import json
import sqlite3
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
REQUEST = "Customers can't sign in after resetting their password"
PLATFORM = "android"
MAX_MINUTES = 10
CODE_REQUEST = "The thermostat's display shows E-104"

client = OpenAI()


def what_it_tests(script):
    return f"{script['title']}. {script['expected']}"


def embed(texts):
    vectors = []
    for start in range(0, len(texts), BATCH):
        response = client.embeddings.create(model=EMBEDDING_MODEL, input=texts[start : start + BATCH])
        vectors += [item.embedding for item in response.data]
        print(f"  Embedding: {len(vectors):,}/{len(texts):,}", end="\r")
    print(" " * 40, end="\r")
    return vectors


def open_database():
    db = sqlite3.connect(DATABASE)
    db.enable_load_extension(True)
    sqlite_vec.load(db)
    db.enable_load_extension(False)
    # One row per script: its vector, columns to filter on, and (after +) columns to carry along.
    db.execute(
        "create virtual table if not exists scripts using vec0("
        "id text primary key, embedding float[1536] distance_metric=cosine,"
        "platform text, minutes integer, +title text, +checksum text)"
    )
    return db


def update(db, scripts):
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
    return len(changed)


def search(db, request, where, parameters):
    [vector] = embed([request])
    return db.execute(
        f"""select id, 1 - distance, platform, minutes, title from scripts
            where embedding match ? and k = 3 {where}
            order by distance""",
        (sqlite_vec.serialize_float32(vector), *parameters),
    ).fetchall()


def show(results):
    for id, similarity, platform, minutes, title in results:
        print(f"  {similarity:.3f}  {id}  {platform:<8} {minutes:>2} min  {title}")


def as_json(results):
    return [dict(zip(["id", "similarity", "platform", "minutes", "title"], r)) for r in results]


db = open_database()
scripts = json.loads((DATA / "test-scripts.json").read_text())
print(f"\nEmbedded {update(db, scripts):,} new or changed scripts into {DATABASE.name}")

print(f"\nRequest: {REQUEST}")
print(f"Criteria: {PLATFORM}, at most {MAX_MINUTES} minutes")
found = search(db, REQUEST, "and platform = ? and minutes <= ?", (PLATFORM, MAX_MINUTES))
show(found)

print(f"\nRequest: {CODE_REQUEST}")
code_found = search(db, CODE_REQUEST, "", ())
show(code_found)

(OUTPUT / "03_vector_database.json").write_text(
    json.dumps(
        {
            "request": REQUEST,
            "criteria": {"platform": PLATFORM, "max_minutes": MAX_MINUTES},
            "found": as_json(found),
            "code_request": CODE_REQUEST,
            "code_found": as_json(code_found),
        },
        indent=2,
    )
)
