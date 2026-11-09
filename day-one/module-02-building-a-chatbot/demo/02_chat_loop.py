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
transcript = []

while True:
    question = input("You: ")
    if not question:
        break

    response = client.responses.create(
        model=MODEL,
        reasoning={"effort": "none"},
        instructions=INSTRUCTIONS,
        input=question,
    )
    print(f"Cat: {response.output_text}\n")
    transcript.append(f"You: {question}\nCat: {response.output_text}\n")

(OUTPUT / "02_chat_loop.txt").write_text("\n".join(transcript))
