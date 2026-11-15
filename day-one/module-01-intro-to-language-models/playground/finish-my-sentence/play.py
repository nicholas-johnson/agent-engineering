# Finish my sentence — watch all four counting models finish your prompt side by side.
# Run from the module folder: uv run python playground/finish-my-sentence/play.py
#                         or: python3 playground/finish-my-sentence/play.py
#
# To play: run the script and type sentence starters (try phrases from Alice vs new ones),
# or change CORPUS below to alice-chapter-1.txt to see how much sooner models get stuck.

import json
import random
import re
from collections import Counter, defaultdict
from pathlib import Path

DATA = Path(__file__).parent.parent.parent / "data"

# Swap to DATA / "alice-chapter-1.txt" to train on chapter 1 instead of the whole book.
CORPUS = DATA / "alice.txt"

vocabulary = set(json.loads((DATA / "tokens.json").read_text()))
longest = max(len(token) for token in vocabulary)


def split_into_words(text):
    return re.findall(r"[a-z']+|[.,!?;:]", text.lower())


def split_into_tokens(text):
    # Greedy longest-match split using the 500-token vocabulary from data/tokens.json.
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


def build_model(items, window):
    # Map every seen tuple of `window` items to {next_item: probability}.
    counts = defaultdict(Counter)
    for i in range(len(items) - window):
        counts[tuple(items[i : i + window])][items[i + window]] += 1
    return {
        context: {item: count / sum(next_items.values()) for item, count in next_items.items()}
        for context, next_items in counts.items()
    }


# Build all four counting models from the corpus.
raw_text = CORPUS.read_text()
words = split_into_words(raw_text)
clean_text = " ".join(raw_text.lower().split())

word_pairs = build_model(words, 1)
five_words = build_model(words, 5)
eight_letters = build_model(clean_text, 8)
four_tokens = build_model(split_into_tokens(clean_text), 4)


def pick(next_options):
    return random.choices(list(next_options), weights=list(next_options.values()))[0]


def complete_words(model, window, start):
    words = split_into_words(start)
    if not words:
        return start + "  [stuck]"
    while len(words) < 100 and words[-1] not in {".", "!", "?"}:
        context = tuple(words[-window:])
        if context not in model:
            return " ".join(words) + "  [stuck]"
        words.append(pick(model[context]))
    return " ".join(words)


def complete_letters(start):
    text = start
    while len(text) < 300 and text[-1] not in ".!?":
        context = tuple(text[-8:])
        if context not in eight_letters:
            return text + "  [stuck]"
        text += pick(eight_letters[context])
    return text


def complete_tokens(start):
    tokens = split_into_tokens(" " + start)
    while len(tokens) < 80 and not any(mark in tokens[-1] for mark in ".!?"):
        context = tuple(tokens[-4:])
        if context not in four_tokens:
            return "".join(tokens).strip() + "  [stuck]"
        tokens.append(pick(four_tokens[context]))
    return "".join(tokens).strip()


# Interactive prompt loop: press Enter on an empty line to quit.
while True:
    start = input("\nStart a sentence (Enter to stop): ").strip().lower()
    if not start:
        break
    print("Word pairs:   ", complete_words(word_pairs, 1, start))
    print("Five words:   ", complete_words(five_words, 5, start))
    print("Eight letters:", complete_letters(start))
    print("Four tokens:  ", complete_tokens(start))
