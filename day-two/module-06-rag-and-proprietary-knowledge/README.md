# Module 6 — RAG and Proprietary Knowledge

> A customer asks Dormouse's support assistant: _"Why does my Dormouse turn the heating on before the time I set?"_ **Just asking** the model gets a confident answer about thermostats in general, nearly right and partly made up: **hallucination**. Putting **all 275 documents in the prompt** gets the right answer, for 191,548 tokens and 24 seconds a question. **RAG** splits the documents into 1,823 **chunks**, stores them in a **vector database**, ChromaDB, and sends the model only the five nearest the question: 906 tokens and two seconds, with the right chunks for 22 of 24 questions. But not for ours. The customer's words aren't the documentation's, Warm Wake comes sixth, and the model fills the gap with a guess. Putting the search behind an **MCP server** shares it with every application, and lets the model write its own searches, in the documentation's words: Warm Wake comes first and all 24 are found, but every question now takes two model calls. An **FAQ**, the questions each chunk answers, written once ahead of time, finds 23 of 24 with the customer's own words, though questions that sound alike can point at the wrong chunk. Last, the model must **quote its sources**, code checks every quote, and the model says when the documentation doesn't answer: all 57 quotes check out, and all 5 questions the documentation can't answer are turned down. But "I don't know" is only as good as the search, and a real quote can still leave out the fact that mattered. And no search in this module asks who is asking, so internal documents reach customers. That is Module 8.

## Learning goals

- Explain why a model makes up answers about things it has never seen (**hallucination**), and why the answers sound right.
- Put documents in a model's prompt, and measure what that costs in **tokens**, money and time for each question.
- Split documents into **chunks**, store them in a **vector database** with **metadata** to filter on, re-embed only what changed, find the relevant chunks, and answer from them: **retrieval-augmented generation** (**RAG**).
- Offer the search to any AI application as an **MCP server**, and let the model write its own searches.
- Turn documentation into the questions customers ask (an **FAQ**), search those too, and **measure** whether it helps.
- Make a model **cite its sources**, check each quote in code, and let it say when the documentation doesn't answer.

---

## The idea: look it up, then answer

A language model only knows what was in its training data. Your specifications, manuals and support articles were not in it. Ask it about your product and it does what it always does: it writes the most likely-sounding answer. For a thermostat, that is an answer about thermostats in general, with the details made up.

The fix is the one a new support agent uses: look it up, then answer. Find the parts of the documentation that are about the question, put them in front of the model, and ask it to answer from them. That is **retrieval-augmented generation**, or **RAG**. The retrieval part is Module 5's vector search. The generation part is Module 2's model call. Everything else in this module is about doing the two well: how much to retrieve, how to share the search, how to find the right part when the customer's words aren't the documentation's, and how to check the answer came from the documents.

## The data

Everything runs on the documentation for **Dormouse**, the smart thermostat from Module 5. **Dormouse and all its documents are invented for this course.** Your own documentation would work the same way.

| File                                           | What                                                                                                                                                                                                                         | Size                               |
| ---------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------- |
| `data/docs/user-guide.md`                      | Written by hand: the user guide, and the source of truth for everything else                                                                                                                                                 | 1 document, 26 sections            |
| `data/docs/internal-relay-click-revision-c.md` | Written by hand: an internal engineering note                                                                                                                                                                                | 1 document                         |
| `data/docs/*.md`                               | The two above, plus 273 written by `gpt-6-luna` with `data/build_docs.py`: support, troubleshooting, app, installation, specification, integration, policy, error-code and release-note documents, and 40 more internal ones | 275 documents, about 154,000 words |
| `data/questions.json`                          | 30 questions, each with the facts a right answer must contain: 24 the documentation answers, 5 it doesn't, and 1 that only an internal document answers                                                                      | 30 questions                       |
| `data/faq.json`                                | The questions each chunk answers, written by `gpt-6-luna` with `data/build_faq.py`, for section 5                                                                                                                            | 6,358 questions                    |

