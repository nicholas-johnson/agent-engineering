# Module 5 — Embeddings and Vector Search

> A test team has a library of 1,000 manual test scripts, and a bug report: customers can't sign in after resetting their password. Which test should they run? We search the library five ways. Keyword search finds scripts that share the request's words, not the one that tests the problem. **Embeddings** turn text into vectors so that "means the same" becomes "is close together", and the right script comes first, along with the same test for the wrong platform. A **vector database** stores the vectors once and filters by the criteria, but blurs exact error codes. **Hybrid search** combines keywords and vectors, and on our requests, measured, it does worse than vectors alone. Finally we give the search to an agent as an MCP tool: it turns a bug report into a search, reads the five closest scripts and picks the best fit.

## Learning goals

- Explain **keyword search** and how **BM25** scores a document: matching words, rare words counting for more.
- Explain what an **embedding** is, and compare two with **cosine similarity**.
- Call an **embeddings model** and search a library by meaning.
- Store vectors in a **vector database**, update only what has changed, and **filter** by criteria such as platform and run time.
- Combine keyword and vector search into **hybrid search** with **reciprocal rank fusion**, and **measure** whether it helps.
- Expose a search to an agent as an **MCP tool**, and say what MCP gives you in practice.

---

## The idea: search by meaning

A request and the test that answers it often share almost no words. "Customers can't sign in after resetting their password" is answered by a script called "Log in with the new password after a password reset": *sign in* versus *log in*, *resetting* versus *reset*. Keyword search sees different words. A person sees the same problem.

An **embedding** is a list of numbers (a **vector**) that stands for a piece of text. An embeddings model is trained so that texts that mean similar things get vectors pointing in similar directions. Searching by meaning is then just arithmetic: turn the request into a vector, and find the scripts whose vectors are closest.

You have seen this before. In Module 1, the neural language model learned a vector of 16 numbers for each token, and arranged them so that *mouse* and *queen* (characters who say things) ended up close together. An embeddings model is the same idea, grown up: 1,536 numbers, and a vector for a whole passage rather than one token.

## The data

Everything runs on a library of manual test scripts for **Dormouse**, a smart thermostat with Android and iOS apps, a web dashboard and the thermostat itself. **Dormouse and every test script are invented for this course.** Your own test library would work the same way.

| File | What | Size |
|------|------|------|
| `data/test-scripts-small.json` | Written by hand: the scripts the demos are built around, and the ones that compete with them | 20 scripts |
| `data/test-scripts.json` | The 20 above, plus 980 written by `gpt-6-luna` with `data/build_test_scripts.py` | 1,000 scripts |
| `data/requests.json` | 20 requests with the scripts that count as right, for measuring search | 20 requests |

Each script has an ID, a title, a platform (`android`, `ios`, `web` or `device`), a component, a priority, a time to run in minutes, preconditions, steps and an expected result:

```json
{
  "id": "TS-1042",
  "title": "Log in with the new password after a password reset",
  "platform": "android",
  "component": "accounts",
  "priority": "high",
  "minutes": 5,
  "preconditions": "A Dormouse account whose password has just been changed using the emailed link. The app is installed and logged out.",
  "steps": ["Open the Dormouse app.", "Enter the account's email address and the new password.", "Tap Log in.", "Log out, then try to log in again with the old password."],
  "expected": "The new password opens the home screen with the account's thermostats. The old password is refused with 'Incorrect email or password'."
}
```

The large library has 277 device scripts, 272 Android, 268 iOS and 183 web, across twelve components. The model wrote its 980 in about two and a half minutes. Rerunning `build_test_scripts.py` writes a different library, so the numbers below would change.

Of the 20 requests in `requests.json`, 14 describe a problem in everyday words, deliberately not the scripts' words ("Holding the knob down for a while makes the temperature jump"). The other 6 quote an error code from the display ("E-104 came up while setting up a new thermostat"). For an everyday request, one script counts as right. For an error code, any script for the thermostat that mentions the code counts.

## Setting up

You need `OPENAI_API_KEY` in `.env` (see Module 2). This module adds one package, `sqlite-vec`, a vector search extension for SQLite. `uv` installs it with everything else.

