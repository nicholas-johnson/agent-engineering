# Log probabilities

From the module folder (`day-one/module-02-building-a-chatbot`):

```bash
uv run python playground/logprobs/play.py
```

Or without `uv` (set up `.venv` once at the repo root with `python3 -m venv .venv && .venv/bin/pip install -e .`):

```bash
source ../../.venv/bin/activate
python playground/logprobs/play.py
```

Needs `OPENAI_API_KEY` in `.env`. The full results are written to `playground/logprobs/output/logprobs.json`.

---

Module 1 was all about vectors of next-token probabilities. A real model produces exactly the same thing, and the API will show you part of it: for each token it wrote, the five most likely tokens it could have written instead.

```text
=== Alice was beginning to get ===
'very'         'very' 80%, 'rather' 15%, 'b' 2%, 't' 2%
' tired'       ' tired' 100%
' of'          ' of' 100%
' sitting'     ' sitting' 100%
' by'          ' by' 100%
' her'         ' her' 100%
' sister'      ' sister' 100%
...

=== The capital of France is ===
'Paris'        ' Paris' 59%, 'Paris' 41%
'.'            '.' 98%
```

The left column is the token the model chose, and the rest are its top choices at that point.

## Things to notice

- **It has memorised *Alice*.** After "very", it is 100% sure of every token: it is reciting the opening line of the book, just like our five-word model in Module 1.
- **`' Paris'` and `'Paris'` are different tokens.** One has a leading space. The model splits its bet between them, but either way the answer is Paris. This is Module 1's tokenizer at work.
- **The model is usually very sure.** That's why the `temperature` playground needs temperature 1.5 before the answer changes.
- The API calls these **log probabilities** (`logprob`), the natural log of the probability. The script turns them back into percentages with `math.exp`.
- Log probabilities only work with reasoning effort `"none"`. Otherwise the API says *"logprobs are not supported with reasoning models."*

## Try this

1. **Your own prompts.** Add prompts to `PROMPTS`. Find one where the model is really unsure.
2. **Famous lines.** Try the opening of another famous book, a song, or a speech. What has the model memorised word for word?
3. **Confidence colours.** Print the reply with each token coloured by how sure the model was: green above 90%, yellow above 50%, red below. (Search for "ANSI colour codes".)
4. **Score a sentence.** Module 1's `score-a-sentence` playground worked out how likely a sentence was. Can you do the same with a real model? (Hint: give it the sentence and ask it to repeat it exactly.)
5. **Where it went wrong.** Ask a question the model gets wrong. Is it unsure at the wrong token, or confidently wrong?

## Questions

For discussion. There are no right answers.

- The model was 100% sure of every word of the book's opening line. Is being confident the same as being right?
- If a chatbot showed you how sure it was of every word, would you trust it more or less?
- The model can recite a famous book word for word. What does that mean for copyright?
