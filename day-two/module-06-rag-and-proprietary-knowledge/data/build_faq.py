# Run from the module folder: uv run python data/build_faq.py
#
# Builds data/faq.json: each document of the knowledge base converted into an FAQ by gpt-6-luna,
# as many questions as a customer might ask, each pointing to the chunk that answers it.
# Demo 5 searches these questions. It saves as it goes and only converts documents that are new
# or have changed, so it can be stopped and run again. Deleting faq.json and rerunning gives new questions.

import hashlib
import json
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

HERE = Path(__file__).parent
DOCS = HERE / "docs"
FAQ = HERE / "faq.json"
MODEL = "gpt-6-luna"

INSTRUCTIONS = """You turn documentation into the questions customers ask.
Convert this Dormouse document into an FAQ: every question a customer might ask that it answers.
Write as many questions as it takes. There is no limit.
Write them as a customer who has never read the documentation would type them into a chat window:
in everyday words, describing what they see or what they want.
Give each question the id of the chunk that answers it. Plain ASCII."""

SCHEMA = {
    "type": "object",
    "properties": {
        "faq": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {"question": {"type": "string"}, "chunk": {"type": "string"}},
                "required": ["question", "chunk"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["faq"],
    "additionalProperties": False,
}

client = OpenAI(timeout=300)  # so a dropped connection fails and is retried, rather than hanging


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
    # The same chunks as the demos: one per section.
    chunks, path, lines = [], [], []

    def finish_section():
        content = "\n".join(lines).strip()
        if content:
            heading = " > ".join([document["title"], *path])
            id = f"{document['name']}#{slug(path[-1]) if path else 'top'}"
            while id in {c["id"] for c in chunks}:
                id += "-2"
            chunks.append({"id": id, "document": document["name"], "text": f"{heading}\n\n{content}"})

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


def write_faq(chunks):
    # The whole document, one chunk after another, each marked with its id.
    response = client.responses.create(
        model=MODEL,
        reasoning={"effort": "none"},
        instructions=INSTRUCTIONS,
        input="\n\n".join(f'<chunk id="{c["id"]}">\n{c["text"]}\n</chunk>' for c in chunks),
        text={"format": {"type": "json_schema", "name": "faq", "schema": SCHEMA, "strict": True}},
    )
    # Occasionally the reply has a second JSON object after the first, so read only the first.
    reply, _ = json.JSONDecoder().raw_decode(response.output_text)
    return chunks, reply["faq"]


def plain_ascii(text):
    for fancy, plain in {
        "‘": "'",
        "’": "'",
        "“": '"',
        "”": '"',
        "–": "-",
        "—": "-",
    }.items():
        text = text.replace(fancy, plain)
    return text.encode("ascii", "ignore").decode()


documents = {d["name"]: split_into_chunks(d) for d in load_documents(DOCS)}
checksums = {c["id"]: hashlib.sha256(c["text"].encode()).hexdigest() for chunks in documents.values() for c in chunks}

# Keep the questions for documents whose chunks haven't changed; convert the rest.
faq = json.loads(FAQ.read_text()) if FAQ.exists() else {}
faq = {id: entry for id, entry in faq.items() if checksums.get(id) == entry["checksum"]}
todo = [chunks for chunks in documents.values() if any(c["id"] not in faq for c in chunks)]

with ThreadPoolExecutor(max_workers=8) as pool:
    for future in as_completed([pool.submit(write_faq, chunks) for chunks in todo]):
        chunks, questions = future.result()
        # Every chunk gets an entry, even one with no questions, so the document isn't converted again.
        for chunk in chunks:
            faq[chunk["id"]] = {"checksum": checksums[chunk["id"]], "questions": []}
        for item in questions:
            if item["chunk"] in {c["id"] for c in chunks}:
                faq[item["chunk"]]["questions"].append(plain_ascii(item["question"]))
        FAQ.write_text(json.dumps(dict(sorted(faq.items())), indent=2) + "\n")
        print(f"Questions for {len(faq):,} of {len(checksums):,} chunks", end="\r")
print()
print(f"data/faq.json has {sum(len(e['questions']) for e in faq.values()):,} questions for {len(faq):,} chunks")
