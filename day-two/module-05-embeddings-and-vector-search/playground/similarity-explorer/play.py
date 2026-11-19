# Similarity explorer — type sentences and see how close their embeddings are.
# Run from the module folder: uv run python playground/similarity-explorer/play.py
#                         or: source ../../.venv/bin/activate && python playground/similarity-explorer/play.py
#
# To play: type a sentence, then the sentences to compare it with (see README.md for pairs to try),
# or change EMBEDDING_MODEL to "text-embedding-3-large" and see if the numbers move.

import json
import math
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OUTPUT = Path(__file__).parent / "output"
OUTPUT.mkdir(exist_ok=True)

EMBEDDING_MODEL = "text-embedding-3-small"  # try "text-embedding-3-large"

client = OpenAI()


def embed(texts):
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=texts)
    return [item.embedding for item in response.data]


def cosine_similarity(a, b):
    return math.sumprod(a, b) / (math.sqrt(math.sumprod(a, a)) * math.sqrt(math.sumprod(b, b)))


results = []

# A sentence, then one or more to compare it with. An empty line ends the list; another one stops.
while True:
    sentence = input("Sentence: ")
    if not sentence:
        break

    others = []
    while True:
        other = input("  Compare with: ")
        if not other:
            break
        others.append(other)
    if not others:
        continue

    [vector, *other_vectors] = embed([sentence, *others])
    compared = sorted(((cosine_similarity(vector, v), other) for v, other in zip(other_vectors, others)), reverse=True)
    print()
    for similarity, other in compared:
        print(f"  {similarity:.3f}  {other}")
    print()

    results.append({"sentence": sentence, "compared": [{"similarity": round(s, 4), "text": t} for s, t in compared]})
    (OUTPUT / "similarities.json").write_text(json.dumps(results, indent=2, ensure_ascii=False))
