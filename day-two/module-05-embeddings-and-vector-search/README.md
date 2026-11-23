# Module 5 — Embeddings and Vector Search

> A customer asks: *"Why is the heating already on before my alarm goes off?"* The answer is in Dormouse's documentation, in a document called "Understand Warm Wake", and we want a search that finds it. **Keyword search** finds it in the 26 sections of the user guide, but in all 275 documents it comes 142nd: rare filler words like "why" and "goes" decide the order, and "alarm" isn't in any document. So we build **embeddings** ourselves from the user guide: a list of numbers for each word, made from the words around it. The easy way is to **count** them. It works (the closest words to *warm* are *wake* and *sunrise*), but each word gets 235 numbers, far too many to picture. Squeezed onto a line, one number each, 16 words we picked mostly fall into place, but each word gets only one place, so *router* ends up beside *schedule*. With two numbers each, they make a **map**: alike words point the same way from the middle, and the angle between them says how alike they are. **Adding up** a text's word vectors gives it one vector, and **cosine similarity**, the angle from the map, compares two. A sentence about heating and one about a password point almost opposite ways, but two numbers can't tell 275 documents apart, and Warm Wake comes 71st. An **embeddings model**, word2vec, learns 20 numbers per word instead, live, in about 11 seconds, and with its sums Warm Wake climbs to 8th. But 1,794 words is far too little text, our question's most important word is one no method so far has seen, and a sum can't see word order, so two sentences with opposite meanings score 1.000. A real embeddings model reads the whole text and turns it into 1,536 numbers, and the Warm Wake document comes first. It finds the right document, but the customer wanted an answer. Storing the vectors in a **vector database** and answering from what it finds is Module 6.

## Learning goals

- Explain how **keyword search** works: splitting text into words, an **inverted index**, and how **BM25** scores a document, with rare words counting for more.
- Explain what an **embedding** is, by building one from **counts** of neighbouring words.
- Draw words on a **map** with two numbers each, group them by direction with **k-means**, and explain why the **angle** between two arrows says how alike they are.
- Turn a sentence or a document into one vector by **adding up** its word vectors, compare two with **cosine similarity**, and explain why the sum loses **word order**.
- Explain how an **embeddings model** learns its vectors, by training a small one, **word2vec**, in plain Python.
- Turn any text into a vector with an **embeddings model**, and use it to **search by meaning**.

---

## The idea: search by meaning

A question and the document that answers it often share almost no words. "Why is the heating already on before my alarm goes off?" is answered by a document that says Warm Wake "starts the heating before a schedule period". The two share "heating" and "before", and so do 100 other documents in the library. A person sees the connection straight away: an alarm means the morning, the morning means the schedule, and heating that starts before the schedule is Warm Wake. Keyword search sees different words.

An **embedding** is a list of numbers (a **vector**) that stands for a piece of text. An embeddings model is trained so that texts that mean similar things get vectors pointing in similar directions. Searching by meaning is then just arithmetic: turn the question into a vector, and find the documents whose vectors are closest.

You have seen this before. In Module 1, the neural language model learned a vector of 16 numbers for each token, as a side effect of predicting the next one, and arranged them so that *mouse* and *queen* (characters who say things) ended up close together. In this module we build vectors like that on purpose: first by counting, then we add them up into one vector per sentence, learn better ones by training, and last use a model that does it for whole documents.

## The data

Everything runs on the documentation for **Dormouse**, a smart thermostat with apps for Android and iOS and a web dashboard. **Dormouse and all its documents are invented for this course.** Your own documentation would work the same way. Module 6 uses the same documents to answer questions.

| File | What | Size |
|------|------|------|
| `data/docs/*.md` | Dormouse's documentation, copied from Module 6 by `data/copy_docs.py`: support, troubleshooting, app, installation, specification, policy, error-code and release-note documents for customers, and internal documents for staff | 275 documents, about 150,000 words |
| `data/docs/user-guide.md` | Written by hand: the user guide. The small library in demos 1, 4, 5 and 6, and the text demos 2, 3 and 5 build word vectors from | 1 document, 26 sections, 1,794 words |
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

You need `OPENAI_API_KEY` in `.env` (see Module 2) for demo 6. Demos 1 to 5 need nothing but Python.

## Running the demos

From this folder:

```bash
uv run python demo/01_keyword_search.py
```

