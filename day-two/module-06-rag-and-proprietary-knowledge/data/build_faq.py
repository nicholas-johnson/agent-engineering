# Run from the module folder: uv run python data/build_faq.py
#
# Builds data/faq.json: for every chunk of the knowledge base, the questions a customer might
# ask that the chunk answers, written by gpt-6-luna. Demo 4 searches these questions.
# It saves as it goes and only writes questions for chunks that are new or have changed,
# so it can be stopped and run again. Deleting faq.json and rerunning gives new questions.

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
CHUNKS_PER_CALL = 10

INSTRUCTIONS = """You turn documentation into the questions customers ask.
For each chunk of Dormouse documentation, write 3 to 5 questions that the chunk answers.
Write them as a customer who has never read the documentation would type them into a chat window:
in everyday words, describing what they see or what they want. Plain ASCII."""

SCHEMA = {
    "type": "object",
    "properties": {
        "chunks": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {"id": {"type": "string"}, "questions": {"type": "array", "items": {"type": "string"}}},
                "required": ["id", "questions"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["chunks"],
    "additionalProperties": False,
}

client = OpenAI(timeout=120)  # so a dropped connection fails and is retried, rather than hanging


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


def write_questions(batch):
    response = client.responses.create(
        model=MODEL,
        reasoning={"effort": "none"},
        instructions=INSTRUCTIONS,
        input="\n\n".join(f'<chunk id="{c["id"]}">\n{c["text"]}\n</chunk>' for c in batch),
        text={"format": {"type": "json_schema", "name": "faq", "schema": SCHEMA, "strict": True}},
    )
    # Occasionally the reply has a second JSON object after the first, so read only the first.
    reply, _ = json.JSONDecoder().raw_decode(response.output_text)
    return reply["chunks"]


def plain_ascii(text):
    for fancy, plain in {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
    }.items():
        text = text.replace(fancy, plain)
    return text.encode("ascii", "ignore").decode()


chunks = [chunk for document in load_documents(DOCS) for chunk in split_into_chunks(document)]
checksums = {c["id"]: hashlib.sha256(c["text"].encode()).hexdigest() for c in chunks}

# Keep the questions for chunks that haven't changed; write the rest.
faq = json.loads(FAQ.read_text()) if FAQ.exists() else {}
faq = {id: entry for id, entry in faq.items() if checksums.get(id) == entry["checksum"]}
todo = [c for c in chunks if c["id"] not in faq]
batches = [todo[i : i + CHUNKS_PER_CALL] for i in range(0, len(todo), CHUNKS_PER_CALL)]

with ThreadPoolExecutor(max_workers=8) as pool:
    for future in as_completed([pool.submit(write_questions, b) for b in batches]):
        for item in future.result():
            if item["id"] in checksums:
                questions = [plain_ascii(q) for q in item["questions"]]
                faq[item["id"]] = {"checksum": checksums[item["id"]], "questions": questions}
        FAQ.write_text(json.dumps(dict(sorted(faq.items())), indent=2) + "\n")
        print(f"Questions for {len(faq):,} of {len(chunks):,} chunks", end="\r")
print()
print(f"data/faq.json has {sum(len(e['questions']) for e in faq.values()):,} questions for {len(faq):,} chunks")
