# Long context or RAG — what the whole knowledge base in every prompt costs, against the top 5 chunks.
# Run from the module folder: uv run python playground/long-context-or-rag/play.py
#                         or: source ../../.venv/bin/activate && python playground/long-context-or-rag/play.py
#
# To play: change QUESTIONS_PER_DAY, the prices or CACHED_SHARE, and rerun. No answers are generated:
# the API only counts tokens, and the counts are kept in output/token-counts.json, so reruns are instant.

import hashlib
import json
import re
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

HERE = Path(__file__).parent
DATA = HERE.parent.parent / "data"
OUTPUT = HERE / "output"
OUTPUT.mkdir(exist_ok=True)

MODEL = "gpt-6-luna"
TOP = 5
QUESTIONS_PER_DAY = 10_000
# Dollars per million tokens for gpt-6-luna, from Module 4's price list (checked 10 November 2026).
INPUT_PRICE = 0.10
OUTPUT_PRICE = 0.50
CACHED_PRICE = INPUT_PRICE / 10  # an assumption: check what OpenAI's pricing page says for cached input
CACHED_SHARE = 0.9  # an assumption: the share of the whole-knowledge-base prompt that is read from the cache
OUTPUT_TOKENS = 100  # an assumption: a short paragraph
INSTRUCTIONS = "You are the support assistant for Dormouse, a smart thermostat. Answer the customer in a short paragraph."
QUESTION = "Why does my Dormouse turn the heating on before the time I set?"

client = OpenAI()


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
    # One chunk per section, starting with "Title > Heading", as in demo 3.
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


def count_tokens(instructions, text):
    # The API counts the tokens a prompt would use, without running the model. Each count is kept by its text.
    counts_file = OUTPUT / "token-counts.json"
    counts = json.loads(counts_file.read_text()) if counts_file.exists() else {}
    key = hashlib.sha256(f"{instructions}\n{text}".encode()).hexdigest()
    if key not in counts:
        counts[key] = client.responses.input_tokens.count(model=MODEL, instructions=instructions, input=text).input_tokens
        counts_file.write_text(json.dumps(counts, indent=2))
    return counts[key]


def dollars(input_tokens, cached_share):
    cached = input_tokens * cached_share
    return ((input_tokens - cached) * INPUT_PRICE + cached * CACHED_PRICE + OUTPUT_TOKENS * OUTPUT_PRICE) / 1_000_000


documents = load_documents(DATA / "docs")
chunks = [chunk for document in documents for chunk in split_into_chunks(document)]

# Demo 2's prompt: every document, in full, then the question.
print("  Counting tokens...", end="\r")
everything = "\n\n".join(path.read_text() for path in sorted((DATA / "docs").glob("*.md")))
long_context = count_tokens(f"{INSTRUCTIONS}\n\nUse our documentation:\n\n{everything}", QUESTION)

# Demo 3's prompt with TOP average chunks. Count every chunk once, then share the count out.
all_chunks = "\n\n".join(f'<chunk id="{c["id"]}">\n{c["text"]}\n</chunk>' for c in chunks)
per_chunk = count_tokens("", all_chunks) / len(chunks)
rag = count_tokens(f"{INSTRUCTIONS}\n\nUse our documentation:", QUESTION) + round(TOP * per_chunk)
print(" " * 40, end="\r")

approaches = [
    ("Whole knowledge base", long_context, 0),
    (f"Whole knowledge base, {CACHED_SHARE:.0%} cached", long_context, CACHED_SHARE),
    (f"Top {TOP} chunks", rag, 0),
]
print(f"\n  {len(documents)} documents, {len(chunks):,} chunks of {per_chunk:.0f} tokens on average.")
print(f"  Every answer also costs {OUTPUT_TOKENS} output tokens (an assumption).\n")
print(f"  {'':<36}{'Tokens in':>10}{'Per question':>14}{f'Per day ({QUESTIONS_PER_DAY:,})':>20}{'Per year':>12}")
results = []
for name, tokens, cached_share in approaches:
    per_question = dollars(tokens, cached_share)
    per_day = per_question * QUESTIONS_PER_DAY
    print(f"  {name:<36}{tokens:>10,}{f'${per_question:.5f}':>14}{f'${per_day:,.2f}':>20}{f'${per_day * 365:,.0f}':>12}")
    results.append({"approach": name, "input_tokens": tokens, "cached_share": cached_share, "dollars": per_question})

settings = {
    "questions_per_day": QUESTIONS_PER_DAY,
    "input_price": INPUT_PRICE,
    "cached_price": CACHED_PRICE,
    "output_price": OUTPUT_PRICE,
    "output_tokens": OUTPUT_TOKENS,
}
(OUTPUT / "costs.json").write_text(json.dumps({"settings": settings, "approaches": results}, indent=2))