| Demo | What it is | Writes to `demo/output/` |
|------|------------|--------------------------|
| `01_keyword_search.py` | BM25 keyword search, in plain Python | `01_keyword_search.json`: every section and document, ranked; `01_index.json`: the index of all 275 documents |
| `02_count_vectors.py` | Build word vectors by counting neighbours in the user guide, then put 16 words on a line | `02_count_vectors.json`: every word's neighbours and their counts; `02_word_line.json`: the 16 words' places on their line, and every word's place on a line of all 235 |
| `03_word_map.py` | Give words two numbers each, a map, and group them by direction | `03_word_map.json`: every word's two numbers, length and angle, and the 16 words' groups |
| `04_sentence_vectors.py` | Add up the map's word vectors into one per sentence, and search with them (run demo 3 first) | `04_sentence_vectors.json`: three pairs of sentences, the question's two numbers and lost words, and every section and document, ranked |
| `05_word_vectors.py` | Train word vectors on the user guide, in plain Python, and search with their sums | `05_word_vectors.txt`: one word per line, then its 20 numbers; `05_question.json`: every section and document, ranked |
| `06_similarity_search.py` | Embed everything and search by cosine similarity | `06_similarity_search.json`: every section and document, ranked |

Demo 6 calls OpenAI's embeddings API. Embedding all 275 documents is 179,993 tokens, which costs less than half a cent at $0.02 per million tokens ([OpenRouter's price list](https://openrouter.ai/api/v1/embeddings/models), checked 18 November 2026).

Every demo gives the same results each time. Demo 5 starts from random numbers, but the seed is fixed (`SEED = 1`). Change it and you get different neighbours. The API can return very slightly different vectors from one call to the next, so similarities can differ in the third decimal place.

---

## 1. Keyword search

**Demo:** `demo/01_keyword_search.py`

**Keyword search** finds the documents that contain the words you typed. It's the oldest way to search with a computer, and still the most common: the search box on many websites, the search in your email, and search engines such as Elasticsearch, OpenSearch and SQLite's full-text search all start here. It needs no model and no API, and it's fast.

It works in two parts. The first is done once, ahead of time, before anyone asks a question.

1. **Split every document into words.** Lower-case everything, and cut wherever there's a character that isn't a letter or a digit.

   Real search engines usually do more here. They cut words down to a common root (**stemming**, so *heating* and *heated* both become *heat*), and some drop very common words (**stop words**). Demo 1 does neither.

2. **Build an index.** For every word, list the documents that contain it, and how many times. This is an **inverted index**, like the index at the back of a book: look up a word, get the pages. The Dormouse documentation has 2,491 different words. Here is the start of one entry, from `demo/output/01_index.json`:

   ```text
   geofencing → away-mode-and-geofencing-qa-report (18), set-up-geofencing (16),
                phone-location-privacy-policy (15), away-mode-turns-on-unexpectedly (14),
                ... 37 documents in all
   ```

3. **Note each document's length.** The score needs it.

```python
def build_index(documents):
    index = {}
    lengths = []
    for number, document in enumerate(documents):
        text = words(document["text"])
        lengths.append(len(text))
        for word, count in Counter(text).items():
            index.setdefault(word, {})[number] = count
    return index, lengths
```

A real search engine keeps its index, and updates it when a document is added or changed. Demo 1 builds it each time it runs, which takes no time at this size.

The second part is done for each question.

1. **Split the question the same way.** Our question becomes eleven words:

   ```text
   why, is, the, heating, already, on, before, my, alarm, goes, off
   ```

2. **Look up each word in the index**, and give a score to every document listed under it.
3. **Sort**, highest score first.

The index is what makes keyword search fast: a search only looks at the documents that contain a word of the question, however many documents there are. Our question doesn't gain much, because it contains "the", and "the" is in all 275 documents, so every document gets a score. That's one reason some engines drop stop words.

Everything interesting is in the score. Counting matching words doesn't work: "the" is in all 275 documents. Count matches for our question, and four of the five longest documents come first, led by the user guide with 257 matches, 171 of them "the". **BM25** ("Best Match 25") is the standard way to score, used by Elasticsearch, OpenSearch and SQLite's full-text search. For each word in the question, it looks up the word's `entry` in the index, and adds to the score of every document listed there:

```python
rarity = math.log(1 + (len(documents) - len(entry) + 0.5) / (len(entry) + 0.5))
scores[number] += rarity * count * (K1 + 1) / (count + K1 * (1 - B + B * lengths[number] / average_length))
```

`len(entry)` is the number of documents that contain the word.

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

## 2. Embeddings

**Demo:** `demo/02_count_vectors.py`

We need numbers that capture what a word *means*, not how it's spelt. Every embedding rests on one idea: **words used in the same places mean similar things**. The linguist Zellig Harris argued it in 1954. "Warm" and "sunrise" keep turning up near "wake" in the user guide, so they should get similar numbers.

The simplest way to turn that idea into numbers is to count. It's Module 1's word-pair counting, turned into vectors, in three steps.

1. **Choose the words.** Split the guide into words, as in section 1, and keep every word that appears at least twice (`MIN_COUNT`). That's 235 different words, which make up 1,585 of the guide's 1,794 words.

2. **Count the neighbours.** Make a table with one row for each of the 235 words, and one column for each of the same words. Go through the guide word by word, and for every word up to 3 places away (`WINDOW`), add one to that word's column in this word's row:

   ```python
   vectors = [[0] * len(vocabulary) for _ in vocabulary]
   for i, word in enumerate(tokens):
       for j in range(max(0, i - WINDOW), min(len(tokens), i + WINDOW + 1)):
           if j != i:
               vectors[word][tokens[j]] += 1
   ```

3. **Each row is a word's vector.** It has 235 numbers: how often each word in the vocabulary turned up near this one. These are the biggest numbers in *warm*'s row:

   ```text
   warm: wake 10, warm 4, is 4, the 3, heating 3, when 2, to 2, sunrise 2, ...
   ```

Two words that keep the same company now have similar rows. There are no random numbers and no training: counting the whole guide takes a fraction of a second.

The demo prints the five closest words to a few others. ("Closest" is measured by cosine similarity, which section 3 explains.)

```text
=== Counted in the user guide: 1,794 words, 235 different words ===
  warm       wake, sunrise, early, heat, is
  password   link, schedules, your, choose, and
  heating    thermostat, when, temperature, and, dial
  alarm      never seen
```

Nobody told it what any word means, yet *warm* is closest to *wake*, *sunrise*, *early* and *heat*, and *heating* to *thermostat* and *temperature*. Those are the words the guide uses together. Open `demo/output/02_count_vectors.json` to see every word's neighbours and their counts.

235 numbers are hard to picture, so the demo also squeezes 16 words we picked from the guide onto a line: one number per word. It works out how alike each pair is (the cosine similarity of their rows). Then it puts the words anywhere on a line and, over and over:

1. moves each word halfway towards the average position of the others, weighted by how alike they are,
2. re-centres the line and stretches it back out. Without this, every word would slide to the same point.

After 24 rounds, nothing moves in the second decimal place. This is **spectral ordering**, the first step of **spectral clustering**: cut the line at zero and you have two groups.

```python
positions = [(p + dot(s, positions) / total) / 2 for p, s, total in zip(positions, similar, pull)]
```

```text
=== 16 words we picked: one number each ===
  -0.43  sunrise
  -0.39  wake
  -0.35  warm
  -0.18  early
  -0.17  frost
  -0.12  heat
   0.03  temperature
   0.08  app
   0.09  schedule
   0.12  router
   0.13  boiler
   0.22  radiator
   0.25  account
   0.25  password
   0.30  phone
   0.39  email
```

Warm Wake's words end up together at one end, with *frost* and *heat*, and the words for signing in at the other. One number loses a lot, though, and a different choice of words would give a different line. *boiler* lands nearer *password* than *heat*. That isn't the line's fault: in the full rows of 235 numbers, *boiler* is also closer to *password* (a cosine similarity of 0.45) than to *heat* (0.36).

The demo also puts all 235 words on a line. That's too many to print, so open `demo/output/02_word_line.json` to see them, under `all`. With every word pulling, the 16 lose their order: *warm* (−0.003) and *wake* (0.03) end up in the middle with everything else, and *password* (−0.032) falls between *frost* and *heat*.

The pull has to come from *similar company*, not from turning up together. Pull the words together by how often they're neighbours, and the line falls apart into three clumps: among these 16 words there are only 13 neighbouring pairs, and *radiator*, *router* and *account* are never near any of the others.

The full rows have their own problems. They are long and mostly zeros: 90.3% of all the numbers in the table are zero, and *warm* has only 24 that aren't. All the documentation has 1,899 words that appear at least twice, so its rows would have 1,899 numbers each. And common words get in the way: *is*, *the* and *and* turn up near nearly everything, so *and* comes among the five closest words to both *password* and *heating*.

**Why this breaks:**

- **One number per word.** On a line, each word has one place, so a word that belongs somewhere else has nowhere to go. *router* belongs with the words for getting connected, and *schedule* with the heating words, yet the line puts them 0.03 apart, in the middle, although their rows have almost nothing in common (a cosine similarity of 0.04). *frost* and *heat* are 0.05 apart, with a similarity of 0.02.

What if each word had two numbers?

## 3. A map of meaning

**Demo:** `demo/03_word_map.py`

A line gives each word one number, and loses most of what the counts say. Two numbers make a map. The demo takes the same 16 words and runs the same pull as the line, on two lines at once. The first number comes out exactly as the line in section 2. The second is another line, kept **at right angles** to the first; without that rule, both would settle on the same line:

```python
overlap = sum(w * x * y for w, x, y in zip(pull, xs, ys)) / sum(w * x * x for w, x in zip(pull, xs))
ys = [y - overlap * x for x, y in zip(xs, ys)]
```

Each word is now a point on a map, and the middle of the map is the average word. Draw an arrow from the middle to each word. The arrow's **direction** says what the word is like. Its **length** says how clearly it belongs anywhere: *boiler* is 0.17 from the middle and *early* and *heat* 0.20, because their counts look a little like everyone's.

**Only the direction counts.** Push every word out to a circle, keeping its direction. Two words are alike when their arrows point the same way, and the smaller the angle between them, the more alike they are. The **cosine** of the angle turns it into a score: 1 for the same direction, 0 at right angles, -1 for opposite. That is **cosine similarity**, which demo 2 used to find the closest words and sections 4 to 6 use to search.

| Words | Angle between them | Cosine |
|---|---|---|
| warm, wake | 2° | 1.00 |
| account, password | 7° | 0.99 |
| warm, frost | 49° | 0.66 |
| warm, password | 133° | -0.68 |

**Group by direction.** **k-means** finds groups in three steps:

1. Start with three directions, evenly spaced round the circle.
2. Give each word to the direction it's most like: the highest cosine similarity.
3. Move each direction to the middle of its words, and go back to step 2 until nothing changes.

Where k-means starts changes where it settles, so the demo starts 12 times and keeps the tightest groups. On the circle, distance and angle say the same thing: for two words at length 1, distance² = 2 − 2 × cosine. So grouping words by how far apart they are is grouping them by cosine similarity.

```text
=== 16 words we picked: two numbers each ===
  group 1    account, password, phone, email, router, radiator
  group 2    frost, wake, warm, sunrise, early
  group 3    heat, temperature, app, schedule, boiler
  warm and wake        2° apart
  warm and password  133° apart

=== All 235 words: two numbers each ===
  warm       network, protection, for, 510, while
  password   your, android, can, members, between
```

On the 16 words it works: signing in, Warm Wake with *frost*, and *heat* with the schedule and the app. It isn't perfect. *router* and *radiator* join the sign-in words, and *radiator* is only 0.23 from the middle, so its direction means little. Open `demo/output/03_word_map.json` to see every word's two numbers, its length and its angle, for both maps.

One problem from section 2 does go away. In the map of all 235 words, *the* is 0.003 from the middle and *and* 0.009. They turn up near everything, so they point nowhere and can't get in the way.

**Why this breaks:**

- **It only works on words we picked.** We chose 16 words from three topics, so three directions were enough. Give all 235 words two numbers each and the map holds nothing clear: the words pointing the same way as *warm* are *network*, *protection*, *for*, *510* and *while*.
- **One vector per word.** Our question is 11 words, and a document is hundreds. A search needs one vector for the whole thing.

## 4. Sentences from words

**Demo:** `demo/04_sentence_vectors.py`

Section 3 gave every word two numbers. Our question is 11 words, and a document is hundreds, and a search needs one vector for each. The simplest way to get one: **add up** the vectors of its words. A word that isn't on the map adds nothing.

```python
def sentence_vector(text, word_vectors):
    known = [word_vectors[w] for w in words(text) if w in word_vectors]
    return [sum(column) for column in zip(*known)]
```

`zip(*known)` lines up every word's first number, then every word's second number, so a sentence gets two numbers, like each of its words. The demo reads them from demo 3's map of all 235 words, so run demo 3 first.

On the map of 16 words you can watch it happen. Put the arrows for *warm*, *wake* and *early* tip to tail: where the last one ends is their sum, an arrow pointing the way its words point. *frost*, *sunrise* and *heat* share none of its words, but they add up to an arrow only 12° away, a similarity of 0.98. *email*, *password* and *account* add up to an arrow pointing 134° away, a similarity of −0.69. (That's on the slide, with the 16 words. The demo uses the map of all 235.)

Two sentences are then compared the way demo 2 compared two words, with **cosine similarity**, the cosine of the angle between their arrows:

```python
def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    length_a = math.sqrt(sum(x * x for x in a))
    length_b = math.sqrt(sum(y * y for y in b))
    return dot / (length_a * length_b)
```

`dot` is the **dot product**: multiply the two vectors number by number and add up. It's large when both have big numbers in the same places with the same signs. Dividing by the two lengths means only the direction counts, and with sums that matters: a document of 300 words adds up to a far longer arrow than a question of 11, and it shouldn't win for being long. It also means the **sum** and the **average** give the same answer: dividing by the number of words changes an arrow's length, not its direction.

The demo compares three pairs of sentences, then ranks the user guide's 26 sections and all 275 documents against the question, as demo 1 did:

```text
=== Two sentences at a time ===
   0.975  Warm Wake starts the heating early
          Frost protection turns the heating on
  -0.605  Warm Wake starts the heating early
          Reset your password by email
   1.000  The heating is off and frost protection is on
          The heating is on and frost protection is off

=== The user guide: 26 sections ===
Q: Why is the heating already on before my alarm goes off?
  0.991  customer  Energy reports
  0.971  customer  Backup batteries
  0.956  customer  The boost button

=== All the documentation: 275 documents ===
Q: Why is the heating already on before my alarm goes off?
  1.000  customer  Thermostat Shows E-217
  1.000  internal  Backup Battery Support Playbook
  0.999  customer  Understand error E-217: Temperature sensor disconnected
```

The pairs come out well. Two sentences that both turn the heating on score 0.975, and heating against a password reset scores −0.605, pointing almost opposite ways. On the map of all 235 words, the heating words happen to point one way (*warm* at 268°, *frost* at 258°, *heating* at 327°) and the sign-in words another (*password* and *your* at 140°, *email* at 160°), so their sums do too. The third pair, opposite meanings in the same words, scores 1.000; section 5 comes back to it.

The question goes badly. Energy reports, backup batteries and an error code come first:

| Where "Warm Wake" came | Keyword search | Two numbers, added up |
|------------------------|----------------|-----------------------|
| The user guide, 26 sections | 1st | 9th |
| All the documentation, 275 documents | 142nd | 71st |

Only 6 of the question's 11 words are on the map, "is, the, heating, on, before, off". "Why, already, my, alarm" and "goes" aren't among the user guide's 235 words. Open `demo/output/04_sentence_vectors.json` to see every section and document ranked, the question's two numbers and the words it lost.

**Why this breaks:**

- **Two numbers are too few.** With two numbers, every text is just a direction round a circle, and 275 documents share 360°. 19 of them are within 8° of the question, a similarity of 0.99 or more, so the order among them means almost nothing. The pairs only worked because their words happen to point different ways.
- **Every pair, first.** Before anything moves, the map compares every word with every other: 27,495 pairs for 235 words, and about 5 billion for a vocabulary of 100,000. More text means counting and comparing all over again.

We need more numbers per word, learned straight from the text.

## 5. Build an embeddings model

**Demo:** `demo/05_word_vectors.py`

Counting gives every word one number per vocabulary word, mostly zeros. The map squeezed those into two, which are too few, and had to compare every pair of words first. **word2vec** (Mikolov and others, 2013) learns a short list instead, straight from the text: here 20 numbers per word, all of them used.

### How to build one

Nobody writes down what words mean. Instead you set the model a guessing game that it can only win by giving similar words similar numbers, and let the numbers learn. word2vec's game is: **given two words, guess whether they appear near each other.** Two words that keep the same company have to make the same guesses, so they end up with similar numbers.

We build one live, in plain Python, from the user guide, in five steps.

1. **Choose the words.** The same 235 words as section 2: every word in the guide that appears at least twice (`MIN_COUNT`). A word seen only once can't teach the model anything.

2. **Start with random numbers.** Give every word a list of 20 random numbers (`SIZE`). This is its **vector**: the embedding we're building. Each word also gets a second list, used when it's another word's neighbour, which starts at zero.

3. **Make examples from the text.** Go through the guide word by word. Every word up to 3 places away (`WINDOW`) is a real neighbour, and the right answer for that pair is 1. Here are the real neighbours of *wake* in "...for your postcode. While Warm Wake is heating early, the display shows the sunrise symbol":

   ```text
   wake: your, while, warm, is, heating, early
   ```

   The window doesn't stop at full stops, so *your* from the sentence before counts. For every real pair, also pick 5 words at random (`NEGATIVES`). They're almost never real neighbours, so the right answer is 0. In the first pass, the random words for *wake* and *warm* were *connected, guide, current, frost* and *not*. One pass through the guide makes 9,498 real pairs and 47,490 random ones.

4. **Guess, and nudge.** For each pair, multiply the two words' numbers together and add them up: the bigger the total, the more the model thinks they're neighbours. `sigmoid` squashes the total into a guess between 0 and 1. At the very start, every guess is 0.5, because the second lists are all zero: the model knows nothing. The **error** is the right answer minus the guess. Both lists of numbers move a little in the direction that would have shrunk the error, more when the guess was further off:

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

5. **Repeat.** 30 passes through the guide (`EPOCHS`), about 1.7 million guesses, take about 11 seconds. Afterwards the model guesses 0.92 that *warm* appears near *wake*, and 0.00 that it appears near *password*.

The lists from step 2 are now the embeddings. This recipe is **skip-gram with negative sampling**: "skip-gram" for guessing a word's neighbours, "negative sampling" for the random words. Module 1's network learned its embeddings as a side effect of predicting the next token. This model has no other job.

The demo prints the five closest words to the same words as demo 2:

```text
=== Trained on the user guide: 1,794 words, 235 different words ===
  warm       wake, sunrise, heat, early, power
  password   sign, network, link, account, cleaning
  heating    hours, switch, early, protection, for
  alarm      never seen
```

Open `demo/output/05_word_vectors.txt` to see all 235 words and their 20 numbers. Set beside counting:

| | Counting (demo 2) | word2vec (demo 5) |
|---|---|---|
| *warm* | wake, sunrise, early, heat, is | wake, sunrise, heat, early, power |
| *password* | link, schedules, your, choose, and | sign, network, link, account, cleaning |
| *heating* | thermostat, when, temperature, and, dial | hours, switch, early, protection, for |
| Numbers per word | 235, mostly zeros | 20 |
| Time | A fraction of a second | About 11 seconds |

On this little text, word2vec's neighbours are no better than counting's: better for *password*, worse for *heating*. What it gains is size: 20 numbers instead of 235, and the gap grows with the vocabulary. The two methods are closer than they look. Levy and Goldberg (2014) showed that word2vec is, in effect, counting neighbours, weighting the counts and squeezing the result into a short list.

### The question again

Then the demo adds up the question and every document, as demo 4 did, but with word2vec's 20 numbers per word instead of the map's two:

```text
=== The user guide: 26 sections ===
Q: Why is the heating already on before my alarm goes off?
  0.930  customer  Frost protection
  0.875  customer  Symbols on the display
  0.842  customer  Warm Wake

=== All the documentation: 275 documents ===
Q: Why is the heating already on before my alarm goes off?
  0.918  customer  Understand frost protection
  0.896  customer  Heating Starts Below Five Degrees
  0.882  customer  Understand the thermostat display symbols
```

| Where "Warm Wake" came | Keyword search | Two numbers, added up | 20 numbers, added up |
|------------------------|----------------|-----------------------|----------------------|
| The user guide, 26 sections | 1st | 9th | 3rd |
| All the documentation, 275 documents | 142nd | 71st | 8th |

It does worse than keyword search on the small library, and far better on the large one. The documents that beat it are about frost protection, which turns the heating on when the heating is off. That's close to what is left of the question: the same 6 of its 11 words as in demo 4, since both know the same 235 words. Open `demo/output/05_question.json` to see every section and document ranked.

**Why this breaks:**

- **Too little text.** *Heating* is closest to *hours*, *switch* and *for*: 1,794 words isn't enough to say much about a word that appears everywhere. Models people use are trained on billions of words.
- **A word it has never seen adds nothing.** Every method so far only has numbers for the 235 words that appear at least twice. "Alarm", the word our question turns on, isn't in the guide at all.
- **Word order is lost.** "The heating is off and frost protection is on" and "The heating is on and frost protection is off" mean opposite things, and scored 1.000 in demo 4. The same words add up to the same sum, in any order, whatever numbers the words have.
- **Every word gets an equal vote.** *The* counts as much as *heating*, and two of the six words the question kept are *is* and *the*.

We need a model that reads the whole text, in order, and has learned from far more of it.

## 6. A commercial embedding model

**Demo:** `demo/06_similarity_search.py`

The better way is a model trained to embed whole passages. OpenAI's `text-embedding-3-small` turns any text up to 8,191 tokens (about 6,000 words) into 1,536 numbers. It reads the text as a whole, word order included, and was trained on far more text than our 1,794 words. It's a different endpoint from the Responses API used everywhere else in the course:

```python
response = client.embeddings.create(model="text-embedding-3-small", input=texts)
vectors = [item.embedding for item in response.data]
```

One call can embed many texts. No single one of the 1,536 numbers means anything you could name, but texts that mean similar things point the same way, so the search works as in demos 4 and 5: the same `cosine_similarity`, in a space with 1,536 directions instead of 2 or 20. (OpenAI's vectors have length 1, or very nearly, so for them the dot product alone gives almost the same order: the `distance-measures` playground finds the same top seven, then two documents that tie to three decimal places swap. On word counts, where lengths vary a lot, the measures disagree completely.)

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

| Where "Warm Wake" came | Keyword search | Two numbers, added up | 20 numbers, added up | `text-embedding-3-small` |
|------------------------|----------------|-----------------------|----------------------|--------------------------|
| The user guide, 26 sections | 1st | 9th | 3rd | 1st |
| All the documentation, 275 documents | 142nd | 71st | 8th | 1st |

One question isn't proof. The `what-to-embed` playground runs this search for the 20 questions in `data/questions.json`, all in customers' own words: a right document comes in the top five for 19 of them.

**Why this breaks:**

- **It finds the document, not the answer.** The customer asked why the heating comes on early. The answer is in the Warm Wake document: it heats ahead of a schedule period, and shows a sunrise symbol while it does. Reading the right document and answering from it is **retrieval-augmented generation** (RAG), in Module 6.
- **It embeds everything, every time.** Each run sends all 275 documents (179,993 tokens) to the API again, and the vectors vanish when the script ends.
- **It compares the question with every document.** 275 comparisons is nothing, but a company's documents, tickets and emails could run to millions.
- **It can't filter.** 41 of the documents are internal, written for staff. A search for customers must never return them, and here nothing stops it.

The last three are what a **vector database** is for. Module 6 keeps its vectors in one, ChromaDB.

---

## Summary

| Step | Finds by | Problem |
|------|----------|---------|
| 1. Keyword search | Shared words, rare ones counting more | Matches words, not meaning |
| 2. Embeddings | Words used in the same places, counted | 235 numbers per word, mostly zeros; on a line, one place per word |
| 3. A map of meaning | The direction from the middle, two numbers per word | Only works on words we picked; one vector per word |
| 4. Sentences from words | The angle between sums of the map's word vectors | Two numbers can't tell documents apart; compares every pair first |
| 5. Build an embeddings model | Words used in the same places, learned in 20 numbers, then added up | Too little text; loses word order; every word counts the same; unknown words add nothing |
| 6. A commercial embedding model | The angle between vectors from a model trained on whole passages | Finds the document, not the answer; embeds and compares everything, every time; can't filter |

## Playground

[`playground/`](playground/) has six things to play with: the word2vec model with its settings exposed, a similarity explorer, distance measures compared, what to embed, searching in other languages, and shrinking the vectors.

## Further reading and extensions

The final exercise is in [`further-reading/`](further-reading/): papers on keyword ranking, counted and learned word vectors, spectral clustering, sentence embeddings and smaller vectors, with a note on what to look for in each and which demo it relates to, plus extension projects to take home.

## Slides

```bash
pnpm slides:05
```
