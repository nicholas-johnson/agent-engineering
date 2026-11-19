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
      title: 'Module 5 — Embeddings and Vector Search',
      subtitle: 'Finding the right test by meaning',
      icon: 'search',
    },
  },
  {
    type: 'description',
    content: {
      title: 'The question',
      icon: 'question',
      description:
        "A library of **1,000 manual test scripts**. A bug report: *customers can't sign in after resetting their password*. The fix ships in ten minutes, on Android. **Which test do we run?**",
    },
  },
  {
    type: 'code',
    content: {
      title: 'The data',
      code: `{
  "id": "TS-1042",
  "title": "Log in with the new password after a password reset",
  "platform": "android",
  "component": "accounts",
  "priority": "high",
  "minutes": 5,
  "preconditions": "A Dormouse account whose password has just been ...",
  "steps": ["Open the Dormouse app.", "Enter the account's email ...", ...],
  "expected": "The new password opens the home screen ..."
}`,
      highlights: [
        '**Dormouse**: a smart thermostat, invented for this course',
        '20 scripts written by hand, 980 more written by `gpt-6-luna`',
        'Platforms: `android`, `ios`, `web` and `device`',
      ],
    },
  },

  // ---- Section 1: Keyword search ----
  {
    type: 'title',
    content: {
      title: '1. Keyword search',
      subtitle: 'Score the words in common',
      icon: 'search',
    },
  },
  {
    type: 'code',
    content: {
      title: 'BM25',
      code: `for word in set(words(request)):
    if word not in counts:
        continue
    rarity = math.log(1 + (len(documents) - appears_in[word] + 0.5)
                          / (appears_in[word] + 0.5))
    count = counts[word]
    score += rarity * count * (K1 + 1) / (
        count + K1 * (1 - B + B * len(document) / average_length))`,
      highlights: [
        '**Rare words count for more**: "resetting" beats "password"',
        'Repeats help, but less and less (`K1`)',
        "Long scripts don't win just by being long (`B`)",
        'Used by Elasticsearch, OpenSearch and SQLite',
      ],
    },
  },
  {
    type: 'title',
    content: {
      title: 'Demo — Keyword search',
      subtitle: 'Switch to terminal: python demo/01_keyword_search.py',
      icon: 'rocket',
    },
  },
  {
    type: 'code',
    content: {
      title: 'Why this breaks',
      code: `=== 20 test scripts ===
   7.72  TS-1076  android  Sign-in screen layout
   4.33  TS-1311  android  Account recovery regression: every way ...
   4.03  TS-1042  android  Log in with the new password after a password reset

=== 1,000 test scripts ===
  11.04  TS-1879  android  Handle an expired password during sign-in
  10.25  TS-1047  ios      Preserve sign-in email after a password error
  10.06  TS-1955  web      Prevent password disclosure in browser history`,
      highlights: [
        'First: a 3-minute check of the screen layout. It says "sign in" twice',
        'The right script says **log in**, not sign in',
        'In 1,000 scripts it falls out of the top three',
        'Keyword search matches **words, not meaning**',
      ],
    },
  },

  // ---- Section 2: Embeddings ----
  {
    type: 'title',
    content: {
      title: '2. Embeddings',
      subtitle: 'Meaning as numbers',
      icon: 'layers',
    },
  },
  {
    type: 'standard',
    content: {
      title: 'What is an embedding?',
      icon: 'layers',
      points: [
        'A **vector**: a list of numbers that stands for a piece of text',
        'Trained so that texts that **mean** similar things point in similar directions',
        'Module 1: 16 numbers per token, and *mouse* ended up near *queen*',
        '`text-embedding-3-small`: **1,536 numbers** for a whole passage',
        'Search by meaning = find the nearest vectors',
      ],
    },
  },
  {
    type: 'code',
    content: {
      title: 'Embedding text',
      code: `response = client.embeddings.create(
    model="text-embedding-3-small",
    input=texts,
)
vectors = [item.embedding for item in response.data]`,
      highlights: [
        'Not the Responses API: a separate **embeddings** endpoint',
        'Many texts per call: we send 100 at a time',
        'All 1,000 scripts: 32,025 tokens, **less than a tenth of a cent**',
      ],
    },
  },
  {
    type: 'equation',
    content: {
      title: 'Cosine similarity',
      mathml: `<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
  <mtext>similarity</mtext>
  <mo>=</mo>
  <mfrac>
    <mrow><mi>a</mi><mo>·</mo><mi>b</mi></mrow>
    <mrow><mo>|</mo><mi>a</mi><mo>|</mo><mspace width="0.2em"/><mo>|</mo><mi>b</mi><mo>|</mo></mrow>
  </mfrac>
</math>`,
      points: [
        'How closely two vectors **point the same way**',
        '1 means the same direction, 0 means unrelated',
        'Only meaningful compared with other similarities',
      ],
    },
  },
  {
    type: 'code',
    content: {
      title: 'What to embed',
      code: `def what_it_tests(script):
    return f"{script['title']}. {script['expected']}"`,
      highlights: [
        'The title and expected result say **what the test checks**',
        'Our request: embed the whole script, and the right one drops from 1st to 4th',
        "All 20 requests, on each one's platform: **a draw**, 18 each. Measure it",
      ],
    },
  },
  {
    type: 'title',
    content: {
      title: 'Demo — Embeddings',
      subtitle: 'Switch to terminal: python demo/02_embeddings.py',
      icon: 'rocket',
    },
  },
  {
    type: 'code',
    content: {
      title: 'By meaning',
      code: `Request: Customers can't sign in after resetting their password
As 1,536 numbers: [0.0235, -0.0048, 0.0286, -0.0008, ...]

=== 1,000 test scripts ===
  0.511  TS-1042  android  Log in with the new password after a password reset
  0.511  TS-1187  ios      Log in with the new password after a password reset
  0.485  TS-1047  ios      Preserve sign-in email after a password error`,
      highlights: [
        'The right script is **first**, in both libraries',
        'It shares only "after" and "password" with the request',
      ],
    },
  },
  {
    type: 'description',
    content: {
      title: 'Why this breaks',
      icon: 'warning',
      description:
        'TS-1042 is **tied with TS-1187**, the same test on iOS. In the small library, third place is a **40-minute** regression suite. The bug is on Android and the fix ships in ten minutes: **it ignores the criteria**. And every run embeds the whole library again.',
    },
  },

  // ---- Section 3: A vector database ----
  {
    type: 'title',
    content: {
      title: '3. A vector database',
      subtitle: 'Store once, filter, search',
      icon: 'database',
    },
  },
  {
    type: 'code',
    content: {
      title: 'A table of vectors',
      code: `db.execute(
    "create virtual table if not exists scripts using vec0("
    "id text primary key, embedding float[1536] distance_metric=cosine,"
    "platform text, minutes integer, +title text, +checksum text)"
)`,
      highlights: [
        '**sqlite-vec**: vector search inside SQLite, in one file',
        'One row per script: its vector, and columns to **filter on**',
        '`+` columns are just carried along',
      ],
    },
  },
  {
    type: 'code',
    content: {
      title: 'Searching is SQL',
      code: `select id, 1 - distance, platform, minutes, title from scripts
where embedding match ? and k = 3
  and platform = ? and minutes <= ?
order by distance`,
      highlights: [
        '`k = 3`: the three nearest vectors',
        'The criteria are ordinary `where` clauses',
        'Filters apply **during** the search, so you still get three',
      ],
    },
  },
  {
    type: 'code',
    content: {
      title: 'Embed once',
      code: `stored = dict(db.execute("select id, checksum from scripts"))
changed = [s for s in scripts if stored.get(s["id"]) != checksums[s["id"]]]

# First run:   Embedded 1,000 new or changed scripts into test-scripts.db
# Second run:  Embedded 0 new or changed scripts into test-scripts.db`,
      highlights: [
        'A checksum of the embedded text, stored in each row',
        'Only new or changed scripts are embedded',
        'Nothing is retrained: the rows change, the model never does',
      ],
    },
  },
  {
    type: 'title',
    content: {
      title: 'Demo — A vector database',
      subtitle: 'Switch to terminal: python demo/03_vector_database.py',
      icon: 'rocket',
    },
  },
  {
    type: 'code',
    content: {
      title: 'With criteria',
      code: `Request: Customers can't sign in after resetting their password
Criteria: android, at most 10 minutes
  0.511  TS-1042  android   5 min  Log in with the new password after ...
  0.473  TS-1879  android   5 min  Handle an expired password during sign-in
  0.443  TS-1887  android   3 min  Reject an incorrect password`,
      highlights: [
        'The iOS twin and the 40-minute suite are gone',
        'Everything shown runs on Android in ten minutes',
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'Every vector, or an index?',
      icon: 'database',
      points: [
        'sqlite-vec compares the request with **every** vector',
        '1,000 vectors: about **3 milliseconds**, and a 6.5 MB file',
        'Millions of vectors: build an **index** (usually **HNSW**)',
        'An index checks a small fraction, and very occasionally misses',
        'pgvector, Qdrant, Chroma, Pinecone, OpenSearch…',
      ],
    },
  },
  {
    type: 'code',
    content: {
      title: 'Why this breaks',
      code: `Request: The thermostat's display shows E-104
  0.699  TS-1474  device   5 min  Check missed Wi-Fi network error
  0.692  TS-1370  device   5 min  Check low backup battery warning
  0.688  TS-1845  device   5 min  Check E-217 sensor error on the display`,
      highlights: [
        'E-104 is the pairing timeout. **None of these is about E-104**',
        'The vector says "an error code on the display", not which one',
        'Embeddings **blur exact identifiers**: codes, part numbers, IDs, names',
      ],
    },
  },

  // ---- Section 4: Hybrid search ----
  {
    type: 'title',
    content: {
      title: '4. Hybrid search',
      subtitle: 'Words and meaning together',
      icon: 'blocks',
    },
  },
  {
    type: 'comparison',
    content: {
      title: 'Two kinds of search',
      left: {
        label: 'Keywords (BM25)',
        items: [
          'Exact words, codes and names',
          'Blind to meaning',
          'Built into SQLite: **FTS5**',
        ],
      },
      right: {
        label: 'Vectors',
        items: ['Meaning, in any words', 'Blurs exact identifiers', 'sqlite-vec'],
      },
    },
  },
  {
    type: 'code',
    content: {
      title: 'Reciprocal rank fusion',
      code: `def hybrid(*rankings):
    scores = Counter()
    for ranking in rankings:
        for rank, id in enumerate(ranking, 1):
            scores[id] += 1 / (60 + rank)
    return [id for id, _ in scores.most_common()]`,
      highlights: [
        'Each search returns its top 20',
        'A script scores `1 / (60 + rank)` in every list it appears in',
        'Ranks only, so the two kinds of score never need comparing',
      ],
    },
  },
  {
    type: 'title',
    content: {
      title: 'Demo — Hybrid search',
      subtitle: 'Switch to terminal: python demo/04_hybrid_search.py',
      icon: 'rocket',
    },
  },
  {
    type: 'code',
    content: {
      title: 'Two requests',
      code: `Request: Customers can't sign in after resetting their password (android)
  TS-1879  Handle an expired password during sign-in
  TS-1887  Reject an incorrect password
  TS-1076  Sign-in screen layout
  TS-1073  Sign out and return to the signed-in account
  TS-1042  Log in with the new password after a password reset

Request: The thermostat's display shows E-104 (device)
  TS-1026  Check sensor readings during pairing timeout
  TS-1845  Check E-217 sensor error on the display
  ...`,
      highlights: [
        'E-104 is now first: TS-1026 covers the pairing timeout',
        'But the password test has slipped from **first to fifth**',
      ],
    },
  },
  {
    type: 'code',
    content: {
      title: 'Measure it',
      code: `A right script in the top 5, for 20 requests:
  keyword 12, vector 18, hybrid 15

Requests                  Keyword   Vector   Hybrid
14 in everyday words            6       12        9
6 quoting an error code         6        6        6`,
      highlights: [
        '`data/requests.json`: 20 requests with known right answers',
        '**Hybrid search did worse than vectors alone**',
      ],
    },
  },
  {
    type: 'description',
    content: {
      title: 'Why hybrid lost',
      icon: 'scale',
      description:
        '*"What happens when someone tries to add more rooms than allowed?"* Vectors ranked the right script **3rd**; keywords never found it. Hybrid put *"Reject a seventh daily schedule period"* first: 11th for keywords **and** 14th for vectors. Two lukewarm votes (1/71 + 1/74 = 0.0276) beat one strong one (1/63 = 0.0159).',
    },
  },
  {
    type: 'standard',
    content: {
      title: 'Measure, with your own requests',
      icon: 'ruler',
      points: [
        'Hybrid helps when people search with **exact terms**: part numbers, ticket IDs, names',
        'It hurts when the keyword side is **noise**',
        'Keep a set of real requests with known answers',
        'Check every change against it',
        "Don't tune on the same requests you measure with",
      ],
    },
  },
  {
    type: 'description',
    content: {
      title: 'Why this breaks',
      icon: 'warning',
      description:
        "Every search here ranks by **similarity**: shared words, or nearby vectors. None of them can judge **fit**. Does this script test what broke? Can it run before the hotfix ships? And people don't type search queries: **they paste bug reports**.",
    },
  },

  // ---- Section 5: A search tool ----
  {
    type: 'title',
    content: {
      title: '5. A search tool',
      subtitle: 'Let the agent search',
      icon: 'robot',
    },
  },
  {
    type: 'code',
    content: {
      title: 'The search, as an MCP tool',
      code: `@server.tool()
def find_test_scripts(
    request: str,
    platform: Literal["android", "ios", "web", "device"],
    max_minutes: int,
) -> str:
    """Search Dormouse's library of 1,000 manual test scripts by meaning.
    In \`request\`, describe the behaviour to test in a few plain words,
    like a test's title ... Returns the five closest scripts as JSON."""`,
      highlights: [
        'Vectors and filters: **the best we measured**',
        '`Literal`: the model can only ask for a real platform',
        "The agent is Module 3's tool loop, unchanged",
      ],
    },
  },
  {
    type: 'title',
    content: {
      title: 'Demo — A search tool',
      subtitle: 'Switch to terminal: python demo/05_agent.py',
      icon: 'rocket',
    },
  },
  {
    type: 'code',
    content: {
      title: 'From bug report to test',
      code: `You: Support say that since this morning's release, customers on Android
     who reset their password can't get back into the app. The hotfix
     ships in ten minutes. Which test should we run?
  [tool] find_test_scripts({"request":"Android user logs in after resetting
         password","platform":"android","max_minutes":10})
         -> TS-1042 Log in with the new password after a password reset
         -> TS-1548 Check password entry with Android autofill
         -> ...
Agent: Run TS-1042, "Log in with the new password after a password reset."
       It's the closest match to the reported Android failure, takes five
       minutes, and verifies that the new password works while the old one
       is rejected.`,
      highlights: [
        '**Criteria** from the bug report: Android, ten minutes',
        'Its **own search**, short and to the point',
        'It **judged** five scripts and picked one',
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'The words matter',
      icon: 'file',
      points: [
        'An earlier tool description said "describe what needs testing in plain words"',
        'The agent searched for *"Verify Android password reset flow and confirm users can sign back into the app afterward, focusing on regression after a release/hotfix"*',
        "Five near misses, and a recommendation it admitted didn't fit",
        'Now: "a few plain words, like a test\'s title", and **search again if nothing fits**',
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'What MCP gives you in practice',
      icon: 'plug',
      points: [
        '**One search, many front ends**: our agent, Claude, Claude Code, Cursor, VS Code',
        'A tester asks for the right test without leaving their editor',
        "**Wrap your system, don't rebuild it**: call your test management API, not a JSON file",
        '**Criteria stay exact**: the model fills in arguments, the database applies them',
      ],
    },
  },
  {
    type: 'description',
    content: {
      title: 'Why this breaks',
      icon: 'warning',
      description:
        'The agent finds the right **test**. But many questions need an **answer**: *"What does E-104 mean, and what should support tell the customer?"* That is written in the product\'s **documentation**, and the model has never read it. Next: **Module 6, RAG**.',
    },
  },

  // ---- Wrap-up ----
  {
    type: 'title',
    content: {
      title: 'Wrap-up',
      subtitle: 'Finding by meaning',
      icon: 'check',
    },
  },
  {
    type: 'standard',
    content: {
      title: 'What we built',
      icon: 'blocks',
      points: [
        '**Keyword search** — shared words, not meaning',
        '**Embeddings** — the right script, on the wrong platform too',
        '**A vector database** — stored once and filtered, but blurs error codes',
        '**Hybrid search** — measured, and worse than vectors alone here',
        '**A search tool** — the agent searches, reads and judges',
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'What we learned',
      icon: 'award',
      points: [
        'An **embedding** turns text into a vector; close vectors, similar meaning',
        '**What you embed** changes what you find: measure it',
        'A **vector database** stores vectors with columns to filter on',
        "**Measure** search with real requests: the usual advice isn't always right",
        'A model can turn a messy request into a search, and **judge** the results',
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'Final exercise: further reading',
      icon: 'book',
      points: [
        '**Spärck Jones (1972)** — why rare words count for more',
        '**Reimers & Gurevych (2019)** — one vector for a whole sentence',
        '**Bruch et al. (2023)** — why our hybrid search lost',
        'Pick a paper, connect it to a demo, then start an extension',
        'Everything is in `further-reading/`',
      ],
    },
  },
];
