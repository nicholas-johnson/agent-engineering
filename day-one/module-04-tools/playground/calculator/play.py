# Calculator — watch an agent plan multi-step calculations across six MCP maths tools.
# Run from the module folder: uv run python playground/calculator/play.py
#                         or: source ../../.venv/bin/activate && python playground/calculator/play.py
#
# To play: add multi-step word problems to QUESTIONS, remove "Use the tools for every
# calculation." from INSTRUCTIONS, or add/remove tools in server.py (see README.md).

import asyncio
import json
import sys
from pathlib import Path

from dotenv import load_dotenv
from mcp import Client
from mcp.client.stdio import StdioServerParameters
from openai import OpenAI

load_dotenv()

HERE = Path(__file__).parent
OUTPUT = HERE / "output"
OUTPUT.mkdir(exist_ok=True)

MODEL = "gpt-6-luna"
INSTRUCTIONS = "Answer in plain text, without LaTeX or Markdown. Use the tools for every calculation."
QUESTIONS = [
    "If I put 1,000 pounds in a savings account paying 4.5% interest a year, how much will I have after 17 years?",
    "What is 2 to the power of 100?",
    "A rectangle is 1,234.5 cm by 678.9 cm. How long is its diagonal?",
]

# Start server.py in a subprocess using the same Python interpreter that ran play.py.
SERVER = StdioServerParameters(command=sys.executable, args=[str(HERE / "server.py")])
openai = OpenAI()


async def ask(calculator, tools, question):
    # Tool loop: ask the model, run any tool calls it requests, and repeat until it answers.
    conversation = [{"role": "user", "content": question}]
    print(f"You: {question}")
    while True:
        response = openai.responses.create(
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
        for call in calls:
            result = await calculator.call_tool(call.name, json.loads(call.arguments))
            answer = result.content[0].text
            print(f"  [tool] {call.name}({call.arguments}) -> {answer}")
            conversation.append({"type": "function_call_output", "call_id": call.call_id, "output": answer})
    print(f"Agent: {response.output_text}\n")
    return [item if isinstance(item, dict) else item.model_dump() for item in conversation]


async def main():
    # Connect to the MCP server, fetch its tool definitions, and run each question.
    async with Client(SERVER) as calculator:
        tools = [
            {"type": "function", "name": t.name, "description": t.description, "parameters": t.input_schema}
            for t in (await calculator.list_tools()).tools
        ]
        transcripts = [await ask(calculator, tools, question) for question in QUESTIONS]
    (OUTPUT / "conversations.json").write_text(json.dumps(transcripts, indent=2))


asyncio.run(main())
