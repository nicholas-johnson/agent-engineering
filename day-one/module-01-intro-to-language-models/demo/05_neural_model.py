# Run from the module folder: uv run python demo/05_neural_model.py

import json
import math
import random
from pathlib import Path

DATA = Path(__file__).parent.parent / "data"
OUTPUT = Path(__file__).parent / "output"
OUTPUT.mkdir(exist_ok=True)

CONTEXT = 3
EMBEDDING_SIZE = 16
HIDDEN_SIZE = 32
LEARNING_RATE = 0.05
STEPS = 30000

vocabulary = json.loads((DATA / "tokens.json").read_text())
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
    return tokens


def random_matrix(rows, columns):
    return [[random.gauss(0, 0.1) for _ in range(columns)] for _ in range(rows)]


embeddings = random_matrix(len(vocabulary), EMBEDDING_SIZE)
hidden_weights = random_matrix(HIDDEN_SIZE, CONTEXT * EMBEDDING_SIZE)
hidden_biases = [0.0] * HIDDEN_SIZE
output_weights = random_matrix(len(vocabulary), HIDDEN_SIZE)
output_biases = [0.0] * len(vocabulary)


def forward(context):
    inputs = [value for token in context for value in embeddings[token]]
    hidden = [
        math.tanh(sum(w * x for w, x in zip(row, inputs)) + bias)
        for row, bias in zip(hidden_weights, hidden_biases)
    ]
    scores = [
        sum(w * h for w, h in zip(row, hidden)) + bias
        for row, bias in zip(output_weights, output_biases)
    ]
    top = max(scores)
    exps = [math.exp(score - top) for score in scores]
    total = sum(exps)
    return inputs, hidden, [e / total for e in exps]


def train(context, target):
    inputs, hidden, probabilities = forward(context)

    # How the loss changes with each output score: predicted minus actual.
    score_grads = probabilities[:]
    score_grads[target] -= 1

    hidden_grads = [0.0] * HIDDEN_SIZE
    for i, grad in enumerate(score_grads):
        row = output_weights[i]
        hidden_grads = [hg + w * grad for hg, w in zip(hidden_grads, row)]
        output_weights[i] = [w - LEARNING_RATE * grad * h for w, h in zip(row, hidden)]
        output_biases[i] -= LEARNING_RATE * grad

    # Back through tanh: its slope is 1 - tanh².
    hidden_grads = [grad * (1 - h * h) for grad, h in zip(hidden_grads, hidden)]

    input_grads = [0.0] * len(inputs)
    for i, grad in enumerate(hidden_grads):
        row = hidden_weights[i]
        input_grads = [ig + w * grad for ig, w in zip(input_grads, row)]
        hidden_weights[i] = [w - LEARNING_RATE * grad * x for w, x in zip(row, inputs)]
        hidden_biases[i] -= LEARNING_RATE * grad

    for position, token in enumerate(context):
        grads = input_grads[position * EMBEDDING_SIZE : (position + 1) * EMBEDDING_SIZE]
        embeddings[token] = [e - LEARNING_RATE * g for e, g in zip(embeddings[token], grads)]

    return -math.log(probabilities[target])


def complete_sentence(start):
    tokens = split_into_tokens(start)
    while len(tokens) < 60 and not any(mark in vocabulary[tokens[-1]] for mark in ".!?"):
        _, _, probabilities = forward(tokens[-CONTEXT:])
        tokens += random.choices(range(len(vocabulary)), weights=probabilities)
    return "".join(vocabulary[token] for token in tokens)


text = " ".join((DATA / "alice.txt").read_text().lower().split())
tokens = split_into_tokens(text)
examples = [(tokens[i : i + CONTEXT], tokens[i + CONTEXT]) for i in range(len(tokens) - CONTEXT)]

for step in range(1, STEPS + 1):
    context, target = random.choice(examples)
    train(context, target)
    if step % 1000 == 0:
        print(f"Training: step {step} of {STEPS}", end="\r")
print()

with open(OUTPUT / "05_neural_model_embeddings.txt", "w") as file:
    for token, vector in zip(vocabulary, embeddings):
        file.write(f"{token!r:16} {' '.join(f'{v:6.2f}' for v in vector)}\n")

print("=== alice ===")
for _ in range(3):
    print(complete_sentence("alice was beginning to get"))
