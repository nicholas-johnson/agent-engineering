# Run from the module folder: uv run python demo/05_agent.py

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
INSTRUCTIONS = (
    "You help Dormouse's testers choose a manual test script. Search the library. If nothing fits "
    "well, search again with different words. Then recommend the single best fit and say why in two "
    "or three sentences. Answer in plain text, without Markdown."
)
BUG_REPORT = (
    "Support say that since this morning's release, customers on Android who reset their password "
    "can't get back into the app. The hotfix ships in ten minutes. Which test should we run?"
)

SEARCH_SERVER = StdioServerParameters(command=sys.executable, args=[str(HERE / "05_search_server.py")])

openai = OpenAI()


async def main():
    async with Client(SEARCH_SERVER) as search:
        tools = [
            {
                "type": "function",
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.input_schema,
            }
            for tool in (await search.list_tools()).tools
        ]

        conversation = [{"role": "user", "content": BUG_REPORT}]
        print(f"You: {BUG_REPORT}")

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
                result = await search.call_tool(call.name, json.loads(call.arguments))
                answer = result.content[0].text
                titles = [f"{s['id']} {s['title']}" for s in json.loads(answer)]
                print(f"  [tool] {call.name}({call.arguments})")
                for title in titles:
                    print(f"         -> {title}")
                conversation.append({"type": "function_call_output", "call_id": call.call_id, "output": answer})

        print(f"Agent: {response.output_text}")

    transcript = [item if isinstance(item, dict) else item.model_dump() for item in conversation]
    (OUTPUT / "05_agent.json").write_text(json.dumps(transcript, indent=2))


asyncio.run(main())
