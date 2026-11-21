# Run from the module folder: uv run python demo/06_dormouse_server.py
# You don't need to run it yourself: demo/06_two_assistants.py starts it, once for each person.

import hashlib
import json
import os
import re
import sqlite3
from datetime import date
from pathlib import Path

import sqlite_vec
from dotenv import load_dotenv
from mcp.server.mcpserver import MCPServer
from openai import OpenAI

load_dotenv()

HERE = Path(__file__).parent
DATA = HERE.parent / "data"
OUTPUT = HERE / "output"
OUTPUT.mkdir(exist_ok=True)

DATABASE = OUTPUT / "knowledge.db"
STATE = OUTPUT / "06_dormouse.json"  # Dormouse's data, as the API sees it; demo 6 resets it each run
EMBEDDING_MODEL = "text-embedding-3-small"
BATCH = 100
TOP = 5

# Stands in for Dormouse's sign-in service: each token belongs to one person, with one role.
TOKENS = {
    "sam-7f3a": {"person": "C-1001", "role": "customer"},
    "priya-91c2": {"person": "S-07", "role": "staff"},
}
AUDIENCES = {"customer": ["customer"], "staff": ["customer", "internal"]}

account = TOKENS[os.environ["DORMOUSE_TOKEN"]]
server = MCPServer("dormouse", log_level="WARNING")


def load_documents(folder):
    documents = []
    for path in sorted(folder.glob("*.md")):
        _, front, body = path.read_text().split("---", 2)
        fields = dict(line.split(": ", 1) for line in front.strip().splitlines())
        documents.append({"name": path.name, **fields, "body": body})
    return documents


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def split_into_chunks(document):
    # One chunk per section: everything under a heading, down to the next heading.
    chunks, path, lines = [], [], []

    def finish_section():
        content = "\n".join(lines).strip()
        if content:
            heading = " > ".join([document["title"], *path])
            id = f"{document['name']}#{slug(path[-1]) if path else 'top'}"
            while id in {c["id"] for c in chunks}:
                id += "-2"
            chunks.append({"id": id, "audience": document["audience"], "text": f"{heading}\n\n{content}"})

    for line in document["body"].splitlines():
        heading = re.match(r"(#{1,3}) (.+)", line)
        if heading:
            finish_section()
            lines = []
            level = len(heading[1])
            path = path[: level - 2] + [heading[2].strip()] if level > 1 else []
        else:
            lines.append(line)
    finish_section()
    return chunks


def embed(texts):
    # No progress line here: a server's stdout carries its messages to the assistant.
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
        "create virtual table if not exists chunks using vec0("
        "id text primary key, embedding float[1536] distance_metric=cosine,"
        "audience text, +text text, +checksum text)"
    )
    return db


def update(db, chunks):
    stored = dict(db.execute("select id, checksum from chunks"))
    checksums = {c["id"]: hashlib.sha256(c["text"].encode()).hexdigest() for c in chunks}
    changed = [c for c in chunks if stored.get(c["id"]) != checksums[c["id"]]]
    for id in (set(stored) - set(checksums)) | {c["id"] for c in changed}:
        db.execute("delete from chunks where id = ?", (id,))
    for chunk, vector in zip(changed, embed([c["text"] for c in changed])):
        db.execute(
            "insert into chunks (id, embedding, audience, text, checksum) values (?, ?, ?, ?, ?)",
            (chunk["id"], sqlite_vec.serialize_float32(vector), chunk["audience"], chunk["text"], checksums[chunk["id"]]),
        )
    db.commit()


def load():
    if not STATE.exists():
        STATE.write_text((DATA / "dormouse.json").read_text())
    return json.loads(STATE.read_text())


def save(dormouse):
    STATE.write_text(json.dumps(dormouse, indent=2, ensure_ascii=False))


def new_ticket(dormouse, customer, about):
    ticket_id = f"T-{3390 + len(dormouse['contacts'])}"
    ticket = {"id": ticket_id, "customer": customer, "date": date.today().isoformat(), "about": about, "outcome": None}
    dormouse["contacts"].append(ticket)
    return ticket


@server.tool()
def search_docs(question: str) -> str:
    """Search Dormouse's documentation. Returns the five most relevant sections."""
    db = open_database()
    update(db, [chunk for document in load_documents(DATA / "kb") for chunk in split_into_chunks(document)])
    [vector] = embed([question])
    audiences = AUDIENCES[account["role"]]
    rows = db.execute(
        f"select id, text from chunks where embedding match ? and k = ? and audience in ({', '.join('?' * len(audiences))})"
        " order by distance",
        (sqlite_vec.serialize_float32(vector), TOP, *audiences),
    )
    return "\n\n".join(f'<chunk id="{id}">\n{text}\n</chunk>' for id, text in rows)


# The server offers each person only the tools their role allows.
if account["role"] == "customer":

    @server.tool()
    def get_my_home() -> str:
        """Look up the customer's home: its address, members, devices, schedule and away status."""
        dormouse = load()
        customer = next(c for c in dormouse["customers"] if c["id"] == account["person"])
        return json.dumps(next(h for h in dormouse["homes"] if h["id"] == customer["home"]))

    @server.tool()
    def contact_support(message: str) -> str:
        """Pass a message to Dormouse's support team, who reply within a working day."""
        dormouse = load()
        ticket = new_ticket(dormouse, account["person"], message)
        save(dormouse)
        return json.dumps(ticket)


if account["role"] == "staff":

    @server.tool()
    def get_customer(customer_id: str) -> str:
        """Look up a customer: their details, home, orders and every time they have contacted support."""
        dormouse = load()
        customer = next(c for c in dormouse["customers"] if c["id"] == customer_id)
        return json.dumps(
            {
                **customer,
                "home": next((h for h in dormouse["homes"] if h["id"] == customer["home"]), None),
                "orders": [o for o in dormouse["orders"] if o["customer"] == customer_id],
                "contacts": [c for c in dormouse["contacts"] if c["customer"] == customer_id],
            }
        )

    @server.tool()
    def offer_replacement(customer_id: str, ticket_id: str) -> str:
        """Send the customer a free replacement thermostat, and close their latest ticket."""
        dormouse = load()
        ticket = next(t for t in dormouse["contacts"] if t["id"] == ticket_id and t["customer"] == customer_id)
        ticket["outcome"] = f"Replacement thermostat sent by {account['person']}."
        save(dormouse)
        return json.dumps(ticket)


server.run()
