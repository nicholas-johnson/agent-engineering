import json
import math
import random
from pathlib import Path

MODULE = Path(__file__).parent.parent.parent

model = json.loads((Path(__file__).parent / "output" / "model.json").read_text())
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
    tokens = split_into_tokens(" " + start)
    while len(tokens) < 60 and not any(mark in vocabulary[tokens[-1]] for mark in ".!?"):
        probabilities = forward(tokens[-model["context"] :])
        tokens += random.choices(range(len(vocabulary)), weights=probabilities)
    return "".join(vocabulary[token] for token in tokens).strip()


while True:
    start = input("\nStart a sentence (Enter to stop): ").strip().lower()
    if not start:
        break
    for _ in range(3):
        print(complete_sentence(start))
