from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OUTPUT = Path(__file__).parent / "output"
OUTPUT.mkdir(exist_ok=True)

MODEL = "gpt-6-luna"
REASONING_EFFORT = "none"
TEMPERATURE = 1.0  # only allowed when REASONING_EFFORT is "none"
MAX_OUTPUT_TOKENS = 500
INSTRUCTIONS = "You are a helpful assistant. Keep your replies short."

client = OpenAI()
messages = []
transcript = []

while True:
    question = input("You: ")
    if not question:
        break

    messages.append({"role": "user", "content": question})
    stream = client.responses.create(
        model=MODEL,
        reasoning={"effort": REASONING_EFFORT},
        temperature=TEMPERATURE,
        max_output_tokens=MAX_OUTPUT_TOKENS,
        instructions=INSTRUCTIONS,
        input=messages,
        stream=True,
    )

    print("Bot: ", end="", flush=True)
    reply = ""
    for event in stream:
        if event.type == "response.output_text.delta":
            print(event.delta, end="", flush=True)
            reply += event.delta
    print("\n")

    messages.append({"role": "assistant", "content": reply})
    transcript.append(f"You: {question}\nBot: {reply}\n")
    (OUTPUT / "conversation.txt").write_text("\n".join(transcript))
