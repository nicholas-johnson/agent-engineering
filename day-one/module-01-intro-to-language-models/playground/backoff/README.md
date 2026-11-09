# Backoff

The five-word model from demo 2 has nothing to say about contexts it has never seen. **Backoff** is the classic fix, from before neural networks: if the last five words are unknown, try the last four. If those are unknown, try three, then two, then one.

```python
for window in range(5, 0, -1):
    context = " ".join(words[-window:])
    if context in models[window]:
        ...
```

```bash
uv run python play.py
```

This builds its own word models for windows 1 to 5 from `data/alice.txt`, so no demos need to be run first. It writes all five to `output/backoff_counts.json`.

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
