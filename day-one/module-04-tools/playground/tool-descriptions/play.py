import json
import math
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OUTPUT = Path(__file__).parent / "output"
OUTPUT.mkdir(exist_ok=True)

MODEL = "gpt-6-luna"
INSTRUCTIONS = "Answer in plain text, without LaTeX or Markdown."
QUESTION = "What is the square root of 7,654,321, to 10 decimal places?"

# The same function every time. Only the description the model sees changes.
DESCRIPTIONS = {
    "clear": "Return the square root of a number, exactly, to full precision.",
    "vague": "Does a calculation.",
    "wrong": "Returns the cube root of a number.",
}

client = OpenAI()
results = {}

for label, description in DESCRIPTIONS.items():
    tools = [
        {
            "type": "function",
            "name": "calculate",
            "description": description,
            "parameters": {
                "type": "object",
                "properties": {"number": {"type": "number"}},
                "required": ["number"],
            },
        }
    ]
    conversation = [{"role": "user", "content": QUESTION}]
    used_tool = False
    while True:
        response = client.responses.create(
            model=MODEL,
            reasoning={"effort": "none"},
            instructions=INSTRUCTIONS,
            input=conversation,
            tools=tools,
        )
        conversation += response.output
        calls = [item for item in response.output if item.type == "function_call"]
        if not calls:
            break
        used_tool = True
        for call in calls:
            answer = str(math.sqrt(json.loads(call.arguments)["number"]))
            conversation.append({"type": "function_call_output", "call_id": call.call_id, "output": answer})

    results[label] = {"description": description, "used_tool": used_tool, "answer": response.output_text}
    print(f"=== {label}: \"{description}\" ===")
    print(f"Used the tool: {'yes' if used_tool else 'no'}")
    print(f"Agent: {response.output_text}\n")

print(f"The right answer: {math.sqrt(7654321):.10f}")
(OUTPUT / "results.json").write_text(json.dumps(results, indent=2))