## Setting up

You need `OPENAI_API_KEY` in `.env` (see Module 2). This module adds one package, **ChromaDB**, a vector database. `uv` installs it with everything else. It's a big install: 84 packages, including numpy and onnxruntime. We give Chroma our own vectors, so it never downloads an embeddings model of its own.

## Running the demos

From this folder:

```bash
uv run python demo/01_just_ask.py
```

| Demo                        | What it is                                                                                 | Writes to `demo/output/`                                                                                              |
| --------------------------- | ------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------- |
| `01_just_ask.py`            | Ask the model three questions, with no documents                                           | `01_just_ask.json`: the instructions and the answers                                                                  |
| `02_whole_manual.py`        | Put the user guide, then all 275 documents, in the prompt                                  | `02_whole_manual.json`: each answer, with its tokens, cost and time                                                   |
| `03_retrieve_and_answer.py` | Chunk, embed and store the documents in ChromaDB, then answer from the five nearest chunks | `03_retrieve_and_answer.json`: the chunks found, the answer, and the 24 questions' checks; `chunks.json`: every chunk |
| `04_agent.py`               | An agent that searches through an MCP server, `04_docs_server.py`, which it starts itself  | `04_agent.json`: every question's searches, results and answer                                                        |
| `05_faq.py`                 | Search the questions each chunk answers, as well as the chunks                             | `05_faq.json`: the chunks found, the answer, and the 24 questions' checks, three ways                                 |
| `06_citations.py`           | Answer only from the chunks, quote them, check every quote, and say when there's no answer | `06_citations.json`: all 30 answers, their quotes and checks, and how each turned out                                 |

The first run of demo 3 embeds all 1,823 chunks, and the first run of demo 5 embeds all 6,358 questions. Both are stored in ChromaDB, in `demo/output/chroma/`, and later runs only embed what has changed. On a slow connection those first runs take several minutes each, so run demos 3 and 5 once before a session. Model output is random, so your answers will differ from the ones quoted here.

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

The model has never seen our documents, and it doesn't say so. It writes the most likely answer for a thermostat in general, and fills in the details. Plausible, confident and wrong is called **hallucination**. It is most dangerous when the answer is _nearly_ right, like the first one, because nobody checks it.

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

|                          | User guide  | Whole knowledge base |
| ------------------------ | ----------- | -------------------- |
| Documents                | 1           | 275                  |
| Tokens read per question | 2,380       | 191,548              |
| Cost per question        | $0.0003     | $0.0192              |
| Time per question        | 3.1 seconds | 24.4 seconds         |

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

2. **Embed** every chunk and store it in a **vector database**: a database that keeps vectors, finds the ones nearest a question's vector, and keeps facts about each one (**metadata**) to filter by. We use **ChromaDB**, which runs inside the script and keeps everything in a folder, `demo/output/chroma/` (33 MB for 1,823 chunks):

   ```python
   database = chromadb.PersistentClient(path=str(DATABASE), settings=Settings(anonymized_telemetry=False))
   collection = database.get_or_create_collection(
       "chunks", configuration={"hnsw": {"space": "cosine"}}, embedding_function=None
   )
   ```

   A **collection** is like a table. We ask it to compare by cosine similarity, and to use the vectors we give it rather than Chroma's built-in embeddings model. `anonymized_telemetry=False` stops Chroma sending usage statistics. Each chunk goes in with its vector, its text and its metadata: the document it came from, who that document is for, and a **checksum**, a short fingerprint of the text that changes whenever the text does:

   ```python
   collection.upsert(
       ids=[c["id"] for c in changed],
       embeddings=embed([c["text"] for c in changed]),
       documents=[c["text"] for c in changed],
       metadatas=[{"document": c["document"], "audience": c["audience"], "checksum": ...} for c in changed],
   )
   ```

   **Embed once.** On every run, only chunks that are new, or whose text has changed, are embedded, and chunks that are no longer in the documents are deleted. The first run embeds all 1,823 chunks. The second:

   ```text
   275 documents, 1,823 chunks. Embedded 0 new or changed chunks.
   ```

