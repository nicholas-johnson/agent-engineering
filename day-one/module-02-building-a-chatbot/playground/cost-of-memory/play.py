# The cost of memory — watch input tokens grow turn by turn as history is resent.
# Run from the module folder: uv run python playground/cost-of-memory/play.py
#                         or: source ../../.venv/bin/activate && python playground/cost-of-memory/play.py
#
# To play: add more turns to QUESTIONS, or slice `input=messages[-4:]` to cap memory
# and see what the chatbot forgets on the final question (see README.md).

from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OUTPUT = Path(__file__).parent / "output"
OUTPUT.mkdir(exist_ok=True)

MODEL = "gpt-6-luna"
QUESTIONS = [
    "Hello! My name is Alice.",
    "I've just fallen down a rabbit hole. Where am I?",
    "There's a little bottle labelled DRINK ME. Should I drink it?",
    "I drank it and now I'm ten inches tall. What now?",
    "There's a cake that says EAT ME. Should I eat it?",
    "Now I'm nine feet tall. This is getting silly.",
    "I've been crying and now there's a pool of tears. Any advice?",
    "A mouse is swimming past. Should I talk to it?",
    "The mouse got offended when I mentioned my cat. Why?",
    "Can you remind me of everything that has happened to me so far?",
]

client = OpenAI()
messages = []
rows = ["turn,input_tokens,cached_tokens,output_tokens"]
total_input = 0

# Play out the conversation, resending the entire `messages` list on every turn.
print("Turn  Input tokens  Output tokens")
for turn, question in enumerate(QUESTIONS, start=1):
    messages.append({"role": "user", "content": question})
    response = client.responses.create(
        model=MODEL,
        reasoning={"effort": "none"},
        instructions="Keep your replies to two or three sentences.",
        input=messages,
    )
    messages.append({"role": "assistant", "content": response.output_text})

    usage = response.usage
    total_input += usage.input_tokens
    cached = usage.input_tokens_details.cached_tokens
    rows.append(f"{turn},{usage.input_tokens},{cached},{usage.output_tokens}")
    print(f"{turn:4}  {usage.input_tokens:12}  {usage.output_tokens:13}")

print(f"\nTotal input tokens over {len(QUESTIONS)} turns: {total_input}")
print(f"\nLast reply: {response.output_text}")
(OUTPUT / "tokens_per_turn.csv").write_text("\n".join(rows) + "\n")
