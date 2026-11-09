from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

HERE = Path(__file__).parent
OUTPUT = HERE / "output"
OUTPUT.mkdir(exist_ok=True)

MODEL = "gpt-6-luna"

personas = sorted((HERE / "instructions").glob("*.txt"))
for number, persona in enumerate(personas, start=1):
    print(f"{number}. {persona.stem}")
persona = personas[int(input("Choose a persona: ")) - 1]
instructions = persona.read_text()
print(f"\nYou are talking to: {persona.stem}\n")

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
        reasoning={"effort": "none"},
        instructions=instructions,
        input=messages,
        stream=True,
    )

    print(f"{persona.stem}: ", end="", flush=True)
    reply = ""
    for event in stream:
        if event.type == "response.output_text.delta":
            print(event.delta, end="", flush=True)
            reply += event.delta
    print("\n")

    messages.append({"role": "assistant", "content": reply})
    transcript.append(f"You: {question}\n{persona.stem}: {reply}\n")
    (OUTPUT / f"{persona.stem}.txt").write_text("\n".join(transcript))
