# Your own generation loop

From the module folder (`day-one/module-03-choosing-a-provider`):

```bash
uv run --extra local python playground/your-own-loop/play.py
```

Or without `uv` (set up `.venv` with the `local` extra once at the repo root: `python3 -m venv .venv && .venv/bin/pip install -e ".[local]"`):

```bash
source ../../.venv/bin/activate
python playground/your-own-loop/play.py
```

The first run downloads `Qwen/Qwen3-1.7B` from Hugging Face (about 4 GB) if it isn't cached yet. Every step, with the top five choices, is written to `playground/your-own-loop/output/steps.json`.

---

In Module 1 we wrote a loop that completed *"alice was beginning to get"* one word at a time, by picking from a vector of probabilities. This is the same loop, written by hand, running on a real open model: Qwen3 1.7B, loaded with `transformers`.

```python
for _ in range(NEW_TOKENS):
    scores = model(tokens).logits[0, -1]
    probabilities = torch.softmax(scores / TEMPERATURE, dim=-1)
    choice = torch.multinomial(probabilities, 1)
    tokens = torch.cat([tokens, choice.unsqueeze(0)], dim=1)
```

Ask the model for scores, turn them into probabilities, pick one, add it to the end, repeat. That's essentially what `model.generate()` does, plus some tricks for speed.

```text
Alice was beginning to get interested in teaching, but she had no time for it, because she had to study for her first degree.
```

## Things to notice

Open `playground/your-own-loop/output/steps.json`. The first step:

```text
chosen ' interested'    top 5: ' tired' 27%, ' worried' 21%, ' nervous' 10%, ' a' 7%, ' the' 4%
```

"tired" (the word in the book) was the favourite, but only at 27%. At temperature 0.8 the loop picked "interested", which wasn't in the top five at all. One unlikely choice, and the whole sentence went somewhere else.

Compare with `gpt-6-luna` in Module 2's `logprobs` playground, which was 100% sure of every word of the opening line. A small model hasn't memorised the book.

There are no chat instructions here, just raw text, so the model simply continues it.

## Try this

1. **Temperature.** Set `TEMPERATURE = 0.1`, then `2.0`. Module 1's temperature playground, on a real model.
2. **Greedy.** Replace the `torch.multinomial` line with `torch.argmax(probabilities).unsqueeze(0)`: always pick the top token. Does it loop, like Module 1's word-pair model did?
3. **Top-k.** Before picking, keep only the 20 most likely tokens. Does it stay more sensible?
4. **A chat.** Build the prompt with `tokenizer.apply_chat_template` (as in demo 5) instead of raw text. Now it answers instead of continuing.
5. **Stop at the end.** Stop the loop when the model picks its end-of-text token (`tokenizer.eos_token_id`), instead of after a fixed number of tokens.
6. **Faster.** Each step runs the whole sequence through the model again. Look up "KV cache" in the `transformers` documentation and pass `past_key_values` between steps. How much faster is it?

## Questions

For discussion. There are no right answers.

- `model.generate()` is essentially this loop. Does seeing the loop change how you think about what a chatbot is?
- One unlikely token sent the whole sentence somewhere else. What does that say about how reliable generated text is?
- You can see every probability here. Could you build something that warns users when a model is unsure? Would they want it?
