import json
import os
import time
from pathlib import Path

import openai
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

DATA = Path(__file__).parent.parent / "data"
OUTPUT = Path(__file__).parent / "output"
OUTPUT.mkdir(exist_ok=True)

INSTRUCTIONS = "Answer directly. One sentence of working, then the answer. No role-play."
# Every label is wrong, and one tin has been opened. Weaker models swap the remaining two.
# Reasoning is off: otherwise a model can spend the whole cap thinking and print no answer.
QUESTION = (
    "Three tins are labelled 'marmalade', 'treacle' and 'marmalade and treacle'. "
    "Every label is wrong. You open the tin labelled 'marmalade and treacle' and find only marmalade. "
    "What is in each tin?"
)
# A cap keeps a reasoning model from writing an essay, and stops OpenRouter reserving
# tens of thousands of tokens against a small credit limit.
MAX_OUTPUT_TOKENS = 250

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
    parts = []
    stream = client.responses.create(
        model=model,
        instructions=INSTRUCTIONS,
        input=QUESTION,
        reasoning={"effort": "none"},
        max_output_tokens=MAX_OUTPUT_TOKENS,
        stream=True,
    )
    usage = None
    for event in stream:
        if event.type == "response.output_text.delta":
            if first_word is None:
                first_word = time.perf_counter() - start
            parts.append(event.delta)
        response = getattr(event, "response", None)
        if response is not None and getattr(response, "usage", None) is not None:
            usage = response.usage
    if usage is None:
        usage = type("Usage", (), {"input_tokens": 0, "output_tokens": 0})()
    return first_word, time.perf_counter() - start, usage, "".join(parts).strip()


print(QUESTION)
print()

scorecard = []
for where, model, price_id in OPTIONS:
    if where not in clients:
        scorecard.append({"model": model, "where": where, "skipped": "no API key"})
        print(f"=== {model} ===\nskipped: no API key\n")
        continue

    try:
        first_word, total, usage, reply = measure(clients[where], model)
    except Exception as error:
        message = str(error).split(" To increase")[0]
        scorecard.append({"model": model, "where": where, "skipped": message})
        print(f"=== {model} ===\n{message}\n")
        continue

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
            "reply": reply,
            "first_word_seconds": round(first_word or total, 2),
            "total_seconds": round(total, 2),
            "input_tokens": usage.input_tokens,
            "output_tokens": usage.output_tokens,
            "cost_per_1000_chats": cost_per_1000,
        }
    )
    print(f"=== {model} ===\n{reply}\n")

(OUTPUT / "06_scorecard.json").write_text(json.dumps(scorecard, indent=2))

print(f"{'Model':32} {'First word':>10} {'Total':>7} {'Tokens out':>10} {'Per 1,000 chats':>16}")
for row in scorecard:
    if "skipped" in row:
        reason = "skipped: no API key" if row["skipped"] == "no API key" else "failed"
        print(f"{row['model']:32} {reason:>46}")
    else:
        cost = f"${row['cost_per_1000_chats']:.4f}" if row["cost_per_1000_chats"] else "free"
        print(
            f"{row['model']:32} {row['first_word_seconds']:9.1f}s {row['total_seconds']:6.1f}s "
            f"{row['output_tokens']:10} {cost:>16}"
        )
