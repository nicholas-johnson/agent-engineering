# Neural knobs

The neural model from demo 5, with two changes:

- **It saves what it learned.** `train.py` trains the model and writes it to `output/model.json`. `complete.py` loads that file, so you can train once and complete as many sentences as you like.
- **It shows the loss as it trains**, so you can see what each setting does.

```bash
uv run python train.py
uv run python complete.py
```

No demos need to be run first. Training takes a minute or two with the default settings.

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

| Setting | Default | What it is |
|---------|---------|------------|
| `CONTEXT` | 3 | How many tokens the model looks at |
| `EMBEDDING_SIZE` | 16 | How many numbers describe each token |
| `HIDDEN_SIZE` | 32 | How many neurons in the hidden layer |
| `LEARNING_RATE` | 0.05 | How big a nudge each training step gives |
| `STEPS` | 30000 | How many training examples it sees |

Change one at a time, retrain, and compare the final loss and the completions. Lower loss is better, but remember the model only ever sees *Alice*, so a very low loss can just mean it has memorised the book.

## Try this

1. **Learning rate.** Try 0.005 and 0.5. One is too slow; what happens with the other?
2. **Context.** Try `CONTEXT = 1`. You now have a neural word-pair model. How does it compare to demo 1? Then try 6.
3. **Train longer.** Try 100,000 steps (start it and go for a coffee). Does the loss keep falling? Do the completions improve?
4. **Is it memorising?** Train on every chapter except the last, then measure the loss on the last chapter, which the model has never seen. Compare it with the training loss. If the training loss keeps falling but the last-chapter loss doesn't, the model is memorising rather than learning.
5. **Temperature.** Add a temperature to `complete.py` (see `../temperature`). Can you make the completions more readable?
6. **Another layer.** Add a second hidden layer. You will need to extend `forward` and the backpropagation in `train`. This is the hardest one here, and the best way to really understand backpropagation.
