# The cost of memory

From the module folder (`day-one/module-02-building-a-chatbot`):

```bash
uv run python playground/cost-of-memory/play.py
```

Or without `uv` (set up `.venv` once at the repo root with `python3 -m venv .venv && .venv/bin/pip install -e .`):

```bash
source ../../.venv/bin/activate
python playground/cost-of-memory/play.py
```

Needs `OPENAI_API_KEY` in `.env`. It needs no typing: the ten messages are in the script. The numbers are written to `playground/cost-of-memory/output/tokens_per_turn.csv`, which opens in any spreadsheet.

---

Demo 3 gave the chatbot memory by sending the whole conversation every turn. This plays out a ten-turn conversation, Alice telling a chatbot about her day, and records how many tokens each turn costs.

```text
Turn  Input tokens  Output tokens
   1            26             21
   2            65             41
   3           126             53
   4           198             67
   5           285             52
   6           354             55
   7           429             54
   8           501             57
   9           576             61
  10           657             65

Total input tokens over 10 turns: 3217
```

Each message is short, but every turn resends every message before it. Turn 10 sends 25 times as much as turn 1. Over the whole conversation the input adds up roughly with the *square* of the number of turns: double the length of the conversation and you roughly quadruple the cost.

The last message asks the chatbot to remind Alice of everything that has happened, and it can, because it has the whole conversation in front of it.

## Try this

1. **A longer chat.** Add another ten messages. Plot the input tokens per turn in a spreadsheet. What shape is it?
2. **Short memory.** Only send the last four messages each turn. How much does it save? What does the chatbot get wrong in its final summary?
3. **Summarise.** Every five turns, ask the model to summarise the conversation so far, and replace the old messages with that summary. How does the cost change? What gets lost?
4. **Caching.** The CSV has a `cached_tokens` column. When the start of a request is the same as one sent recently, OpenAI can reuse its work and charge less. Make the instructions much longer (a page or two of text) and watch that column. When does caching start?
5. **Let the API remember.** Use `previous_response_id` instead of sending `messages`. Does `input_tokens` go down? (Read the numbers carefully: you are still charged for the whole conversation.)

## Questions

For discussion. There are no right answers.

- Long conversations get slow and expensive. Should a chatbot ever forget things on purpose? Who should decide what it forgets?
- Summarising old messages loses detail. What kinds of detail would be dangerous to lose?
- If the provider stores your conversation for you (`previous_response_id`), what does that mean for privacy?
