# Parallel calls

Ask about five cards at once. Does the model look them up one at a time, or all together?

```bash
uv run python play.py
```

It needs `OPENAI_API_KEY` and an internet connection, and uses the cards server from demo 4. The whole conversation is written to `output/conversation.json`.

```text
You: What are these Magic: The Gathering cards worth right now: Sol Ring, Lightning Bolt, Counterspell, Llanowar Elves and Dark Ritual? Which is the most expensive?
Round 1: the model asked for 5 tool calls at once
  [tool] find_card({"name":"Sol Ring"})
  [tool] find_card({"name":"Lightning Bolt"})
  [tool] find_card({"name":"Counterspell"})
  [tool] find_card({"name":"Llanowar Elves"})
  [tool] find_card({"name":"Dark Ritual"})
Round 2: the answer
Agent: Current listed prices in USD (for the specific printings returned; prices vary by set, condition, and foil treatment):

Sol Ring: $1.25
Lightning Bolt: $1.14
Counterspell: $4.03
Llanowar Elves: $0.28
Dark Ritual: $9.27

Dark Ritual is the most expensive of these listings.
```

Five lookups, one round trip to the model. A single response can contain several `function_call` items: these are **parallel tool calls**. Our loop already handles them, because it runs every call in the response before asking again.

## Things to notice

- **Rounds cost more than calls.** Each round sends the whole conversation to the model again (Module 2's cost of memory). Five calls in one round is much cheaper and faster than five rounds.
- **"Parallel" is up to us.** The model asked for five calls at once, but our loop still runs them one after another, and the cards server waits half a second before each one to stay within Scryfall's limit.
- **It noticed the small print.** Scryfall returns one printing of each card, and the model said so: "prices vary by set, condition, and foil treatment". A good tool result, and a careful answer.

## Try this

1. **Turn it off.** Add `parallel_tool_calls=False` to `responses.create`. How many rounds does it take now?
2. **Dependent calls.** Ask "What's the most expensive rabbit creature, and what does the second most expensive one do?" Which calls can happen in parallel, and which have to wait?
3. **Really parallel.** Use `asyncio.gather` to run all the calls in a round at the same time. How much faster is it? (Scryfall's half-second limit still applies per request.)
4. **Count the cost.** Print `response.usage.input_tokens` for each round. How much does the second round cost compared with the first?
5. **A long list.** Ask about twenty cards. Does it still do them all in one round?
