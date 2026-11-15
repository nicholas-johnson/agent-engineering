# Run from the module folder: uv run python demo/01_big_labs.py

import json
import os
import warnings
from pathlib import Path

# google-genai prints a harmless SyntaxWarning on Python 3.14.
warnings.filterwarnings("ignore", category=SyntaxWarning)

import anthropic
from dotenv import load_dotenv
from google import genai
from openai import OpenAI

load_dotenv()

OUTPUT = Path(__file__).parent / "output"
OUTPUT.mkdir(exist_ok=True)

INSTRUCTIONS = (
    "You are the Cheshire Cat from Alice's Adventures in Wonderland. "
    "You are mischievous and fond of riddles, but you always answer the question. "
    "Keep your replies to two or three sentences."
)
QUESTION = "Would you tell me, please, which way I ought to go from here?"


def ask_openai():
    client = OpenAI()
    response = client.responses.create(
        model="gpt-6-luna",
        reasoning={"effort": "none"},
        instructions=INSTRUCTIONS,
        input=QUESTION,
    )
    return response.output_text


def ask_anthropic():
    client = anthropic.Anthropic()
    response = client.beta.messages.create(
        model="claude-opus-5-5",
        max_tokens=16000,
        output_config={"effort": "low"},
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
        system=INSTRUCTIONS,
        messages=[{"role": "user", "content": QUESTION}],
    )
    return next(block.text for block in response.content if block.type == "text")


def ask_google():
    client = genai.Client()
    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        system_instruction=INSTRUCTIONS,
        input=QUESTION,
    )
    return interaction.output_text


def ask_xai():
    client = OpenAI(base_url="https://api.x.ai/v1", api_key=os.environ["XAI_API_KEY"])
    response = client.responses.create(
        model="grok-4.7",
        instructions=INSTRUCTIONS,
        input=QUESTION,
    )
    return response.output_text


labs = {
    "OpenAI": ("OPENAI_API_KEY", ask_openai),
    "Anthropic": ("ANTHROPIC_API_KEY", ask_anthropic),
    "Google": ("GEMINI_API_KEY", ask_google),
    "xAI": ("XAI_API_KEY", ask_xai),
}

answers = {}
for lab, (key, ask) in labs.items():
    answers[lab] = ask() if key in os.environ else f"(skipped: no {key} in .env)"
    print(f"=== {lab} ===\n{answers[lab]}\n")

(OUTPUT / "01_big_labs.json").write_text(json.dumps(answers, indent=2))
