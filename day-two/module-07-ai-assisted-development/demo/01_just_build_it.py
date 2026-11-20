# Run from the module folder: uv run python demo/01_just_build_it.py

import re
from html import unescape
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

HERE = Path(__file__).parent
OUTPUT = HERE / "output"
OUTPUT.mkdir(exist_ok=True)

MODEL = "gpt-6-luna"
INSTRUCTIONS = "You build prototypes. Reply with one complete, self-contained HTML file and nothing else."
REQUEST = "Build the settings screen for the Dormouse thermostat app, where customers choose how early Warm Wake starts the heating."

client = OpenAI()


def build(instructions, request):
    # Stream the reply: a long file shows progress, and the connection never sits idle.
    with client.responses.stream(model=MODEL, reasoning={"effort": "none"}, instructions=instructions, input=request) as stream:
        written = 0
        for event in stream:
            if event.type == "response.output_text.delta":
                written += len(event.delta)
                print(f"Building... {written:,} characters", end="\r")
        print()
        return stream.get_final_response().output_text


def html_only(reply):
    # Models sometimes wrap the file in a Markdown code fence.
    return re.sub(r"^```(?:html)?\s*|\s*```$", "", reply.strip())


def screen_text(html):
    """The words a customer would see on the page, one line each."""
    html = re.sub(r"<(script|style|head)\b.*?</\1>", "", html, flags=re.DOTALL | re.IGNORECASE)
    lines = (unescape(line).strip() for line in re.sub(r"<[^>]+>", "\n", html).splitlines())
    return [line for line in lines if line]


html = html_only(build(INSTRUCTIONS, REQUEST))
(OUTPUT / "01_prototype.html").write_text(html)

print(f"\nRequest: {REQUEST}\n")
print("On the screen:")
for line in screen_text(html):
    print(f"  {line}")
print("\nOpen demo/output/01_prototype.html in a browser.")
