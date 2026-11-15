# Run from the module folder: uv run python demo/04_agent.py

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
    "Which Magic: The Gathering rabbit creature is worth the most right now, "
    "what does it do, and what is the square root of its price?"
)

MATHS_SERVER = StdioServerParameters(command=sys.executable, args=[str(HERE / "03_maths_server.py")])
CARDS_SERVER = StdioServerParameters(command=sys.executable, args=[str(HERE / "04_cards_server.py")])

openai = OpenAI()


async def main():
    async with Client(MATHS_SERVER) as maths, Client(CARDS_SERVER) as cards:
        # Collect the tools from both servers, and remember which server owns each one.
        tools, owners = [], {}
        for server in [maths, cards]:
            for tool in (await server.list_tools()).tools:
                tools.append(
                    {
                        "type": "function",
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.input_schema,
                    }
                )
                owners[tool.name] = server

        conversation = [{"role": "user", "content": QUESTION}]
        print(f"You: {QUESTION}")

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
                result = await owners[call.name].call_tool(call.name, json.loads(call.arguments))
                answer = result.content[0].text
                print(f"  [tool] {call.name}({call.arguments}) -> {answer[:100]}")
                conversation.append(
                    {"type": "function_call_output", "call_id": call.call_id, "output": answer}
                )

        print(f"Agent: {response.output_text}")

    transcript = [item if isinstance(item, dict) else item.model_dump() for item in conversation]
    (OUTPUT / "04_agent.json").write_text(json.dumps(transcript, indent=2))


asyncio.run(main())
