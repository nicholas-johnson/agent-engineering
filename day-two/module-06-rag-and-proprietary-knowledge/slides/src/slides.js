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
        "A customer writes in: *why does my Dormouse turn the heating on before the time I set?* The answer is in our documentation. The model has never read our documentation. **How do we get it to answer from our documents, and only from them?**",
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
        '**Dormouse**: the thermostat from Module 5, now with its documentation',
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
        "**Embed** every chunk and store it: Module 5's vector database",
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
        'A checksum per chunk: a rerun only embeds what changed',
      ],
    },
  },
  {
    type: 'code',
    content: {
      title: 'Retrieve, then answer',
      code: `rows = db.execute(
    """select id, 1 - distance, text from chunks
       where embedding match ? and k = 5
       order by distance""",
    (sqlite_vec.serialize_float32(vector),),
)

documentation = "\\n\\n".join(
    f'<chunk id="{c["id"]}">\\n{c["text"]}\\n</chunk>' for c in found)
response = client.responses.create(
    model=MODEL,
    instructions=f"{INSTRUCTIONS}\\n\\nUse our documentation:\\n\\n{documentation}",
    input=question,
)`,
      highlights: [
        'The same search as Module 5',
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
        items: ['191,548 tokens per question', '$0.0192 per question', '24.4 seconds', 'The right answer'],
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
];
