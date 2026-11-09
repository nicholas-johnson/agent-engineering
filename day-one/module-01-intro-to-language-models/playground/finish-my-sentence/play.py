import json
import random
import re
from pathlib import Path

MODULE = Path(__file__).parent.parent.parent
MODELS = MODULE / "demo" / "output"

word_pairs = json.loads((MODELS / "01_word_pairs_alice.json").read_text())
five_words = json.loads((MODELS / "02_context_window_alice.json").read_text())
eight_letters = json.loads((MODELS / "03_letters_alice.json").read_text())
four_tokens = json.loads((MODELS / "04_tokens_alice.json").read_text())

vocabulary = set(json.loads((MODULE / "data" / "tokens.json").read_text()))
longest = max(len(token) for token in vocabulary)


def split_into_words(text):
    return re.findall(r"[a-z']+|[.,!?;:]", text)


def split_into_tokens(text):
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


def pick(next_options):
    return random.choices(list(next_options), weights=list(next_options.values()))[0]


def complete_words(model, window, start):
    words = split_into_words(start)
    while len(words) < 100 and words[-1] not in {".", "!", "?"}:
        context = " ".join(words[-window:])
        if context not in model:
            return " ".join(words) + "  [stuck]"
        words.append(pick(model[context]))
    return " ".join(words)


def complete_letters(start):
    text = start
    while len(text) < 300 and text[-1] not in ".!?":
        if text[-8:] not in eight_letters:
            return text + "  [stuck]"
        text += pick(eight_letters[text[-8:]])
    return text


def complete_tokens(start):
    tokens = split_into_tokens(" " + start)
    while len(tokens) < 80 and not any(mark in tokens[-1] for mark in ".!?"):
        context = "|".join(tokens[-4:])
        if context not in four_tokens:
            return "".join(tokens).strip() + "  [stuck]"
        tokens.append(pick(four_tokens[context]))
    return "".join(tokens).strip()


while True:
    start = input("\nStart a sentence (Enter to stop): ").strip().lower()
    if not start:
        break
    print("Word pairs:   ", complete_words(word_pairs, 1, start))
    print("Five words:   ", complete_words(five_words, 5, start))
    print("Eight letters:", complete_letters(start))
    print("Four tokens:  ", complete_tokens(start))