## Running the demos

From this folder:

```bash
uv run python demo/01_keyword_search.py
```

| Demo | What it is | Writes |
|------|------------|--------|
| `01_keyword_search.py` | BM25 keyword search, in plain Python | `01_keyword_search.json`: the top ten for each library |
| `02_embeddings.py` | Embed every script and search by cosine similarity | `02_embeddings.json`: the request's vector and the top ten |
| `03_vector_database.py` | Store the vectors in SQLite with sqlite-vec, and filter | `test-scripts.db`, `03_vector_database.json` |
| `04_hybrid_search.py` | Keyword and vector search together, measured on 20 requests | `04_hybrid_search.json`: every request's top five, three ways |
| `05_search_server.py` | An MCP server with a `find_test_scripts` tool | `test-scripts.db` |
| `05_agent.py` | An agent that starts the server and uses it | `05_agent.json`: the whole conversation |

Demos 2 to 5 call OpenAI's embeddings API. Embedding the whole library is 32,025 tokens, which costs less than a tenth of a cent at $0.02 per million tokens ([OpenRouter's price list](https://openrouter.ai/api/v1/embeddings/models), checked 18 November 2026). Demos 1 to 4 give the same results every time; the agent's words differ from run to run.

---

## 1. Keyword search

**Demo:** `demo/01_keyword_search.py`

The oldest way to search: score each script by the words it shares with the request. **BM25** ("Best Match 25") is the standard scoring, used by Elasticsearch, OpenSearch and SQLite's full-text search. For each word in the request that a script contains, it adds:

```python
rarity = math.log(1 + (len(documents) - appears_in[word] + 0.5) / (appears_in[word] + 0.5))
score += rarity * count * (K1 + 1) / (count + K1 * (1 - B + B * len(document) / average_length))
```

Three ideas are packed in there:

- **Rare words count for more.** "password" is in a lot of scripts; "resetting" is in few. The rarity term is large for words that appear in few scripts.
- **Repeats help, but less and less.** The second "password" adds less than the first. `K1` (1.5) controls how fast it levels off.
- **Long scripts don't win just by being long.** `B` (0.75) scales the count down for scripts longer than average.

The text searched is the whole script: title, preconditions, steps and expected result.

```text
=== test-scripts-small.json: 20 test scripts ===
Request: Customers can't sign in after resetting their password
   7.72  TS-1076  android  Sign-in screen layout
   4.33  TS-1311  android  Account recovery regression: every way back into a locked account
   4.03  TS-1042  android  Log in with the new password after a password reset

=== test-scripts.json: 1,000 test scripts ===
Request: Customers can't sign in after resetting their password
  11.04  TS-1879  android  Handle an expired password during sign-in
  10.25  TS-1047  ios      Preserve sign-in email after a password error
  10.06  TS-1955  web      Prevent password disclosure in browser history
```

In the small library the winner is "Sign-in screen layout", a three-minute check that the screen has a logo, two fields and a button. It says "sign in" twice and "password" three times. The right script, TS-1042, is third. In the large library it isn't in the top three at all: plenty of scripts say "sign in" and "password".

**Why this breaks:** keyword search matches **words, not meaning**. The script that answers the request says "log in", not "sign in". Every extra script that happens to share words with the request is another chance to push the right one down.

## 2. Embeddings

**Demo:** `demo/02_embeddings.py`

`text-embedding-3-small` turns any text into 1,536 numbers. It's a different endpoint from the Responses API used everywhere else in the course:

```python
response = client.embeddings.create(model="text-embedding-3-small", input=texts)
vectors = [item.embedding for item in response.data]
```

One call can embed many texts; we send 100 at a time. Here is our request as a vector:

```text
Request: Customers can't sign in after resetting their password
As 1,536 numbers: [0.0235, -0.0048, 0.0286, -0.0008, ...]
```

No single number means anything you could name. What matters is the **direction** the vector points in. **Cosine similarity** measures how closely two vectors point the same way: 1 means the same direction, 0 means unrelated.

```python
def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))
```

To search, embed every script, embed the request, and sort by similarity.

### What to embed

We embed each script's **title and expected result**: what the test checks. For our request, that matters. Embed the whole script, and the right one drops from first to fourth, behind scripts whose steps are also full of emails and passwords. But it isn't a rule. Over all 20 requests in `data/requests.json`, the whole script does as well: searching each request's own platform, both put a right script in the top five for 18 of the 20. Sometimes the meaning is in the steps. The `what-to-embed` playground compares three choices, request by request.

```python
def what_it_tests(script):
    return f"{script['title']}. {script['expected']}"
```

### The result

```text
=== test-scripts-small.json: 20 test scripts ===
  0.511  TS-1042  android  Log in with the new password after a password reset
  0.511  TS-1187  ios      Log in with the new password after a password reset
  0.449  TS-1311  android  Account recovery regression: every way back into a locked account

=== test-scripts.json: 1,000 test scripts ===
  0.511  TS-1042  android  Log in with the new password after a password reset
  0.511  TS-1187  ios      Log in with the new password after a password reset
  0.485  TS-1047  ios      Preserve sign-in email after a password error
```

The right script comes first in both libraries, though it shares only "after" and "password" with the request. A similarity of 0.511 sounds low, but similarities only mean something compared with each other: here, the closest scripts all score around 0.5.

Embedding all 1,000 scripts took about five seconds.

**Why this breaks:**

- **It ignores the criteria.** TS-1042 is tied with TS-1187, the same test on iOS: identical text, identical vector. In the small library, third place is a 40-minute regression suite. The bug is on Android, and the fix ships in ten minutes.
- **It forgets everything.** Every run embeds the whole library again, and keeps the vectors only until the script ends.

## 3. A vector database

**Demo:** `demo/03_vector_database.py`

A **vector database** stores vectors and searches them, alongside the ordinary columns you want to filter on. We use **sqlite-vec**, an extension that adds vector search to SQLite. The whole database is one file: 6.5 MB for 1,000 scripts.

```python
db.execute(
    "create virtual table if not exists scripts using vec0("
    "id text primary key, embedding float[1536] distance_metric=cosine,"
    "platform text, minutes integer, +title text, +checksum text)"
)
```

One row per script: its vector, the columns to filter on (`platform`, `minutes`), and columns that are just carried along (marked with `+`). Searching is SQL, with the criteria in the `where`:

```sql
select id, 1 - distance, platform, minutes, title from scripts
where embedding match ? and k = 3 and platform = ? and minutes <= ?
order by distance
```

`k = 3` asks for the three nearest. The filters are applied *during* the search, so you still get three results that pass them.

**Embed once.** Each row stores a checksum of the text that was embedded. On every run, only scripts that are new, or whose text has changed, are embedded:

```text
Embedded 1,000 new or changed scripts into test-scripts.db
```

The second run:

```text
Embedded 0 new or changed scripts into test-scripts.db
```

Change one script and one gets embedded. Nothing is retrained: the embeddings model never changes, only the rows. (The same idea comes back in Module 6, for keeping a knowledge base up to date.)

### The result

```text
Request: Customers can't sign in after resetting their password
Criteria: android, at most 10 minutes
  0.511  TS-1042  android   5 min  Log in with the new password after a password reset
  0.473  TS-1879  android   5 min  Handle an expired password during sign-in
  0.443  TS-1887  android   3 min  Reject an incorrect password
```

The iOS twin and the 40-minute suite are gone. TS-1042 is first, and everything shown can be run on Android in ten minutes.

sqlite-vec compares the request with every vector. At 1,000 vectors that takes about 3 milliseconds. At millions, databases such as pgvector, Qdrant or Chroma build an **index** (usually **HNSW**, a graph of near neighbours) that checks only a small fraction of the vectors, and very occasionally misses the true nearest one.

**Why this breaks:** the demo asks one more question:

```text
Request: The thermostat's display shows E-104
  0.699  TS-1474  device    5 min  Check missed Wi-Fi network error
  0.692  TS-1370  device    5 min  Check low backup battery warning
  0.688  TS-1845  device    5 min  Check E-217 sensor error on the display
```

E-104 is the pairing timeout. None of these is about E-104. The embedding captures "an error code on the thermostat's display", but not *which* code: to an embedding, E-104 and E-217 are nearly the same thing. Keyword search would have found E-104 exactly. **Embeddings blur exact identifiers**: error codes, part numbers, ticket IDs, names.

## 4. Hybrid search

**Demo:** `demo/04_hybrid_search.py`

If keywords are good at exact words and vectors are good at meaning, use both. SQLite has keyword search built in: **FTS5**, ranked with BM25 as in demo 1. Each search returns its top 20, and **reciprocal rank fusion** merges the two lists. Each script scores `1 / (60 + rank)` in every list it appears in:

```python
def hybrid(*rankings):
    scores = Counter()
    for ranking in rankings:
        for rank, id in enumerate(ranking, 1):
            scores[id] += 1 / (RRF_K + rank)
    return [id for id, _ in scores.most_common()]
```

It only uses ranks, not scores, so it doesn't matter that BM25 scores and cosine similarities are on different scales. It's widely used: Elasticsearch, OpenSearch, Azure AI Search and many vector databases offer it.

### The result

```text
Request: Customers can't sign in after resetting their password (android)
  TS-1879  Handle an expired password during sign-in
  TS-1887  Reject an incorrect password
  TS-1076  Sign-in screen layout
  TS-1073  Sign out and return to the signed-in account
  TS-1042  Log in with the new password after a password reset

Request: The thermostat's display shows E-104 (device)
  TS-1026  Check sensor readings during pairing timeout
  TS-1845  Check E-217 sensor error on the display
  TS-1065  Check E-510 firmware failure display
  TS-1135  Check E-312 boiler fault display
  TS-1335  Check E-305 boiler not responding display
```

E-104 is now first: TS-1026's expected result says the thermostat shows E-104 after pairing times out. But the other four are still the wrong codes, and the password test has slipped from first to fifth.

Two examples prove nothing, so the demo measures. For each of the 20 requests in `data/requests.json`, is a right script in the top five?

```text
A right script in the top 5, for 20 requests:
  keyword 12, vector 18, hybrid 15
```

| Requests | Keyword | Vector | Hybrid |
|----------|--------:|-------:|-------:|
| 14 in everyday words | 6 | 12 | 9 |
| 6 quoting an error code | 6 | 6 | 6 |
| **All 20** | **12** | **18** | **15** |

**Hybrid search did worse than vectors alone.**

Here's why. "What happens when someone tries to add more rooms than allowed?" is answered by "Attempt to create a fifth zone". Vector search ranked it third. Keyword search didn't find it at all: no shared words. Hybrid search ranked it eighth, and put "Reject a seventh daily schedule period" first, because that was 11th for keywords *and* 14th for vectors. Rank fusion rewards agreement: two lukewarm votes (1/71 + 1/74 = 0.0276) beat one strong one (1/63 = 0.0159). When the keyword side is noise, it drags good vector results down.

The error-code requests didn't need keywords either, because each came with context ("while setting up a new thermostat") that the embedding could use. A bare "E-104", as in section 3, is where keywords win.

So the lesson isn't "use hybrid search" or "don't". It's **measure, with your own requests**. Hybrid search helps when people search with exact terms the embeddings model doesn't know: part numbers, ticket IDs, product names. It hurts when the keyword side is just noise. You only find out which by keeping a set of real requests with known answers, and checking every change against it. Be careful not to tune on the same requests you measure with (the `fusion-knobs` playground shows how easily you can fool yourself).

**Why this breaks:** every search here ranks by similarity: shared words, or nearby vectors. None of them can judge *fit*. Does this script test what actually broke? Can it be run before the hotfix ships? And people don't type search queries: they paste bug reports.

## 5. A search tool

**Demos:** `demo/05_search_server.py` and `demo/05_agent.py`

Give the search to a model. As in Module 3, it becomes a tool on an MCP server. It uses vector search with filters, the best measured in section 4:

```python
@server.tool()
def find_test_scripts(request: str, platform: Literal["android", "ios", "web", "device"], max_minutes: int) -> str:
    """Search Dormouse's library of 1,000 manual test scripts by meaning. In `request`, describe
    the behaviour to test in a few plain words, like a test's title: for example "log in after
    changing the password". Only scripts for `platform` that take at most `max_minutes` to run
    are returned. Returns the five closest scripts as JSON, closest first, with their steps and
    expected results."""
```

The criteria are arguments: `Literal` becomes a list of allowed values in the tool's schema, so the model can only ask for a real platform. The server keeps the database up to date on every call, so the first search embeds the library and later ones embed only what has changed.

The agent is Module 3's tool loop, unchanged, with this bug report:

```text
You: Support say that since this morning's release, customers on Android who reset their password can't get back into the app. The hotfix ships in ten minutes. Which test should we run?
  [tool] find_test_scripts({"request":"Android user logs in after resetting password","platform":"android","max_minutes":10})
         -> TS-1042 Log in with the new password after a password reset
         -> TS-1548 Check password entry with Android autofill
         -> TS-1879 Handle an expired password during sign-in
         -> TS-1968 Keep sign-in safe after app backgrounding
         -> TS-1594 Reject mismatched registration passwords
Agent: Run TS-1042, “Log in with the new password after a password reset.” It’s the closest match to the reported Android failure, takes five minutes, and verifies that the new password works while the old one is rejected.
```

The model did three things a search can't:

- **It turned a bug report into criteria.** "Customers on Android" became `platform: "android"`; "ships in ten minutes" became `max_minutes: 10`.
- **It wrote its own search.** Short and to the point, as the tool's description asks.
- **It judged the results.** It read five scripts with their steps and expected results, picked one, and said why.

The instructions also say *"If nothing fits well, search again with different words"*, and sometimes it does, searching a second time for something like "reset forgotten password by email link then sign in on Android". The tool's description matters too. An earlier version just said "describe what needs testing in plain words". The agent then searched for *"Verify Android password reset flow and confirm users can sign back into the app afterward, focusing on regression after a release/hotfix"*, got five near misses, and recommended one while admitting it didn't really fit.

### What MCP gives you in practice

- **One search, many front ends.** The same server works in our agent, Claude, Claude Code, Cursor, VS Code and any other MCP client. Add it as a stdio server whose command is `uv run python demo/05_search_server.py`, and a tester can ask their assistant for the right test without leaving their editor.
- **Your system, wrapped, not rebuilt.** The tool is a thin layer over what you already have. In a real company it would call your test management system's API instead of a JSON file, and the agent wouldn't know or care.
- **The criteria stay exact.** The model fills in the arguments; the database applies them. The model can't decide that a 40-minute test "probably" fits in ten.

**Why this breaks:** the agent can find the right test. But many questions need an *answer*, not a script: *"What does E-104 mean, and what should support tell the customer?"* That answer is written in the product's documentation, and the model has never read it. **Module 6** puts the documentation in front of the model: retrieval-augmented generation.

---

## Summary

| Step | Finds by | Problem |
|------|----------|---------|
| 1. Keyword search | Shared words, rare ones counting more | Matches words, not meaning |
| 2. Embeddings | Nearby vectors | Ignores the criteria; embeds everything every run |
| 3. A vector database | Nearby vectors, filtered, stored once | Blurs exact identifiers like error codes |
| 4. Hybrid search | Both, merged by rank | Measured: worse than vectors alone on our requests |
| 5. A search tool | An agent's own searches, judged by the agent | Finds tests, but can't answer questions from documentation |

## Playground

[`playground/`](playground/) has six things to play with: a similarity explorer, what to embed, finding duplicate scripts, searching in other languages, shrinking the vectors, and the knobs of hybrid search.

## Further reading and extensions

The final exercise is in [`further-reading/`](further-reading/): papers on keyword ranking, embeddings, vector indexes and fusing rankings, with a note on what to look for in each and which demo it relates to, plus extension projects to take home.

## Slides

```bash
pnpm slides:05
```
