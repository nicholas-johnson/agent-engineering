# Tokenizer lab — build BPE vocabularies of different sizes and see how they split text.
# Run from the module folder: uv run python playground/tokenizer-lab/play.py
#                         or: python3 playground/tokenizer-lab/play.py
#
# To play: add strings to SAMPLES, try larger vocabulary SIZES (e.g. 5000),
# or train on Python code instead of Alice (see README.md).

import json
import re
from collections import Counter
from pathlib import Path

MODULE = Path(__file__).parent.parent.parent
OUTPUT = Path(__file__).parent / "output"
OUTPUT.mkdir(exist_ok=True)

# Vocabulary sizes to compare (the first N merges of one BPE run give a size-N vocabulary).
SIZES = [100, 500, 2000]

SAMPLES = [
    "alice was beginning to get very tired of sitting by her sister",
    "the server returned a timeout error",
    "où est ma chatte?",
    "strawberry",
    "1234 + 5678 = 6912",
    "def add(a, b): return a + b",
]


def build_vocabulary(text, size):
    # Start with single characters, then repeatedly merge the most frequent adjacent pair.
    pieces = Counter(re.findall(r" ?[a-z]+| ?[^a-z ]", text))
    words = {tuple(piece): count for piece, count in pieces.items()}
    tokens = sorted(set(text))

    while len(tokens) < size:
        pairs = Counter()
        for symbols, count in words.items():
            for pair in zip(symbols, symbols[1:]):
                pairs[pair] += count

        first, second = max(pairs, key=pairs.get)
        tokens.append(first + second)

        merged_words = {}
        for symbols, count in words.items():
            merged = []
            i = 0
            while i < len(symbols):
                if symbols[i : i + 2] == (first, second):
                    merged.append(first + second)
                    i += 2
                else:
                    merged.append(symbols[i])
                    i += 1
            merged_words[tuple(merged)] = count
        words = merged_words
    return tokens


def split_into_tokens(text, vocabulary):
    # Greedy longest-match tokeniser; characters not in Alice stay as single characters.
    longest = max(len(token) for token in vocabulary)
    tokens = []
    i = 0
    while i < len(text):
        for size in range(longest, 0, -1):
            if text[i : i + size] in vocabulary:
                tokens.append(text[i : i + size])
                i += size
                break
        else:
            tokens.append(text[i])
            i += 1
    return tokens


# Learn up to max(SIZES) tokens from Alice, then slice out each vocabulary size.
text = " ".join((MODULE / "data" / "alice.txt").read_text().lower().split())
all_tokens = build_vocabulary(text, max(SIZES))

vocabularies = {}
for size in SIZES:
    vocabularies[size] = set(all_tokens[:size])
    (OUTPUT / f"tokens_{size}.json").write_text(json.dumps(all_tokens[:size], indent=2))

# Show how each sample gets split at every vocabulary size.
for sample in SAMPLES:
    print(f"=== {sample} ===")
    for size in SIZES:
        tokens = split_into_tokens(sample, vocabularies[size])
        print(f"{size:>5} tokens in vocabulary: {len(tokens):>2} tokens  {tokens}")
    print()
