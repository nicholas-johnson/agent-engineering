# Tokenizer lab

How big should a token vocabulary be, and what happens to text the tokenizer wasn't trained on? You'll build vocabularies of 100, 500 and 2,000 tokens from *Alice*, then split some sample text with each one.

From the module folder (`day-one/module-01-intro-to-language-models`):

```bash
uv run python playground/tokenizer-lab/play.py
```

Or without `uv` (standard library only, no packages needed):

```bash
python3 playground/tokenizer-lab/play.py
```

Takes a few seconds, and writes each vocabulary to `playground/tokenizer-lab/output/tokens_<size>.json`.

---

This builds a byte-pair encoding vocabulary from *Alice*, the same way as `data/build_tokens.py`, but carries on to 2,000 tokens. Because each merge is added to the end of the list, the first 100 tokens are a 100-token vocabulary, the first 500 are a 500-token vocabulary, and so on. It then splits some sample text with each one.

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

## Further reading

- **Sennrich, R., Haddow, B. & Birch, A. (2016). "Neural Machine Translation of Rare Words with Subword Units." *ACL 2016*.** [arXiv:1508.07909](https://arxiv.org/abs/1508.07909). The paper that used byte-pair encoding for language. The algorithm is a short Python listing. Compare it with the vocabulary this playground builds.
- **Radford, A., Wu, J., Child, R., Luan, D., Amodei, D. & Sutskever, I. (2019). "Language Models are Unsupervised Multitask Learners." OpenAI.** [PDF](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf). Section 2.2, byte-level BPE: start from all 256 bytes, so a character this vocabulary has never seen, such as a digit, is never unknown.

## Rabbit holes

Optional. These leave the script.

1. **tiktoken.** Split the same samples with the encoding it uses for current OpenAI models (`o200k_base`): "strawberry", a line of Python, and a line of Chinese. Where does it agree with the 2,000-token vocabulary from *Alice*, and where does it spend more tokens?
2. **The pre-tokenizer.** In tiktoken's source, find the regular expression that runs before any merge. The merges are the easy part. The expression is why code, contractions and spaces split the way they do.
