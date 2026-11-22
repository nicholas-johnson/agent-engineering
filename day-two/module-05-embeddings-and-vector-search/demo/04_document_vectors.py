# Run from the module folder: uv run python demo/04_document_vectors.py

import json
import re
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

HERE = Path(__file__).parent
DOCS = HERE.parent / "data" / "docs"
OUTPUT = HERE / "output"
OUTPUT.mkdir(exist_ok=True)

WORD_VECTORS = OUTPUT / "03_word_vectors.txt"
EMBEDDING_MODEL = "text-embedding-3-small"
QUESTION = "Why is the heating already on before my alarm goes off?"
DOCUMENTS = ["understand-warm-wake", "enter-your-boiler-size-for-energy-reports"]
SHOW = 6

client = OpenAI()


def read_document(name):
    _, header, text = (DOCS / f"{name}.md").read_text().split("---", 2)
    title = re.search(r"^title: (.+)$", header, re.MULTILINE)[1]
    return title, text.strip()


def words(text):
    return re.findall(r"[a-z0-9]+", text.lower())


def average_vector(text, word_vectors):
    # Our model has one vector per word, so a text becomes the average of its words' vectors.
    known = [word_vectors[w] for w in words(text) if w in word_vectors]
    left_out = sorted({w for w in words(text) if w not in word_vectors})
    return [sum(column) / len(known) for column in zip(*known)], left_out


def show(name, vector, decimals):
    numbers = ", ".join(f"{x:.{decimals}f}" for x in vector[:SHOW])
    print(f"  {name}\n    {len(vector):,} numbers: [{numbers}, ...]")


if not WORD_VECTORS.exists():
    sys.exit("Run demo/03_word_vectors.py first: this demo uses the word vectors it trains.")
word_vectors = {}
for line in WORD_VECTORS.read_text().splitlines():
    word, *numbers = line.split()
    word_vectors[word] = [float(x) for x in numbers]

texts = {"Q: " + QUESTION: QUESTION} | dict(read_document(name) for name in DOCUMENTS)
written = {}

print("\n=== Our model: the average of the word vectors ===")
for name, text in texts.items():
    vector, left_out = average_vector(text, word_vectors)
    show(name, vector, 2)
    print(f"    left out {len(left_out)} words it has never seen: {', '.join(left_out[:6])}{', ...' if len(left_out) > 6 else ''}")
    written[name] = {"our_model": vector, "left_out": left_out}

print(f"\n=== {EMBEDDING_MODEL} ===")
response = client.embeddings.create(model=EMBEDDING_MODEL, input=list(texts.values()))
for name, item in zip(texts, response.data):
    show(name, item.embedding, 4)
    written[name][EMBEDDING_MODEL] = item.embedding

(OUTPUT / "04_document_vectors.json").write_text(json.dumps(written, indent=2))
