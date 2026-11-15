# Local models — compare two sizes of Qwen3 running locally in Ollama.
# Pull the models first:      ollama pull qwen3:0.6b && ollama pull qwen3:1.7b
# Run from the module folder: uv run python playground/local-models/play.py
#                         or: source ../../.venv/bin/activate && python playground/local-models/play.py
#
# To play: pull larger or different Ollama models and add them to MODELS, add your own
# questions to QUESTIONS, or remove reasoning={"effort": "none"} to let Qwen3 think.

import time
from pathlib import Path

from openai import OpenAI

OUTPUT = Path(__file__).parent / "output"
OUTPUT.mkdir(exist_ok=True)

# Every model here must be pulled in Ollama first (e.g. `ollama pull qwen3:4b`).
MODELS = ["qwen3:0.6b", "qwen3:1.7b"]
QUESTIONS = [
    "Who wrote Alice's Adventures in Wonderland, and in what year was it published?",
    "If Alice is 7 and her sister is twice her age, how old will her sister be in 3 years?",
    "Write one sentence describing the Cheshire Cat.",
]

# Ollama speaks OpenAI's Responses API locally on port 11434; no real API key needed.
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
lines = []

for question in QUESTIONS:
    print(f"=== {question} ===")
    lines.append(f"=== {question} ===")
    for model in MODELS:
        start = time.perf_counter()
        response = client.responses.create(model=model, reasoning={"effort": "none"}, input=question)
        seconds = time.perf_counter() - start
        answer = response.output_text.strip().replace("\n", " ")
        print(f"{model:12} {seconds:4.1f}s  {answer}")
        lines.append(f"{model:12} {seconds:4.1f}s  {answer}")
    print()
    lines.append("")

(OUTPUT / "answers.txt").write_text("\n".join(lines))
