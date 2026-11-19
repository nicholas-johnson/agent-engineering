# Run from the module folder: uv run python demo/02_whole_manual.py

import json
import time
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

HERE = Path(__file__).parent
DOCS = HERE.parent / "data" / "docs"
OUTPUT = HERE / "output"
OUTPUT.mkdir(exist_ok=True)

MODEL = "gpt-6-luna"
# Dollars per million tokens, from Module 4's price list (checked 10 November 2026).
INPUT_PRICE = 0.10
OUTPUT_PRICE = 0.50
INSTRUCTIONS = "You are the support assistant for Dormouse, a smart thermostat. Answer the customer in a short paragraph."
QUESTION = "Why does my Dormouse turn the heating on before the time I set?"

client = OpenAI()


def ask(question, documentation):
    start = time.perf_counter()
    response = client.responses.create(
        model=MODEL,
        reasoning={"effort": "none"},
        instructions=f"{INSTRUCTIONS}\n\nUse our documentation:\n\n{documentation}",
        input=question,
    )
    seconds = time.perf_counter() - start
    usage = response.usage
    cost = (usage.input_tokens * INPUT_PRICE + usage.output_tokens * OUTPUT_PRICE) / 1_000_000
    return {
        "answer": response.output_text,
        "input_tokens": usage.input_tokens,
        "output_tokens": usage.output_tokens,
        "cost_dollars": round(cost, 5),
        "seconds": round(seconds, 1),
    }


user_guide = (DOCS / "user-guide.md").read_text()
everything = "\n\n".join(path.read_text() for path in sorted(DOCS.glob("*.md")))
libraries = {
    "The user guide": (1, user_guide),
    "The whole knowledge base": (len(list(DOCS.glob("*.md"))), everything),
}

results = {}
for name, (count, documentation) in libraries.items():
    print(f"\n=== {name}: {count:,} document{'s' * (count > 1)} ===")
    result = ask(QUESTION, documentation)
    print(f"Q: {QUESTION}\nA: {result['answer']}")
    print(f"   {result['input_tokens']:,} tokens in, ${result['cost_dollars']:.4f}, {result['seconds']} seconds")
    results[name] = result

(OUTPUT / "02_whole_manual.json").write_text(json.dumps({"question": QUESTION, "results": results}, indent=2))
