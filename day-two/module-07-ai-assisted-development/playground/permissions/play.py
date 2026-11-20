# Permissions — the coding agent asks before every change it makes. Say no, and tell it why.
# Run from the module folder: uv run python playground/permissions/play.py
#                         or: source ../../.venv/bin/activate && python playground/permissions/play.py
#
# To play: answer y to allow a change, or n and a reason to refuse it. Can you steer it to DOR-231 without the ticket?
# The agent works on a copy of data/project in output/project, so every run starts from the same code.

import difflib
import json
import shutil
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

HERE = Path(__file__).parent
PROJECT = HERE.parent.parent / "data" / "project"
OUTPUT = HERE / "output"
OUTPUT.mkdir(exist_ok=True)
WORK = OUTPUT / "project"

MODEL = "gpt-6-luna"
MAX_STEPS = 40
REQUEST = "Let customers choose how early Warm Wake starts the heating."
INSTRUCTIONS = """You are a coding agent working in a small Python project. Use the tools to look at the code,
change it and run the tests. When you have finished, reply with a short summary of what you changed."""


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
answers = []  # every change the agent asked to make, and what the developer said


def inside(path):
    """The full path of a file in the project, refusing anything outside it."""
    full = (WORK / path).resolve()
    if not full.is_relative_to(WORK.resolve()):
        raise ValueError(f"{path} is outside the project")
    return full


def run_tests():
    result = subprocess.run([sys.executable, "-m", "unittest"], cwd=WORK, capture_output=True, text=True, timeout=60)
    return result.stderr[-4000:]


def ask_permission(path, content):
    """Show the developer this one change, and ask. Returns None if they allow it, or the refusal for the model."""
    full = inside(path)
    old = full.read_text().splitlines(keepends=True) if full.exists() else []
    for line in difflib.unified_diff(old, content.splitlines(keepends=True), f"a/{path}", f"b/{path}"):
        print(f"      {line.rstrip()}")
    if input(f"\n  Allow this change to {path}? (y/n) ").strip().lower() == "y":
        answers.append({"path": path, "allowed": True})
        return None
    reason = input("  Why not? ").strip()
    answers.append({"path": path, "allowed": False, "reason": reason})
    return f"The developer refused this change: {reason}"


def run_tool(name, args):
    if name == "list_files":
        return "\n".join(str(p.relative_to(WORK)) for p in sorted(WORK.rglob("*")) if p.is_file() and "__pycache__" not in p.parts)
    if name == "read_file":
        return inside(args["path"]).read_text()
    if name == "write_file":
        # Like Claude Code and Cursor: nothing is written until a person has seen it and said yes.
        refusal = ask_permission(args["path"], args["content"])
        if refusal:
            return refusal
        path = inside(args["path"])
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(args["content"])
        return f"Wrote {args['path']}"
    if name == "run_tests":
        return run_tests()
    raise ValueError(f"No tool called {name}")


def run_agent(request, instructions):
    # Demo 3's tool loop: call the model, run the tools it asks for, and repeat until it answers.
    conversation = [{"role": "user", "content": request}]
    for step in range(MAX_STEPS):
        response = client.responses.create(
            model=MODEL, reasoning={"effort": "none"}, instructions=instructions, input=conversation, tools=TOOLS
        )
        conversation += response.output
        calls = [item for item in response.output if item.type == "function_call"]
        if not calls:
            return response.output_text, conversation
        for call in calls:
            args = json.loads(call.arguments)
            print(f"  {call.name:<10} {args.get('path', '')}")
            try:
                output = run_tool(call.name, args)
            except Exception as error:
                output = f"Error: {error}"
            conversation.append({"type": "function_call_output", "call_id": call.call_id, "output": output})
    return "Stopped: too many steps.", conversation


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

print(f"Request: {REQUEST}\n")
summary, conversation = run_agent(REQUEST, instructions)
print(f"\nAgent: {summary}\n")

diff = changes(PROJECT, WORK)
(OUTPUT / "changes.diff").write_text(diff)
transcript = [item if isinstance(item, dict) else item.model_dump() for item in conversation]
(OUTPUT / "transcript.json").write_text(json.dumps({"answers": answers, "conversation": transcript}, indent=2))

refused = sum(not answer["allowed"] for answer in answers)
print(f"You allowed {len(answers) - refused} changes and refused {refused}.")
lines = run_tests().strip().splitlines()
print(f"Tests: {next(line for line in lines if line.startswith('Ran ')).split(' in ')[0]}, {lines[-1]}")
print("The changes are in playground/permissions/output/changes.diff")
