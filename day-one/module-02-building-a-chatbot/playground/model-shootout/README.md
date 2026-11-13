# Model shootout

The same questions, sent to four different OpenAI models. How long does each take, how many tokens does it use, and is it any better?

```bash
uv run python play.py
```

Everything, including each model's full answer, is written to `output/shootout.json`.

```text
=== Why is a raven like a writing-desk? ===
gpt-6-luna       1.3s    24 tokens  Because Edgar Allan Poe wrote on both—though Lewis Carroll's original riddle had no intended answer.
gpt-6-sol        2.6s    86 tokens  Lewis Carroll originally intended the riddle to have no answer. He later suggested that both can produce a few notes, though they're very flat.
gpt-6.1-terra    2.7s    69 tokens  Because both can produce notes, though they're often flat. Lewis Carroll originally intended the riddle to have no answer.
gpt-6.1-sol      3.7s    78 tokens  Lewis Carroll originally gave the Mad Hatter's riddle no answer, but later suggested: "Because it can produce a few notes, tho they are very flat; and it is nevar put with the wrong end in front!" The deliberate spelling "nevar" is "raven" backward.
```

The Mad Hatter's riddle has no answer in the book, but Carroll added one in a later preface. Only `gpt-6.1-sol` knew the whole of it, including the joke: "nevar" is "raven" backwards. It also took nearly three times as long as `gpt-6-luna`, which went for a popular answer other people have suggested since ("Poe wrote on both").

All four got the strawberry question right ("3 times"), even though, as the Module 1 tokenizer lab showed, a model sees strawberry as a few tokens rather than ten letters. It became a famous test of language models, and current ones pass it.

## Things to notice

- All four models run with reasoning effort `"low"`, because `gpt-6.1-sol` doesn't support `"none"`. The token counts include the model's hidden reasoning tokens; `shootout.json` shows how many.
- The more capable models are usually slower and more expensive per token. For simple questions, they aren't always better.

## Try this

1. **Add a model.** Run `uv run python -c "from openai import OpenAI; print(sorted(m.id for m in OpenAI().models.list()))"` to list the models your key can use. Add an older one, such as `gpt-5.6-luna`.
2. **Price it.** Look up each model's price per million input and output tokens on OpenAI's pricing page, and add a cost column. What did each answer cost?
3. **Harder questions.** Add a maths word problem, or a logic puzzle. Where do the small models start getting things wrong?
4. **Think harder.** Run every model at `"low"` and then `"high"` reasoning effort. How much slower is it, how many more reasoning tokens does it use, and does the answer change?
5. **Judge it.** Ask one model to read all four answers to each question and pick the best. Does it always pick itself?

## Questions

For discussion. There are no right answers.

- Only the most expensive model knew the whole answer to the riddle. How would you decide which questions deserve the expensive model?
- If a cheap model is wrong one time in twenty, is that acceptable? What does it depend on?
- Should you trust a model to judge other models' answers? What could go wrong?
