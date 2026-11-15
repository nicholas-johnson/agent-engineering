import json
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

DATA = Path(__file__).parent.parent / "data"
OUTPUT = Path(__file__).parent / "output"
OUTPUT.mkdir(exist_ok=True)

INSTRUCTIONS = (
    "You are the Cheshire Cat from Alice's Adventures in Wonderland. "
    "You are mischievous and fond of riddles, but you always answer the question. "
    "Keep your replies to two or three sentences."
)
QUESTION = "Would you tell me, please, which way I ought to go from here?"

# (where it runs, model name there, model id in prices.json)
OPTIONS = [
    ("openai", "gpt-6-luna", "openai/gpt-6-luna"),
    ("openrouter", "anthropic/claude-haiku-5.5", "anthropic/claude-haiku-5.5"),
    ("openrouter", "anthropic/claude-opus-5.5", "anthropic/claude-opus-5.5"),
    ("openrouter", "google/gemini-3.8-flash", "google/gemini-3.8-flash"),
    ("openrouter", "x-ai/grok-4.7", "x-ai/grok-4.7"),
    ("openrouter", "deepseek/deepseek-v4.1-flash", "deepseek/deepseek-v4.1-flash"),
    ("openrouter", "qwen/qwen3.8-flash", "qwen/qwen3.8-flash"),
    ("openrouter", "mistralai/mistral-small-2603", "mistralai/mistral-small-2603"),
    ("ollama", "qwen3:1.7b", None),
]

prices = {model["id"]: model for model in json.loads((DATA / "prices.json").read_text())["models"]}

clients = {"ollama": OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")}
if "OPENAI_API_KEY" in os.environ:
    clients["openai"] = OpenAI()
if "OPENROUTER_API_KEY" in os.environ:
    clients["openrouter"] = OpenAI(
        base_url="https://openrouter.ai/api/v1", api_key=os.environ["OPENROUTER_API_KEY"]
    )


def measure(client, model):
    start = time.perf_counter()
    first_word = None
    stream = client.responses.create(
        model=model, instructions=INSTRUCTIONS, input=QUESTION, stream=True
    )
    for event in stream:
        if event.type == "response.output_text.delta" and first_word is None:
            first_word = time.perf_counter() - start
        if event.type == "response.completed":
            usage = event.response.usage
    return first_word, time.perf_counter() - start, usage


scorecard = []
for where, model, price_id in OPTIONS:
    if where not in clients:
        scorecard.append({"model": model, "where": where, "skipped": "no API key"})
        continue

    first_word, total, usage = measure(clients[where], model)
    if price_id:
        price = prices[price_id]
        cost = usage.input_tokens * price["input_per_million"] + usage.output_tokens * price["output_per_million"]
        cost_per_1000 = round(cost / 1000, 4)
    else:
        cost_per_1000 = 0.0
    scorecard.append(
        {
            "model": model,
            "where": where,
            "first_word_seconds": round(first_word, 2),
            "total_seconds": round(total, 2),
            "input_tokens": usage.input_tokens,
            "output_tokens": usage.output_tokens,
            "cost_per_1000_chats": cost_per_1000,
        }
    )

(OUTPUT / "06_scorecard.json").write_text(json.dumps(scorecard, indent=2))

print(f"{'Model':32} {'First word':>10} {'Total':>7} {'Tokens out':>10} {'Per 1,000 chats':>16}")
for row in scorecard:
    if "skipped" in row:
        print(f"{row['model']:32} {'skipped: no API key':>46}")
    else:
        cost = f"${row['cost_per_1000_chats']:.4f}" if row["cost_per_1000_chats"] else "free"
        print(
            f"{row['model']:32} {row['first_word_seconds']:9.1f}s {row['total_seconds']:6.1f}s "
            f"{row['output_tokens']:10} {cost:>16}"
        )
