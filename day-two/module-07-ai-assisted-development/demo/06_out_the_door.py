# Run from the module folder: uv run python demo/06_out_the_door.py

import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

HERE = Path(__file__).parent
DATA = HERE.parent / "data"
OUTPUT = HERE / "output" / "06_launch"
OUTPUT.mkdir(parents=True, exist_ok=True)

MODEL = "gpt-6-luna"
SKILLS = ["release-notes", "help-article", "launch-email", "social-post", "sales-sheet"]

client = OpenAI()


def load_skill(name):
    _, front, body = (DATA / "skills" / name / "SKILL.md").read_text().split("---", 2)
    return body.strip()


def run_skill(name, materials):
    response = client.responses.create(
        model=MODEL, reasoning={"effort": "none"}, instructions=load_skill(name), input=materials
    )
    return response.output_text


def banned_words():
    """The list under "Words we don't use" in the brand voice."""
    voice = (DATA / "brain" / "voice.md").read_text()
    section = voice.split("## Words we don't use", 1)[1]
    return [line[2:].strip() for line in section.splitlines() if line.startswith("- ")]


def check(text):
    """Problems a person would otherwise have to spot: banned words, and savings figures."""
    problems = [f'"{word}"' for word in banned_words() if re.search(rf"\b{re.escape(word)}\b", text, re.IGNORECASE)]
    problems += [f'a savings figure, "{m}"' for m in re.findall(r"\d+ ?%|\d+ per ?cent", text)]
    return problems


brain = "\n\n".join(path.read_text() for path in sorted((DATA / "brain").glob("*.md")))
ticket = (DATA / "tickets" / "DOR-231.md").read_text()
change = (DATA / "changes" / "DOR-231.diff").read_text()
article = (DATA / "help" / "warm-wake.md").read_text()
materials = (
    f"# The ticket\n\n{ticket}\n\n# The change\n\n```diff\n{change}```\n\n"
    f"# The help article today\n\n{article}\n\n# The company brain\n\n{brain}"
)

print(f"Running {len(SKILLS)} skills for the launch of DOR-231...", end="\r")
with ThreadPoolExecutor() as pool:
    results = dict(zip(SKILLS, pool.map(lambda name: run_skill(name, materials), SKILLS)))

print(f"Launch kit for DOR-231, in demo/output/06_launch/:{' ' * 20}\n")
for name, text in results.items():
    (OUTPUT / f"{name}.md").write_text(text)
    problems = check(text)
    print(f"  {name + '.md':<20} {', '.join(problems) if problems else 'voice check passed'}")

print(f"\n=== social-post ===\n\n{results['social-post']}")
