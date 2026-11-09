import json
import math
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OUTPUT = Path(__file__).parent / "output"
OUTPUT.mkdir(exist_ok=True)

MODEL = "gpt-6-luna"
PROMPTS = [
    "Alice was beginning to get",
    "The capital of France is",
    "My favourite colour is",
]

client = OpenAI()
results = {}

for prompt in PROMPTS:
    response = client.responses.create(
        model=MODEL,
        reasoning={"effort": "none"},
        instructions="Continue the text. Reply with the continuation only.",
        input=prompt,
        max_output_tokens=16,
        top_logprobs=5,
        include=["message.output_text.logprobs"],
    )
    tokens = response.output[0].content[0].logprobs

    print(f"=== {prompt} ===")
    results[prompt] = []
    for token in tokens:
        options = {option.token: round(math.exp(option.logprob), 4) for option in token.top_logprobs}
        results[prompt].append({"token": token.token, "top_5": options})
        print(f"{token.token!r:14} " + ", ".join(f"{t!r} {p:.0%}" for t, p in options.items()))
    print()

(OUTPUT / "logprobs.json").write_text(json.dumps(results, indent=2))
