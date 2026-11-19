# Run from the module folder: uv run python demo/01_just_ask.py

import json
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

HERE = Path(__file__).parent
OUTPUT = HERE / "output"
OUTPUT.mkdir(exist_ok=True)

MODEL = "gpt-6-luna"
INSTRUCTIONS = "You are the support assistant for Dormouse, a smart thermostat. Answer the customer in a short paragraph."
QUESTIONS = [
    "Why does my Dormouse turn the heating on before the time I set?",
    "My thermostat is showing E-305. What should I do?",
    "How much does a Dormouse thermostat cost?",
]

client = OpenAI()

answers = []
for question in QUESTIONS:
    response = client.responses.create(
        model=MODEL,
        reasoning={"effort": "none"},
        instructions=INSTRUCTIONS,
        input=question,
    )
    print(f"\nQ: {question}\nA: {response.output_text}")
    answers.append({"question": question, "answer": response.output_text})

(OUTPUT / "01_just_ask.json").write_text(json.dumps({"instructions": INSTRUCTIONS, "answers": answers}, indent=2))
