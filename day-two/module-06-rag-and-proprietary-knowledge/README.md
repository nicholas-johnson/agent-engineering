# Module 6 — RAG and Proprietary Knowledge

> **Draft.** Sections 1 to 3 and 7 below are written from real runs. Sections 4 to 6 (FAQs, citations, keeping it current), the summary and their slides are still to come. The demos for them are in `demo/`, and the data they use is built.

## Learning goals

- Explain why a model makes up answers about things it has never seen (**hallucination**), and why the answers sound right.
- Put documents in a model's prompt, and measure what that costs in **tokens**, money and time for each question.
- Split documents into **chunks**, find the relevant ones with a vector search, and answer from them: **retrieval-augmented generation** (**RAG**).
- Turn documentation into the questions customers ask (an **FAQ**), search those too, and **measure** whether it helps.
- Make a model **cite its sources**, check each quote in code, and let it say when the documentation doesn't answer.
- Update what a model knows by changing documents, not by **retraining**, and re-embed only what changed.
- Offer the search to any AI application as an **MCP server**, and let the model write its own searches.

---

## The idea: look it up, then answer

A language model only knows what was in its training data. Your specifications, manuals and support articles were not in it. Ask it about your product and it does what it always does: it writes the most likely-sounding answer. For a thermostat, that is an answer about thermostats in general, with the details made up.

The fix is the one a new support agent uses: look it up, then answer. Find the parts of the documentation that are about the question, put them in front of the model, and ask it to answer from them. That is **retrieval-augmented generation**, or **RAG**. The retrieval part is Module 5's vector search. The generation part is Module 2's model call. Everything else in this module is about doing the two well: how much to retrieve, how to find it when the customer's words aren't the documentation's, how to check the answer came from the documents, and how to keep the documents current.

## The data

Everything runs on the documentation for **Dormouse**, the smart thermostat from Module 5. **Dormouse and all its documents are invented for this course.** Your own documentation would work the same way.

| File | What | Size |
|------|------|------|
| `data/docs/user-guide.md` | Written by hand: the user guide, and the source of truth for everything else | 1 document, 26 sections |
| `data/docs/internal-relay-click-revision-c.md` | Written by hand: an internal engineering note | 1 document |
| `data/docs/*.md` | The two above, plus 273 written by `gpt-6-luna` with `data/build_docs.py`: support, troubleshooting, app, installation, specification, integration, policy, error-code and release-note documents, and 40 more internal ones | 275 documents, about 154,000 words |
| `data/updates/` | Written by hand: firmware 4.2's release notes and new user guide, for section 6 | 2 documents |
| `data/questions.json` | 30 questions, each with the facts a right answer must contain | 30 questions |
| `data/faq.json` | The questions each chunk answers, written by `gpt-6-luna` with `data/build_faq.py`, for section 4 | 6,358 questions |

## Running the demos

From this folder:

```bash
uv run python demo/01_just_ask.py
```

The first run of demo 3 embeds all 1,823 chunks, and the first run of demo 4 embeds all 6,358 questions. Both are stored in `demo/output/knowledge.db`, and later runs only embed what has changed. On a slow connection those first runs take several minutes each, so run demos 3 and 4 once before a session. Demo 7 starts its MCP server, `demo/07_docs_server.py`, itself. Model output is random, so your answers will differ from the ones quoted here.

## 1. Just ask

**Demo:** `demo/01_just_ask.py`

Start with no documents at all. The instructions tell the model it is Dormouse's support assistant, and we ask three questions:

```python
response = client.responses.create(
    model=MODEL,
    reasoning={"effort": "none"},
    instructions=INSTRUCTIONS,
    input=question,
)
```

