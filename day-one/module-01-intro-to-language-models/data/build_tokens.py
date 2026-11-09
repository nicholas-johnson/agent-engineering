import json
import re
from collections import Counter
from pathlib import Path

DATA = Path(__file__).parent
VOCABULARY_SIZE = 500

text = " ".join((DATA / "alice.txt").read_text().lower().split())

# Start with every single character, then repeatedly merge the most common pair.
pieces = Counter(re.findall(r" ?[a-z]+| ?[^a-z ]", text))
words = {tuple(piece): count for piece, count in pieces.items()}
tokens = sorted(set(text))

while len(tokens) < VOCABULARY_SIZE:
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

(DATA / "tokens.json").write_text(json.dumps(tokens, indent=2))
print(f"Wrote {len(tokens)} tokens")
