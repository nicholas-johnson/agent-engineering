# Neural knobs

The neural model from the module, with its settings out where you can change them. You'll train it, watch the loss fall, then complete sentences with the model you saved.

From the module folder (`day-one/module-01-intro-to-language-models`):

```bash
uv run python playground/neural-knobs/train.py
uv run python playground/neural-knobs/complete.py
```

Or without `uv` (standard library only, no packages needed):

```bash
python3 playground/neural-knobs/train.py
python3 playground/neural-knobs/complete.py
```

Training takes a minute or two with the default settings and saves `playground/neural-knobs/output/model.json`; `complete.py` is interactive (press Enter on an empty line to stop).

---

Two things are different from demo 5:

- **It saves what it learned.** `train.py` trains the model and writes it to `playground/neural-knobs/output/model.json`. `complete.py` loads that file, so you can train once and complete as many sentences as you like.
- **It shows the loss as it trains**, so you can see what each setting does.

```text
Loss from random guessing: 6.21
Step 1000: loss 5.85
...
Step 30000: loss 4.26
Saved output/model.json
```

```text
Start a sentence (Enter to stop): the mouse said to
the mouse said to a they!
```

## The knobs

All at the top of `train.py`:

| Setting          | Default | What it is                               |
| ---------------- | ------- | ---------------------------------------- |
| `CONTEXT`        | 3       | How many tokens the model looks at       |
| `EMBEDDING_SIZE` | 16      | How many numbers describe each token     |
| `HIDDEN_SIZE`    | 32      | How many neurons in the hidden layer     |
| `LEARNING_RATE`  | 0.05    | How big a nudge each training step gives |
| `STEPS`          | 30000   | How many training examples it sees       |

Change one at a time, retrain, and compare the final loss and the completions. Lower loss is better, but remember the model only ever sees _Alice_, so a very low loss can just mean it has memorised the book.

## Try this

1. **Learning rate.** Try 0.005 and 0.5. One is too slow; what happens with the other?
2. **Context.** Try `CONTEXT = 1`. You now have a neural word-pair model. How does it compare to demo 1? Then try 6.
3. **Train longer.** Try 100,000 steps (start it and go for a coffee). Does the loss keep falling? Do the completions improve?
4. **Is it memorising?** Train on every chapter except the last, then measure the loss on the last chapter, which the model has never seen. Compare it with the training loss. If the training loss keeps falling but the last-chapter loss doesn't, the model is memorising rather than learning.
5. **Temperature.** Add a temperature to `complete.py` (see `../temperature`). Can you make the completions more readable?
6. **Another layer.** Add a second hidden layer. You will need to extend `forward` and the backpropagation in `train`. This is the hardest one here, and the best way to really understand backpropagation.

## Questions

For discussion. There are no right answers.

- The loss keeps going down. Is a lower loss always better? How would you know if the model was just memorising the book?
- We trained for two minutes on a laptop. Frontier models train for months on thousands of GPUs. What changes, and what stays the same?
- Which knob made the biggest difference, and why do you think that was?

## Further reading

- **Bengio, Y., Ducharme, R., Vincent, P. & Jauvin, C. (2003). "A Neural Probabilistic Language Model." _Journal of Machine Learning Research_ 3:1137–1155.** [PDF](https://www.jmlr.org/papers/volume3/bengio03a/bengio03a.pdf). The model you are training. The introduction is the problem the knobs are for: too many contexts to count, so learn a vector for each word.
- **Kaplan, J., McCandlish, S., Henighan, T., Brown, T. B., Chess, B., Child, R., Gray, S., Radford, A., Wu, J. & Amodei, D. (2020). "Scaling Laws for Neural Language Models."** [arXiv:2001.08361](https://arxiv.org/abs/2001.08361). What happens to the loss as the model gets bigger and the training gets longer. It falls smoothly, as a power law.

## Rabbit holes

Optional extensions and interesting things to look at.

1. **makemore, part 2.** Andrej Karpathy's second makemore lecture, on [karpathy.ai/zero-to-hero](https://karpathy.ai/zero-to-hero.html), builds this model line by line: a vector per word, one hidden layer, a loss, a backward pass.
2. **Check the gradients.** Rebuild `forward` in PyTorch and compare its gradients with the ones `train.py` works out by hand. Where they disagree, the hand-written backward pass is wrong.
