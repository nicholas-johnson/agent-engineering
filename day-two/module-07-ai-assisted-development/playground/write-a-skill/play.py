# Write a skill — run any skill folder on the DOR-231 materials: the one that ships here, the module's, or your own.
# Run from the module folder: uv run python playground/write-a-skill/play.py
#                         or: source ../../.venv/bin/activate && python playground/write-a-skill/play.py
#
# To play: edit support-reply/SKILL.md, or copy the folder and write a new skill, then point SKILL at it.
# Change REQUEST to whatever you'd type when asking for the skill. The reply is written to output/.

from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

HERE = Path(__file__).parent
DATA = HERE.parent.parent / "data"
OUTPUT = HERE / "output"
OUTPUT.mkdir(exist_ok=True)

MODEL = "gpt-6-luna"
# A folder with a SKILL.md in it. Try DATA / "skills" / "release-notes", or any folder in data/skills/.
SKILL = HERE / "support-reply"
# What you ask for. For a module skill, something like "Write the release notes."
REQUEST = (
    "Reply to this customer: Is it normal for the heating to switch on at 5:30 for a 7:00 period? "
    "My neighbour has the same thermostat and hers doesn't."
)

client = OpenAI()


def load_skill(folder):
    """A skill is a Markdown file of instructions, with its name and description at the top."""
    _, front, body = (folder / "SKILL.md").read_text().split("---", 2)
    fields = dict(line.split(": ", 1) for line in front.strip().splitlines())
    return fields, body.strip()


# Everything any of the module's skills might need. A skill's instructions say which parts it uses.
brain = "\n\n".join(path.read_text() for path in sorted((DATA / "brain").glob("*.md")))
materials = (
    f"# The ticket\n\n{(DATA / 'tickets' / 'DOR-231.md').read_text()}\n\n"
    f"# The project's AGENTS.md\n\n{(DATA / 'project' / 'AGENTS.md').read_text()}\n\n"
    f"# The change\n\n```diff\n{(DATA / 'changes' / 'DOR-231.diff').read_text()}```\n\n"
    f"# The help article today\n\n{(DATA / 'help' / 'warm-wake.md').read_text()}\n\n"
    f"# The company brain\n\n{brain}"
)

fields, instructions = load_skill(SKILL)
print(f"Skill: {fields['name']}\n  {fields['description']}\n\nRequest: {REQUEST}\n")
print("Running the skill...", end="\r")

response = client.responses.create(
    model=MODEL, reasoning={"effort": "none"}, instructions=instructions, input=f"{materials}\n\n# The request\n\n{REQUEST}"
)
reply = response.output_text
(OUTPUT / f"{fields['name']}.md").write_text(reply)

print(f"{reply}\n\n({len(reply.split())} words, written to playground/write-a-skill/output/{fields['name']}.md)")
