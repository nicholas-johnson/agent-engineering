# Test first — the agent turns the ticket into failing tests, then writes the code that makes them pass.
# Run from the module folder: uv run python playground/test-first/play.py
#                         or: source ../../.venv/bin/activate && python playground/test-first/play.py
#
# To play: reword WRITE_TESTS or BUILD, or let the agent change the tests in the second step, and rerun.
# The agent works on a copy of data/project in output/project, so every run starts from the same code.

import difflib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

HERE = Path(__file__).parent
DATA = HERE.parent.parent / "data"
PROJECT = DATA / "project"
TICKET = DATA / "tickets" / "DOR-231.md"
OUTPUT = HERE / "output"
OUTPUT.mkdir(exist_ok=True)
WORK = OUTPUT / "project"

MODEL = "gpt-6-luna"
MAX_STEPS = 40
INSTRUCTIONS = """You are a coding agent working in a small Python project. Use the tools to look at the code,
change it and run the tests. When you have finished, reply with a short summary of what you did."""
WRITE_TESTS = """Don't build anything yet. First, write tests for every acceptance criterion in the ticket, in tests/.
Run them. The new tests should fail, because nothing is built yet. Check each one fails for the right reason,
and not because of a mistake in the test. Then reply with each test's name and the criterion it checks."""
BUILD = "The tests are written and failing. Now change the code in dormouse/ until every test passes."


def tool(name, description, **properties):
    return {
        "type": "function",
        "name": name,
        "description": description,
        "parameters": {
            "type": "object",
            "properties": {key: {"type": "string", "description": text} for key, text in properties.items()},
            "required": list(properties),
            "additionalProperties": False,
        },
        "strict": True,
    }


TOOLS = [
    tool("list_files", "List every file in the project."),
    tool("read_file", "Read a file.", path="Path from the project folder"),
    tool("write_file", "Replace a file with new content, or create it.", path="Path from the project folder", content="The whole new file"),
    tool("run_tests", "Run the project's tests, and see what passed and failed."),
]

client = OpenAI()


def inside(path):
    """The full path of a file in the project, refusing anything outside it."""
    full = (WORK / path).resolve()
    if not full.is_relative_to(WORK.resolve()):
        raise ValueError(f"{path} is outside the project")
    return full


def run_tests():
    result = subprocess.run([sys.executable, "-m", "unittest", "-v"], cwd=WORK, capture_output=True, text=True, timeout=60)
    return result.stderr


def run_tool(name, args, writable):
    if name == "list_files":
        return "\n".join(str(p.relative_to(WORK)) for p in sorted(WORK.rglob("*")) if p.is_file() and "__pycache__" not in p.parts)
    if name == "read_file":
        return inside(args["path"]).read_text()
    if name == "write_file":
        path = inside(args["path"])
        if path.relative_to(WORK.resolve()).parts[0] != writable:
            raise ValueError(f"In this step you can only change files in {writable}/")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(args["content"])
        return f"Wrote {args['path']}"
    if name == "run_tests":
        return run_tests()[-4000:]
    raise ValueError(f"No tool called {name}")


def run_agent(conversation, instructions, writable):
    # Demo 3's tool loop: call the model, run the tools it asks for, and repeat until it answers.
    for step in range(MAX_STEPS):
        response = client.responses.create(
            model=MODEL, reasoning={"effort": "none"}, instructions=instructions, input=conversation, tools=TOOLS
        )
        conversation += response.output
        calls = [item for item in response.output if item.type == "function_call"]
        if not calls:
            return response.output_text
        for call in calls:
            args = json.loads(call.arguments)
            print(f"  {call.name:<10} {args.get('path', '')}")
            try:
                output = run_tool(call.name, args, writable)
            except Exception as error:
                output = f"Error: {error}"
            conversation.append({"type": "function_call_output", "call_id": call.call_id, "output": output})
    return "Stopped: too many steps."


def show_test_run(heading):
    """Each test and whether it passed, without the tracebacks."""
    lines = run_tests().strip().splitlines()
    print(f"\n{heading}")
    for line in lines:
        if " ... " in line:
            print("    " + re.sub(r" \(.*?\)", "", line, count=1))  # drop the "(tests.test_pages.TestSettingsPage...)" part
    print(f"  {next(line for line in lines if line.startswith('Ran ')).split(' in ')[0]}: {lines[-1]}\n")


def changes(before, after):
    """A diff of every file that differs between two copies of the project."""
    def files(folder):
        return {str(p.relative_to(folder)) for p in folder.rglob("*") if p.is_file() and "__pycache__" not in p.parts}

    diff = []
    for name in sorted(files(before) | files(after)):
        old = (before / name).read_text().splitlines(keepends=True) if (before / name).exists() else []
        new = (after / name).read_text().splitlines(keepends=True) if (after / name).exists() else []
        diff += difflib.unified_diff(old, new, f"a/{name}", f"b/{name}")
    return "".join(diff)


shutil.rmtree(WORK, ignore_errors=True)
shutil.copytree(PROJECT, WORK, ignore=shutil.ignore_patterns("__pycache__"))
instructions = f"{INSTRUCTIONS}\n\n{(WORK / 'AGENTS.md').read_text()}"

# One conversation for both steps, so the agent remembers the tests it wrote.
# Step 1 may only write in tests/, and step 2 only in dormouse/, so it can't make a test pass by changing the test.
conversation = [{"role": "user", "content": f"{TICKET.read_text()}\n\n{WRITE_TESTS}"}]
print("1. Write the tests:\n")
run_agent(conversation, instructions, "tests")
show_test_run("Before: the tests, with no code written")
(OUTPUT / "tests.diff").write_text(changes(PROJECT, WORK))

conversation.append({"role": "user", "content": BUILD})
print("2. Make them pass:\n")
summary = run_agent(conversation, instructions, "dormouse")
show_test_run("After:")
print(f"Agent: {summary}")

(OUTPUT / "changes.diff").write_text(changes(PROJECT, WORK))
transcript = [item if isinstance(item, dict) else item.model_dump() for item in conversation]
(OUTPUT / "transcript.json").write_text(json.dumps(transcript, indent=2))
print("\nThe tests it wrote are in playground/test-first/output/tests.diff, and every change in changes.diff")
