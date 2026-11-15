import json
import os
from pathlib import Path

from dotenv import load_dotenv
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
MODELS = [
    "deepseek/deepseek-v4.1-flash",
    "qwen/qwen3.8-max-0902",
    "moonshotai/kimi-k3.1-pro",
    "z-ai/glm-5.3",
    "minimax/minimax-m3",
    "baidu/ernie-5.5-flash-preview",
]

if "OPENROUTER_API_KEY" not in os.environ:
    raise SystemExit("This demo needs OPENROUTER_API_KEY in .env")

client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.environ["OPENROUTER_API_KEY"])
answers = {}

for model in MODELS:
    response = client.responses.create(model=model, instructions=INSTRUCTIONS, input=QUESTION)
    answers[model] = response.output_text
    print(f"=== {model} ===\n{response.output_text}\n")

(OUTPUT / "03_chinese_labs.json").write_text(json.dumps(answers, indent=2))
