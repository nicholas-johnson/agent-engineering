# Open versus closed

From the module folder (`day-one/module-03-choosing-a-provider`):

```bash
uv run python playground/open-vs-closed/play.py
```

Or without `uv` (set up `.venv` once at the repo root with `python3 -m venv .venv && .venv/bin/pip install -e .`):

```bash
source ../../.venv/bin/activate
python playground/open-vs-closed/play.py
```

Needs `OPENAI_API_KEY` in `.env`, and Ollama running with `qwen3:1.7b` (`ollama pull qwen3:1.7b`). The answers are written to `playground/open-vs-closed/output/answers.json`.

---

A small open model on your laptop against a hosted frontier model, on the same four questions: a fact from *Alice*, a classic trick question, a translation and some code.

```text
=== What is the March Hare's excuse for there being no room at the tea table? ===
--- gpt-6-luna (OpenAI's servers) ---
The March Hare says there's **no room** because the table is already full—then he offers Alice some wine, though there isn't any.
--- qwen3:1.7b (this laptop) ---
... The March Hare gives an excuse, and it is:

**"I am not a bear, I am a hare."**

=== Translate into French: 'Off with her head!' said the Queen. ===
--- gpt-6-luna (OpenAI's servers) ---
« Qu'on lui coupe la tête ! » dit la Reine.
--- qwen3:1.7b (this laptop) ---
« Off avec sa tête ! » dit la Reine.
```

## Things to notice

- **The small model made up a quotation**, and explained the joke in it at length. Nothing like it is in the book.
- **Its French is half English.**
- **But it got the other two right.** Both models solved the bat-and-ball puzzle ($0.05) and wrote a working Fibonacci function. Small models can be perfectly good at the right jobs.

## Try this

1. **Your own questions.** Replace `QUESTIONS` with four things from your own work. Where is the small model good enough?
2. **A fair fight.** Swap `gpt-6-luna` for a bigger open model through OpenRouter, such as `qwen/qwen3.8-max-0902` or `deepseek/deepseek-v4.1-flash`. Open versus closed, at the same size.
3. **A judge.** Ask `gpt-6-luna` to read both answers to each question and say which is better, and why. Does it agree with you?
4. **Give it the book.** Put the tea-party chapter of *Alice* (from Module 1's `data/`) in the instructions and ask the March Hare question again. Does the small model get it right when it has the text?
5. **Speed.** Time each answer. Which is faster: your laptop, or a data centre across the internet?

## Questions

For discussion. There are no right answers.

- The small model invented a quotation and then explained the joke in it. Why is a confident invention worse than "I don't know"?
- If open models catch up with closed ones, what's left for the closed providers to sell?
- Would you rather depend on a company's API, or on a model you can download? What risks come with each?
