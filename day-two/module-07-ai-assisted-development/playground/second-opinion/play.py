# Second opinion — the review skill on the same change, from different models and settings. Do they agree?
# Run from the module folder: uv run python playground/second-opinion/play.py
#                         or: source ../../.venv/bin/activate && python playground/second-opinion/play.py
#
# To play: add a reviewer to REVIEWERS (another effort, another model), or review a different diff, and rerun.
# Each review is written to output/, one file per reviewer, so you can read them side by side.

import os
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import anthropic
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

HERE = Path(__file__).parent
DATA = HERE.parent.parent / "data"
OUTPUT = HERE / "output"
OUTPUT.mkdir(exist_ok=True)

MODEL = "gpt-6-luna"
CLAUDE = "claude-opus-5-5"
SKILL = DATA / "skills" / "review" / "SKILL.md"
CHANGE = DATA / "changes" / "DOR-231.diff"  # the change one run of demo 4's agent made


def review_openai(effort, skill, materials):
    # Streamed, so the connection stays busy while it thinks.
    with OpenAI().responses.stream(model=MODEL, reasoning={"effort": effort}, instructions=skill, input=materials) as stream:
        for event in stream:
            pass
        return stream.get_final_response().output_text


def review_claude(effort, skill, materials):
    with anthropic.Anthropic().beta.messages.stream(
        model=CLAUDE,
        max_tokens=16000,
        output_config={"effort": effort},
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
        system=skill,
        messages=[{"role": "user", "content": materials}],
    ) as stream:
        message = stream.get_final_message()
    if message.stop_reason == "refusal":
        return "(Claude declined to review this change.)"
    return "".join(block.text for block in message.content if block.type == "text")


# Each reviewer: the key it needs, the function that asks it, and its effort setting.
REVIEWERS = {
    "gpt-6-luna-none": ("OPENAI_API_KEY", review_openai, "none"),
    "gpt-6-luna-high": ("OPENAI_API_KEY", review_openai, "high"),
    "claude-opus-5-5-medium": ("ANTHROPIC_API_KEY", review_claude, "medium"),
}


def load_skill(path):
    """A skill is a Markdown file of instructions, with its name and description at the top."""
    _, front, body = path.read_text().split("---", 2)
    return body.strip()


def timed(name, skill, materials):
    key, review, effort = REVIEWERS[name]
    start = time.time()
    return review(effort, skill, materials), time.time() - start


def headline(review):
    """The verdict and what must be fixed: where reviewers most often disagree."""
    return re.split(r"\n\W*Should fix", review, maxsplit=1, flags=re.IGNORECASE)[0].strip()


skill = load_skill(SKILL)
ticket = (DATA / "tickets" / "DOR-231.md").read_text()
agents = (DATA / "project" / "AGENTS.md").read_text()
materials = f"# The ticket\n\n{ticket}\n\n# The project's AGENTS.md\n\n{agents}\n\n# The change\n\n```diff\n{CHANGE.read_text()}```"

ready = [name for name, (key, *_) in REVIEWERS.items() if key in os.environ]
results = {}
with ThreadPoolExecutor() as pool:
    jobs = {pool.submit(timed, name, skill, materials): name for name in ready}
    for job in as_completed(jobs):
        results[jobs[job]] = job.result()
        print(f"Reviewing the change for DOR-231: {len(results)}/{len(ready)} reviews back", end="\r")
print()

for name, (key, *_) in REVIEWERS.items():
    if name not in results:
        print(f"\n=== {name} ===\n\n  Skipped: no {key} in .env")
        continue
    review, seconds = results[name]
    (OUTPUT / f"{name}.md").write_text(review)
    print(f"\n=== {name} ({seconds:.0f} seconds) ===\n\n{headline(review)}")

print("\nThe full reviews are in playground/second-opinion/output/")
