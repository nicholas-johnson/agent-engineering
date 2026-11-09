import math
import re
from collections import Counter, defaultdict
from pathlib import Path

MODULE = Path(__file__).parent.parent.parent
OUTPUT = Path(__file__).parent / "output"
OUTPUT.mkdir(exist_ok=True)

SMOOTHING = 0.01

SENTENCES = [
    "Alice was beginning to get very tired of sitting by her sister on the bank.",
    "The Queen was beginning to get very cross with the Hatter.",
    "Bank the on sister her by sitting of tired very get to beginning was Alice.",
    "The server returned an error because the database was down.",
]


def split_into_words(text):
    return re.findall(r"[a-z']+|[.,!?;:]", text.lower())


words = split_into_words((MODULE / "data" / "alice.txt").read_text())
counts = defaultdict(Counter)
for word, next_word in zip(words, words[1:]):
    counts[word][next_word] += 1
vocabulary_size = len(set(words)) + 1


def probability(word, next_word):
    # Add a little to every count, so words never seen together still get a small chance.
    total = sum(counts[word].values()) + SMOOTHING * vocabulary_size
    return (counts[word][next_word] + SMOOTHING) / total


with open(OUTPUT / "scores.txt", "w") as file:
    for sentence in SENTENCES:
        sentence_words = split_into_words(sentence)
        probabilities = [probability(w, n) for w, n in zip(sentence_words, sentence_words[1:])]
        perplexity = math.exp(-sum(math.log(p) for p in probabilities) / len(probabilities))

        file.write(f"{sentence}\nPerplexity: {perplexity:.0f}\n")
        for word, next_word, p in zip(sentence_words, sentence_words[1:], probabilities):
            file.write(f"  {word:>14} -> {next_word:<14} {p:.6f}\n")
        file.write("\n")

        print(f"{perplexity:8.0f}  {sentence}")
