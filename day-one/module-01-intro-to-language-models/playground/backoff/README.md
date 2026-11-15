# Backoff

When a long context has never been seen, **backoff** tries a shorter one: five words, then four, then three, then two, then one. You'll complete a sentence and see which window each word came from.

From the module folder (`day-one/module-01-intro-to-language-models`):

```bash
uv run python playground/backoff/play.py
```

Or without `uv` (standard library only, no packages needed):

```bash
python3 playground/backoff/play.py
```

Builds word models for windows 1 to 5 from `data/alice.txt`, and writes all five to `playground/backoff/output/backoff_counts.json`.

---

If the last five words are unknown, try the last four, and keep stepping down:

```python
for window in range(5, 0, -1):
    context = " ".join(words[-window:])
    if context in models[window]:
        ...
```

Each generated word gets a small number showing which window it came from:

```text
=== the mouse said to the ===
the mouse said to the dormouse³ ,⁴ not⁵ choosing⁵ to⁵ notice⁵ this⁵ last⁵ remark⁵ .⁵

=== she looked at the dragon ===
she looked at the dragon  [stuck]
```

"the mouse said to the" has never been seen, so the model backs off to three words: "to the dormouse". After that it finds a five-word context it knows, and from then on it is reciting the book again.

"dragon" isn't in the book at all, so even one word of context doesn't help.

## Things to notice

- How quickly does it lock back onto a five-word context? Once it does, it is copying the book.
- Most of the "creative" moments are the low numbers.

## Try this

1. **Shorter memory.** Set `LONGEST_WINDOW = 3`. Is the text more inventive? Is it still English?
2. **Interpolation.** Instead of using only the longest window that matches, mix them all. Add up the probabilities from every window, giving longer windows more weight (say 1, 2, 4, 8, 16). Does it still recite?
3. **Unknown words.** When even one word fails, pick a common word like "the" or "and" instead of giving up. What happens after "the dragon"?
4. **Add-one smoothing.** Pretend every word in the vocabulary followed every context once more than it did. Now no word ever has zero probability. What does that do to the completions?
5. **Tokens.** Back off over token windows instead of word windows. Unknown words stop being a problem. Why?

## Questions

For discussion. There are no right answers.

- Backoff guesses from less information when it doesn't know. When should a model admit it doesn't know instead of guessing?
- Most of the surprising words came from the short windows. Is creativity just guessing with less to go on?
- How is backoff like what you do when you half understand a sentence in a language you are learning?

## Further reading

- **Katz, S. M. (1987). "Estimation of probabilities from sparse data for the language model component of a speech recognizer." *IEEE Transactions on Acoustics, Speech, and Signal Processing* 35(3):400–401.** Two pages that introduced backoff, and kept the probabilities adding up to 1. This playground is that idea.
- **Brants, T., Popat, A. C., Xu, P., Och, F. J. & Dean, J. (2007). "Large Language Models in Machine Translation." *EMNLP-CoNLL 2007*.** Counting models trained on up to two trillion words. At that scale a version they called "stupid backoff" worked as well as the careful one.
