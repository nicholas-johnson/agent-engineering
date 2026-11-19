# Run from the module folder: uv run python demo/02_embeddings.py

import json
import math
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

HERE = Path(__file__).parent
DATA = HERE.parent / "data"
OUTPUT = HERE / "output"
OUTPUT.mkdir(exist_ok=True)

EMBEDDING_MODEL = "text-embedding-3-small"
BATCH = 100
LIBRARIES = ["test-scripts-small.json", "test-scripts.json"]
REQUEST = "Customers can't sign in after resetting their password"

client = OpenAI()


def what_it_tests(script):
    # The title and expected result say what a test checks.
    return f"{script['title']}. {script['expected']}"


def embed(texts):
    vectors = []
    for start in range(0, len(texts), BATCH):
        response = client.embeddings.create(model=EMBEDDING_MODEL, input=texts[start : start + BATCH])
        vectors += [item.embedding for item in response.data]
        print(f"  Embedding: {len(vectors):,}/{len(texts):,}", end="\r")
    print(" " * 40, end="\r")
    return vectors


def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))


[request_vector] = embed([REQUEST])
numbers = ", ".join(f"{x:.4f}" for x in request_vector[:4])
print(f"\nRequest: {REQUEST}")
print(f"As {len(request_vector):,} numbers: [{numbers}, ...]")

found = {}
for library in LIBRARIES:
    scripts = json.loads((DATA / library).read_text())
    print(f"\n=== {library}: {len(scripts):,} test scripts ===")
    vectors = embed([what_it_tests(s) for s in scripts])

    results = sorted(
        ((cosine_similarity(request_vector, v), s) for v, s in zip(vectors, scripts)),
        key=lambda r: r[0],
        reverse=True,
    )
    for similarity, script in results[:3]:
        print(f"  {similarity:.3f}  {script['id']}  {script['platform']:<8} {script['title']}")

    found[library] = [
        {"similarity": round(sim, 4), "id": s["id"], "platform": s["platform"], "title": s["title"]}
        for sim, s in results[:10]
    ]

(OUTPUT / "02_embeddings.json").write_text(
    json.dumps({"request": REQUEST, "request_vector": request_vector, "found": found}, indent=2)
)
