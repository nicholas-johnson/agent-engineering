# Model shootout — send the same questions to four OpenAI models and compare speed & tokens.
# Run from the module folder: uv run python playground/model-shootout/play.py
#                         or: source ../../.venv/bin/activate && python playground/model-shootout/play.py
#
# To play: add harder questions to QUESTIONS, add or swap model IDs in MODELS,
# or try reasoning={"effort": "high"} to compare latency and reasoning tokens.

import json
import time
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OUTPUT = Path(__file__).parent / "output"
OUTPUT.mkdir(exist_ok=True)

MODELS = ["gpt-6-luna", "gpt-6-sol", "gpt-6.1-terra", "gpt-6.1-sol"]
QUESTIONS = [
    "How many times does the letter r appear in the word strawberry?",
    "Why is a raven like a writing-desk?",
]

client = OpenAI()
results = []

# Time each model on each question; effort is "low" because gpt-6.1-sol requires reasoning.
for question in QUESTIONS:
    print(f"=== {question} ===")
    for model in MODELS:
        start = time.perf_counter()
        response = client.responses.create(
            model=model,
            reasoning={"effort": "low"},
            instructions="Answer in one or two sentences.",
            input=question,
        )
        seconds = time.perf_counter() - start

        usage = response.usage
        results.append(
            {
                "question": question,
                "model": model,
                "seconds": round(seconds, 2),
                "input_tokens": usage.input_tokens,
                "reasoning_tokens": usage.output_tokens_details.reasoning_tokens,
                "output_tokens": usage.output_tokens,
                "answer": response.output_text,
            }
        )
        print(f"{model:14} {seconds:5.1f}s  {usage.output_tokens:4} tokens  {response.output_text}")
    print()

# Full answers and reasoning-token breakdowns go to output/shootout.json.
(OUTPUT / "shootout.json").write_text(json.dumps(results, indent=2))
