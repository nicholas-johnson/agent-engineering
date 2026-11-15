# Price calculator

Token prices, turned into a monthly bill. You'll cost out one company chatbot on every model in `data/prices.json`.

From the module folder (`day-one/module-03-choosing-a-provider`):

```bash
uv run python playground/price-calculator/play.py
```

Or without `uv` (standard library only, no packages needed):

```bash
python3 playground/price-calculator/play.py
```

No API keys needed. The results are written to `playground/price-calculator/output/monthly_costs.csv`.

---

The scenario is at the top of `play.py`: a company chatbot for 1,000 people, 20 messages each a working day, 1,500 tokens in and 200 out per message.

```text
420,000 messages a month, prices checked 2026-11-10

$     31.72  z-ai/glm-5.3-flash               China    open weights
$    105.00  anthropic/claude-haiku-5.5       USA
$    105.00  openai/gpt-6-luna                USA
$    133.98  qwen/qwen3.8-flash               China    open weights
...
$  4,200.00  anthropic/claude-opus-5.5        USA
$  8,400.00  anthropic/claude-fable-5.2       USA
$ 10,500.00  openai/gpt-6-astra               USA
```

The same chatbot costs anything from $32 to $10,500 a month: a factor of more than 300.

## Things to notice

- **Input usually costs more than output.** Each message sends 1,500 tokens and gets 200 back. In a chatbot, most of the input is the conversation so far (Module 2's `cost-of-memory` playground).
- **The cheap end is mostly open weights**, and mostly Chinese labs.

## Try this

1. **Your own scenario.** Change the numbers to match something you'd build: a customer-support bot, a nightly report, a coding assistant.
2. **Shorter memory.** Halve `INPUT_TOKENS_PER_MESSAGE`. Which models does that help most?
3. **Fresh prices.** Run `uv run python data/build_prices.py` (or `python3 data/build_prices.py`), then run this again. Has anything changed since 10 November 2026?
4. **Add models.** Add more model IDs to `MODELS` in `data/build_prices.py`. The `model-catalogue` playground lists every ID.
5. **Caching.** Many providers charge much less for input they've seen recently (prompt caching). OpenRouter's model list has an `input_cache_read` price. If 80% of each message's input were cached, how would the order change?
6. **Is it worth it?** Pick three models from very different price points and run the same ten real questions through each. Is the expensive one 100 times better?

## Questions

For discussion. There are no right answers.

- The cheapest model is more than 300 times cheaper than the most expensive. When is the expensive one worth it?
- Prices keep falling. Should you design for today's prices, or for next year's?
- Who in an organisation should decide which model to use: the engineers, finance, or legal?

## Further reading

- **DeepSeek-AI (2024). "DeepSeek-V3 Technical Report."** [arXiv:2412.19437](https://arxiv.org/abs/2412.19437). The cost table near the start: what the training run cost, and why a model can be cheap to run. Read it next to a monthly bill where the models are hundreds of times apart.
- **[Artificial Analysis](https://artificialanalysis.ai).** Independent measurements of quality, speed and price, for when the numbers in `data/prices.json` have gone stale.
