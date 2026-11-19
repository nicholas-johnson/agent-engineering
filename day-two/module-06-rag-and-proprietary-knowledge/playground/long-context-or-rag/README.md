# Long context or RAG

Demo 2 put the whole knowledge base in the prompt, and it worked. Here you'll work out what that costs once real customers start asking, against RAG's top five chunks: per question, per day and per year, with and without prompt caching. Nothing is answered. The script only asks the API to count tokens, then does the sums.

From the module folder (`day-two/module-06-rag-and-proprietary-knowledge`):

```bash
uv run python playground/long-context-or-rag/play.py
```

Or without `uv` (set up `.venv` once at the repo root with `python3 -m venv .venv && .venv/bin/pip install -e .`):

```bash
source ../../.venv/bin/activate
python playground/long-context-or-rag/play.py
```

Needs `OPENAI_API_KEY` in `.env`, to count tokens. The first run counts the whole knowledge base twice, as documents and as chunks, which took almost two minutes. The counts are kept in `playground/long-context-or-rag/output/token-counts.json`, so after that, changing a price and rerunning is instant. The costs are written to `playground/long-context-or-rag/output/costs.json`.

---

OpenAI will count the tokens in a prompt without running the model:

```python
client.responses.input_tokens.count(model=MODEL, instructions=instructions, input=text).input_tokens
```

The script counts two prompts:

- **Whole knowledge base**: demo 2's prompt, all 275 documents and then the question. To check the count, I sent this prompt to `gpt-6-luna` for real, and `usage.input_tokens` came back as 191,548, the same number.
- **Top 5 chunks**: demo 3's instructions and question, counted exactly, plus five chunks of average size. That part is an estimate: the script counts all 1,823 chunks together and divides by 1,823. [how-many-chunks](../how-many-chunks/) measures real top-five prompts for the 24 answerable questions, and got 612 tokens: the chunks a search picks are a little shorter than average.

The settings at the top of the file:

| Setting | Value | Where it comes from |
|---------|-------|---------------------|
| `QUESTIONS_PER_DAY` | 10,000 | Made up. Use your own |
| `INPUT_PRICE`, `OUTPUT_PRICE` | $0.10 and $0.50 per million tokens | Module 4's price list, checked 10 November 2026 |
| `CACHED_PRICE` | a tenth of `INPUT_PRICE` | **An assumption to check**: see below |
| `CACHED_SHARE` | 0.9 | **An assumption**: the share of the whole-knowledge-base prompt read from the cache |
| `OUTPUT_TOKENS` | 100 | **An assumption**: a short paragraph. Two real answers used 70 and 95 |

```text
  275 documents, 1,823 chunks of 129 tokens on average.
  Every answer also costs 100 output tokens (an assumption).

                                       Tokens in  Per question    Per day (10,000)    Per year
  Whole knowledge base                   191,548      $0.01920             $192.05     $70,098
  Whole knowledge base, 90% cached       191,548      $0.00369              $36.89     $13,466
  Top 5 chunks                               693      $0.00012               $1.19        $435
```

**Prompt caching** means the provider keeps the work it did on the start of a prompt, so the next prompt that starts the same way is cheaper to read. The whole knowledge base is the same for every question, so it caches well; the top five chunks change with every question, so they don't. RAG's prompt is also shorter than the 1,024 tokens OpenAI needs before it caches anything at all.

## Things to notice

- **RAG sends 276 times fewer tokens.** 693 against 191,548. Everything else follows from that.
- **Caching helps a lot, and not enough.** Reading 90% from the cache cuts the long-context bill by more than five times, from $192 a day to $37. RAG is still 31 times cheaper.
- **For RAG, the answer costs nearly as much as the question.** Output tokens cost five times as much as input tokens, so 100 tokens out ($0.00005) comes close to 693 tokens in ($0.00007). With the whole knowledge base, output is a rounding error.
- **The cache is real, and 90% is cautious.** When I sent demo 2's prompt twice, a few seconds apart and with different questions, the second call read 191,526 of its 191,546 input tokens from the cache. But OpenAI's guide says a cache entry lasts 30 minutes by default, so a quiet spell empties it, and writing to the cache costs 1.25 times the normal price. The script leaves out the writes.
- **It fits, for now.** 191,548 tokens is under a fifth of `gpt-6-luna`'s 1,050,000-token context window. A knowledge base six times bigger wouldn't fit at all, and long prompts are slower: demo 2 prints how long each one took.

## Try this

1. **Your own traffic.** Set `QUESTIONS_PER_DAY` to 100, then 1,000,000. At what volume does the difference stop being worth the engineering?
2. **A pricier model.** Put another model's prices from Module 4's `data/prices.json` into `INPUT_PRICE` and `OUTPUT_PRICE`. Does the gap grow or shrink?
3. **Measure the cache yourself.** Send demo 2's prompt twice with `client.responses.create` and print `response.usage.input_tokens_details.cached_tokens` each time. Then wait 40 minutes and send it again.
4. **Pay for the writes.** Add the cache writes to `dollars()`: one full write at 1.25 times `INPUT_PRICE` whenever the cache has expired. If questions arrive only between 9 and 5, how many writes is that a day?
5. **A real top five.** Replace the average chunk with real retrieval: embed the 24 answerable questions, find each one's top five as demo 3 does, and count those prompts. Is the average close?
6. **Where's the break-even?** Halve the knowledge base, then halve it again, by loading fewer documents. How small does it have to be before sending all of it costs no more than RAG?

## Questions

For discussion. There are no right answers.

- At 10,000 questions a day, RAG saves about $190 a day, or $70,000 a year. Is that worth building and looking after a retrieval system? Who should decide, and with what numbers?
- Long context can't retrieve the wrong chunks, because it never retrieves anything. How would you put a price on the questions RAG gets wrong because the right chunk wasn't in its top five?
- Caching only pays while questions keep coming. How would the answer change for a helpdesk that's busy from 9 to 5 and silent overnight?
- Prices for the same quality have fallen fast. If they fall tenfold again, does this comparison still matter?

## Further reading

- **Li, Z., Li, C., Zhang, M., Mei, Q. & Bendersky, M. (2024). "Retrieval Augmented Generation or Long-Context LLMs? A Comprehensive Study and Hybrid Approach." _EMNLP 2024 Industry Track_.** [arXiv:2407.16833](https://arxiv.org/abs/2407.16833). Compares the two approaches on the same questions. Look for the trade-off this script prices: long context did better on average when the model was strong enough, and RAG cost far less. Their answer, **Self-Route**, asks RAG first and only falls back to the whole document when the model says the chunks aren't enough.
- **[OpenAI: Prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching)**. How the cache works and what it costs: the 1,024-token minimum, the 30-minute default lifetime, and the prices of cache reads and writes. Check `CACHED_PRICE` against it.
