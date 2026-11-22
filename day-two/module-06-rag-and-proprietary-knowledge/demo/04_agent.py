# Run from the module folder: uv run python demo/04_agent.py

import asyncio
import json
import re
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from mcp import Client
from mcp.client.stdio import StdioServerParameters
from openai import OpenAI

load_dotenv()

HERE = Path(__file__).parent
DATA = HERE.parent / "data"
OUTPUT = HERE / "output"
OUTPUT.mkdir(exist_ok=True)

MODEL = "gpt-6-luna"
INPUT_PRICE = 0.10
OUTPUT_PRICE = 0.50
INSTRUCTIONS = """You are the support assistant for Dormouse, a smart thermostat. Answer the customer in a short paragraph.
Search the documentation first, and answer only from what you find. If the results don't answer the question, search again with different words.
End each sentence that relies on the documentation with the id of the section it came from, in square brackets."""
QUESTION = "Why does my Dormouse turn the heating on before the time I set?"

DOCS_SERVER = StdioServerParameters(command=sys.executable, args=[str(HERE / "04_docs_server.py")])

openai = OpenAI()


async def ask(docs, tools, question):
    # Module 3's tool loop: the model searches as often as it likes, then answers.
    conversation = [{"role": "user", "content": question}]
    searches, input_tokens, output_tokens = [], 0, 0
    start = time.perf_counter()
    while True:
        response = openai.responses.create(
            model=MODEL,
            reasoning={"effort": "none"},
            instructions=INSTRUCTIONS,
            input=conversation,
            tools=tools,
        )
        conversation += response.output
        input_tokens += response.usage.input_tokens
        output_tokens += response.usage.output_tokens

        calls = [item for item in response.output if item.type == "function_call"]
        if not calls:
            transcript = [item if isinstance(item, dict) else item.model_dump() for item in conversation]
            return {
                "answer": response.output_text,
                "searches": searches,
                "input_tokens": input_tokens,
                "cost_dollars": round((input_tokens * INPUT_PRICE + output_tokens * OUTPUT_PRICE) / 1_000_000, 5),
                "seconds": round(time.perf_counter() - start, 1),
                "transcript": transcript,
            }

        for call in calls:
            arguments = json.loads(call.arguments)
            result = await docs.call_tool(call.name, arguments)
            output = result.content[0].text
            searches.append({"query": arguments.get("query"), "found": json.loads(output)})
            conversation.append({"type": "function_call_output", "call_id": call.call_id, "output": output})


def plain(text):
    text = text.lower().replace("→", ">").replace("->", ">").replace("°c", " degrees")
    return re.sub(r"\s*>\s*", ">", re.sub(r"\s+", " ", text))


def contains_facts(text, facts):
    return all(any(re.search(rf"\b{re.escape(plain(option))}\b", plain(text)) for option in fact.split("|")) for fact in facts)


async def main():
    async with Client(DOCS_SERVER) as docs:
        # The agent doesn't know the tools in advance: it asks the server.
        tools = [
            {"type": "function", "name": tool.name, "description": tool.description, "parameters": tool.input_schema}
            for tool in (await docs.list_tools()).tools
        ]
        print(f"\nThe server offers: {', '.join(tool['name'] for tool in tools)}")

        print(f"\nQ: {QUESTION}")
        shown = await ask(docs, tools, QUESTION)
        for search in shown["searches"]:
            print(f'   search_docs("{search["query"]}")')
            for chunk in search["found"]:
                print(f"      {chunk['similarity']:.3f}  {chunk['id']}")
        print(f"A: {shown['answer']}")
        print(f"   {shown['input_tokens']:,} tokens in, ${shown['cost_dollars']:.4f}, {shown['seconds']} seconds")

        # How often do the agent's own searches find the facts a right answer needs?
        questions = [q for q in json.loads((DATA / "questions.json").read_text()) if q["kind"] in ("everyday", "error code")]
        checks = []
        for n, q in enumerate(questions, 1):
            print(f"  Asking {n}/{len(questions)}", end="\r")
            reply = await ask(docs, tools, q["question"])
            found = [chunk for search in reply["searches"] for chunk in search["found"]]
            hit = any(contains_facts(chunk["text"], q["facts"]) for chunk in found)
            checks.append({"id": q["id"], "question": q["question"], "found": hit, **reply})
        print(" " * 40, end="\r")

    hits = sum(c["found"] for c in checks)
    searches = sum(len(c["searches"]) for c in checks)
    print(
        f"\nThe answer was in the chunks the agent found, for {len(questions)} questions: {hits}"
        f" ({searches / len(questions):.1f} searches a question)"
    )

    (OUTPUT / "04_agent.json").write_text(
        json.dumps({"question": QUESTION, **shown, "found": hits, "checks": checks}, indent=2)
    )


asyncio.run(main())
