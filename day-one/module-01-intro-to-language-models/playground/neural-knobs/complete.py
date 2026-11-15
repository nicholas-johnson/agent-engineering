# Neural knobs (part 2: complete) — load output/model.json and complete sentences.
# Run train.py first, then from the module folder:
#   uv run python playground/neural-knobs/complete.py
#   or: python3 playground/neural-knobs/complete.py
#
# To play: type any sentence starter (even words never seen together in Alice),
# or add a TEMPERATURE setting before sampling (see ../temperature/play.py).

import json
import math
import random
from pathlib import Path

MODULE = Path(__file__).parent.parent.parent
MODEL_FILE = Path(__file__).parent / "output" / "model.json"

if not MODEL_FILE.exists():
    raise SystemExit("No trained model found — run train.py first.")

model = json.loads(MODEL_FILE.read_text())
vocabulary = json.loads((MODULE / "data" / "tokens.json").read_text())
token_ids = {token: i for i, token in enumerate(vocabulary)}
longest = max(len(token) for token in vocabulary)


def split_into_tokens(text):
    tokens = []
    i = 0
    while i < len(text):
        for size in range(longest, 0, -1):
            if text[i : i + size] in token_ids:
                tokens.append(token_ids[text[i : i + size]])
                i += size
                break
        else:
            i += 1
    return tokens


def forward(context):
    # Run the saved network forward to get a probability for every token in the vocabulary.
    inputs = [value for token in context for value in model["embeddings"][token]]
    hidden = [
        math.tanh(sum(w * x for w, x in zip(row, inputs)) + bias)
        for row, bias in zip(model["hidden_weights"], model["hidden_biases"])
    ]
    scores = [
        sum(w * h for w, h in zip(row, hidden)) + bias
        for row, bias in zip(model["output_weights"], model["output_biases"])
    ]
    top = max(scores)
    exps = [math.exp(score - top) for score in scores]
    total = sum(exps)
    return [e / total for e in exps]


def complete_sentence(start):
    # Pad short prompts if needed so the network always receives `context` tokens.
    tokens = split_into_tokens(" " + start)
    if len(tokens) < model["context"]:
        tokens = [token_ids[" "]] * (model["context"] - len(tokens)) + tokens
    while len(tokens) < 60 and not any(mark in vocabulary[tokens[-1]] for mark in ".!?"):
        probabilities = forward(tokens[-model["context"] :])
        tokens += random.choices(range(len(vocabulary)), weights=probabilities)
    return "".join(vocabulary[token] for token in tokens).strip()


# Interactive loop: print three completions per prompt; press Enter to stop.
while True:
    start = input("\nStart a sentence (Enter to stop): ").strip().lower()
    if not start:
        break
    for _ in range(3):
        print(complete_sentence(start))
