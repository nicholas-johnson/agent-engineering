import json
import re
from collections import Counter
from pathlib import Path

MODULE = Path(__file__).parent.parent.parent
OUTPUT = Path(__file__).parent / "output"
OUTPUT.mkdir(exist_ok=True)

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


text = " ".join((MODULE / "data" / "alice.txt").read_text().lower().split())
all_tokens = build_vocabulary(text, max(SIZES))

vocabularies = {}
for size in SIZES:
    vocabularies[size] = set(all_tokens[:size])
    (OUTPUT / f"tokens_{size}.json").write_text(json.dumps(all_tokens[:size], indent=2))

for sample in SAMPLES:
    print(f"=== {sample} ===")
    for size in SIZES:
        tokens = split_into_tokens(sample, vocabularies[size])
        print(f"{size:>5} tokens in vocabulary: {len(tokens):>2} tokens  {tokens}")
    print()
