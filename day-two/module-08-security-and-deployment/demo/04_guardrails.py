# Run from the module folder: uv run python demo/04_guardrails.py

import hashlib
import json
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import sqlite_vec
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

HERE = Path(__file__).parent
DATA = HERE.parent / "data"
OUTPUT = HERE / "output"
OUTPUT.mkdir(exist_ok=True)

DATABASE = OUTPUT / "knowledge.db"
MODEL = "gpt-6-luna"
EMBEDDING_MODEL = "text-embedding-3-small"
BATCH = 100
TOP = 5
MAX_STEPS = 10
INSTRUCTIONS = """You are Ask Dormouse, the support assistant in the Dormouse app. Answer the customer in a short
paragraph of plain text. Start by looking up their home, so you know which devices they have. Use the
documentation and the tools."""

AUDIT_LOG = OUTPUT / "04_audit.jsonl"
FOLLOW_UP = "Please invite my brother Ben to the household: ben.taylor@example.com"

# Set by the app when Sam signs in. The model never sees it and can't change it.
SESSION = {"customer": "C-1001", "audience": "customer"}

client = OpenAI()
dormouse = json.loads((DATA / "dormouse.json").read_text())
attacks = json.loads((DATA / "attacks.json").read_text())


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
    vectors = []
    for start in range(0, len(texts), BATCH):
        response = client.embeddings.create(model=EMBEDDING_MODEL, input=texts[start : start + BATCH])
        vectors += [item.embedding for item in response.data]
        print(f"  Embedding the knowledge base: {len(vectors):,}/{len(texts):,}", end="\r")
    print(" " * 50, end="\r")
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
    # Embed new and changed chunks only, so later runs start straight away.
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


def search(db, question):
    vector = client.embeddings.create(model=EMBEDDING_MODEL, input=question).data[0].embedding
    # Module 5's metadata filter: only documents for this audience are searched at all.
    rows = db.execute(
        "select id, text from chunks where embedding match ? and k = ? and audience = ? order by distance",
        (sqlite_vec.serialize_float32(vector), TOP, SESSION["audience"]),
    )
    return [{"id": id, "text": text} for id, text in rows]


def tool(name, description, **properties):
    return {
        "type": "function",
        "name": name,
        "description": description,
        "parameters": {
            "type": "object",
            "properties": {key: {"type": "string", "description": text} for key, text in properties.items()},
            "required": list(properties),
            "additionalProperties": False,
        },
        "strict": True,
    }


# Every action has a tier, set in code. Removing members, changing the owner and deleting the home
# are the fourth tier, "never": the model isn't given a tool for them at all.
TIERS = {
    "get_my_home": "read",
    "get_my_orders": "read",
    "contact_support": "reversible",
    "invite_member": "confirm",
}
TOOLS = [
    tool("get_my_home", "Look up the customer's home: its address, members, devices, schedule and away status."),
    tool("get_my_orders", "Look up the customer's orders."),
    tool(
        "contact_support",
        "Pass a message to Dormouse's support team, who reply within a working day.",
        message="What the customer needs",
    ),
    tool(
        "invite_member",
        "Invite someone to the customer's household by email. The app asks the customer to confirm first.",
        email="Their email address",
    ),
]


def my_home():
    customer = next(c for c in dormouse["customers"] if c["id"] == SESSION["customer"])
    return next(h for h in dormouse["homes"] if h["id"] == customer["home"])


def renamed_by_chris(home):
    # As in demo 3: Chris renamed the hall thermostat before moving out.
    home = json.loads(json.dumps(home))
    for device in home["devices"]:
        if device["id"] == attacks["injection"]["device"]:
            device["name"] = attacks["injection"]["helpful"]
    return home


def log(event, **details):
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    record = {"time": now, "customer": SESSION["customer"], "event": event, **details}
    with AUDIT_LOG.open("a") as file:
        file.write(json.dumps(record) + "\n")


def confirm(name, args):
    # The app writes the question from the action itself, never from the model's words.
    home = my_home()
    if name == "invite_member":
        print(f"\n  Ask Dormouse wants to invite {args['email']} to your home, {home['address']}.")
        print("  They would be able to see and change your heating, and see when nobody is home.")
    try:
        answer = input("  Allow this? [y/N] ").strip().lower()
    except EOFError:
        answer = ""
    allowed = answer == "y"
    print("  Allowed" if allowed else "  Declined")
    log("confirmation", tool=name, args=args, allowed=allowed)
    return allowed


def run_tool(name, args):
    tier = TIERS[name]
    if tier == "confirm" and not confirm(name, args):
        return {"status": "declined", "by": "the customer"}
    if name == "get_my_home":
        result = renamed_by_chris(my_home())
    elif name == "get_my_orders":
        result = [o for o in dormouse["orders"] if o["customer"] == SESSION["customer"]]
    elif name == "contact_support":
        result = {"ticket": "T-3391", "message": args["message"]}
    elif name == "invite_member":
        result = {"invited": args["email"]}
    if tier != "read":
        log("action", tool=name, tier=tier, args=args, result=result)
    return result


def reply(db, conversation):
    question = conversation[-1]["content"]
    log("message", text=question)
    documentation = "\n\n".join(f'<chunk id="{c["id"]}">\n{c["text"]}\n</chunk>' for c in search(db, question))
    for step in range(MAX_STEPS):
        response = client.responses.create(
            model=MODEL,
            reasoning={"effort": "none"},
            instructions=f"{INSTRUCTIONS}\n\nOur documentation:\n\n{documentation}",
            input=conversation,
            tools=TOOLS,
        )
        conversation += response.output
        requested = [item for item in response.output if item.type == "function_call"]
        if not requested:
            break
        for call in requested:
            args = json.loads(call.arguments)
            print(f"  [tool] {call.name}({', '.join(args.values())})")
            output = json.dumps(run_tool(call.name, args))
            conversation.append({"type": "function_call_output", "call_id": call.call_id, "output": output})
    log("reply", text=response.output_text)
    return response.output_text


documents = load_documents(DATA / "kb")
chunks = [chunk for document in documents for chunk in split_into_chunks(document)]
db = open_database()
update(db, chunks)
AUDIT_LOG.unlink(missing_ok=True)

conversation = []
for message in [attacks["question"], FOLLOW_UP]:
    print(f"\nSam: {message}")
    conversation.append({"role": "user", "content": message})
    print(f"Ask Dormouse: {reply(db, conversation)}")

events = AUDIT_LOG.read_text().splitlines()
print(f"\nThe audit log has {len(events)} events: demo/output/04_audit.jsonl")
