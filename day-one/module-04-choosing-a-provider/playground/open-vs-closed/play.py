# Open versus closed — pit a small local model on your laptop against a hosted frontier model.
# Needs OPENAI_API_KEY in .env, plus Ollama running (`ollama pull qwen3:1.7b`).
# Run from the module folder: uv run python playground/open-vs-closed/play.py
#                         or: source ../../.venv/bin/activate && python playground/open-vs-closed/play.py
#
# To play: replace QUESTIONS with tasks from your own work, or swap model names below
# to compare against a larger open model via OpenRouter (see README.md).

import json
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OUTPUT = Path(__file__).parent / "output"
OUTPUT.mkdir(exist_ok=True)

CLOSED_MODEL = "gpt-6-luna"
LOCAL_MODEL = "qwen3:1.7b"

QUESTIONS = [
    "What is the March Hare's excuse for there being no room at the tea table?",
    "A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the ball. How much does the ball cost?",
    "Translate into French: 'Off with her head!' said the Queen.",
    "Write a Python function that returns the n-th Fibonacci number.",
]

# Same OpenAI client class for both: one talks to OpenAI, the other to local Ollama.
closed = OpenAI()
local = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
results = []

for question in QUESTIONS:
    big = closed.responses.create(model=CLOSED_MODEL, reasoning={"effort": "none"}, input=question)
    small = local.responses.create(model=LOCAL_MODEL, reasoning={"effort": "none"}, input=question)
    results.append({"question": question, CLOSED_MODEL: big.output_text, LOCAL_MODEL: small.output_text})
    print(f"=== {question} ===")
    print(f"--- {CLOSED_MODEL} (OpenAI's servers) ---\n{big.output_text.strip()}")
    print(f"--- {LOCAL_MODEL} (this laptop) ---\n{small.output_text.strip()}\n")

(OUTPUT / "answers.json").write_text(json.dumps(results, indent=2, ensure_ascii=False))
