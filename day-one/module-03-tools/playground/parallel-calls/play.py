# Parallel calls — ask about five Magic cards at once and watch the model batch tool calls.
# Run from the module folder: uv run python playground/parallel-calls/play.py
#                         or: source ../../.venv/bin/activate && python playground/parallel-calls/play.py
#
# To play: pass parallel_tool_calls=False to responses.create() to compare round counts,
# or ask a question where one lookup depends on the result of another (see README.md).

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
INSTRUCTIONS = "Answer in plain text, without LaTeX or Markdown."
QUESTION = (
    "What are these Magic: The Gathering cards worth right now: Sol Ring, Lightning Bolt, "
    "Counterspell, Llanowar Elves and Dark Ritual? Which is the most expensive?"
)

# Launch the Scryfall MCP server from demo/04_cards_server.py automatically.
CARDS_SERVER = StdioServerParameters(
    command=sys.executable, args=[str(HERE.parent.parent / "demo" / "04_cards_server.py")]
)
openai = OpenAI()


async def main():
    async with Client(CARDS_SERVER) as cards:
        tools = [
            {"type": "function", "name": t.name, "description": t.description, "parameters": t.input_schema}
            for t in (await cards.list_tools()).tools
        ]
        conversation = [{"role": "user", "content": QUESTION}]
        print(f"You: {QUESTION}")

        # Count how many model round trips it takes; one response can request multiple calls.
        rounds = 0
        while True:
            response = openai.responses.create(
                model=MODEL,
                reasoning={"effort": "none"},
                instructions=INSTRUCTIONS,
                input=conversation,
                tools=tools,
            )
            rounds += 1
            conversation += response.output
            calls = [item for item in response.output if item.type == "function_call"]
            if not calls:
                break
            print(f"Round {rounds}: the model asked for {len(calls)} tool calls at once")
            for call in calls:
                result = await cards.call_tool(call.name, json.loads(call.arguments))
                answer = result.content[0].text
                print(f"  [tool] {call.name}({call.arguments})")
                conversation.append({"type": "function_call_output", "call_id": call.call_id, "output": answer})

        print(f"Round {rounds}: the answer\nAgent: {response.output_text}")

    transcript = [item if isinstance(item, dict) else item.model_dump() for item in conversation]
    (OUTPUT / "conversation.json").write_text(json.dumps(transcript, indent=2))


asyncio.run(main())
