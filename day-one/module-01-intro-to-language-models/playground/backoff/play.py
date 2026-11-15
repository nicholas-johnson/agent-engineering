# Backoff — when a 5-word context is unseen, fall back to 4, 3, 2, then 1 word.
# Run from the module folder: uv run python playground/backoff/play.py
#                         or: python3 playground/backoff/play.py
#
# To play: change LONGEST_WINDOW or STARTS below, or edit next_word() to blend
# windows together or handle completely unknown words (see README.md).

import json
import random
import re
from collections import Counter, defaultdict
from pathlib import Path

MODULE = Path(__file__).parent.parent.parent
OUTPUT = Path(__file__).parent / "output"
OUTPUT.mkdir(exist_ok=True)

# Longest context window to try first before backing off to shorter ones.
LONGEST_WINDOW = 5
STARTS = [
    "alice was beginning to get",
    "the queen was beginning to get",
    "the mouse said to the",
    "she looked at the dragon",
]
SMALL_NUMBERS = "⁰¹²³⁴⁵⁶⁷⁸⁹"


def split_into_words(text):
    return re.findall(r"[a-z']+|[.,!?;:]", text.lower())


def build_model(words, window):
    counts = defaultdict(Counter)
    for i in range(len(words) - window):
        counts[" ".join(words[i : i + window])][words[i + window]] += 1
    return {context: dict(next_words) for context, next_words in counts.items()}


def next_word(words):
    # Try the longest window first; step down until we find a context seen in Alice.
    for window in range(LONGEST_WINDOW, 0, -1):
        context = " ".join(words[-window:])
        if context in models[window]:
            next_words = models[window][context]
            choice = random.choices(list(next_words), weights=list(next_words.values()))[0]
            return choice, window
    return None, 0


def complete_sentence(start):
    words = split_into_words(start)
    marked = list(words)
    while len(words) < 100 and words[-1] not in {".", "!", "?"}:
        word, window = next_word(words)
        if word is None:
            return " ".join(marked) + "  [stuck]"
        words.append(word)
        # Tag each generated word with the window size that produced it (e.g. dormouse³).
        marked.append(word + SMALL_NUMBERS[window])
    return " ".join(marked)


# Build word models for every window from 1 up to LONGEST_WINDOW.
words = split_into_words((MODULE / "data" / "alice.txt").read_text())
models = {window: build_model(words, window) for window in range(1, LONGEST_WINDOW + 1)}
(OUTPUT / "backoff_counts.json").write_text(json.dumps(models, indent=2))

for start in STARTS:
    print(f"=== {start} ===")
    for _ in range(3):
        print(complete_sentence(start))
    print()
