# Module 4 — Tools

> A language model is brilliant with words and hopeless at arithmetic: ask it for a square root to ten decimal places and it confidently makes one up, differently every time. Python gets it right instantly, but can't read a question. In this module we join the two. We write a function, turn it into a **tool** on an **MCP server**, and give it to the model with a **tool loop**: the model decides when it needs the tool, our code runs it, and the model uses the result. Then we connect a second server that reaches out to a live API on the internet, and our agent can look things up in the real world.

## Learning goals

- Explain why a language model can't be trusted with exact calculations.
- Write a **tool**: a function the model can ask us to run.
- Build an **MCP server** that offers tools, and an **MCP client** that uses them.
- Write a **tool loop**, and trace a conversation through it.
- Connect an agent to more than one server, including one that calls an **external API**.
- Name the risks that arrive with tools: wrong results, unavailable services, and text from outside that the model will read as if it were true.

---

## The idea

A language model predicts text. It has read so much that it can predict text that *looks* like a calculation, but nothing in it is calculating. A computer calculates exactly, but only does what it is told.

A **tool** joins them. The model is told that tools exist, what they do and what arguments they take. When it decides it needs one, it doesn't answer: it asks for the tool to be run, with arguments. Our code runs it and sends the result back. The model reads the result, and either asks for another tool or answers.

The model does the understanding and the explaining. The tool does the exact work.

## Setting up

You need `OPENAI_API_KEY` in `.env` (see Module 2), and an internet connection for section 4. This module adds one package, `mcp`, the official Python package for the **Model Context Protocol**.

## The data

