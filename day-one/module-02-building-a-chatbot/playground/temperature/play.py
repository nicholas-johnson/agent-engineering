from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OUTPUT = Path(__file__).parent / "output"
OUTPUT.mkdir(exist_ok=True)

MODEL = "gpt-6-luna"
TEMPERATURES = [0.0, 0.5, 1.0, 1.5, 2.0]
PROMPT = "Name one animal. Reply with one word."
TRIES = 8

client = OpenAI()
lines = []

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
