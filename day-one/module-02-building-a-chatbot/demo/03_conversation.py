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
messages = []
transcript = []

while True:
    question = input("You: ")
    if not question:
        break

    messages.append({"role": "user", "content": question})
    response = client.responses.create(
        model=MODEL,
        reasoning={"effort": "none"},
        instructions=INSTRUCTIONS,
        input=messages,
    )
    messages.append({"role": "assistant", "content": response.output_text})

    print(f"Cat: {response.output_text}\n")
    usage = response.usage
    transcript.append(
        f"You: {question}\nCat: {response.output_text}\n"
        f"(input tokens: {usage.input_tokens}, output tokens: {usage.output_tokens})\n"
    )

(OUTPUT / "03_conversation.txt").write_text("\n".join(transcript))
