# Weather server — a clean two-tool MCP agent template using the free Open-Meteo API.
# Run from the module folder: uv run python playground/weather-server/play.py
#                         or: source ../../.venv/bin/activate && python playground/weather-server/play.py
#
# To play: change QUESTION (try comparing several cities), add a new tool in server.py,
# or copy this folder to wrap another free API of your own (see README.md).

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
QUESTION = "Is tomorrow a good day for a picnic by the river in Oxford, where Lewis Carroll first told the story of Alice?"

# Start server.py automatically as a subprocess.
SERVER = StdioServerParameters(command=sys.executable, args=[str(HERE / "server.py")])
openai = OpenAI()


async def main():
    # Connect to the weather MCP server, advertise its tools to the model, and run the loop.
    async with Client(SERVER) as weather:
        tools = [
            {"type": "function", "name": t.name, "description": t.description, "parameters": t.input_schema}
            for t in (await weather.list_tools()).tools
        ]
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
                result = await weather.call_tool(call.name, json.loads(call.arguments))
                answer = result.content[0].text
                print(f"  [tool] {call.name}({call.arguments}) -> {answer[:100]}")
                conversation.append({"type": "function_call_output", "call_id": call.call_id, "output": answer})
        print(f"Agent: {response.output_text}")

    transcript = [item if isinstance(item, dict) else item.model_dump() for item in conversation]
    (OUTPUT / "conversation.json").write_text(json.dumps(transcript, indent=2))


asyncio.run(main())
