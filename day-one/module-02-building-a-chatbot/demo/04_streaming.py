# Run from the module folder: uv run python demo/04_streaming.py

from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OUTPUT = Path(__file__).parent / "output"
OUTPUT.mkdir(exist_ok=True)

MODEL = "gpt-6-luna"
INSTRUCTIONS = (
    "You are the Cheshire Cat from Alice's Adventures in Wonderland. "
    "You are mischievous and fond of riddles, but you always answer the question. "
    "Keep your replies to two or three sentences."
)

client = OpenAI()


def stream_reply(messages):
    stream = client.responses.create(
        model=MODEL,
        reasoning={"effort": "none"},
        instructions=INSTRUCTIONS,
        input=messages,
        stream=True,
    )
    reply = ""
    for event in stream:
        if event.type == "response.output_text.delta":
            print(event.delta, end="", flush=True)
            reply += event.delta
    print("\n")
    return reply


messages = []
transcript = []

while True:
    question = input("You: ")
    if not question:
        break

    messages.append({"role": "user", "content": question})
    print("Cat: ", end="", flush=True)
    reply = stream_reply(messages)
    messages.append({"role": "assistant", "content": reply})
    transcript.append(f"You: {question}\nCat: {reply}\n")

(OUTPUT / "04_streaming.txt").write_text("\n".join(transcript))
