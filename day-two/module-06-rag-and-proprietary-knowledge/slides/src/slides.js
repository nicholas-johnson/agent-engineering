export const slides = [
  {
    type: 'title',
    content: {
      title: 'Agent Engineering',
      subtitle: 'Nicholas Johnson',
      icon: 'sparkles',
    },
  },
  {
    type: 'title',
    content: {
      title: 'Module 6 — RAG and Proprietary Knowledge',
      subtitle: 'Answering from your own documents',
      icon: 'book',
    },
  },
  {
    type: 'description',
    content: {
      title: 'The question',
      icon: 'question',
      description:
        'A customer writes in: *why does my Dormouse turn the heating on before the time I set?* The answer is in our documentation. The model has never read our documentation. **How do we get it to answer from our documents, and only from them?**',
    },
  },
  {
    type: 'code',
    content: {
      title: 'The data',
      code: `---
title: Dormouse Thermostat User Guide
product: thermostat
type: guide
audience: customer
firmware: 4.1
updated: 2026-08-17
---

# Dormouse Thermostat User Guide

## Schedules

### Warm Wake

Warm Wake makes sure the home has already reached the target
temperature when a schedule period starts ...`,
      highlights: [
        '**Dormouse**: the thermostat whose documents Module 5 searched',
        'A user guide written by hand, plus **274 documents** written by `gpt-6-luna`',
        'Support, installation, apps, specs, policies, release notes, and **41 internal** documents',
        '**30 questions**, each with the facts a right answer must contain',
      ],
    },
  },

  // ---- Section 1: Just ask ----
  {
    type: 'title',
    content: {
      title: '1. Just ask',
      subtitle: 'What does the model already know?',
      icon: 'message-square',
    },
  },
  {
    type: 'standard',
    content: {
      title: 'What the model knows',
      icon: 'brain',
      points: [
        'Everything in its **training data**: the public web, books, code',
        'Not your specifications, manuals, tickets or wiki',
        'Not anything written after its training finished',
        'Asked anyway, it does what it always does: writes the **most likely** answer',
      ],
    },
  },
  {
    type: 'title',
    content: {
      title: 'Demo — Just ask',
      subtitle: 'Switch to terminal: python demo/01_just_ask.py',
      icon: 'rocket',
    },
  },
  {
    type: 'code',
    content: {
      title: 'Why this breaks',
      code: `Q: Why does my Dormouse turn the heating on before the time I set?
A: Dormouse may start heating early so your home reaches the target
   temperature by the time you set ... Check whether "early start" or a
   similar feature is enabled in your schedule settings ...

Q: My thermostat is showing E-305. What should I do?
A: ... try restarting the thermostat by turning it off at the breaker
   for 30 seconds and switching it back on ...`,
      highlights: [
        'The right **idea**, the wrong **details**: the feature is called Warm Wake',
        'E-305 means the boiler is not responding: check its pressure, not the breaker',
        'Confident and plausible: this is **hallucination**',
        'It has never seen our documents, and it does not say so',
      ],
    },
  },

  // ---- Section 2: Put the documents in the prompt ----
  {
    type: 'title',
    content: {
      title: '2. Put the documents in the prompt',
      subtitle: 'If it needs to read them, give it them',
      icon: 'file',
    },
  },
  {
    type: 'standard',
    content: {
      title: 'The context window',
      icon: 'layers',
      points: [
        'Everything the model reads in one call: instructions, documents, question',
        '`gpt-6-luna`: **1,050,000 tokens**, about 800,000 words',
        'Priced per token read: **$0.10 per million** input tokens',
        'Small first: the user guide. Then large: all 275 documents',
      ],
    },
  },
  {
    type: 'code',
    content: {
      title: 'Documentation in the instructions',
      code: `response = client.responses.create(
    model=MODEL,
    reasoning={"effort": "none"},
    instructions=f"{INSTRUCTIONS}\\n\\nUse our documentation:\\n\\n{documentation}",
    input=question,
)
usage = response.usage
cost = (usage.input_tokens * INPUT_PRICE
        + usage.output_tokens * OUTPUT_PRICE) / 1_000_000`,
      highlights: [
        'The same call as Module 2, with the documents pasted in',
        '`usage` says how many tokens were read: that is the bill',
        'We time it too',
      ],
    },
  },
  {
    type: 'title',
    content: {
      title: 'Demo — The whole manual',
      subtitle: 'Switch to terminal: python demo/02_whole_manual.py',
      icon: 'rocket',
    },
  },
  {
    type: 'code',
    content: {
      title: 'Why this breaks',
      code: `=== The user guide: 1 document ===
A: Warm Wake is probably on ... can start heating up to 90 minutes
   before a scheduled period ... go to Settings > Heating > Warm Wake
   2,380 tokens in, $0.0003, 3.1 seconds

=== The whole knowledge base: 275 documents ===
A: That's likely Warm Wake ... You can turn it off in
   Settings > Heating > Warm Wake in the app or web dashboard.
   191,548 tokens in, $0.0192, 24.4 seconds`,
      highlights: [
        'Both right. For a small, stable set of documents, **this is a fair answer**',
        'But every question pays for, and waits for, **every token**',
        '10,000 questions a day: about **$190 a day** and 24 seconds each',
        "A real company's documentation is bigger than any context window",
      ],
    },
  },

  // ---- Section 3: Retrieve, then answer ----
  {
    type: 'title',
    content: {
      title: '3. Retrieve, then answer',
      subtitle: 'Send only the part that matters',
      icon: 'search',
    },
  },
  {
    type: 'standard',
    content: {
      title: 'Retrieval-augmented generation',
      icon: 'route',
      points: [
        '**Split** each document into **chunks**: one per section',
        '**Embed** every chunk and store it in a **vector database**: ChromaDB',
        '**Retrieve** the 5 chunks nearest the question',
        '**Generate** the answer from those chunks alone',
        'Retrieve, then generate: **RAG**',
      ],
    },
  },
  {
    type: 'code',
    content: {
      title: 'A chunk',
      code: `Dormouse Thermostat User Guide > Schedules > Warm Wake

Warm Wake makes sure the home has already reached the target
temperature when a schedule period starts, rather than starting
to warm up at that time. It learns how long your home takes to
heat up, and starts the heating early by up to 90 minutes. ...`,
      highlights: [
        'Everything under one heading, down to the next',
        'Starts with the **title and headings** above it, so it says what it is about',
        '275 documents make **1,823 chunks**, 86 words on average',
      ],
    },
  },
  {
    type: 'code',
    content: {
      title: 'ChromaDB',
      code: `database = chromadb.PersistentClient(
    path=str(DATABASE),
    settings=Settings(anonymized_telemetry=False),
)
collection = database.get_or_create_collection(
    "chunks",
    configuration={"hnsw": {"space": "cosine"}},
    embedding_function=None,
)`,
      highlights: [
        'A **vector database**: stores vectors, finds the nearest, filters by facts about each',
        'Runs inside our script: one folder, **33 MB** for 1,823 chunks',
        'A **collection** is like a table. Compare by **cosine**',
        "`embedding_function=None`: **our** vectors, not Chroma's own model",
      ],
    },
  },
  {
    type: 'code',
    content: {
      title: 'Store once',
      code: `collection.upsert(
    ids=[c["id"] for c in changed],
    embeddings=embed([c["text"] for c in changed]),
    documents=[c["text"] for c in changed],
    metadatas=[{"document": ..., "audience": ...,
                "checksum": ...} for c in changed],
)`,
      highlights: [
        '**Metadata**: facts about each chunk, to filter by',
        'A **checksum** of the text: embed only what is new or changed',
        'First run: **1,823** chunks embedded. Second run: **0**',
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'Not every vector is compared',
      icon: 'route',
      points: [
        '**HNSW**: each vector is linked to its near neighbours',
        'A search **hops** from vector to vector towards the question',
        'Millions of vectors in milliseconds',
        '**Approximate**: very occasionally it misses a slightly closer one. Here, the same top 5 as comparing all 1,823',
      ],
      credit:
        'Malkov & Yashunin (2018). "Efficient and Robust Approximate Nearest Neighbor Search Using Hierarchical Navigable Small World Graphs." arXiv:1603.09320',
    },
  },
  {
    type: 'code',
    content: {
      title: 'Retrieve, then answer',
      code: `results = collection.query(query_embeddings=[vector], n_results=5)
found = zip(results["ids"][0], results["documents"][0])

documentation = "\\n\\n".join(
    f'<chunk id="{id}">\\n{text}\\n</chunk>' for id, text in found)
response = client.responses.create(
    model=MODEL,
    instructions=f"{INSTRUCTIONS}\\n\\nUse our documentation:\\n\\n{documentation}",
    input=question,
)`,
      highlights: [
        "Module 5's nearest-neighbour search: the **5 closest** chunks",
        '`where={"document": "user-guide.md"}`: only chunks whose metadata matches',
        'Each chunk keeps its id, so we can tell where an answer came from',
      ],
    },
  },
  {
    type: 'title',
    content: {
      title: 'Demo — Retrieve, then answer',
      subtitle: 'Switch to terminal: python demo/03_retrieve_and_answer.py',
      icon: 'rocket',
    },
  },
  {
    type: 'comparison',
    content: {
      title: 'Results',
      left: {
        label: 'The whole knowledge base in the prompt',
        items: [
          '191,548 tokens per question',
          '$0.0192 per question',
          '24.4 seconds',
          'The right answer',
        ],
      },
      right: {
        label: 'The top 5 chunks',
        items: [
          '906 tokens per question',
          '$0.0001 per question',
          '2.1 seconds',
          'Right chunks in the top 5 for **22 of 24** questions',
        ],
      },
    },
  },
  {
    type: 'code',
    content: {
      title: 'Why this breaks',
      code: `Q: Why does my Dormouse turn the heating on before the time I set?
   0.667  create-a-smart-home-heating-routine.md#leave-temperature-...
   0.633  create-a-smart-home-heating-routine.md#keep-temperature-...
   0.627  use-a-smart-plug-alongside-dormouse.md#use-dormouse-for-...
   0.611  use-a-smart-plug-alongside-dormouse.md#troubleshooting-...
   0.609  create-a-smart-home-heating-routine.md#troubleshoot-carefully
A: Dormouse may turn the heating on early so the room reaches the
   scheduled temperature by the time you set. Check the current
   target and schedule period in the app ...`,
      highlights: [
        'Our question is one of the two misses: Warm Wake came **sixth** (0.606)',
        'The customer says *before the time I set*; the guide says *starts the heating early*',
        'In 1,823 chunks, lots are about heating and schedules',
        'The vague first sentence is in none of the chunks: **a guess again**',
      ],
    },
  },

  // ---- Section 4: Share it ----
  {
    type: 'title',
    content: {
      title: '4. Share it: an MCP server',
      subtitle: 'One search for every assistant',
      icon: 'share',
    },
  },
  {
    type: 'standard',
    content: {
      title: 'One search, many copies',
      icon: 'layers',
      points: [
        'A person who missed would **search again**, in other words. Demo 3 searches once',
        'And demo 3 carries **its own copy** of the search: 89 lines',
        'The support chat, the website, staff tools and Claude would all need one',
        'Copies drift apart, and **answers start to disagree**',
        'Module 3: an **MCP server** offers tools to any client',
        'So put the search behind **one server**, and let every application ask it',
      ],
    },
  },
  {
    type: 'code',
    content: {
      title: 'The server',
      code: `server = MCPServer("dormouse-docs")

@server.tool()
def search_docs(query: str) -> str:
    """Search Dormouse's documentation by meaning ...
    Describe what to look for in \`query\`, in the words the
    documentation would use. Returns the five closest sections
    as JSON, closest first, each with an id to cite and its text."""
    db = open_database()
    update(db, [chunk for document in load_documents(DATA / "docs")
                for chunk in split_into_chunks(document)])
    [vector] = embed([query])
    ...  # demo 3's search`,
      highlights: [
        "Demo 3's search, behind **one tool**",
        "The docstring is the tool's **description**: all a client's model knows about it",
        'Checks the documents on every search, so an edit can be found at once',
      ],
    },
  },
  {
    type: 'code',
    content: {
      title: 'The model writes the search',
      code: `INSTRUCTIONS = """You are the support assistant for Dormouse ...
Search the documentation first, and answer only from what you
find. If the results don't answer the question, search again
with different words.
End each sentence that relies on the documentation with the id
of the section it came from, in square brackets."""

async with Client(DOCS_SERVER) as docs:
    tools = [... for tool in (await docs.list_tools()).tools]`,
      highlights: [
        "Demo 3 embedded the customer's words, once",
        'Now the model **chooses the words**, and can **search again**',
        "The agent asks the server for its tools, then runs Module 3's tool loop",
      ],
    },
  },
  {
    type: 'title',
    content: {
      title: 'Demo — Share it',
      subtitle: 'Switch to terminal: python demo/04_agent.py',
      icon: 'rocket',
    },
  },
  {
    type: 'code',
    content: {
      title: 'The model found Warm Wake',
      code: `Q: Why does my Dormouse turn the heating on before the time I set?
   search_docs("Thermostat starts heating before scheduled set time
     preheat early start learning warm-up schedule target temperature")
      0.683  user-guide.md#warm-wake
      0.629  understand-warm-wake.md#what-warm-wake-does
      0.627  heating-starts-below-five-degrees.md#if-the-room-is-...
A: Dormouse’s Warm Wake feature starts heating up to 90 minutes
   before a scheduled period ... you can turn it off in
   **Settings > Heating > Warm Wake**. [user-guide.md#warm-wake]
   1,056 tokens in, $0.0002, 4.7 seconds`,
      highlights: [
        "The model wrote **the documentation's words**: *preheat, early start*",
        'Warm Wake came **first**; demo 3 had it sixth',
        'The right answer: 90 minutes, how it learns, where to turn it off',
      ],
    },
  },
  {
    type: 'comparison',
    content: {
      title: 'We search, or the model searches',
      left: {
        label: 'Demo 3: we search',
        items: [
          "The customer's words, as they are",
          'Answer found for **22 of 24** questions',
          'Warm Wake 6th',
          '906 tokens, 2.1 seconds',
        ],
      },
      right: {
        label: 'Demo 4: the model searches',
        items: [
          'Words the model chooses: **1.1 searches** a question',
          'Answer found for **24 of 24** questions',
          'Warm Wake 1st',
          '1,056 tokens, 4.7 seconds: **two model calls**',
        ],
      },
    },
  },
  {
    type: 'code',
    content: {
      title: 'The same server in Claude',
      code: `claude mcp add dormouse-docs -- \\
    uv run --directory "$PWD" python demo/04_docs_server.py

{
  "mcpServers": {
    "dormouse-docs": {
      "command": "uv",
      "args": ["run", "--directory", "/full/path/to/module-06-...",
               "python", "demo/04_docs_server.py"]
    }
  }
}`,
      highlights: [
        '**Claude Code**: one command, from this folder',
        '**Claude Desktop**: the same command as JSON, in Settings > Developer',
        'Cursor, VS Code and others: the same command in their own settings',
        "**The server doesn't change**",
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'What MCP gives us',
      icon: 'plug',
      points: [
        '**One search, many applications**: improve it once, and every one gets it',
        "**The model writes the search**: the customer's words become the documentation's",
        '**The description is the contract**: a name, a description and arguments',
        "**A thin layer over what exists**: demo 3's code with a decorator on it",
      ],
    },
  },
  {
    type: 'description',
    content: {
      title: 'Why this breaks',
      icon: 'warning',
      description: `**Every question pays for the rewrite.** Two model calls instead of one: 4.7 seconds instead of 2.1. Customers ask in the same words every week, and the model works out the manual's words again every time.

        **Nothing checks what goes back.** The client writes the answer. And the server searches every document: across 24 customer questions it handed the model 3 internal sections, and one answer **cited an internal specification**.

        Start with the first. What if the documentation came with **the questions customers ask**, written once, ahead of time?`,
    },
  },

  // ---- Section 5: FAQs ----
  {
    type: 'title',
    content: {
      title: '5. FAQs',
      subtitle: 'The questions customers ask',
      icon: 'help-circle',
    },
  },
  {
    type: 'code',
    content: {
      title: 'Convert each document into an FAQ',
      code: `INSTRUCTIONS = """You turn documentation into the questions customers ask.
Convert this Dormouse document into an FAQ: every question
a customer might ask that it answers.
Write as many questions as it takes. There is no limit.
Write them as a customer who has never read the documentation
would type them into a chat window ...
Give each question the id of the chunk that answers it."""`,
      highlights: [
        '`data/build_faq.py`: **one document a call**, its chunks marked with their ids',
        '**7,987 questions** for 1,823 chunks: still about **4 a chunk**, and none for 37',
        'Done **once**. When a document changes, it is converted again',
      ],
    },
  },
  {
    type: 'code',
    content: {
      title: 'The questions for Warm Wake',
      code: `user-guide.md#warm-wake:
   What does Warm Wake do?
   Why does the heating start before the scheduled time?
   How early can Warm Wake start heating?
   How does Warm Wake know when to start heating?
   What does the sunrise symbol mean when Warm Wake is running?
   Is Warm Wake on by default?
   How do I turn Warm Wake off?
   What happens to heating times when Warm Wake is off?`,
      highlights: [
        '**Eight** questions. With a limit of 3 to 5, it wrote four',
        "The second is **nearly the customer's question**",
        'The section itself never says anything like it',
      ],
    },
  },
  {
    type: 'code',
    content: {
      title: 'Chroma metadata',
      code: `question_store.get(ids=["user-guide.md#warm-wake?1"],
    include=["embeddings", "documents", "metadatas"])

id:        user-guide.md#warm-wake?1
embedding: [-0.0479, 0.0298, -0.0241, ...]   1,536 numbers
document:  Why does the heating start before the scheduled time?
metadata:  {"chunk": "user-guide.md#warm-wake",
            "checksum": "e6d70af51bff01e2..."}`,
      highlights: [
        'Each record: an **id**, a **vector**, the **text**, and **metadata**, a dictionary of facts about it',
        '`chunk`: the chunk that answers the question. **That chunk** is what the model gets',
        '`checksum`: of the chunk and its questions. Change either, and they are embedded again',
        '`where={"chunk": "user-guide.md#warm-wake"}`: all **8** of its questions',
      ],
    },
  },
  {
    type: 'code',
    content: {
      title: 'Search the questions too',
      code: `results = question_store.query(
    query_embeddings=[vector], n_results=20,
    include=["distances", "documents", "metadatas"],
)
for distance, question, metadata in zip(...):
    chunk = metadata["chunk"]
    best[chunk] = max(best.get(chunk, 0), 1 - distance)`,
      highlights: [
        "Search chunks and questions with the **customer's own words**",
        'Each question found leads, through its metadata, to **its chunk**',
        "Keep each chunk's best match, and send the top 5 **chunks**, as in demo 3",
        '**One model call**: the rewriting was done ahead of time',
      ],
    },
  },
  {
    type: 'title',
    content: {
      title: 'Demo — FAQs',
      subtitle: 'Switch to terminal: python demo/05_faq.py',
      icon: 'rocket',
    },
  },
  {
    type: 'code',
    content: {
      title: 'Lost among the questions',
      code: `Q: Why does my Dormouse turn the heating on before the time I set?
   0.771  create-a-smart-home-heating-routine.md#leave-...
            via "Where do I change my Dormouse heating schedule?"
   0.771  coordinate-radiator-valves-with-smart-home-routines.md#...
            via "Where do I change my Dormouse heating schedule?"
   ...
   0.714  android-app-notifications-screen-guide.md#heating-...
            via "When does Dormouse send the heating-while-away ..."
A: Dormouse follows your schedule, where each period’s temperature
   stays in effect until the next period starts. If heating comes
   on earlier than you expect, check the current target ...`,
      highlights: [
        'The top two: **the same question**, written for two chunks',
        "Warm Wake came **eighth** (0.707), through a release note's question",
        'The answer never mentions Warm Wake: **a guess again**',
      ],
    },
  },
  {
    type: 'three-way',
    content: {
      title: 'Answer in what was found',
      columns: [
        {
          label: 'Demo 3: chunks',
          items: ['**22 of 24**', 'Missed Q01 and Q11', '1 model call'],
        },
        {
          label: 'Demo 4: the model searches',
          items: ['**24 of 24**', 'Missed none', '2 or more model calls'],
        },
        {
          label: 'Demo 5: chunks and questions',
          items: [
            '**23 of 24**',
            'Missed Q06',
            '1 model call, 6,358 questions written ahead',
          ],
        },
      ],
    },
  },
  {
    type: 'description',
    content: {
      title: 'Why this breaks',
      icon: 'warning',
      description: `**Questions that sound alike.** Q06, *"How many people in my family can control the heating?"*, matched *"How many thermostats and heating zones can I have in my home?"*. "How many" and "heating" were enough. Searching the chunks alone had found it.

        **Finding the chunk isn't checking the answer.** Every count so far asks whether the right chunk was found, not whether the answer came from it. Demo 3's first sentence was in none of its chunks.

        What if the model had to **show where each sentence came from**, and we checked?`,
    },
  },

  // ---- Section 6: Citations ----
  {
    type: 'title',
    content: {
      title: '6. Citations',
      subtitle: 'Show the source, and check it',
      icon: 'check-square',
    },
  },
  {
    type: 'code',
    content: {
      title: 'Stricter instructions',
      code: `Use only the documentation below, never what you know
from elsewhere.
Quote, word for word, each sentence you rely on, with the
id of the chunk it comes from.
If the documentation does not answer the question, set
answered to false and say so. Do not guess.`,
      highlights: [
        '**Only** the documentation',
        "**Quote** it, with the chunk's id",
        "Say when it **doesn't answer**",
        'The same search as demo 3: only the instructions and the check change',
      ],
    },
  },
  {
    type: 'code',
    content: {
      title: 'A fixed shape, and a check',
      code: `text={"format": {"type": "json_schema", "name": "answer",
                 "schema": SCHEMA, "strict": True}}
# {"answered": ..., "answer": ...,
#  "citations": [{"chunk": ..., "quote": ...}]}

def check(citations, found):
    texts = {c["id"]: words(c["text"]) for c in found}
    return [{**c, "checked": words(c["quote"])
             in texts.get(c["chunk"], "")} for c in citations]`,
      highlights: [
        '**Structured outputs**: the reply is JSON that matches a schema',
        '`answered`: true or false, so code can tell a refusal',
        'A quote counts only if it **is in the chunk it cites**',
      ],
    },
  },
  {
    type: 'title',
    content: {
      title: 'Demo — Citations',
      subtitle: 'Switch to terminal: python demo/06_citations.py',
      icon: 'rocket',
    },
  },
  {
    type: 'code',
    content: {
      title: 'Honest, and checked',
      code: `Q: Why does my Dormouse turn the heating on before the time I set?
A: The documentation doesn’t explain why Dormouse might turn
   the heating on before a scheduled time.

Q: How much does a Dormouse thermostat cost?
A: The documentation does not provide the Dormouse Thermostat’s price.

Of 24 questions the documentation answers: answered right 19,
  answered wrong 4, said it didn't know 1
Of 5 questions it doesn't: said it didn't know 5
Quotes found in the chunk they cite: 57 of 57`,
      highlights: [
        "Demo 3 **guessed** our question. Now: *the documentation doesn't explain*",
        "All **5** questions it can't answer: turned down",
        'Every quote is really in its chunk. In an earlier run, one of 60 was **tidied**, and caught',
      ],
    },
  },
  {
    type: 'code',
    content: {
      title: 'The quote has it, the answer doesn’t',
      code: `Q: Can I have a separate thermostat for upstairs?
A: Yes. You can use a separate thermostat to control upstairs
   as its own zone and schedule. ...
   [thermostat-valve-and-sensor-zone-planning.md#choose-the-zones]
   "A home can have up to four thermostats, each controlling its
    own zone with its own schedule." (quote checked)`,
      highlights: [
        'The quote says **up to four**. The answer leaves it out',
        'Q22 the same: the quote says *AA batteries*, the answer *the batteries*',
        "Q11 explains Away mode, when it's **geofencing** that turns it on",
      ],
    },
  },
  {
    type: 'description',
    content: {
      title: 'Why this breaks',
      icon: 'warning',
      description: `**"I don't know" is only as good as the search.** Our question was turned down because the search missed Warm Wake. Sections 4 and 5 found it.

        **A real quote can still give a poor answer.** All four wrong answers passed the check.

        **We can only check the answers we write.** Behind the MCP server, the client writes them.

        **No search here asks who is asking.** In demo 4, an answer to a customer cited an internal specification. Who may see what, enforced in code: **Module 8**.`,
    },
  },

  // ---- Wrap-up ----
  {
    type: 'title',
    content: {
      title: 'Wrap-up',
      subtitle: 'Answering from your own documents',
      icon: 'check',
    },
  },
  {
    type: 'standard',
    content: {
      title: 'What we built',
      icon: 'blocks',
      points: [
        '**Just ask**: confident, and made up',
        '**Documents in the prompt**: right, for 191,548 tokens a question',
        "**Retrieve, then answer**: 906 tokens, but the customer's words miss",
        '**An MCP server**: the model writes the search, in two calls a question',
        '**FAQs**: questions written once, but more questions crowded out the right one',
        '**Citations**: checked quotes and honest refusals, only as good as the search',
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'What we learned',
      icon: 'award',
      points: [
        "A model makes up what it hasn't seen: **hallucination**",
        '**RAG**: retrieve the chunks that matter, then answer from them',
        'A **vector database** stores chunks once, with metadata to filter by',
        'Most misses are **search** misses: measure what was found, not just the answer',
        'Make the model **cite**, and check the citations in code',
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'Final exercise: further reading',
      icon: 'book',
      points: [
        '**Lewis et al. (2020)**: the paper that named RAG',
        '**Nogueira et al. (2019)**: doc2query, documents turned into questions',
        '**Gao et al. (2023)**: scoring citations',
        'Pick a paper, connect it to a demo, then start an extension',
        'Everything is in `further-reading/`',
      ],
    },
  },
];
