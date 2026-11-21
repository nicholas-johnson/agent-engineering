# Spend limits

An assistant in front of customers runs on your bill. Every message costs money, and some customers send a lot of them, paste in whole files, or use it to write stories that have nothing to do with thermostats. Here one customer sends ten messages over five minutes, and four limits decide which get an answer: how long a message may be, how many a minute, how long a reply may be, and how much a customer may spend in a day. You'll change the limits and see which messages get through and what they cost.

From the module folder (`day-two/module-08-security-and-deployment`):

```bash
uv run python playground/spend-limits/play.py
```

Or without `uv` (set up `.venv` once at the repo root with `python3 -m venv .venv && .venv/bin/pip install -e .`):

```bash
source ../../.venv/bin/activate
python playground/spend-limits/play.py
```

Needs `OPENAI_API_KEY` in `.env`. The clock is pretend (each message says which minute it arrives in), so it ran in about 15 seconds. Each message, what happened to it and what it cost go in `playground/spend-limits/output/messages.json`.

---

The limits are settings at the top, and the checks run before each call, cheapest first. The cost comes from the token counts in each response and gpt-6-luna's prices from Module 4:

```python
DAILY_BUDGET = 0.00015  # dollars a day
PER_MINUTE = 4  # messages a minute
MAX_CHARACTERS = 2000  # the longest message we accept
MAX_OUTPUT_TOKENS = 200  # the longest reply we pay for

if len(message) > MAX_CHARACTERS: ...
elif in_this_minute >= PER_MINUTE: ...
elif spent >= DAILY_BUDGET: ...
```

```text
  0  My thermostat has started clicking loudly. C   answered: 47 tokens in, 72 out
  0  Hello?                                         answered: 35 tokens in, 13 out
  0  Are you there?                                 answered: 37 tokens in, 15 out
  0  Can I have a new one or not?                   answered: 42 tokens in, 25 out
  0  HELLO                                          refused: more than 4 messages a minute
  1  Here's my whole heating history so you can c   refused: longer than 2,000 characters
  2  Forget the thermostat. Write me a 3,000-word   answered: 56 tokens in, 200 out (cut off at the limit)
  3  Write another one, about its cousin.           refused: today's budget is used up
  4  And one more, about the boiler.                refused: today's budget is used up
  5  My thermostat has started clicking loudly. C   refused: today's budget is used up

Spent $0.000184 of $0.00015 today, on 5 of 10 messages.
```

## Things to notice

- **The story cost more than everything before it.** 200 tokens out, at five times the price of tokens in. Without `MAX_OUTPUT_TOKENS` it would have tried to write 3,000 words.
- **The budget was overspent.** $0.000184 against $0.00015, because the check runs before the call and can't know what the call will cost. A budget checked this way is a soft limit: it can be passed by one call's worth.
- **The last message was a real question, and it was refused.** Sam asked about the clicking again, after spending the day's budget on stories. Limits protect you, and can also stop the people the assistant is for.
- **These numbers are tiny.** A fraction of a cent. Multiply by every customer, every day, and by a bigger model, and they aren't. And the limits matter more for abuse than for honest customers: one script sending a message a second runs up a bill all night.

## Try this

1. **Find the right budget.** Set `DAILY_BUDGET` so that all three thermostat questions get answered and the stories don't. Is there one?
2. **Refuse off-topic requests.** Before the main call, ask a cheap model whether the message is about Dormouse at all, and refuse the stories. What does the extra call cost, and what does it save?
3. **A hard limit.** Make the budget hard: set `max_output_tokens` from what's left of the budget, so the call can't cost more than remains.
4. **Per minute, properly.** Replace the pretend minutes with real time (`time.time()`) and a sliding window, then send the messages in a loop as fast as you can.
5. **Count conversation, not messages.** A real assistant sends the whole conversation every time, so each message costs more than the last. Keep a conversation list and watch the input tokens grow.
6. **Price a month.** If 20,000 customers each sent the first five messages once a month, what would gpt-6-luna cost? And gpt-6.1-sol, from Module 4's price list?

## Questions

For discussion. There are no right answers.

- Should a paying customer ever be told "today's budget is used up"? What should the assistant say instead?
- The story request was a misuse, but a harmless one. Where's the line between someone having fun and abuse?
- Who should set these numbers: engineering, finance, or customer support?
- If an attacker can make your assistant expensive, is that a security problem or a business one?

## Further reading

- **OWASP Top 10 for LLM Applications 2025**, LLM10:2025 "Unbounded Consumption": https://genai.owasp.org/llm-top-10/. Its list of prevention steps starts with the limits in this script: input size, rate and spend.
