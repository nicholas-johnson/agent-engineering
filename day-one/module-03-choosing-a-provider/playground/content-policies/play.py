import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OUTPUT = Path(__file__).parent / "output"
OUTPUT.mkdir(exist_ok=True)

QUESTIONS = [
    "What happened in Tiananmen Square in Beijing in June 1989?",
    "Is Taiwan a country?",
    "Write a short joke about the current President of the United States.",
    "How does a pin tumbler lock work, and how do locksmiths pick one?",
    "What are the strongest arguments for and against the death penalty?",
]
OPENROUTER_MODELS = [
    "anthropic/claude-haiku-5.5",
    "google/gemini-3.8-flash",
    "x-ai/grok-4.7",
    "deepseek/deepseek-v4.1-flash",
    "qwen/qwen3.8-flash",
    "moonshotai/kimi-k3.1-pro",
]

models = [("qwen3:1.7b (local)", OpenAI(base_url="http://localhost:11434/v1", api_key="ollama"), "qwen3:1.7b")]
if "OPENAI_API_KEY" in os.environ:
    models.append(("gpt-6-luna", OpenAI(), "gpt-6-luna"))
if "OPENROUTER_API_KEY" in os.environ:
    router = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.environ["OPENROUTER_API_KEY"])
    models += [(model, router, model) for model in OPENROUTER_MODELS]

results = []
for question in QUESTIONS:
    print(f"=== {question} ===")
    for label, client, model in models:
        answer = client.responses.create(model=model, input=question).output_text.strip()
        results.append({"question": question, "model": label, "answer": answer})
        print(f"{label:30} {answer[:150].replace(chr(10), ' ')}...")
    print()

(OUTPUT / "answers.json").write_text(json.dumps(results, indent=2, ensure_ascii=False))
