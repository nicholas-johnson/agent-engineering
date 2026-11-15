# Temperature

Every LLM API has a `temperature` setting. You'll complete the same sentence at five temperatures and see what that does to the probabilities.

From the module folder (`day-one/module-01-intro-to-language-models`):

```bash
uv run python playground/temperature/play.py
```

Or without `uv` (standard library only, no packages needed):

```bash
python3 playground/temperature/play.py
```

Builds a word-pair model from `data/alice.txt`, completes the same sentence at five temperatures, and writes `playground/temperature/output/after_the.json`.

---

Before picking the next word, raise every probability to the power `1 / temperature`, then rescale so they add up to 1 again:

```python
weights = {word: p ** (1 / temperature) for word, p in next_words.items()}
```

- **Low temperature** (0.1) makes likely words much more likely. The model almost always takes its top choice.
- **Temperature 1** leaves the probabilities alone. This is what the demos do.
- **High temperature** (5) flattens everything out. Rare words get nearly as much chance as common ones.

The script completes the same sentence three times at each temperature. It also writes `playground/temperature/output/after_the.json`: the top ten words after "the" at each temperature, so you can see the vector being reshaped.

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
4. **Letters instead of words.** Count eight-letter contexts instead of word pairs (as in demo 3). What does high temperature do to letters?
5. **Find the sweet spot.** Which temperature gives the most Alice-like sentences? Is it always 1?

## Questions

For discussion. There are no right answers.

- Always picking the most likely word makes the text go round in circles. Why isn't the most likely word the best word?
- What temperature would you want for a legal contract? A poem? A chatbot answering customers' questions?
- Temperature doesn't change the model at all, only how we pick from its probabilities. Is it part of the model, or part of how we use it?

## Further reading

- **Holtzman, A., Buys, J., Du, L., Forbes, M. & Choi, Y. (2020). "The Curious Case of Neural Text Degeneration." _ICLR 2020_.** [arXiv:1904.09751](https://arxiv.org/abs/1904.09751). Why always picking the most likely word goes round in circles, on large neural models as well as this one. **Top-p** sampling, in the exercises, comes from this paper.

## Rabbit holes

Optional extensions and interesting things to look at.

1. **llama.cpp's sampler.** Temperature, top-k, top-p and min-p are separate steps in a chain. Read `llama_sampler` in [llama.cpp](https://github.com/ggml-org/llama.cpp) and match each step to the formula above.
2. **Min-p.** **Nguyen, M. N. et al. (2025). "Turning Up the Heat: Min-p Sampling for Creative and Coherent LLM Outputs." _ICLR 2025_.** [arXiv:2407.01082](https://arxiv.org/abs/2407.01082). Drop every token whose probability is below a fraction of the top token's. Implement it beside top-p, and see which one still makes sense at a high temperature.
