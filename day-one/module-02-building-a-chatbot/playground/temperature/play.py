# Temperature — ask a real model the same question across temperatures 0.0 to 2.0.
# Run from the module folder: uv run python playground/temperature/play.py
#                         or: source ../../.venv/bin/activate && python playground/temperature/play.py
#
# To play: change PROMPT (try an open-ended opening line), increase TRIES,
# or pass top_p=... alongside temperature in responses.create() (see README.md).

from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OUTPUT = Path(__file__).parent / "output"
OUTPUT.mkdir(exist_ok=True)

MODEL = "gpt-6-luna"
TEMPERATURES = [0.0, 0.5, 1.0, 1.5, 2.0]  # 2.0 is the API maximum
PROMPT = "Name one animal. Reply with one word."
TRIES = 8

client = OpenAI()
lines = []

# Ask PROMPT TRIES times at each temperature; reasoning must be "none" for temperature to work.
for temperature in TEMPERATURES:
    answers = []
    for _ in range(TRIES):
        response = client.responses.create(
            model=MODEL,
            reasoning={"effort": "none"},
            temperature=temperature,
            max_output_tokens=16,
            input=PROMPT,
        )
        answers.append(response.output_text.strip())
    line = f"{temperature:3}  {', '.join(answers)}"
    print(line)
    lines.append(line)

(OUTPUT / "temperatures.txt").write_text(f"{PROMPT}\n\n" + "\n".join(lines) + "\n")