3. **Retrieve and answer.** Embed the question, ask the collection for the 5 nearest chunks, and paste just those into the instructions:

```python
results = collection.query(query_embeddings=[vector], n_results=5, include=["distances", "documents"])
found = [{"id": id, "text": text} for id, text in zip(results["ids"][0], results["documents"][0])]

documentation = "\n\n".join(f'<chunk id="{c["id"]}">\n{c["text"]}\n</chunk>' for c in found)
response = client.responses.create(
    model=MODEL,
    reasoning={"effort": "none"},
    instructions=f"{INSTRUCTIONS}\n\nUse our documentation:\n\n{documentation}",
    input=question,
)
```

That is **retrieval-augmented generation**: retrieve, then generate. The 275 documents make 1,823 chunks, 86 words long on average.

**Search with a filter.** `where` limits a search to the chunks whose metadata matches. The demo uses it to search the user guide alone, then the whole knowledge base:

```python
collection.query(query_embeddings=[vector], n_results=5, where={"document": "user-guide.md"})
```

The same filter on `audience` would keep a customer away from the 41 internal documents. None of this module's demos use it; Module 8 does.

**Not every vector is compared.** Chroma organises the vectors as an **HNSW** graph ("hierarchical navigable small world"): each vector is linked to its near neighbours, and a search hops from vector to vector towards the question instead of checking them all. That's how a vector database searches millions of vectors in milliseconds. The price is that the search is **approximate**: very occasionally it misses a vector that's slightly closer. Here it made no difference: an exact search, comparing all 1,823, finds the same five chunks with the same similarities.

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

|                      | Chunks searched | Answer in the top 5 |
| -------------------- | --------------- | ------------------- |
| User guide           | 26              | 23 of 24            |
| Whole knowledge base | 1,823           | 22 of 24            |

The two misses on the whole knowledge base are our running question and Q11, "The heating turns down every time I nip out to the shops", which is about geofencing.

### Why this breaks

The customer and the documentation describe the same thing in different words. The customer says the heating comes on _before the time I set_. The user guide says Warm Wake _starts the heating early_, and never mentions a time the customer set. A question about "heating" and "the time I set" looks most like other sections about heating and schedules. With 26 chunks that doesn't matter much; with 1,823, plenty of chunks are about heating and schedules. The more documents you add, the more near misses there are to beat the right one.

A support agent who didn't find it would search again, in other words. Our code can't: it embeds the customer's words once and takes what comes back. A model could, if we gave it the search as a tool.

## 4. Share it: an MCP server

**Demo:** `demo/04_agent.py`, which starts `demo/04_docs_server.py`

Module 3 gave a model tools, and the search can be one. Making it a tool solves a second problem too. Our search lives inside our script: demo 3 carries its own copy of the code that reads the documents, splits them into chunks, embeds them and searches the database, 89 lines of it. That's fine for teaching. In a company, the support chat, the help website, the staff's own tools and the AI assistants people already use would all need that search. A copy in each, every one a little different, is how answers start to disagree.

Module 3 had the fix: an **MCP server**, a small program that offers tools to any MCP client. So we put the search behind one server, and every application asks it. This is what _exposing existing company functionality to an LLM_ means in practice. The search already exists; the server is a thin layer that lets any model use it.

### The server

`demo/04_docs_server.py` has one tool, and its body is demo 3's search. The docstring becomes the tool's **description**, which is all a client's model knows about the tool, so it says what is searched and how to ask:

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

It uses the same ChromaDB collection as demo 3, in `demo/output/chroma/`, and checks it against the documents on every search. So an edited document can be found straight away, without restarting the server.

### The agent

`demo/04_agent.py` starts the server, asks it for its tools, and runs Module 3's tool loop. One thing has changed since demo 3. **We no longer search for the customer: the model does.** It chooses the words, and whether to search again:

