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

  // ---- Sections 4 to 6 (FAQs, citations, keeping it current) go here ----

  // ---- Section 7: Share it ----
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
        'Demos 3 to 6 each carry **their own copy** of the search: 89 lines in demo 3',
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
      subtitle: 'Switch to terminal: python demo/07_agent.py',
      icon: 'rocket',
    },
  },
  {
    type: 'code',
    content: {
      title: 'The model found Warm Wake',
      code: `Q: Why does my Dormouse turn the heating on before the time I set?
   search_docs("thermostat heating starts before scheduled time
     set; early start, preheat, learns how long home takes to
     warm to target temperature")
      0.684  user-guide.md#warm-wake
      0.623  set-a-heating-schedule.md#before-you-start
      0.622  understand-warm-wake.md#what-warm-wake-does
A: Dormouse’s Warm Wake feature starts heating early so your
   home reaches the scheduled target temperature ... may start
   up to 90 minutes early ... [user-guide.md#warm-wake]
   1,063 tokens in, $0.0002, 5.6 seconds`,
      highlights: [
        "The model wrote **the documentation's words**: *early start, preheat*",
        'Warm Wake came **first**; demo 3 had it sixth',
        'The right answer: 90 minutes, the sunrise symbol, where to turn it off',
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
        label: 'Demo 7: the model searches',
        items: [
          'Words the model chooses: **1.2 searches** a question',
          'Answer found for **24 of 24** questions',
          'Warm Wake 1st',
          '1,063 tokens, 5.6 seconds: **two model calls**',
        ],
      },
    },
  },
  {
    type: 'code',
    content: {
      title: 'The same server in Claude',
      code: `claude mcp add dormouse-docs -- \\
    uv run --directory "$PWD" python demo/07_docs_server.py

{
  "mcpServers": {
    "dormouse-docs": {
      "command": "uv",
      "args": ["run", "--directory", "/full/path/to/module-06-...",
               "python", "demo/07_docs_server.py"]
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
    type: 'code',
    content: {
      title: 'Why this breaks',
      code: `Q: What's the coldest I can set the thermostat to?
A: The coldest target temperature you can set is 5°C. The
   thermostat’s frost protection is always on and will turn
   the heating on if the room drops below 5°C.
   [thermostat-physical-and-environmental-limits.md#indoor-...]
   [thermostat-electrical-safety-policy.md#limits-and-safety-...]`,
      highlights: [
        'The first source is an **internal** specification',
        '5 internal sections reached the model, across 24 customer questions',
        "No sign-in: the server **can't tell who is asking**",
        'Nothing checks the quotes now: the client writes the answer',
        'Who may see what, enforced in code: **Module 8**',
      ],
    },
  },
];