```text
Q: Why does my Dormouse turn the heating on before the time I set?
A: Dormouse may start heating early so your home reaches the target temperature by the time you set—especially in colder weather or if your home takes a while to warm up. Check whether “early start” or a similar feature is enabled in your schedule settings; turning it off should make heating begin at the scheduled time instead.

Q: My thermostat is showing E-305. What should I do?
A: E-305 can mean different things depending on your Dormouse model. Check the app or thermostat’s help screen for the model-specific meaning, then try restarting the thermostat by turning it off at the breaker for 30 seconds and switching it back on. If the code returns, contact Dormouse Support with your model and any details shown on screen; don’t open the thermostat or touch wiring.

Q: How much does a Dormouse thermostat cost?
A: I don’t have current pricing for the Dormouse thermostat. Please check Dormouse’s website or contact their sales team for the latest price.
```

The first answer is the interesting one, because it is nearly right. Lots of thermostats start heating early, so "early start" is a good guess. But the feature is called **Warm Wake**, it starts up to 90 minutes early, and it is turned off in Settings > Heating > Warm Wake, not "in your schedule settings". The second answer is worse: E-305 means the boiler isn't responding, and the fix is to check the boiler is on and its pressure is between 1 and 1.5 bar. Switching the thermostat off at the breaker does nothing for that. The third is honest about the price, and then sends the customer to a website and a sales team it knows nothing about.

### Why this breaks

The model has never seen our documents, and it doesn't say so. It writes the most likely answer for a thermostat in general, and fills in the details. Plausible, confident and wrong is called **hallucination**. It is most dangerous when the answer is *nearly* right, like the first one, because nobody checks it.

## 2. Put the documents in the prompt

**Demo:** `demo/02_whole_manual.py`

If the model needs to read our documentation, give it the documentation. Everything a model reads in one call, the instructions, any documents and the question, has to fit in its **context window**. `gpt-6-luna`'s is 1,050,000 tokens, roughly 800,000 words, and it charges $0.10 per million input tokens (Module 4's price list, checked on 10 November 2026). So we paste the documentation into the instructions and read the bill from `response.usage`:

```python
response = client.responses.create(
    model=MODEL,
    reasoning={"effort": "none"},
    instructions=f"{INSTRUCTIONS}\n\nUse our documentation:\n\n{documentation}",
    input=question,
)
usage = response.usage
cost = (usage.input_tokens * INPUT_PRICE + usage.output_tokens * OUTPUT_PRICE) / 1_000_000
```

Small first, the user guide on its own; then large, all 275 documents:

```text
=== The user guide: 1 document ===
Q: Why does my Dormouse turn the heating on before the time I set?
A: Warm Wake is probably on. It learns how long your home takes to heat up and can start heating up to 90 minutes before a scheduled period so the home is at the target temperature when it begins. The sunrise symbol appears while it’s warming early. To turn this off, go to **Settings > Heating > Warm Wake** in the app or web dashboard.
   2,380 tokens in, $0.0003, 3.1 seconds

=== The whole knowledge base: 275 documents ===
Q: Why does my Dormouse turn the heating on before the time I set?
A: That’s likely Warm Wake: it starts heating ahead of a scheduled period so your home is warm when that period begins. The sunrise symbol on the thermostat means Warm Wake is active. You can turn it off in Settings > Heating > Warm Wake in the app or web dashboard.
   191,548 tokens in, $0.0192, 24.4 seconds
```

Both answers are right, with the feature's real name and the real place to turn it off. The model hasn't learned anything: it read the answer this time.

| | User guide | Whole knowledge base |
|---|---|---|
| Documents | 1 | 275 |
| Tokens read per question | 2,380 | 191,548 |
| Cost per question | $0.0003 | $0.0192 |
| Time per question | 3.1 seconds | 24.4 seconds |

Be honest about this result: **for a small set of documents that rarely changes, putting it all in the prompt is a fair answer.** It is simple, and nothing can go wrong in a search step, because there isn't one. Providers also cache a prompt that starts the same way each time and charge less for the cached part, which helps here.

### Why this breaks