```python
INSTRUCTIONS = """You are the support assistant for Dormouse, a smart thermostat. Answer the customer in a short paragraph.
Search the documentation first, and answer only from what you find. If the results don't answer the question, search again with different words.
End each sentence that relies on the documentation with the id of the section it came from, in square brackets."""
```

```text
The server offers: search_docs

Q: Why does my Dormouse turn the heating on before the time I set?
   search_docs("Thermostat starts heating before scheduled set time preheat early start learning warm-up schedule target temperature")
      0.683  user-guide.md#warm-wake
      0.629  understand-warm-wake.md#what-warm-wake-does
      0.627  heating-starts-below-five-degrees.md#if-the-room-is-not-below-five-degrees
      0.621  set-a-heating-schedule.md#before-you-start
      0.619  set-a-heating-schedule.md#how-schedule-periods-work
A: Dormouse’s Warm Wake feature starts heating up to 90 minutes before a scheduled period so your home reaches the target temperature by the time the period begins. It learns how quickly your home heats using recent heating history and your local outside temperature. Warm Wake is on by default; you can turn it off in **Settings > Heating > Warm Wake**. [user-guide.md#warm-wake]
   1,056 tokens in, $0.0002, 4.7 seconds

The answer was in the chunks the agent found, for 24 questions: 24 (1.1 searches a question)
```

Look at what it searched for. The customer wrote "before the time I set". The model wrote "preheat", "early start" and "learning warm-up": the words a manual uses. That is the gap demo 3 fell into, and the model stepped over it. Warm Wake came **first**, where demo 3 had it sixth, and the answer has the 90 minutes, how Warm Wake learns, and the place to turn it off. It cites the section it used, once at the end, although we asked for a citation after every sentence.

|                             | Demo 3: we search                 | Demo 4: the model searches          |
| --------------------------- | --------------------------------- | ----------------------------------- |
| What is searched for        | The customer's words, as they are | Words the model chooses             |
| Searches per question       | 1                                 | 1.1: two of the 24 searched twice   |
| Answer in what was found    | 22 of 24                          | 24 of 24, all from the first search |
| Warm Wake, for our question | 6th                               | 1st                                 |
| Our question: tokens in     | 906                               | 1,056                               |
| Our question: cost          | $0.0001                           | $0.0002                             |
| Our question: time          | 2.1 seconds                       | 4.7 seconds                         |

Both of demo 3's misses were found: our question, and Q11, _"The heating turns down every time I nip out to the shops"_, where the model searched for "presence detection away mode geofencing how to disable". Both second searches were for error codes, E-305 and E-217: the first search found what the code means, and the second went back for what to do about it. (Every question's searches and answer are in `demo/output/04_agent.json`.)

### The same server, another client

The server isn't tied to our agent. To give it to Claude Code, run this from this folder:

```bash
claude mcp add dormouse-docs -- uv run --directory "$PWD" python demo/04_docs_server.py
```

Claude Desktop takes the same command as JSON, in `claude_desktop_config.json` (Settings > Developer > Edit Config):

