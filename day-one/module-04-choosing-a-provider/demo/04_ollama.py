# Run from the module folder: uv run python demo/04_ollama.py

from pathlib import Path

from openai import OpenAI

OUTPUT = Path(__file__).parent / "output"
OUTPUT.mkdir(exist_ok=True)

MODEL = "qwen3:1.7b"
INSTRUCTIONS = (
    "You are the Cheshire Cat from Alice's Adventures in Wonderland. "
    "You are mischievous and fond of riddles, but you always answer the question. "
    "Keep your replies to two or three sentences."
)
QUESTION = "Would you tell me, please, which way I ought to go from here?"

# Ollama runs on your own machine. No API key, and nothing leaves your laptop.
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

stream = client.responses.create(
    model=MODEL,
    reasoning={"effort": "none"},
    instructions=INSTRUCTIONS,
    input=QUESTION,
    stream=True,
)

print(f"=== {MODEL}, on this laptop ===")
reply = ""
for event in stream:
    if event.type == "response.output_text.delta":
        print(event.delta, end="", flush=True)
        reply += event.delta
print()

(OUTPUT / "04_ollama.txt").write_text(f"{QUESTION}\n\n{reply}\n")