Every question pays for, and waits for, every token. The large answer read 80 times as many tokens as the small one, cost 68 times as much and took eight times as long, to say the same thing (and it left out the 90 minutes). At 10,000 questions a day, that is about $190 a day, with each customer waiting 24 seconds. And our knowledge base is small. A real company's specifications, manuals, tickets and wiki run to many millions of tokens, which no context window holds.

The model only needed one section of one document. What if we sent just that?

## 3. Retrieve, then answer

**Demo:** `demo/03_retrieve_and_answer.py`

Demo 2's model needed one section of one document, and read 275 documents to find it. So find that section first, and send only it. Three steps:

1. **Split** every document into **chunks**, one per section: everything under a heading, down to the next heading. Each chunk starts with its document's title and the headings above it, so a section called "Fix" still says what it is the fix for:

   ```text
   Dormouse Thermostat User Guide > Schedules > Warm Wake

   Warm Wake makes sure the home has already reached the target temperature when a schedule period starts, ...
   ```

2. **Embed** every chunk and store it in a vector database. Module 5 used ChromaDB; here we use **sqlite-vec**, which adds vector search to SQLite, so a search is one SQL query. The idea is the same: one row per chunk with its vector, its document (to filter on) and its text. A checksum on each chunk means a rerun only embeds what has changed.

3. **Retrieve and answer.** Embed the question, take the 5 nearest chunks, and paste just those into the instructions:

```python
documentation = "\n\n".join(f'<chunk id="{c["id"]}">\n{c["text"]}\n</chunk>' for c in found)
response = client.responses.create(
    model=MODEL,
    reasoning={"effort": "none"},
    instructions=f"{INSTRUCTIONS}\n\nUse our documentation:\n\n{documentation}",
    input=question,
)
```

That is **retrieval-augmented generation**: retrieve, then generate. The 275 documents make 1,823 chunks, 86 words long on average.

```text
275 documents, 1,823 chunks. Embedded 1,823 new or changed chunks.

Q: Why does my Dormouse turn the heating on before the time I set?
   0.667  create-a-smart-home-heating-routine.md#leave-temperature-control-to-dormouse
   0.633  create-a-smart-home-heating-routine.md#keep-temperature-schedules-on-dormouse
   0.627  use-a-smart-plug-alongside-dormouse.md#use-dormouse-for-heating
   0.611  use-a-smart-plug-alongside-dormouse.md#troubleshooting-the-separate-automation
   0.609  create-a-smart-home-heating-routine.md#troubleshoot-carefully
A: Dormouse may turn the heating on early so the room reaches the scheduled temperature by the time you set. Check the current target and schedule period in the app or web dashboard; you can edit the schedule there. Manual temperature changes last only until the next period starts, and routines shouldn’t repeatedly adjust the target temperature.
   906 tokens in, $0.0001, 2.1 seconds

The answer was in the top 5 chunks, for 24 questions: user guide 23, knowledge base 22
```

The cost has collapsed: 906 tokens instead of 191,548, a two-hundredth as many, for under a hundredth of the price, in about two seconds. And across the 24 questions the documentation answers, the top 5 chunks held the facts a right answer needs for 22 of them. (A chunk counts if it contains every fact listed for the question in `questions.json`.) Small first, large second: searching only the user guide's chunks found 23.

But look at our question. All five chunks are about smart-home routines and smart plugs: sections that talk about schedules, heating and Dormouse, the question's words. The Warm Wake section came **sixth**, with a similarity of 0.606 against 0.609 for fifth place. The answer is vague, and its first sentence isn't in any of the five chunks: the model filled the gap with a guess, just as in demo 1.

| | Chunks searched | Answer in the top 5 |
|---|---|---|
| User guide | 26 | 23 of 24 |
| Whole knowledge base | 1,823 | 22 of 24 |

The two misses on the whole knowledge base are our running question and Q11, "The heating turns down every time I nip out to the shops", which is about geofencing.

