# Chatbot — a complete streaming chatbot with memory and every knob at the top.
# Run from the module folder: uv run python playground/chatbot/play.py
#                         or: source ../../.venv/bin/activate && python playground/chatbot/play.py
#
# To play: tweak MODEL, REASONING_EFFORT, TEMPERATURE, MAX_OUTPUT_TOKENS or INSTRUCTIONS
# below (note: remove `temperature=` if REASONING_EFFORT is anything other than "none").

from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OUTPUT = Path(__file__).parent / "output"
OUTPUT.mkdir(exist_ok=True)

# Chatbot settings — try changing these and see how the replies feel.
MODEL = "gpt-6-luna"          # try "gpt-6-sol"
REASONING_EFFORT = "none"     # "none", "low", "medium" or "high"
TEMPERATURE = 1.0             # 0.0 to 2.0 (only allowed when REASONING_EFFORT is "none")
MAX_OUTPUT_TOKENS = 500       # cut-off length for each reply (try 20)
INSTRUCTIONS = "You are a helpful assistant. Keep your replies short."

client = OpenAI()
messages = []    # full conversation history sent on every turn
transcript = []

# Chat loop: press Enter on an empty line to quit.
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

    # Print each chunk of text as it arrives from the API.
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
