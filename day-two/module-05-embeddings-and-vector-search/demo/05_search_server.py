# Run from the module folder: uv run python demo/05_search_server.py
# You don't need to run it yourself: demo/05_agent.py starts it.

import hashlib
import json
import sqlite3
from pathlib import Path
from typing import Literal

import sqlite_vec
from dotenv import load_dotenv
from mcp.server.mcpserver import MCPServer
from openai import OpenAI

load_dotenv()

HERE = Path(__file__).parent
DATA = HERE.parent / "data"
OUTPUT = HERE / "output"
OUTPUT.mkdir(exist_ok=True)

DATABASE = OUTPUT / "test-scripts.db"
EMBEDDING_MODEL = "text-embedding-3-small"
BATCH = 100
RESULTS = 5

# Log warnings only, so every embedding request isn't reported on the agent's terminal.
server = MCPServer("test-scripts", log_level="WARNING")


def what_it_tests(script):
    return f"{script['title']}. {script['expected']}"


def embed(texts):
    # No progress line here: a server's stdout carries its messages to the agent.
    client = OpenAI()
    vectors = []
    for start in range(0, len(texts), BATCH):
        response = client.embeddings.create(model=EMBEDDING_MODEL, input=texts[start : start + BATCH])
        vectors += [item.embedding for item in response.data]
    return vectors


def open_database():
    db = sqlite3.connect(DATABASE)
    db.enable_load_extension(True)
    sqlite_vec.load(db)
    db.enable_load_extension(False)
    db.execute(
        "create virtual table if not exists scripts using vec0("
        "id text primary key, embedding float[1536] distance_metric=cosine,"
        "platform text, minutes integer, +title text, +checksum text)"
    )
    return db


def update(db, scripts):
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


library = json.loads((DATA / "test-scripts.json").read_text())
scripts = {s["id"]: s for s in library}


@server.tool()
def find_test_scripts(request: str, platform: Literal["android", "ios", "web", "device"], max_minutes: int) -> str:
    """Search Dormouse's library of 1,000 manual test scripts by meaning. In `request`, describe
    the behaviour to test in a few plain words, like a test's title: for example "log in after
    changing the password". Only scripts for `platform` that take at most `max_minutes` to run
    are returned. Returns the five closest scripts as JSON, closest first, with their steps and
    expected results."""
    db = open_database()
    update(db, library)  # Embeds the whole library on the first search, then only what changes.
    [vector] = embed([request])
    found = db.execute(
        "select id from scripts where embedding match ? and k = ? and platform = ? and minutes <= ?"
        " order by distance",
        (sqlite_vec.serialize_float32(vector), RESULTS, platform, max_minutes),
    )
    return json.dumps([scripts[id] for (id,) in found], indent=2)


server.run()
