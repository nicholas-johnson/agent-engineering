# Brain tools

Section 6's company-brain server has three tools. Here you'll add a fourth, and see exactly what a model would get back from each one, without a model: `play.py` starts the server and calls the tools itself, the way Claude Code or Cursor would. Then you can attach your version to a real tool.

From the module folder (`day-two/module-07-ai-assisted-development`):

```bash
uv run python playground/brain-tools/play.py
```

Or without `uv` (set up `.venv` once at the repo root with `python3 -m venv .venv && .venv/bin/pip install -e .`):

```bash
source ../../.venv/bin/activate
python playground/brain-tools/play.py
```

It needs no API key and takes about a second. Every answer, in full, goes to `playground/brain-tools/output/calls.json`.

---

`server.py` is a copy of `demo/06_brain_server.py`. `play.py` asks it for its tools, then makes the calls in one list:

```python
CALLS = [
    ("get_ticket", {"ticket_id": "DOR-233"}),
    ("read_brain", {"topic": "decisions"}),
    ("search_feedback", {"words": "early cold"}),
]
```

```text
The server offers:

  read_brain(topic)
    Read one part of Dormouse's company brain. `topic` is one of: product (every feature, and where each setting l...
  get_ticket(ticket_id)
    Read one ticket, such as DOR-231: the problem, what we're building, and its acceptance criteria.
  search_feedback(words)
    Customer feedback from September and October 2026 that contains any of these words, as JSON: each piece with i...

get_ticket({"ticket_id": "DOR-233"})

  # DOR-233: Let customers choose how long Boost lasts

  - **Type:** Feature
  - **Status:** Ready for development
  - **Reporter:** Product

  ## Problem

  Boost always heats for one hour. Customers who only want to take the chill off a room for a few minutes leave it running, and customers working from home...

read_brain({"topic": "decisions"})

  # Decisions

  Product decisions we have made, newest first, and why. Check here before proposing something that goes against one.

  ## 2026-05: Settings about when the heating runs live under Schedule

  Customers look under Schedule when the heating comes on at a time they didn't expect. Any setting th...

search_feedback({"words": "early cold"})

  [
    {
      "id": "F10",
      "channel": "support chat",
      "date": "2026-09-14",
      "text": "Heating seems to come on early every morning. Is that normal or is the thermostat faulty?"
    },
    {
      "id": "F14",
      "channel": "survey",
      "date": "2026-09-20",
      "text": "The early heating feature ...
```

The first lines are everything a model knows about the server before it calls anything: three names, three arguments and three descriptions. The rest is what comes back: plain text, which goes straight into the model's context.

## Things to notice

- **The description is the whole interface.** `read_brain`'s says when to use it: "Read decisions before making any product decision". That sentence is what makes Claude Code read the decisions before building DOR-233.
- **Searching by words is weak.** Customers wrote "comes on at 5:40", not "early". `search_feedback("early")` finds 3 of the 14 pieces about the heating coming on early. Module 6's search by meaning would find more.
- **Nothing checks who is asking.** Anyone whose tool can start this server can read every ticket and every piece of feedback.

## Try this

1. **List the tickets.** Add a tool `list_tickets()` that returns each ticket's id and title. Add a call to `CALLS`, and run it.
2. **A better description.** Rewrite `search_feedback`'s description so a model would try several words for the same thing. Attach the server to Claude Code (see `demo/06_company_brain.md`) and ask "What do customers say about the heating coming on early?". Does it search more than once?
3. **Search by meaning.** Replace `search_feedback`'s word match with Module 6's embeddings (it needs `OPENAI_API_KEY`). Does it find more of the 14?
4. **Write as well as read.** Add `add_feedback(channel, text)`, which appends to a copy of the feedback in `output/`. Should an AI tool be able to change the company brain? What would you check first?
5. **A resource, not a tool.** MCP servers can also offer **resources**: files a person chooses to attach, rather than tools a model chooses to call. Offer each brain file as a resource, and find how Claude Code lets you attach one.
6. **A prompt.** MCP servers can offer **prompts**, which tools show as commands. Offer the release-notes skill as a prompt, and find it in Claude Code's `/` menu.

## Questions

For discussion. There are no right answers.

- A tool's description tells the model when to use it. Who should write those sentences: the person who wrote the server, or the people whose knowledge it serves?
- `read_brain` returns a whole file. When is it better to return less?
- The brain is now one server that every tool reads. What happens on the day someone writes something wrong in `decisions.md`?
- This server runs on your laptop. What would change if every employee's tools used it at once?

## Further reading

- **Model Context Protocol. "Specification."** [modelcontextprotocol.io/specification](https://modelcontextprotocol.io/specification). The protocol the server speaks. Read the server features: tools, resources and prompts, and who is meant to choose each one.

## Rabbit holes

- **Run it remotely.** Change the server to serve over HTTP, run it, and attach it to Claude Code with `claude mcp add --transport http`. Then think about what Module 8 says it would need before anyone outside your laptop could reach it.
- **One server for everything.** Combine this server with Module 6's `search_docs`, so one connection gives a tool the brain, the tickets, the feedback and the documentation. Is one big server better than three small ones?
