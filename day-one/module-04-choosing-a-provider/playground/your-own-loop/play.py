# Your own generation loop — Module 1's next-token loop, by hand, on Qwen3 1.7B in PyTorch.
# Run from the module folder: uv run --extra local python playground/your-own-loop/play.py
#                         or: source ../../.venv/bin/activate && python playground/your-own-loop/play.py
#                             (requires `.venv/bin/pip install -e ".[local]"`)
#
# To play: change PROMPT, TEMPERATURE or NEW_TOKENS below, or swap multinomial sampling
# for greedy argmax / top-k filtering inside the loop (see README.md).

import json
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

OUTPUT = Path(__file__).parent / "output"
OUTPUT.mkdir(exist_ok=True)

MODEL = "Qwen/Qwen3-1.7B"
PROMPT = "Alice was beginning to get"
TEMPERATURE = 0.8
NEW_TOKENS = 30

# Load weights onto Apple silicon / CUDA GPU if available (downloads ~4 GB on first run).
device = torch.accelerator.current_accelerator() or "cpu"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForCausalLM.from_pretrained(MODEL, dtype=torch.bfloat16).to(device)

tokens = tokenizer(PROMPT, return_tensors="pt")["input_ids"].to(device)
steps = []
print(PROMPT, end="", flush=True)

# Generate one token at a time: logits -> softmax probabilities -> sample -> append.
for _ in range(NEW_TOKENS):
    with torch.no_grad():
        scores = model(tokens).logits[0, -1]
    probabilities = torch.softmax(scores / TEMPERATURE, dim=-1)
    choice = torch.multinomial(probabilities, 1)
    tokens = torch.cat([tokens, choice.unsqueeze(0)], dim=1)

    top = torch.topk(probabilities, 5)
    steps.append(
        {
            "chosen": tokenizer.decode(choice),
            "top_5": {tokenizer.decode(t): round(p.item(), 4) for p, t in zip(top.values, top.indices)},
        }
    )
    print(tokenizer.decode(choice), end="", flush=True)
print()

# Inspect every chosen token and its top-5 alternatives in output/steps.json.
(OUTPUT / "steps.json").write_text(json.dumps(steps, indent=2, ensure_ascii=False))
