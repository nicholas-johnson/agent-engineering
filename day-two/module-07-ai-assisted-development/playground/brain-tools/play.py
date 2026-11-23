# Brain tools: start the company-brain MCP server, list its tools, and call each one, the way Claude Code would.
# Run from the module folder: uv run python playground/brain-tools/play.py
#                         or: source ../../.venv/bin/activate && python playground/brain-tools/play.py
#
# To play: add a tool to server.py, then add a line to CALLS to try it. No API key needed:
# this script calls the tools itself, so you see exactly what a model would get back.

import asyncio
import json
import sys
from pathlib import Path

from mcp import Client
from mcp.client.stdio import StdioServerParameters

HERE = Path(__file__).parent
OUTPUT = HERE / "output"
OUTPUT.mkdir(exist_ok=True)

SERVER = HERE / "server.py"
# Each call: a tool's name and its arguments.
CALLS = [
    ("get_ticket", {"ticket_id": "DOR-233"}),
    ("read_brain", {"topic": "decisions"}),
    ("search_feedback", {"words": "early cold"}),
]
SHOW = 300  # characters of each answer to print; the whole answer goes to output/


async def main():
    async with Client(StdioServerParameters(command=sys.executable, args=[str(SERVER)])) as client:
        tools = (await client.list_tools()).tools
        print("The server offers:\n")
        for tool in tools:
            print(f"  {tool.name}({', '.join(tool.input_schema['properties'])})")
            description = " ".join(tool.description.split())
            print(f"    {description[:110]}{'...' if len(description) > 110 else ''}")

        results = []
        for name, arguments in CALLS:
            answer = (await client.call_tool(name, arguments)).content[0].text
            results.append({"tool": name, "arguments": arguments, "answer": answer})
            print(f"\n{name}({json.dumps(arguments)})\n")
            print("  " + answer[:SHOW].replace("\n", "\n  ") + ("..." if len(answer) > SHOW else ""))

    (OUTPUT / "calls.json").write_text(json.dumps(results, indent=2))
    print("\nEvery answer, in full: playground/brain-tools/output/calls.json")


asyncio.run(main())