### Why this breaks

The customer and the documentation describe the same thing in different words. The customer says the heating comes on *before the time I set*. The user guide says Warm Wake *starts the heating early*, and never mentions a time the customer set. A question about "heating" and "the time I set" looks most like other sections about heating and schedules. With 26 chunks that doesn't matter much; with 1,823, plenty of chunks are about heating and schedules. The more documents you add, the more near misses there are to beat the right one.

What if the documentation came with the questions customers actually ask?

<!-- Sections 4 to 6 (FAQs, citations, keeping it current) go here. -->

## 7. Share it: an MCP server

**Demo:** `demo/07_agent.py`, which starts `demo/07_docs_server.py`

Our search lives inside our scripts. Demos 3 to 6 each carry their own copy of the code that reads the documents, splits them into chunks, embeds them and searches the database: 89 lines in demo 3. That's fine for teaching. In a company, the support chat, the help website, the staff's own tools and the AI assistants people already use would all need that search. A copy in each, every one a little different, is how answers start to disagree.

Module 3 had the fix: an **MCP server**, a small program that offers tools to any MCP client. So we put the search behind one server, and every application asks it. This is what *exposing existing company functionality to an LLM* means in practice. The search already exists; the server is a thin layer that lets any model use it.

### The server

`demo/07_docs_server.py` has one tool, and its body is demo 3's search. The docstring becomes the tool's **description**, which is all a client's model knows about the tool, so it says what is searched and how to ask:

```python
@server.tool()
def search_docs(query: str) -> str:
    """Search Dormouse's documentation by meaning: the user guide, and support, troubleshooting,
    installation, specification, policy, error-code and release-note articles. Describe what to
    look for in `query`, in the words the documentation would use. Returns the five closest
    sections as JSON, closest first, each with an id to cite and its text."""
    db = open_database()
    # Always the documents as they are now: only new or changed chunks are embedded.
    update(db, [chunk for document in load_documents(DATA / "docs") for chunk in split_into_chunks(document)])
    [vector] = embed([query])
    ...
```

It uses the same database as demos 3 to 6, `demo/output/knowledge.db`, and checks it against the documents on every search. So an edited document can be found straight away, as in section 6, without restarting the server.

### The agent

`demo/07_agent.py` starts the server, asks it for its tools, and runs Module 3's tool loop. One thing has changed since demo 3. **We no longer search for the customer: the model does.** It chooses the words, and whether to search again:

```python
INSTRUCTIONS = """You are the support assistant for Dormouse, a smart thermostat. Answer the customer in a short paragraph.
Search the documentation first, and answer only from what you find. If the results don't answer the question, search again with different words.
End each sentence that relies on the documentation with the id of the section it came from, in square brackets."""
```

```text
The server offers: search_docs

Q: Why does my Dormouse turn the heating on before the time I set?
   search_docs("thermostat heating starts before scheduled time set; early start, preheat, learns how long home takes to warm to target temperature")
      0.684  user-guide.md#warm-wake
      0.623  set-a-heating-schedule.md#before-you-start
      0.622  understand-warm-wake.md#what-warm-wake-does
      0.621  set-a-heating-schedule.md#how-schedule-periods-work
      0.610  heating-starts-below-five-degrees.md#if-the-room-is-not-below-five-degrees
A: Dormouse’s Warm Wake feature starts heating early so your home reaches the scheduled target temperature by the time the period begins. It learns how long your home takes to warm up and may start up to 90 minutes early; you’ll see a sunrise symbol while it’s doing this. Warm Wake is on by default, but you can turn it off in Settings > Heating > Warm Wake. [user-guide.md#warm-wake]
   1,063 tokens in, $0.0002, 5.6 seconds

The answer was in the chunks the agent found, for 24 questions: 24 (1.2 searches a question)
```

