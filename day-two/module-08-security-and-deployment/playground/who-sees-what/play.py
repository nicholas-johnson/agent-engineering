# Who sees what — search the knowledge base as a customer and as a support agent, and filter before or after.
# Run from the module folder: uv run python playground/who-sees-what/play.py
#                         or: source ../../.venv/bin/activate && python playground/who-sees-what/play.py
#
# To play: change QUESTION, add a role to ROLES, or set FILTER = "after" and count what a customer is left with.
# No API key needed: it uses a simple keyword search, so it runs in a moment.

import json
import math
import re
from pathlib import Path

HERE = Path(__file__).parent
KB = HERE.parent.parent / "data" / "kb"
OUTPUT = HERE / "output"
OUTPUT.mkdir(exist_ok=True)

TOP = 5
QUESTION = "Why does my thermostat click so loudly? Can I have a replacement?"
# Which audiences each role may read. Every document says its audience in its front matter.
ROLES = {
    "customer": ["customer"],
    "support agent": ["customer", "internal"],
}
FILTER = "before"  # "before": search only what the role may read. "after": search everything, then remove the rest.
COMMON = set("a an and are as at be by can do does for from has have how i if in is it its my of on or so that the this to what when why with you your".split())


def load_chunks():
    # One chunk per section, labelled with its document's audience.
    chunks = []
    for path in sorted(KB.glob("*.md")):
        _, front, body = path.read_text().split("---", 2)
        audience = re.search(r"audience: (\w+)", front)[1]
        for section in re.split(r"\n(?=#{1,3} )", body.strip()):
            heading = section.splitlines()[0].lstrip("# ")
            chunks.append({"id": f"{path.name}#{heading}", "audience": audience, "text": section})
    return chunks


def words(text):
    # Lower case, without common words, and "clicking", "clicks" and "clicked" all become "click".
    found = re.findall(r"[a-z]+", text.lower())
    return [re.sub(r"(ing|ed|es|s)$", "", w) if len(w) > 4 else w for w in found if w not in COMMON]


def rarity(chunks):
    # A word in every chunk ("thermostat") tells you little; a rare one ("click") tells you a lot.
    seen = [set(words(c["text"])) for c in chunks]
    return {w: math.log(len(chunks) / sum(w in s for s in seen)) for w in set().union(*seen)}


def score(question, chunk):
    found = set(words(chunk["text"]))
    return round(sum(RARITY.get(w, 0) for w in set(words(question)) if w in found), 1)


def search(chunks, question, audiences):
    allowed = [c for c in chunks if c["audience"] in audiences]
    if FILTER == "before":
        return sorted(allowed, key=lambda c: -score(question, c))[:TOP]
    top = sorted(chunks, key=lambda c: -score(question, c))[:TOP]
    return [c for c in top if c["audience"] in audiences]


chunks = load_chunks()
RARITY = rarity(chunks)
print(f"{len(chunks)} chunks. Question: {QUESTION}")
print(f"Filtering {FILTER} the search.\n")
results = {}
for role, audiences in ROLES.items():
    found = search(chunks, QUESTION, audiences)
    results[role] = [c["id"] for c in found]
    print(f"As a {role} ({', '.join(audiences)}): {len(found)} of {TOP} results")
    for c in found:
        print(f"  {score(QUESTION, c):>4}  {c['audience']:<9} {c['id']}")
    print()

(OUTPUT / "results.json").write_text(json.dumps({"question": QUESTION, "filter": FILTER, "results": results}, indent=2))
