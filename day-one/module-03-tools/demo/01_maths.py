# Run from the module folder: uv run python demo/01_maths.py

import json
import math
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OUTPUT = Path(__file__).parent / "output"
OUTPUT.mkdir(exist_ok=True)

MODEL = "gpt-6-luna"
INSTRUCTIONS = "Answer in plain text, without LaTeX or Markdown."
QUESTION = "What is the square root of 7,654,321, to 10 decimal places?"

client = OpenAI()
answers = []

print(f"You: {QUESTION}")
for _ in range(3):
    response = client.responses.create(
        model=MODEL,
        reasoning={"effort": "none"},
        instructions=INSTRUCTIONS,
        input=QUESTION,
    )
    answers.append(response.output_text)
    print(f"Model: {response.output_text}")

print(f"\nThe right answer: {math.sqrt(7654321):.10f}")

(OUTPUT / "01_maths.json").write_text(json.dumps({"question": QUESTION, "answers": answers}, indent=2))