There are no data files: section 4 reads live data from [Scryfall](https://scryfall.com/docs/api), a free API for *Magic: The Gathering* cards.

## Running the demos

From this folder:

```bash
uv run python demo/01_maths.py
```

| Demo | What it is | Writes |
|------|------------|--------|
| `01_maths.py` | Ask the model for a square root | `01_maths.json` |
| `02_function.py` | The same square root, in Python | `02_function.txt` |
| `03_maths_server.py` | An MCP server with one tool | — |
| `03_agent.py` | An agent that starts the maths server and uses it | `03_agent.json`: the whole conversation, tool calls included |
| `04_cards_server.py` | An MCP server that calls the Scryfall API | — |
| `04_agent.py` | An agent that uses both servers | `04_agent.json` |

You don't run the servers yourself: each agent starts the servers it needs. The model's answers are random, so yours will differ from the examples below.

---

## 1. Maths with a language model

**Demo:** `demo/01_maths.py`

Ask `gpt-6-luna` for the square root of 7,654,321, to ten decimal places. Three times:

```text
You: What is the square root of 7,654,321, to 10 decimal places?
Model: The square root of 7,654,321, to 10 decimal places, is 2,766.6443672823.
Model: The square root of 7,654,321, to 10 decimal places, is 2,766.6443839608.
Model: The square root of 7,654,321, to 10 decimal places, is 2,766.6442826149.

The right answer: 2766.6443573398
```

Three different answers, every one stated with complete confidence, and every one wrong by the fourth or fifth decimal place. Run it again and you get three more.

**Why this breaks:** the model isn't calculating. It's predicting the next token, as in Module 1. It has seen enough maths to get the first few digits right: the square root is somewhere near 2,766.64. After that, each digit is a plausible guess. Nothing in the answer tells you which digits to trust.

**What about reasoning?** With reasoning effort turned up, the model writes hidden "thinking" before it answers, and can work the calculation through step by step. We tried it six times, at `low`, `medium` and `high` effort, and it got 2766.6443573398 every time. But each answer took between 9 and 57 seconds and 668 to 4,543 thinking tokens, all paid for. And it's still a model predicting digits, so nothing guarantees it. The tool in section 3 takes about a second, and is right because it's arithmetic.

## 2. A function

**Demo:** `demo/02_function.py`

Python's `math.sqrt` gets it right, instantly, every time:

```python
def square_root(number: float) -> float:
    """Return the square root of a number, exactly, to full precision."""
    return math.sqrt(number)
```

```text
square_root(7654321) = 2766.6443573398
```

**Why this breaks:** we now have two halves that can't talk to each other. The function is exact, but it can't read a question: someone had to know to call `square_root`, and with `7654321`. The model can read any question, but it can't run code. We need a way for the model to say *"please run `square_root` with 7654321"*, and for us to send back the answer.

## 3. A tool

**Demos:** `demo/03_maths_server.py` and `demo/03_agent.py`

### The server

The **Model Context Protocol (MCP)** is an open standard, introduced by Anthropic in 2024, for offering tools to AI applications. An **MCP server** is a small program that says "here are my tools" and runs them on request. An **MCP client** connects to servers and uses their tools.

Here is our whole server:

```python
from mcp.server.mcpserver import MCPServer

server = MCPServer("maths")


@server.tool()
def square_root(number: float) -> float:
    """Return the square root of a number, exactly, to full precision."""
    return math.sqrt(number)


server.run()
```

The `@server.tool()` decorator turns our function into a tool. The name comes from the function's name, the description from its docstring, and the arguments from its type hints:

```text
square_root | Return the square root of a number, exactly, to full precision.
            | {'type': 'object', 'properties': {'number': {'title': 'Number', 'type': 'number'}}, 'required': ['number']}
```

That description is all the model will ever know about the tool. Write it for the model.

Because it's a standard, the same server works with any MCP client: our agent, but also Claude, ChatGPT, Cursor, VS Code and many others. Write a tool once, and every MCP application can use it.

### The agent

The agent starts the server as a separate program and talks to it over the server's standard input and output (this is the **stdio** transport; servers on the internet use HTTP instead):

```python
MATHS_SERVER = StdioServerParameters(command=sys.executable, args=["03_maths_server.py"])

async with Client(MATHS_SERVER) as maths:
    tools = [
        {"type": "function", "name": tool.name, "description": tool.description, "parameters": tool.input_schema}
        for tool in (await maths.list_tools()).tools
    ]
```

It asks the server for its tools, and describes each one to OpenAI in the format the Responses API expects. (The MCP package is written with `async`, Python's way of waiting for several things at once. You only need to know that `await` means "wait for this", and that the whole thing runs inside `asyncio.run(main())`.)

### The tool loop

```text
            ┌──────────────────────────────────┐
            ▼                                  │
question ─▶ model ─▶ asks for a tool? ── yes ─▶ run it on the server,
                          │                     add the result to the conversation
                          no
                          ▼
                        answer
```

In code:

```python
while True:
    response = openai.responses.create(model=MODEL, input=conversation, tools=tools, ...)
    conversation += response.output

    calls = [item for item in response.output if item.type == "function_call"]
    if not calls:
        break

    for call in calls:
        result = await maths.call_tool(call.name, json.loads(call.arguments))
        answer = result.content[0].text
        conversation.append({"type": "function_call_output", "call_id": call.call_id, "output": answer})

print(response.output_text)
```

When the model wants a tool, its response contains a `function_call` item with the tool's name and its arguments as JSON, instead of an answer. We run the tool, add a `function_call_output` with the same `call_id`, and ask again. When a response has no function calls, it's the answer.

It's the conversation memory from Module 2, with two new kinds of message in it.

```text
You: What is the square root of 7,654,321, to 10 decimal places?
  [tool] square_root({"number":7654321}) -> 2766.644357339772
Agent: The square root of 7,654,321 to 10 decimal places is 2766.6443573398.
```

Right first time, every time. `demo/output/03_agent.json` has the whole conversation, including the function call and its output.

**Both worlds.** The model did what it's good at: it understood the question, worked out that it needed a square root, pulled the number out of "7,654,321", and rounded and explained the answer. Python did what it's good at: the exact calculation. Neither could have done it alone. This is what an **agent** is: a model that can decide to take actions, in a loop, until the job is done.

**Why this breaks:** our agent can now do one thing exactly. But everything it knows about the world is still frozen in its training. It can't look anything up.

## 4. The wider world

**Demos:** `demo/04_cards_server.py` and `demo/04_agent.py`

A tool can do anything Python can do, including calling an API on the internet. Our second server offers two tools that call [Scryfall](https://scryfall.com/docs/api), a free database of every *Magic: The Gathering* card, with today's prices:

```python
@server.tool()
def search_cards(query: str) -> str:
    """Search Magic: The Gathering cards using Scryfall search syntax, for example
    'name:rabbit t:creature' or 'o:"draw a card" c:blue'. Returns up to 10 card names
    with their current US dollar prices, most expensive first."""
    found = scryfall("cards/search", q=query, order="usd", dir="desc")
    ...
```

`find_card` looks one card up by name. Scryfall asks every program to name itself in its requests and to make at most two requests a second, so the server does both.

The agent connects to **both** servers, collects all their tools, and remembers which server owns which tool. The tool loop doesn't change at all. Then we ask a question no model could answer from its training:

```text
You: Which Magic: The Gathering rabbit creature is worth the most right now, what does it do, and what is the square root of its price?
  [tool] search_cards({"query":"t:creature t:rabbit"}) -> [{"name": "Preston, the Vanisher", "usd": "62.89"}, {"name": "Zodiac Rabbit", "usd": "22.07"}, ...
  [tool] find_card({"name":"Preston, the Vanisher"}) -> {"name": "Preston, the Vanisher", "mana_cost": "{3}{W}", "type_line": "Legendary Creature — Rab...
  [tool] square_root({"number":62.89}) -> 7.930321557162736
Agent: Preston, the Vanisher is the most valuable rabbit creature I found, at $62.89 USD. Its ability creates a 0/1 white Illusion copy whenever another nontoken creature you control enters without being cast. You can also pay {1}{W} and sacrifice five Illusions to exile a target nonland permanent.

The square root of $62.89 is approximately 7.93.
```

Look at what the model did by itself:

- It wrote its own search, in Scryfall's search language. It chose `t:rabbit` (rabbit as a creature *type*), which is better than searching names.
- It took the top result from the search and looked it up for the details.
- It took the price from that and passed it to a tool on a *different* server.
- It wrote the answer from all three results.

Nobody told it the steps. It planned them, one tool call at a time.

Our agent is now connected to the wider world: live data, today's prices, from a service it had never seen until we described the tools.

**Watch out for:** every new tool brings new ways to go wrong.

- **Services fail.** The API can be down, slow, or rate-limit you. Your tools need to handle it, and tell the model clearly when something failed.
- **Results aren't always right.** The agent trusts whatever a tool returns. A buggy tool gives confidently wrong answers (see the `lying-tools` playground).
- **Text from outside is not instructions.** A tool's result goes straight into the model's context. If a web page or an email says "ignore your instructions and...", the model may do it. This is **prompt injection**, and it's the biggest security problem with agents.
- **Tools act.** These tools only read. A tool that sends emails, moves money or deletes files needs much more care: who allowed it, and can it be undone? That's where the rest of the course goes.

---

## Summary

| Step | What we added | What was missing |
|------|---------------|------------------|
| 1. Maths with a model | Ask the model directly | It guesses digits, confidently and differently each time |
| 2. A function | Exact Python | It can't read a question; the model can't run it |
| 3. A tool | An MCP server, and a tool loop | The agent can calculate, but can't look anything up |
| 4. The wider world | A second server, calling a live API | Every tool can fail, be wrong, or carry instructions from outside |

## Playground

[`playground/`](playground/) has six things to play with: a calculator server with many tools, the effect of tool descriptions, the MCP protocol by hand, a tool that lies, many tool calls at once, and a server of your own for another API.

## Further reading and extensions

The final exercise is in [`further-reading/`](further-reading/): papers on teaching models to use tools, on agents that reason and act in a loop, and on the security problems tools bring, plus extension projects to take home.

## Slides

```bash
pnpm slides:04
```
