# Score a sentence — run a bigram model backwards to measure how surprising text is.
# Run from the module folder: uv run python playground/score-a-sentence/play.py
#                         or: python3 playground/score-a-sentence/play.py
#
# To play: add your own sentences to SENTENCES, or change SMOOTHING (try 1.0 vs 0.01)
# to see how unseen word pairs affect perplexity (see README.md).

import math
import re
from collections import Counter, defaultdict
from pathlib import Path

MODULE = Path(__file__).parent.parent.parent
OUTPUT = Path(__file__).parent / "output"
OUTPUT.mkdir(exist_ok=True)

# Extra count added to every possible next word so unseen pairs never get probability 0.
SMOOTHING = 0.01

SENTENCES = [
    "Alice was beginning to get very tired of sitting by her sister on the bank.",
    "The Queen was beginning to get very cross with the Hatter.",
    "Bank the on sister her by sitting of tired very get to beginning was Alice.",
    "The server returned an error because the database was down.",
]


def split_into_words(text):
    return re.findall(r"[a-z']+|[.,!?;:]", text.lower())


# Count word pairs in Alice.
words = split_into_words((MODULE / "data" / "alice.txt").read_text())
counts = defaultdict(Counter)
for word, next_word in zip(words, words[1:]):
    counts[word][next_word] += 1
vocabulary_size = len(set(words)) + 1  # +1 for any word not in Alice


def probability(word, next_word):
    # Smoothed probability of `next_word` following `word`.
    total = sum(counts[word].values()) + SMOOTHING * vocabulary_size
    return (counts[word][next_word] + SMOOTHING) / total


# Score each sentence and write every word-by-word step to output/scores.txt.
with open(OUTPUT / "scores.txt", "w") as file:
    for sentence in SENTENCES:
        sentence_words = split_into_words(sentence)
        probabilities = [probability(w, n) for w, n in zip(sentence_words, sentence_words[1:])]
        # Perplexity: lower means the model was less surprised by the sentence.
        perplexity = math.exp(-sum(math.log(p) for p in probabilities) / len(probabilities))

        file.write(f"{sentence}\nPerplexity: {perplexity:.0f}\n")
        for word, next_word, p in zip(sentence_words, sentence_words[1:], probabilities):
            file.write(f"  {word:>14} -> {next_word:<14} {p:.6f}\n")
        file.write("\n")

        print(f"{perplexity:8.0f}  {sentence}")
