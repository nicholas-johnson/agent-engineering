import json
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OUTPUT = Path(__file__).parent / "output"
OUTPUT.mkdir(exist_ok=True)

QUESTIONS = [
    "What is the March Hare's excuse for there being no room at the tea table?",
    "A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the ball. How much does the ball cost?",
    "Translate into French: 'Off with her head!' said the Queen.",
    "Write a Python function that returns the n-th Fibonacci number.",
]

closed = OpenAI()
local = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
results = []

for question in QUESTIONS:
    big = closed.responses.create(model="gpt-6-luna", reasoning={"effort": "none"}, input=question)
    small = local.responses.create(model="qwen3:1.7b", reasoning={"effort": "none"}, input=question)
    results.append({"question": question, "gpt-6-luna": big.output_text, "qwen3:1.7b": small.output_text})
    print(f"=== {question} ===")
    print(f"--- gpt-6-luna (OpenAI's servers) ---\n{big.output_text.strip()}")
    print(f"--- qwen3:1.7b (this laptop) ---\n{small.output_text.strip()}\n")

(OUTPUT / "answers.json").write_text(json.dumps(results, indent=2, ensure_ascii=False))
