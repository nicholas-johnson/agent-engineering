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
QUESTION = "What is the square root of 7,654,321, to 10 decimal places?"

# Start the maths server as a separate program, and talk to it over stdin and stdout.
MATHS_SERVER = StdioServerParameters(command=sys.executable, args=[str(HERE / "03_maths_server.py")])

openai = OpenAI()


async def main():
    async with Client(MATHS_SERVER) as maths:
        tools = [
            {
                "type": "function",
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.input_schema,
            }
            for tool in (await maths.list_tools()).tools
        ]

        conversation = [{"role": "user", "content": QUESTION}]
        print(f"You: {QUESTION}")

        # The tool loop: keep going until the model answers instead of asking for a tool.
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
                result = await maths.call_tool(call.name, json.loads(call.arguments))
                answer = result.content[0].text
                print(f"  [tool] {call.name}({call.arguments}) -> {answer}")
                conversation.append(
                    {"type": "function_call_output", "call_id": call.call_id, "output": answer}
                )

        print(f"Agent: {response.output_text}")

    transcript = [item if isinstance(item, dict) else item.model_dump() for item in conversation]
    (OUTPUT / "03_agent.json").write_text(json.dumps(transcript, indent=2))


asyncio.run(main())
