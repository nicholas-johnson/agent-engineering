import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OUTPUT = Path(__file__).parent / "output"
OUTPUT.mkdir(exist_ok=True)

INSTRUCTIONS = (
    "You are the Cheshire Cat from Alice's Adventures in Wonderland. "
    "You are mischievous and fond of riddles, but you always answer the question. "
    "Keep your replies to two or three sentences."
)
QUESTION = "Would you tell me, please, which way I ought to go from here?"
MODELS = [
    "openai/gpt-6-luna",
    "anthropic/claude-haiku-5.5",
    "google/gemini-3.8-flash",
    "x-ai/grok-4.7",
    "meta/muse-spark-open",
    "mistralai/mistral-large-4-0",
    "cohere/command-a-plus",
]

if "OPENROUTER_API_KEY" not in os.environ:
    raise SystemExit("This demo needs OPENROUTER_API_KEY in .env")

client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.environ["OPENROUTER_API_KEY"])
answers = {}

for model in MODELS:
    response = client.responses.create(model=model, instructions=INSTRUCTIONS, input=QUESTION)
    answers[model] = response.output_text
    print(f"=== {model} ===\n{response.output_text}\n")

(OUTPUT / "02_one_key.json").write_text(json.dumps(answers, indent=2))
