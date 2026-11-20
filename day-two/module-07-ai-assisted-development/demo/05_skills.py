# Run from the module folder: uv run python demo/05_skills.py

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

HERE = Path(__file__).parent
DATA = HERE.parent / "data"
OUTPUT = HERE / "output"
OUTPUT.mkdir(exist_ok=True)

MODEL = "gpt-6-luna"
SKILLS = ["review", "test-plan", "change-summary"]
# The change one run of demo 4's agent made for DOR-231, saved so everyone reviews the same one.
CHANGE = DATA / "changes" / "DOR-231.diff"

client = OpenAI()


def load_skill(name):
    """A skill is a Markdown file of instructions, with its name and description at the top."""
    _, front, body = (DATA / "skills" / name / "SKILL.md").read_text().split("---", 2)
    return body.strip()


def run_skill(name, materials):
    response = client.responses.create(
        model=MODEL, reasoning={"effort": "none"}, instructions=load_skill(name), input=materials
    )
    return response.output_text


ticket = (DATA / "tickets" / "DOR-231.md").read_text()
agents = (DATA / "project" / "AGENTS.md").read_text()
materials = f"# The ticket\n\n{ticket}\n\n# The project's AGENTS.md\n\n{agents}\n\n# The change\n\n```diff\n{CHANGE.read_text()}```"

# Run the skills at the same time: they don't depend on each other.
print(f"Running {len(SKILLS)} skills on the change for DOR-231...", end="\r")
with ThreadPoolExecutor() as pool:
    results = dict(zip(SKILLS, pool.map(lambda name: run_skill(name, materials), SKILLS)))

for name, text in results.items():
    (OUTPUT / f"05_{name}.md").write_text(text)

print(f"=== review ===\n\n{results['review']}\n")
print(f"=== change-summary ===\n\n{results['change-summary']}\n")
print("The test plan is in demo/output/05_test-plan.md")
