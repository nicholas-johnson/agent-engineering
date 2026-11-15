# Finish my sentence

From the module folder (`day-one/module-01-intro-to-language-models`):

```bash
uv run python playground/finish-my-sentence/play.py
```

Or without `uv` (standard library only, no packages needed):

```bash
python3 playground/finish-my-sentence/play.py
```

Builds all four counting models directly from `data/alice.txt`. Press Enter on an empty line to stop.

---

Type the start of a sentence and watch all four counting models finish it, side by side. When a model reaches a context it has never seen, it gives up and prints `[stuck]`.

```text
Start a sentence (Enter to stop): the queen said
Word pairs:    the queen said alice , said was mouth ; you ever : she felt unhappy at it .
Five words:    the queen said  [stuck]
Eight letters: the queen said nothing of the busy farm-yard - while the duchess took no notice of her favourite word 'moral,' and the muscular strength, which gave the experiment?
Four tokens:   the queen said  [stuck]
```

## Things to notice

- Each model needs a prompt at least as long as its window: five words, eight letters, four tokens. "the queen said" is only three tokens, so the token model is stuck before it starts.
- Even with a long enough prompt, the five-word and four-token models are stuck on almost anything not copied from the book. Try `alice was beginning to get`, then `the king looked at the`.
- Try a word that isn't in the book at all, like `the robot`. Which models can cope?

## Try this

1. **Find a prompt that beats every model.** What is the shortest prompt that leaves all four `[stuck]`?
2. **Show the odds.** Print the probability of each word as it is chosen. Where is the model sure, and where is it guessing?
3. **Don't get stuck.** When the five-word model is stuck, fall back to the word-pair model instead of giving up. (The `backoff` playground does this properly.)
4. **Add the neural model.** Train one with the `neural-knobs` playground, then load its `model.json` here and add a fifth line. Does it ever get stuck?
5. **Use chapter 1.** Change `CORPUS` at the top of `play.py` to `DATA / "alice-chapter-1.txt"`. How much more often does each model get stuck?

## Questions

For discussion. There are no right answers.

- Which of the four models would you call the best? Best at what: sounding like English, saying something new, or never getting stuck?
- The five-word model is fluent on anything from the book and stuck on almost everything else. Is a model that can only recite useful for anything?
- Our models say `[stuck]` when they don't know. Real chatbots never do. Which would you rather have, and why?
