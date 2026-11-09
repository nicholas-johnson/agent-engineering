import json
import math
import random
from pathlib import Path

MODULE = Path(__file__).parent.parent.parent
OUTPUT = Path(__file__).parent / "output"
OUTPUT.mkdir(exist_ok=True)

CONTEXT = 3
EMBEDDING_SIZE = 16
HIDDEN_SIZE = 32
LEARNING_RATE = 0.05
STEPS = 30000

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

    score_grads = probabilities[:]
    score_grads[target] -= 1

    hidden_grads = [0.0] * HIDDEN_SIZE
    for i, grad in enumerate(score_grads):
        row = output_weights[i]
        hidden_grads = [hg + w * grad for hg, w in zip(hidden_grads, row)]
        output_weights[i] = [w - LEARNING_RATE * grad * h for w, h in zip(row, hidden)]
        output_biases[i] -= LEARNING_RATE * grad

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


text = " ".join((MODULE / "data" / "alice.txt").read_text().lower().split())
tokens = split_into_tokens(text)
examples = [(tokens[i : i + CONTEXT], tokens[i + CONTEXT]) for i in range(len(tokens) - CONTEXT)]
print(f"Loss from random guessing: {math.log(len(vocabulary)):.2f}")

total_loss = 0
for step in range(1, STEPS + 1):
    context, target = random.choice(examples)
    total_loss += train(context, target)
    if step % 1000 == 0:
        print(f"Step {step}: loss {total_loss / 1000:.2f}")
        total_loss = 0

model = {
    "context": CONTEXT,
    "embeddings": embeddings,
    "hidden_weights": hidden_weights,
    "hidden_biases": hidden_biases,
    "output_weights": output_weights,
    "output_biases": output_biases,
}
(OUTPUT / "model.json").write_text(json.dumps(model))
print("Saved output/model.json")
