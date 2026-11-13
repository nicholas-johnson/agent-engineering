# Tokenizer lab

How big should a token vocabulary be, and what happens to text the tokenizer wasn't trained on?

This builds a byte-pair encoding vocabulary from *Alice*, the same way as `data/build_tokens.py`, but carries on to 2,000 tokens. Because each merge is added to the end of the list, the first 100 tokens are a 100-token vocabulary, the first 500 are a 500-token vocabulary, and so on. It then splits some sample text with each one.

```bash
uv run python play.py
```

No demos need to be run first. It takes a few seconds, and writes each vocabulary to `output/tokens_<size>.json`.

```text
=== alice was beginning to get very tired of sitting by her sister ===
  100 tokens in vocabulary: 34 tokens  ['a', 'lice', ' w', 'as', ' be', 'g', 'in', 'n', 'ing', ...]
  500 tokens in vocabulary: 19 tokens  ['al', 'ice', ' was', ' begin', 'ning', ' to', ' get', ...]
 2000 tokens in vocabulary: 12 tokens  ['alice', ' was', ' beginning', ' to', ' get', ' very', ' tired', ...]

=== strawberry ===
 2000 tokens in vocabulary:  5 tokens  ['st', 'raw', 'be', 'r', 'ry']

=== 1234 + 5678 = 6912 ===
 2000 tokens in vocabulary: 18 tokens  ['1', '2', '3', '4', ' ', '+', ' ', '5', ...]
```

## Things to notice

- **Bigger vocabulary, fewer tokens.** With 2,000 tokens, every word in the *Alice* sentence is a single token. Fewer tokens means a context window holds more text, but there are more possible contexts.
- **Text from somewhere else costs more.** "server", "returned" and "error" never appear in *Alice*, so they get chopped into pieces. This is why text in languages that weren't well represented in a tokenizer's training data uses more tokens, and costs more.
- **Strawberry.** The model sees `'st', 'raw', 'be', 'r', 'ry'`, not ten letters. Ask it how many r's are in strawberry and it has to work that out from tokens it has never seen the inside of. This is why LLMs famously get it wrong.
- **Unknown characters.** *Alice* has no digits, `+` or `=`, so they are not in any vocabulary and each falls back to a single unknown character. Real tokenizers start from all 256 possible bytes instead of the characters in the book, so nothing is ever unknown.

## Try this

1. **Find the cost of a word.** Which words in the samples take the most tokens? Write some modern sentences and count their tokens with each vocabulary.
2. **Train on code.** Build the vocabulary from some Python source instead of *Alice* (see `../other-books/play.py` for where to find some). What do the first 100 merges look like? Is `"    "` (four spaces) a token?
3. **Real BPE.** The splitter here takes the longest token that matches. Real BPE splits text into single characters and then replays the merges, in the order they were learned. Write that, and find a word where the two give different answers.
4. **Numbers.** Add some digits to the training text. Does `1234` become one token, two, or four? Why might that make arithmetic hard for an LLM?
5. **Bigger still.** Try 5,000 tokens. What kinds of tokens does it add at the end? Does anything get worse?

## Questions

For discussion. There are no right answers.

- Text in languages the tokenizer wasn't trained on uses more tokens, so it costs more and fits less in the context window. Is that fair? Who pays?
- Why might a bigger vocabulary not always be better?
- The model never sees the letters inside "strawberry". What other tasks might be hard for the same reason?
