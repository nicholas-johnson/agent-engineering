# Further reading and extensions

Why can't a model do arithmetic? How did models learn to use tools? Where did the tool loop come from? And what goes wrong when an agent reads the outside world?

## The exercise

1. **Pick one paper** from the reading list. If you're not sure, start with one marked ⭐.
2. **Read the part that matters.** You don't need to read it all. Each description says what to look for.
3. **Connect it to a demo.** Write two or three sentences: what problem was the paper solving, and which of our demos or playgrounds does it relate to?
4. **Pick one extension** from the list at the end and start it. Most will take longer than a break, so take them home.

---

## Reading list

### Why models get maths wrong

**⭐ Singh, A. K. & Strouse, D. J. (2024). "Tokenization counts: the impact of tokenization on arithmetic in frontier LLMs." [arXiv:2402.14903](https://arxiv.org/abs/2402.14903)**

A number is split into tokens like any other text, and how it is split changes how well the model does arithmetic. Splitting digits from the right instead of the left makes a large difference. Read it alongside demo 1, and remember Module 1's tokenizer lab, where `1234` was four separate tokens.

**Cobbe, K. et al. (2021). "Training Verifiers to Solve Math Word Problems." [arXiv:2110.14168](https://arxiv.org/abs/2110.14168)**

The paper that introduced GSM8K, a set of 8,500 school maths word problems still used to test models. Look for the "calculator annotations": even here, the arithmetic inside each solution was handed to a calculator rather than trusted to the model.

### Teaching models to use tools

**⭐ Schick, T. et al. (2023). "Toolformer: Language Models Can Teach Themselves to Use Tools." *NeurIPS 2023*. [arXiv:2302.04761](https://arxiv.org/abs/2302.04761)**

A model that learned, by itself, where in a piece of text calling a tool would help: a calculator, a search engine, a translator, a calendar. Look at figure 1, with the calculator call written into the middle of a sentence. It's demo 3, learned instead of programmed.

**Karpas, E. et al. (2022). "MRKL Systems: A modular, neuro-symbolic architecture that combines large language models, external knowledge sources and discrete reasoning." [arXiv:2205.00445](https://arxiv.org/abs/2205.00445)**

An early statement of this module's argument: language models are bad at exact things like arithmetic, so route those parts to "experts" such as a calculator, and let the model handle the language. Look at the arithmetic examples.

**Gao, L. et al. (2023). "PAL: Program-aided Language Models." *ICML 2023*. [arXiv:2211.10435](https://arxiv.org/abs/2211.10435)**

Instead of calling a calculator one step at a time, have the model write a short Python program that solves the problem, and run it. Compare with the last "Try this" in the `calculator` playground.

**Patil, S. G., Zhang, T., Wang, X. & Gonzalez, J. E. (2023). "Gorilla: Large Language Model Connected with Massive APIs." [arXiv:2305.15334](https://arxiv.org/abs/2305.15334)**

Models asked to call real APIs often invent ones that don't exist. Gorilla trains a model to call thousands of real APIs correctly, by reading their documentation. Look for "hallucination" of API calls. Our model wrote correct Scryfall searches in demo 4 because the tool description told it the syntax.

**Qin, Y. et al. (2024). "ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs." *ICLR 2024*. [arXiv:2307.16789](https://arxiv.org/abs/2307.16789)**

Demo 4 at scale: more than 16,000 real APIs, and a way to train and test models on using them. Look at how they search for the right tool when there are far too many to describe to the model at once.

### The agent loop

**⭐ Yao, S. et al. (2023). "ReAct: Synergizing Reasoning and Acting in Language Models." *ICLR 2023*. [arXiv:2210.03629](https://arxiv.org/abs/2210.03629)**

The paper behind the tool loop. The model alternates between *thinking* about what to do, *acting* (calling a tool), and *observing* the result, until it can answer. Look at figure 1 and compare it with our loop, and with demo 4's three steps.

**Nakano, R. et al. (2021). "WebGPT: Browser-assisted question-answering with human feedback." [arXiv:2112.09332](https://arxiv.org/abs/2112.09332)**

A model given a text-based web browser as a tool: search, click, scroll, quote. Look at the list of commands. Demo 4's Scryfall server is a much smaller version of the same idea: give the model a way to look things up, and have it cite what it found.

### What can go wrong

**⭐ Greshake, K. et al. (2023). "Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection." *AISec 2023*. [arXiv:2302.12173](https://arxiv.org/abs/2302.12173)**

The paper that showed **indirect prompt injection**: instructions hidden in a web page, email or document that the agent reads through a tool, and then follows. Look at the attack examples. Then run the `lying-tools` playground again.

**Radosevich, B. & Halloran, J. (2025). "MCP Safety Audit: LLMs with the Model Context Protocol Allow Major Security Exploits." [arXiv:2504.03767](https://arxiv.org/abs/2504.03767)**

What goes wrong when agents get powerful MCP tools, such as file access: the authors got models to run malicious code and leak credentials through ordinary-looking tools. Read it before you write an MCP server that can change anything.

---

## Guides, docs and posts

- **[Model Context Protocol](https://modelcontextprotocol.io)**: the specification, with guides to writing servers and clients, and lists of existing servers.
- **[MCP Python SDK](https://py.sdk.modelcontextprotocol.io)**: the `mcp` package we used. Version 2 renamed `FastMCP` to `MCPServer`, so be careful with older tutorials.
- **[OpenAI function calling guide](https://developers.openai.com/api/docs/guides/function-calling)**: the `function_call` and `function_call_output` items from our tool loop, in detail.
- **[Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)**: when you need an agent, when a fixed sequence of steps is better, and common patterns. The best short introduction.
- **[Simon Willison on prompt injection](https://simonwillison.net/series/prompt-injection/)**: the person who named it, writing about it since 2022. Start with the oldest posts.
- **[Scryfall API](https://scryfall.com/docs/api)** and **[Open-Meteo](https://open-meteo.com)**: the two APIs our servers use, both well documented and free.

---

## Extensions

Bigger projects than the playground. ★ is an afternoon, ★★★ is a weekend.

**★ Fail well.** Make the cards server handle failure properly: a timeout, Scryfall being down, a card that doesn't exist. Return a clear message the model can act on, and test each one (turn off your Wi-Fi). What does the agent tell the user in each case?

**★ A tool log.** Record every tool call the agent makes: the time, the tool, the arguments, the result and how long it took. Write them to a file, one line each. Then ask the agent five questions and read the log. This is how you'll debug every agent you build.

**★★ Ask first.** Before running any tool, show the user which tool and arguments the model wants, and ask "Run this? (y/n)". If they say no, tell the model it was refused. This is a **human in the loop**, and it's how you'd want an agent that can spend money or send email to work.

**★★ Over the network.** Run the cards server with the `streamable-http` transport instead of stdio (`server.run(transport="streamable-http")`), and change the agent to connect to its URL. Now the server can live on another machine, and several agents can share it.

**★★ A deck builder.** Give the agent the cards server and ask it to build a 60-card *Magic* deck around a theme, under a budget. It will need many searches. Add a tool if it needs one. How good is the deck? How much did the conversation cost?

**★★ Your notes.** Write an MCP server that can list and read the text files in one folder (and only that folder). Point it at a folder of your own notes, and ask the agent questions about them. How do you make sure it can't read anything outside the folder? This is a preview of where the course goes next.

**★★★ Tools that write tools.** Let the agent write a new Python function when it needs a tool that doesn't exist. Show you the code, add it to the server only if you approve, and restart the server so the agent can use it. What could go wrong? How would you limit it?

**★★★ Red team.** Build an agent with a "read email" tool (reading from a folder of text files) and a "send email" tool (which only writes to a file). Write an email that tricks the agent into sending something it shouldn't. Then defend against it: instructions, checks, asking first. Read Greshake et al. first. Can you make it safe?