Look at what it searched for. The customer wrote "before the time I set". The model wrote "early start, preheat, learns how long home takes to warm to target temperature": the words a manual uses. That is the gap demo 3 fell into, and the model stepped over it. Warm Wake came **first**, where demo 3 had it sixth, and the answer has the 90 minutes, the sunrise symbol and the place to turn it off. It cites the section it used, once at the end, although we asked for a citation after every sentence.

| | Demo 3: we search | Demo 7: the model searches |
|---|---|---|
| What is searched for | The customer's words, as they are | Words the model chooses |
| Searches per question | 1 | 1.2: four of the 24 searched twice |
| Answer in what was found | 22 of 24 | 24 of 24 (23 from the first search alone) |
| Warm Wake, for our question | 6th | 1st |
| Our question: tokens in | 906 | 1,063 |
| Our question: cost | $0.0001 | $0.0002 |
| Our question: time | 2.1 seconds | 5.6 seconds |

Both of demo 3's misses were found: our question, and Q11, *"The heating turns down every time I nip out to the shops"*, where the model searched for "stop away mode geofencing presence detection". Three of the four second searches were for error codes: the first search found what the code means, and the second went back for the fix. The fourth was Q11 going back for how to turn geofencing off. (Every question's searches and answer are in `demo/output/07_agent.json`.)

The price is a second model call. The model reads the question to write a search, then reads the results to answer, so every question takes at least two calls instead of one. It is still a fraction of a cent, but it is more than twice as slow.

### The same server, another client

The server isn't tied to our agent. To give it to Claude Code, run this from this folder:

```bash
claude mcp add dormouse-docs -- uv run --directory "$PWD" python demo/07_docs_server.py
```

Claude Desktop takes the same command as JSON, in `claude_desktop_config.json` (Settings > Developer > Edit Config):

```json
{
  "mcpServers": {
    "dormouse-docs": {
      "command": "uv",
      "args": ["run", "--directory", "/full/path/to/module-06-rag-and-proprietary-knowledge", "python", "demo/07_docs_server.py"]
    }
  }
}
```

If Claude Desktop can't find `uv`, give its full path, which `which uv` prints. Cursor, VS Code and other MCP clients take the same command in their own settings, and the server doesn't change. We haven't quoted a Claude session here: try it, and ask Claude why your Dormouse heats early.

In practical terms, this is what MCP gives us:

- **One search, many applications.** The chunking, the embeddings and the database are written once and run in one place. Improve the search, and every application gets the improvement.
- **The model writes the search.** Given a tool instead of a fixed search, a model rewrites the customer's words into the documentation's, and goes back for more when the first results aren't enough.
- **The description is the contract.** A client knows nothing about our tool but its name, its description and its arguments. Writing the description is part of building the tool.
- **A thin layer over what already exists.** The server is demo 3's code with a decorator on it. A company's own search, ticket system or product API can be put behind a server the same way.

### Why this breaks

The server searches every document it has, for whoever runs it. That includes the 41 internal ones: engineering notes, support playbooks and QA reports. Across the 24 customer questions, the server handed the model 5 sections from internal documents, and one answer cited one:

```text
Q: What's the coldest I can set the thermostat to?
A: The coldest target temperature you can set is 5°C. The thermostat’s frost protection is always on and will turn the heating on if the room drops below 5°C. [thermostat-physical-and-environmental-limits.md#indoor-operating-range] [thermostat-electrical-safety-policy.md#limits-and-safety-features]
```

The first source is an internal specification. This time the fact was harmless. Next time it could be a supplier's name, a known fault or another customer's details.

The server can't do better, because it has no idea who is asking. There is no sign-in: a customer's chat, a member of staff and anyone else given the command all get the same search. And section 5's check, that every quote really is in the chunk it cites, has gone: the client writes the answer now, and nothing checks it. Sharing the search with every application shared it with everyone. Deciding who may see what, and enforcing it in code rather than in a prompt, is Module 8.
