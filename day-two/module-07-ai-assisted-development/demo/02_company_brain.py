# Run from the module folder: uv run python demo/02_company_brain.py

import json
import re
from html import unescape
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

HERE = Path(__file__).parent
DATA = HERE.parent / "data"
OUTPUT = HERE / "output"
OUTPUT.mkdir(exist_ok=True)

MODEL = "gpt-6-luna"
REQUEST = "Build the settings screen for the Dormouse thermostat app, where customers choose how early Warm Wake starts the heating."
SPEC_INSTRUCTIONS = """You are a product manager at Dormouse. The team has been asked for the request below. Don't build it:
write a one-page spec for it, in Markdown:
the problem, with evidence from the customer feedback; what we're building; acceptance criteria; and what is out of scope.
Follow our decisions, and write in our voice."""
PROTOTYPE_INSTRUCTIONS = """You build prototypes for Dormouse. Build the screen in the spec, following our design.
Reply with one complete, self-contained HTML file and nothing else."""

client = OpenAI()


def ask(instructions, request, doing):
    # Stream the reply: a long file shows progress, and the connection never sits idle.
    with client.responses.stream(model=MODEL, reasoning={"effort": "none"}, instructions=instructions, input=request) as stream:
        written = 0
        for event in stream:
            if event.type == "response.output_text.delta":
                written += len(event.delta)
                print(f"{doing}... {written:,} characters", end="\r")
        print()
        return stream.get_final_response().output_text


def html_only(reply):
    return re.sub(r"^```(?:html)?\s*|\s*```$", "", reply.strip())


def screen_text(html):
    """The words a customer would see on the page, one line each."""
    html = re.sub(r"<(script|style|head)\b.*?</\1>", "", html, flags=re.DOTALL | re.IGNORECASE)
    lines = (unescape(line).strip() for line in re.sub(r"<[^>]+>", "\n", html).splitlines())
    return [line for line in lines if line]


# The company brain: what Dormouse knows about itself, written down once.
brain = "\n\n".join(path.read_text() for path in sorted((DATA / "brain").glob("*.md")))
feedback = "\n".join(f"- {f['id']} ({f['channel']}): {f['text']}" for f in json.loads((DATA / "feedback.json").read_text()))

spec = ask(
    f"{SPEC_INSTRUCTIONS}\n\n{brain}\n\n# Customer feedback, September and October\n\n{feedback}",
    f"The request: {REQUEST}",
    "Writing the spec",
)
(OUTPUT / "02_spec.md").write_text(spec)

html = html_only(ask(f"{PROTOTYPE_INSTRUCTIONS}\n\n{brain}\n\n# The spec\n\n{spec}", REQUEST, "Building"))
(OUTPUT / "02_prototype.html").write_text(html)

print(f"\nRequest: {REQUEST}\n")
print("On the screen:")
for line in screen_text(html):
    print(f"  {line}")
print("\nOpen demo/output/02_prototype.html in a browser, and read the spec in demo/output/02_spec.md.")