```json
{
  "mcpServers": {
    "dormouse-docs": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/full/path/to/module-06-rag-and-proprietary-knowledge",
        "python",
        "demo/04_docs_server.py"
      ]
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

**Every question pays for the rewrite.** The model reads the question to write a search, then reads the results to answer, so every question takes at least two model calls instead of one. It is still a fraction of a cent, but our question took 4.7 seconds instead of 2.1. And the work is the same each time: customers ask why the heating comes on early in much the same words every week, and the model works out the manual's words for them again, every time.

**Nothing checks what goes back.** The client writes the answer now, so nothing checks that it came from what the search found. And the server searches every document it has, for whoever runs it, including the 41 internal ones. Across the 24 customer questions it handed the model 3 sections from internal documents: a specification, support notes and a support playbook. One answer cited the specification:

```text
Q: What's the coldest I can set the thermostat to?
A: The coldest target temperature you can set is 5°C, in half-degree steps. [thermostat-physical-and-environmental-limits.md#indoor-operating-range]
```

This time the fact was harmless, and the user guide says the same. Next time it could be a supplier's name, a known fault or another customer's details. We come back to both problems at the end of the module.

Start with the first. Matching the customer's words to the documentation's could be done once, ahead of time, instead of on every question. What if the documentation came with the questions customers actually ask?

## 5. FAQs: the questions customers ask

**Demo:** `demo/05_faq.py`

A manual is written in the manual's words. Customers ask in theirs. So turn every chunk into the questions it answers, written the way a customer would type them, and search those as well. It is what a good **FAQ** does, for every section at once.

`data/build_faq.py` did the writing, once. It sends `gpt-6-luna` ten chunks at a time with these instructions:

```python
INSTRUCTIONS = """You turn documentation into the questions customers ask.
For each chunk of Dormouse documentation, write 3 to 5 questions that the chunk answers.
Write them as a customer who has never read the documentation would type them into a chat window:
in everyday words, describing what they see or what they want. Plain ASCII."""
```

The 1,823 chunks got 6,358 questions, saved in `data/faq.json` with a checksum of the chunk they came from. When a chunk changes, only its questions are written again.

The demo embeds every question into a second ChromaDB collection, `questions`. Each question's metadata says which chunk it came from:

```python
question_store.upsert(
    ids=[f"{id}?{n}" for id, n, _ in batch],
    embeddings=vectors[start : start + STORE_BATCH],
    documents=[question for _, _, question in batch],
    metadatas=[{"chunk": id, "checksum": current[id]} for id, _, _ in batch],
)
```

To answer, it searches both collections with the customer's own words, keeps each chunk's best match, and sends the model the top five chunks, exactly as demo 3 did. The model still sees chunks, never the made-up questions. There is one model call, and no rewriting at question time: that was done when the questions were written.

```text
1,823 chunks, and 6,358 questions they answer.

The questions written for user-guide.md#warm-wake:
   Why does my heating start before a schedule period begins?
   What does the sunrise symbol on the display mean?
   How do I turn Warm Wake off?
   How far ahead can Warm Wake start heating?

Q: Why does my Dormouse turn the heating on before the time I set?
   0.728  thermostat-shows-the-wrong-room-temperature.md#top  via "Why does my Dormouse Thermostat show the wrong room temperature?"
   0.728  thermostat-physical-dimensions-and-display-specification.md#product  via "What does the Dormouse Thermostat do?"
   0.707  radiator-valve-does-not-heat-to-its-own-temperature.md#top  via "Why isn't my Dormouse Radiator Valve heating my radiator to its own temperature?"
   0.693  create-a-smart-home-heating-routine.md#keep-temperature-schedules-on-dormouse  via "How can I keep heating schedules in Dormouse while using smart-home routines?"
   0.684  firmware-4-0-release-notes.md#warm-wake  via "Why does my heating start before my schedule begins?"
A: This may be Warm Wake: it starts heating up to 90 minutes before a scheduled period so your home reaches the target temperature by the time you set. To turn it off, go to **Settings > Heating > Warm Wake**.

The answer was in the top 5 chunks, for 24 questions: searching chunks 22, searching questions 23, searching both 23
```

The first question written for the user guide's Warm Wake section is nearly the customer's question: _"Why does my heating start before a schedule period begins?"_ The section itself never says anything like it. A Warm Wake chunk came in fifth, through the firmware 4.0 release notes' question _"Why does my heating start before my schedule begins?"_, and the answer is right: Warm Wake, 90 minutes, and where to turn it off. But look at what came first: two questions about other problems that start like ours, _"Why does my Dormouse Thermostat show the wrong room temperature?"_ and _"Why isn't my Dormouse Radiator Valve heating..."_, then _"What does the Dormouse Thermostat do?"_, a question about everything, and one about schedules and smart-home routines. They share our question's words, "why", "Dormouse", "heating", more than its meaning.

|                          | Demo 3: chunks | Demo 4: the model searches | Demo 5: chunks and questions |
| ------------------------ | -------------- | -------------------------- | ---------------------------- |
| Answer in what was found | 22 of 24       | 24 of 24                   | 23 of 24                     |
| Missed                   | Q01, Q11       | none                       | Q06                          |
| Model calls per question | 1              | 2 or more                  | 1                            |
| Written ahead of time    | nothing        | nothing                    | 6,358 questions              |

Searching the questions found both of demo 3's misses, our question and Q11 (geofencing), with the customer's own words. Searching the questions alone also found 23, with the same miss. (Every question's top five, and the question each chunk matched through, are in `demo/output/05_faq.json`.)

### Why this breaks

- **Questions that sound alike.** A question is short, so a few shared words count for a lot. Q06, _"How many people in my family can control the heating?"_, matched _"How many thermostats and heating zones can I have in my home?"_ first, and none of the five chunks it found says how many people a household can have. "How many" and "heating" were enough. Searching the chunks alone had found it. And for our question, the right chunk came fifth, behind four that only share its words.
- **Finding the chunk isn't checking the answer.** Every count so far asks whether the right chunk was found. None asks whether the answer came from it. Demo 3's first sentence was in none of its chunks. This answer happens to be right, but nothing in it says where it came from, and a customer can't tell a fact from a guess.

What if the model had to show where each sentence came from, and we checked?

## 6. Citations: show the source, check it

**Demo:** `demo/06_citations.py`

Three changes to demo 3, and nothing else. The search stays as it was, the customer's words against the chunks, so we can see what the instructions and the check change on their own.

1. **Stricter instructions.** Use only the documentation, quote it word for word, and say when it doesn't answer:

   ```python
   INSTRUCTIONS = """You are the support assistant for Dormouse, a smart thermostat. Answer the customer in a short paragraph.
   Use only the documentation below, never what you know from elsewhere.
   Quote, word for word, each sentence you rely on, with the id of the chunk it comes from.
   If the documentation does not answer the question, set answered to false and say so. Do not guess."""
   ```

2. **A fixed shape for the reply.** **Structured outputs** make the model reply with JSON that matches a schema: `answered` (true or false), `answer`, and a list of `citations`, each a chunk id and a quote:

   ```python
   text={"format": {"type": "json_schema", "name": "answer", "schema": SCHEMA, "strict": True}}
   ```

3. **Check every quote in code.** A quote counts only if it really is in the chunk it cites, ignoring case, spacing and Markdown symbols:

   ```python
   def check(citations, found):
       texts = {c["id"]: words(c["text"]) for c in found}
       return [{**c, "checked": words(c["quote"]) in texts.get(c["chunk"], "")} for c in citations]
   ```

The demo asks two questions, then all 30 in `data/questions.json`: the 24 the documentation answers, the 5 it doesn't, and 1 only an internal note answers.

```text
Q: Why does my Dormouse turn the heating on before the time I set?
A: The documentation doesn’t explain why Dormouse might turn the heating on before a scheduled time.

Q: How much does a Dormouse thermostat cost?
A: The documentation does not provide the Dormouse Thermostat’s price.

Of 24 questions the documentation answers: answered right 19, answered wrong 4, said it didn't know 1
Of 5 questions it doesn't: said it didn't know 5
Quotes found in the chunk they cite: 57 of 57
```

Our question first. Demo 3 searched the same way, missed Warm Wake, and guessed. Told not to, the model now says the documentation doesn't explain it. That is honest, and it is no help to the customer. The price question is better than demo 1, which sent the customer to a website and a sales team it knew nothing about. All five questions the documentation doesn't answer (the price, the founder, the next model, a discount and a phone number) got "the documentation doesn't say". For the phone number it added that support is in the app under Help > Contact support, with a checked quote. The internal question, about a loud click, got "the documentation does not explain".

Every one of the 57 quotes is in the chunk it cites. That isn't guaranteed: in an earlier run of the same demo, one quote of 60 wasn't. The chunk said _"It keeps the home at the away temperature until you turn Away mode off."_ The model had tidied it into _"Away mode keeps the home at the away temperature until you turn it off"_ and still called it a quote, and the check caught it. A check that looks for the exact words doesn't have to decide whether a change matters.

| Outcome                          | Questions |
| -------------------------------- | --------- |
| Answerable: answered right       | 19 of 24  |
| Answerable: answered wrong       | 4 of 24   |
| Answerable: said it didn't know  | 1 of 24   |
| Not covered: said it didn't know | 5 of 5    |
| Internal: kept it internal       | 1 of 1    |

The four counted wrong aren't made up. Two of them quote the very fact they leave out. From `demo/output/06_citations.json`:

```text
Q: Can I have a separate thermostat for upstairs?
A: Yes. You can use a separate thermostat to control upstairs as its own zone and schedule. Each thermostat controls its own zone, and separate thermostats can control downstairs and upstairs heating.
   [thermostat-valve-and-sensor-zone-planning.md#choose-the-zones] "A home can have up to four thermostats, each controlling its own zone with its own schedule." (quote checked)
   [wired-thermostat-and-wireless-zone-devices.md#zone-planning-and-schedules] "For example, separate thermostats can control downstairs and upstairs heating." (quote checked)
```

The quote says up to four; the answer doesn't, and the score reads the answer. Q22 is the same: its quote says "Replace both AA batteries", its answer only "the batteries". The other two answer a different question from the one asked. Q21 gets what E-217 means, but not that the thermostat needs a replacement. Q11 gets how to turn Away mode off by hand, when it's geofencing that turns it on.

### Why this breaks

- **"I don't know" is only as good as the search.** Our question was answered "the documentation doesn't explain" because the search missed Warm Wake. Sections 4 and 5 found it; this demo searches as demo 3 did.
- **A real quote can still give a poor answer.** The check proves a quote is in the chunk it cites. It doesn't prove the answer says what the quote says, or that it answers the question. All four wrong answers passed the check.
- **We can only check the answers we write.** Behind the MCP server in section 4, the client writes the answer, and nothing checks its quotes.
- **No search here asks who is asking.** Every search in this module looks at all 275 documents. In section 4, an answer to a customer cited an internal specification. Deciding who may see what, and enforcing it in code rather than in a prompt, is Module 8.

---

## Summary

| Step                               | Answers from                                   | Problem                                                                                |
| ---------------------------------- | ---------------------------------------------- | -------------------------------------------------------------------------------------- |
| 1. Just ask                        | What the model already knows                   | Makes up what it doesn't know: hallucination                                           |
| 2. Put the documents in the prompt | Every document, every time                     | 191,548 tokens and 24 seconds a question, and a real company's documents won't fit     |
| 3. Retrieve, then answer           | The 5 chunks nearest the customer's words      | The customer's words aren't the documentation's: it misses, then guesses               |
| 4. Share it: an MCP server         | The chunks the model searches for              | Two model calls a question; nothing checks the answer, or who is asking                |
| 5. FAQs                            | Chunks found through the questions they answer | Questions that sound alike point at the wrong chunk; the answer isn't checked          |
| 6. Citations                       | Quotes from the chunks, checked in code        | Refuses when the search misses; real quotes, incomplete answers; no idea who is asking |

## Playground

[`playground/`](playground/) has seven things to play with: a chat over your own documents with checked quotes, chunk sizes, chunk headings, how many chunks to send, grounding rules, finding every stale copy of a fact, and the bill for long context against RAG.

## Further reading and extensions

The final exercise is in [`further-reading/`](further-reading/): papers on hallucination, long context, RAG, vector search, turning documents into questions, citations and fine-tuning, with a note on what to look for in each and which demo it relates to, plus extension projects to take home.

## Slides

```bash
pnpm slides:06
```
