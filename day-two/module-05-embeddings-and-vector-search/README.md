# Module 5 — Embeddings and Vector Search

> A customer asks: *"Why is the heating already on before my alarm goes off?"* The answer is in Dormouse's documentation, in a document called "Understand Warm Wake", and we want a search that finds it. **Keyword search** finds it in the 26 sections of the user guide, but in all 275 documents it comes 142nd: rare filler words like "why" and "goes" decide the order, and "alarm" isn't in any document. So we build an **embeddings model** ourselves, live, from the user guide: a list of numbers for each word, learned from the words around it. It works (the closest words to *warm* are *wake* and *sunrise*), but 1,794 words is far too little text, and our question's most important word is one it has never seen. A real embeddings model turns a whole document into 1,536 numbers. **Cosine similarity** compares two lists of numbers, and with it the Warm Wake document comes first. Last, a **vector database**, ChromaDB, stores the vectors once and filters them, so a customer never sees an internal engineering note. It finds the right document, but the customer wanted an answer, which is Module 6.

## Learning goals

- Explain **keyword search** and how **BM25** scores a document: matching words, with rare words counting for more.
- Explain what an **embedding** is, by training a small one, **word2vec**, in plain Python.
- Turn a whole document into a vector, by **averaging** word vectors and with an **embeddings model**.
- Compare vectors with **cosine similarity**, and use it to **search by meaning**.
- Store vectors in a **vector database**, embed only what has changed, and **filter** by **metadata** such as who a document is for.

---

## The idea: search by meaning

A question and the document that answers it often share almost no words. "Why is the heating already on before my alarm goes off?" is answered by a document that says Warm Wake "starts the heating before a schedule period". The two share "heating" and "before", and so do 100 other documents in the library. A person sees the connection straight away: an alarm means the morning, the morning means the schedule, and heating that starts before the schedule is Warm Wake. Keyword search sees different words.

An **embedding** is a list of numbers (a **vector**) that stands for a piece of text. An embeddings model is trained so that texts that mean similar things get vectors pointing in similar directions. Searching by meaning is then just arithmetic: turn the question into a vector, and find the documents whose vectors are closest.

You have seen this before. In Module 1, the neural language model learned a vector of 16 numbers for each token, as a side effect of predicting the next one, and arranged them so that *mouse* and *queen* (characters who say things) ended up close together. In this module we build vectors like that on purpose, then use a model that does it for whole documents.

## The data

Everything runs on the documentation for **Dormouse**, a smart thermostat with apps for Android and iOS and a web dashboard. **Dormouse and all its documents are invented for this course.** Your own documentation would work the same way. Module 6 uses the same documents to answer questions.

| File | What | Size |
|------|------|------|
| `data/docs/*.md` | Dormouse's documentation, copied from Module 6 by `data/copy_docs.py`: support, troubleshooting, app, installation, specification, policy, error-code and release-note documents for customers, and internal documents for staff | 275 documents, about 150,000 words |
| `data/docs/user-guide.md` | Written by hand: the user guide. The small library in demos 1 and 4, and the training text in demo 2 | 1 document, 26 sections, 1,794 words |
| `data/questions.json` | 20 questions in customers' own words, each with the documents that answer it, for the playgrounds | 20 questions |

Each document starts with a few lines of **metadata**, facts about the document rather than its text:

```text
---
title: Understand Warm Wake
product: thermostat
type: support
audience: customer
firmware: 4.1
updated: 2025-10-08
---
```

234 documents are for customers and 41 are internal: engineering notes, support playbooks and QA reports. The longest document is the user guide, so every document is short enough to embed whole. Splitting long documents into **chunks** comes in Module 6.

## Setting up

You need `OPENAI_API_KEY` in `.env` (see Module 2). This module adds one package, **ChromaDB**, a vector database. `uv` installs it with everything else. It's a big install: 84 packages, including numpy and onnxruntime. We give Chroma our own vectors, so it never downloads an embeddings model of its own.

## Running the demos

From this folder:

