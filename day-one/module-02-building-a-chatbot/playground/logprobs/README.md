# Log probabilities

A real model's next-token probabilities, the same kind of vector the models in Module 1 produced. For each token it writes, you'll see the ones it nearly wrote instead.

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

- **It has memorised _Alice_.** After "very", it is 100% sure of every token: it is reciting the opening line of the book, just like our five-word model in Module 1.
- **`' Paris'` and `'Paris'` are different tokens.** One has a leading space. The model splits its bet between them, but either way the answer is Paris. This is Module 1's tokenizer at work.
- **The model is usually very sure.** That's why the `temperature` playground needs temperature 1.5 before the answer changes.
- The API calls these **log probabilities** (`logprob`), the natural log of the probability. The script turns them back into percentages with `math.exp`.
- Log probabilities only work with reasoning effort `"none"`. Otherwise the API says _"logprobs are not supported with reasoning models."_

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

## Further reading

- **Kadavath, S. et al. (2022). "Language Models (Mostly) Know What They Know."** [arXiv:2207.05221](https://arxiv.org/abs/2207.05221). When a model gives an answer a 70% probability, is it right about 70% of the time? Mostly, before it is trained to be an assistant.
- **OpenAI (2023). "GPT-4 Technical Report."** [arXiv:2303.08774](https://arxiv.org/abs/2303.08774). Figure 8. After that training, the probabilities sit too close to 100%. That is the wall of certainty in the output above.

## Rabbit holes

Optional extensions and interesting things to look at.

1. **Semantic entropy.** **Farquhar, S., Kossen, J., Kuhn, L. & Gal, Y. (2024). "Detecting hallucinations in large language models using semantic entropy." _Nature_ 630:625–630.** [PMC11186750](https://pmc.ncbi.nlm.nih.gov/articles/PMC11186750/). A token at 40% can be the same answer as the token at 60%. Sample several replies, group them by what they mean, and measure the uncertainty of the groups. The percentages in this playground are per token. Semantic entropy is per meaning.
2. **A wrong answer it is sure of.** Ask something the model usually misses, several times. If every sample says the same wrong thing, both kinds of uncertainty are low: it is sure, and wrong. The paper is about the other case, where the words change and the meaning changes with them.
