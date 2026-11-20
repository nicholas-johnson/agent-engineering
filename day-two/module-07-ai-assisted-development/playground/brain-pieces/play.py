# Brain pieces — demo 2's request, with a different part of the company brain each time. Which file changes what?
# Run from the module folder: uv run python playground/brain-pieces/play.py
#                         or: source ../../.venv/bin/activate && python playground/brain-pieces/play.py
#
# To play: change the lists of files in PIECES, or add your own, and rerun.
# Each prototype is written to output/ as HTML, and as the words on its screen, so you can compare them.

import re
from concurrent.futures import ThreadPoolExecutor
from html import unescape
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

HERE = Path(__file__).parent
BRAIN = HERE.parent.parent / "data" / "brain"
OUTPUT = HERE / "output"
OUTPUT.mkdir(exist_ok=True)

MODEL = "gpt-6-luna"
REQUEST = "Build the settings screen for the Dormouse thermostat app, where customers choose how early Warm Wake starts the heating."
INSTRUCTIONS = """You build prototypes for Dormouse. Follow anything we have written down about ourselves below.
Reply with one complete, self-contained HTML file and nothing else."""

# Which files from data/brain/ each prototype is given.
PIECES = {
    "nothing": [],
    "product": ["product.md"],
    "product, decisions": ["product.md", "decisions.md"],
    "product, decisions, design, voice": ["product.md", "decisions.md", "design.md", "voice.md"],
}

client = OpenAI()
written = {}


def build(name):
    brain = "\n\n".join((BRAIN / file).read_text() for file in PIECES[name])
    # Stream the reply: a long file shows progress, and the connection never sits idle.
    with client.responses.stream(
        model=MODEL, reasoning={"effort": "none"}, instructions=f"{INSTRUCTIONS}\n\n{brain}", input=REQUEST
    ) as stream:
        for event in stream:
            if event.type == "response.output_text.delta":
                written[name] = written.get(name, 0) + len(event.delta)
                print(f"Building {len(PIECES)} prototypes... {sum(written.values()):,} characters", end="\r")
        return html_only(stream.get_final_response().output_text)


def html_only(reply):
    # Models sometimes wrap the file in a Markdown code fence.
    return re.sub(r"^```(?:html)?\s*|\s*```$", "", reply.strip())


def screen_text(html):
    """The words a customer would see on the page, one line each."""
    html = re.sub(r"<(script|style|head)\b.*?</\1>", "", html, flags=re.DOTALL | re.IGNORECASE)
    lines = (unescape(line).strip() for line in re.sub(r"<[^>]+>", "\n", html).splitlines())
    return [line for line in lines if line]


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


# Build them all at once: they don't depend on each other.
with ThreadPoolExecutor() as pool:
    prototypes = dict(zip(PIECES, pool.map(build, PIECES)))
print()

print(f"\nRequest: {REQUEST}")
for name, html in prototypes.items():
    text = screen_text(html)
    (OUTPUT / f"{slug(name)}.html").write_text(html)
    (OUTPUT / f"{slug(name)}.txt").write_text("\n".join(text) + "\n")
    # The colours show what design.md changed, which the words can't.
    colours = sorted({colour.upper() for colour in re.findall(r"#[0-9A-Fa-f]{6}\b", html)})
    print(f"\n=== {name} ===")
    print(f"  Brain files: {', '.join(PIECES[name]) or 'none'}")
    print(f"  Colours: {', '.join(colours[:8])}{' ...' if len(colours) > 8 else ''}")
    print("  On the screen:")
    for line in text:
        print(f"    {line}")

print("\nOpen the prototypes in playground/brain-pieces/output/ in a browser.")
