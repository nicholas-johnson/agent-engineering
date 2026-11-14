"""The single neuron in clip 2, learning one thing: with dark clouds and a rain
forecast, take an umbrella. Prints the weights and answers the clip shows.

Run with: uv run python social-scripts/02-how-ai-learns/neuron.py
"""

import math
import random

SEED = 7  # chosen so the neuron starts out clearly wrong
LEARNING_RATE = 1.0
INPUTS = [1.0, 1.0]  # dark clouds, rain forecast
TARGET = 1.0  # yes, take an umbrella
ROUNDS = 4


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


random.seed(SEED)
weights = [random.uniform(-1, 1) for _ in INPUTS]

for round in range(ROUNDS):
    output = sigmoid(sum(w * x for w, x in zip(weights, INPUTS)))
    error = TARGET - output
    print(f"round {round + 1}: weights {weights[0]:+.2f} {weights[1]:+.2f}  answer {output:.2f}  error {error:+.2f}")
    weights = [w + LEARNING_RATE * error * x for w, x in zip(weights, INPUTS)]
