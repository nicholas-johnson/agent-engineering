# Temperature

Every LLM API has a `temperature` setting. This is what it does.

Before picking the next word, raise every probability to the power `1 / temperature`, then rescale so they add up to 1 again:

```python
weights = {word: p ** (1 / temperature) for word, p in next_words.items()}
```

- **Low temperature** (0.1) makes likely words much more likely. The model almost always takes its top choice.
- **Temperature 1** leaves the probabilities alone. This is what the demos do.
- **High temperature** (5) flattens everything out. Rare words get nearly as much chance as common ones.

```bash
uv run python play.py
```

Run demo 1 first: this uses the whole-book word-pair model from `demo/output/`.

The script completes the same sentence three times at each temperature. It also writes `output/after_the.json`: the top ten words after "the" at each temperature, so you can see the vector being reshaped.

```text
=== temperature 0.1 ===
alice was beginning to get out of the queen , and the queen , and the gryphon , and the queen , and the king , and the king ,

=== temperature 5.0 ===
alice was beginning to get through into her mouth close by talking such dainties would catch him : really clever ?
```

At 0.1 the chance of "queen" after "the" goes from 4% to 56%. The model goes round in circles: the queen, and the king, and the queen...

## Try this

1. **Greedy.** Write `temperature 0`: always take the single most likely word, no randomness. How quickly does it start looping? Why can't it ever stop?
2. **Top-k.** Before picking, keep only the `k` most likely words and throw the rest away. Try `k = 3`. How does it compare to a low temperature?
3. **Top-p.** Keep the most likely words until their probabilities add up to `p` (say 0.9), and throw away the rest. This is what most LLM APIs call `top_p`. Why might it be better than top-k?
4. **A different model.** Load the letter model (`03_letters_alice.json`) instead. What does high temperature do to letters?
5. **Find the sweet spot.** Which temperature gives the most Alice-like sentences? Is it always 1?
