# Run from the module folder: uv run python demo/01_one_response.py

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

response = client.responses.create(
    model=MODEL,
    reasoning={"effort": "none"},
    instructions=INSTRUCTIONS,
    input="Would you tell me, please, which way I ought to go from here?",
)

(OUTPUT / "01_response.json").write_text(response.model_dump_json(indent=2))
print(response.output_text)