```bash
uv run python demo/01_keyword_search.py
```

| Demo | What it is | Writes to `demo/output/` |
|------|------------|--------------------------|
| `01_keyword_search.py` | BM25 keyword search, in plain Python | `01_keyword_search.json`: every section and document, ranked |
| `02_word_vectors.py` | Train word vectors on the user guide, in plain Python | `02_word_vectors.txt`: one word per line, then its 20 numbers |
| `03_document_vectors.py` | A question and two documents as vectors, two ways (run demo 2 first) | `03_document_vectors.json`: every vector in full |
| `04_similarity_search.py` | Embed everything and search by cosine similarity | `04_similarity_search.json`: every section and document, ranked |
| `05_vector_database.py` | Store the vectors in ChromaDB, and filter | `chroma/`, the database; `05_vector_database.json` |

Demos 3 to 5 call OpenAI's embeddings API. Embedding all 275 documents is 179,993 tokens, which costs less than half a cent at $0.02 per million tokens ([OpenRouter's price list](https://openrouter.ai/api/v1/embeddings/models), checked 18 November 2026).

Every demo gives the same results each time. Demo 2 starts from random numbers, but the seed is fixed (`SEED = 1`). Change it and you get different neighbours. The API can return very slightly different vectors from one call to the next, so similarities can differ in the third decimal place.

---

## 1. Keyword search

**Demo:** `demo/01_keyword_search.py`

The oldest way to search: score each document by the words it shares with the question. **BM25** ("Best Match 25") is the standard scoring, used by Elasticsearch, OpenSearch and SQLite's full-text search. For each word in the question that a document contains, it adds:

```python
rarity = math.log(1 + (len(texts) - appears_in[word] + 0.5) / (appears_in[word] + 0.5))
score += rarity * count * (K1 + 1) / (count + K1 * (1 - B + B * len(text) / average_length))
```

Three ideas are packed in there:

- **Rare words count for more.** "the" is in every document, so it adds almost nothing. A word that's in only a few documents adds a lot.
- **Repeats help, but less and less.** The second "heating" adds less than the first. `K1` (1.5) controls how fast it levels off.
- **Long documents don't win just by being long.** `B` (0.75) scales the count down for documents longer than average.

We search two libraries: first the user guide, split into its 26 sections, then all 275 documents.

```text
=== The user guide: 26 sections ===
Q: Why is the heating already on before my alarm goes off?
   7.64  Warm Wake
   6.98  Frost protection
   4.62  Energy reports

=== All the documentation: 275 documents ===
Q: Why is the heating already on before my alarm goes off?
   7.02  Enter your boiler size for energy reports
   6.82  Web dashboard: Household screen guide
   6.56  Web dashboard: Energy screen guide
```

In the user guide it works. Only one section, Warm Wake, contains "already" ("the home has already reached the target temperature"), and that rare word puts it first.

In all 275 documents it fails. "Understand Warm Wake" comes **142nd**. The winners share the question's least important words:

| Word | Documents it appears in |
|------|-------------------------|
| why | 7 |
| goes | 1 |
| already | 38 |
| off | 132 |
| before | 153 |
| alarm | 0 |

"Why" is in only 7 documents, so it counts for a lot, and the boiler-size document contains it once. "Goes" is in just one document, the household screen guide, which comes second. "Already" is no longer rare. And "alarm", the word that says *when*, isn't in any document at all.

**Why this breaks:** keyword search matches **words, not meaning**. The document that answers the question doesn't use the question's words. Every extra document that happens to share a rare word is another chance to push the right one down, so a search that worked on 26 sections fails on 275 documents.

## 2. Build an embeddings model

**Demo:** `demo/02_word_vectors.py`

We need numbers that capture what a word *means*, not how it's spelt. **word2vec** (Mikolov and others, 2013) learns them from one idea: **words used in the same places mean similar things**. "Warm" and "sunrise" keep turning up near "wake" in the user guide, so they should get similar numbers.

We train it live, in plain Python, on the user guide. Every word starts with 20 random numbers. Then, for every word in the guide and each neighbour up to `WINDOW` (3) words away, the model makes a guess: is this word a real neighbour? It also makes the same guess for 5 random words, which almost never are. Each wrong guess nudges the numbers:

```python
samples = [(tokens[j], 1)] + [(random.choice(noise), 0) for _ in range(NEGATIVES)]
for other, is_neighbour in samples:
    neighbour = neighbours[other]
    guess = sigmoid(sum(a * b for a, b in zip(vector, neighbour)))
    error = is_neighbour - guess
    for k in range(SIZE):
        change[k] += rate * error * neighbour[k]
        neighbour[k] += rate * error * vector[k]
```

Multiply two words' numbers together and add them up, and `sigmoid` turns the total into a guess between 0 and 1. A real neighbour should score near 1, so the error pulls the two closer. A random word should score near 0, so the error pushes it away. This is **skip-gram with negative sampling**. After 30 passes through the guide (about 11 seconds), words used in the same places have similar numbers. Module 1's network learned its embeddings as a side effect of predicting the next token. This model has no other job.

The demo prints the five closest words to a few others. ("Closest" is measured by cosine similarity, which section 4 explains.)

```text
=== Trained on the user guide: 1,794 words, 235 different words ===
  warm       wake, sunrise, heat, early, power
  password   sign, network, link, account, cleaning
  heating    hours, switch, early, protection, for
  alarm      never seen
```

Nobody told the model what any word means, yet *warm* is closest to *wake*, *sunrise* and *early*, and *password* to *sign*, *link* and *account*. Those are the words the guide uses together. Open `demo/output/02_word_vectors.txt` to see all 235 words and their numbers.

**Why this breaks:**

- **Too little text.** *Heating* is closest to *hours*, *switch* and *for*: 1,794 words isn't enough to say much about a word that appears everywhere. Models people use are trained on billions of words.
- **Words it has never seen.** The model only has numbers for the 235 words that appear at least twice. "Alarm", the word our question turns on, isn't in the guide at all.
- **One vector per word.** Our question is 11 words, and a document is hundreds. We need one vector for the whole thing.

## 3. Turn a document into numbers

**Demo:** `demo/03_document_vectors.py`

The simplest way to make one vector from many words: **average** them. Add up the vectors of every word the model knows, and divide by how many there are:

```python
known = [word_vectors[w] for w in words(text) if w in word_vectors]
return [sum(column) / len(known) for column in zip(*known)]
```

The better way is a model trained to embed whole passages. OpenAI's `text-embedding-3-small` turns any text up to 8,191 tokens (about 6,000 words) into 1,536 numbers. It reads the text as a whole, word order included, and was trained on far more text than our 1,794 words. It's a different endpoint from the Responses API used everywhere else in the course:

```python
response = client.embeddings.create(model="text-embedding-3-small", input=texts)
vectors = [item.embedding for item in response.data]
```

One call can embed many texts. The demo turns the question and two documents into vectors both ways: "Understand Warm Wake", which answers the question, and "Enter your boiler size for energy reports", which keyword search put first.

```text
=== Our model: the average of the word vectors ===
  Q: Why is the heating already on before my alarm goes off?
    20 numbers: [-0.61, -0.77, 0.33, 0.24, -0.31, 0.08, ...]
    left out 5 words it has never seen: alarm, already, goes, my, why
  Understand Warm Wake
    20 numbers: [-0.55, -0.97, 0.08, 0.21, -0.22, -0.23, ...]
    left out 10 words it has never seen: active, ahead, currently, does, feature, helps, ...
  Enter your boiler size for energy reports
    20 numbers: [-0.18, -0.45, 0.45, 0.08, -0.30, 0.39, ...]
    left out 36 words it has never seen: 1st, accuracy, also, appears, applies, arrive, ...

=== text-embedding-3-small ===
  Q: Why is the heating already on before my alarm goes off?
    1,536 numbers: [-0.0109, 0.0147, -0.0659, -0.0318, -0.0398, -0.0046, ...]
  Understand Warm Wake
    1,536 numbers: [-0.0090, 0.0321, -0.0258, 0.0117, -0.0217, -0.0029, ...]
  Enter your boiler size for energy reports
    1,536 numbers: [0.0211, 0.0359, 0.0435, -0.0261, -0.0010, 0.0006, ...]
```

Averaging throws a lot away. Our model kept 6 of the question's 11 words: "is, the, heating, on, before, off", the least telling ones. It also loses the order: "the heating is on before the alarm" and "the alarm is on before the heating" average to the same numbers.

No single number in either list means anything you could name. Open `demo/output/03_document_vectors.json` to see every number of every vector.

**Why this breaks:** a list of numbers doesn't find anything on its own. Which document is closer to the question, Warm Wake or boiler size? Looking at the first six numbers, you can't tell. We need a way to measure how close two vectors are.

## 4. Find by similarity

**Demo:** `demo/04_similarity_search.py`

Think of each vector as an arrow pointing somewhere in a space with 1,536 directions. Texts that mean similar things should point the same way. **Cosine similarity** measures how closely two arrows point the same way: 1 means the same direction, 0 means unrelated, and -1 means opposite.

```python
def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    length_a = math.sqrt(sum(x * x for x in a))
    length_b = math.sqrt(sum(y * y for y in b))
    return dot / (length_a * length_b)
```

`dot` is the **dot product**: multiply the two vectors number by number and add up. It's large when both have big numbers in the same places with the same signs. Dividing by the two lengths means only the direction counts: a long document doesn't win just because its arrow is longer. (OpenAI's vectors have length 1, or very nearly, so for them the dot product alone gives almost the same order: the `distance-measures` playground finds the same top seven, then two documents that tie to three decimal places swap. On word counts, where lengths vary a lot, the measures disagree completely.)

To search, embed every document, embed the question, and sort by similarity:

```text
=== The user guide: 26 sections ===
Q: Why is the heating already on before my alarm goes off?
  0.618  customer  Warm Wake
  0.420  customer  Boost
  0.408  customer  The boost button

=== All the documentation: 275 documents ===
Q: Why is the heating already on before my alarm goes off?
  0.488  customer  Understand Warm Wake
  0.455  customer  Heating Starts Below Five Degrees
  0.427  customer  Set a heating schedule
```

The right document comes first in both libraries, though it shares only "heating" and "before" with the question, and 100 other documents contain both. The model has learned that a question about an alarm going off is about the morning, and so about heating that starts before the schedule. A similarity of 0.488 sounds low, but similarities only mean something compared with each other: here the closest documents all score between 0.4 and 0.5.

| Where "Warm Wake" came | Keyword search | Cosine similarity |
|------------------------|----------------|-------------------|
| The user guide, 26 sections | 1st | 1st |
| All the documentation, 275 documents | 142nd | 1st |

One question isn't proof. The `what-to-embed` playground runs this search for the 20 questions in `data/questions.json`, all in customers' own words: a right document comes in the top five for 19 of them.

**Why this breaks:**

- **It embeds everything, every time.** Each run sends all 275 documents (179,993 tokens) to the API again, and the vectors vanish when the script ends.
- **It compares the question with every document.** 275 comparisons is nothing, but a company's documents, tickets and emails could run to millions.
- **It can't filter.** 41 of the documents are internal, written for staff. A search for customers must never return them, and here nothing stops it.

## 5. A vector database

**Demo:** `demo/05_vector_database.py`

A **vector database** stores vectors, searches them, and keeps facts about each one to filter by. We use **ChromaDB**, which runs inside our script and keeps everything in a folder, `demo/output/chroma/` (9.7 MB for 275 documents).

```python
database = chromadb.PersistentClient(path=str(DATABASE), settings=Settings(anonymized_telemetry=False))
collection = database.get_or_create_collection(
    "dormouse-docs", configuration={"hnsw": {"space": "cosine"}}, embedding_function=None
)
```

A **collection** is like a table. We ask it to compare by cosine similarity, and to use the vectors we give it rather than Chroma's built-in embeddings model. `anonymized_telemetry=False` stops Chroma sending usage statistics. Each document goes in with its vector, its text and its metadata:

```python
collection.upsert(
    ids=[d["id"] for d in changed],
    embeddings=embed([d["text"] for d in changed]),
    documents=[d["text"] for d in changed],
    metadatas=[{"title": d["title"], "type": d["type"], "audience": d["audience"], "checksum": ...}],
)
```

**Embed once.** The metadata includes a **checksum** of each document's text, a short fingerprint that changes whenever the text does. On every run, only documents that are new, or whose text has changed, are embedded. The first run:

```text
Stored 275 new or changed documents in chroma/
```

The second run:

```text
Stored 0 new or changed documents in chroma/
```

**Search with a filter.** The question's vector goes in, and `where` limits the search to documents whose metadata matches:

```python
collection.query(query_embeddings=[vector], n_results=3, where={"audience": "customer"})
```

```text
Q: Why is the heating already on before my alarm goes off?  (customers only)
  0.487  customer  Understand Warm Wake
  0.455  customer  Heating Starts Below Five Degrees
  0.427  customer  Set a heating schedule
```

Our question never reaches an internal document, so the filter changes nothing here. A second customer question shows why it matters:

```text
Q: My thermostat makes a clicking noise  (every document)
  0.520  internal  Relay click on hardware revision C
  0.440  customer  Thermostat Does Not Respond to Dial Changes
  0.424  customer  Thermostat Shows the Wrong Room Temperature

Q: My thermostat makes a clicking noise  (customers only)
  0.440  customer  Thermostat Does Not Respond to Dial Changes
  0.424  customer  Thermostat Shows the Wrong Room Temperature
  0.411  customer  Radiator Valve Does Not Heat to Its Own Temperature
```

Without the filter, the closest document is an internal engineering note about a fault in one hardware revision, not something to show a customer. With it, the note can't come back at all. Module 8 uses the same kind of filter to keep a customer assistant away from staff documents.

**Not every vector is compared.** Chroma organises the vectors as an **HNSW** graph ("hierarchical navigable small world"): each vector is linked to its near neighbours, and a search hops from vector to vector towards the question instead of checking them all. That's how a vector database searches millions of vectors in milliseconds. The price is that the search is **approximate**: very occasionally it misses a vector that's slightly closer.

**Why this breaks:**

- **It finds the document, not the answer.** The customer asked why the heating comes on early. The answer is in the Warm Wake document: it heats ahead of a schedule period, and shows a sunrise symbol while it does. Reading the right document and answering from it is **Module 6, RAG**.
- **It always returns something.** No customer document is about the click, so the filtered search returns three documents that don't answer the question, at similarities of 0.411 to 0.440, against 0.520 for the note that does. Similarity ranks documents. It can't tell you that none of them fits.

---

## Summary

| Step | Finds by | Problem |
|------|----------|---------|
| 1. Keyword search | Shared words, rare ones counting more | Matches words, not meaning |
| 2. Build an embeddings model | Words used in the same places | Too little text; one vector per word |
| 3. Turn a document into numbers | Averaged word vectors, or a model trained on passages | Numbers alone don't find anything |
| 4. Find by similarity | The angle between two vectors | Embeds and compares everything, every time; can't filter |
| 5. A vector database | Nearby vectors, filtered, stored once | Finds the document, not the answer, and always returns something |

## Playground

[`playground/`](playground/) has six things to play with: the word2vec model with its settings exposed, a similarity explorer, distance measures compared, what to embed, searching in other languages, and shrinking the vectors.

## Further reading and extensions

The final exercise is in [`further-reading/`](further-reading/): papers on keyword ranking, word vectors, sentence embeddings and vector indexes, with a note on what to look for in each and which demo it relates to, plus extension projects to take home.

## Slides

```bash
pnpm slides:05
```
