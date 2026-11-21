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
      subtitle: 'Finding the right information by meaning',
      icon: 'search',
    },
  },
  {
    type: 'description',
    content: {
      title: 'The question',
      icon: 'question',
      description:
        'Dormouse has **275 documents**: a user guide, support and troubleshooting articles, policies, and internal notes for staff. A customer asks: *"Why is the heating already on before my alarm goes off?"* The answer is in there somewhere. **How do we find it?**',
    },
  },
  {
    type: 'code',
    content: {
      title: 'The data',
      code: `---
title: Understand Warm Wake
product: thermostat
type: support
audience: customer
---

# Understand Warm Wake

## What Warm Wake does

Warm Wake is a heating feature that starts the heating
before a schedule period. ...`,
      highlights: [
        '**Dormouse**: a smart thermostat, invented for this course',
        'The **user guide**, written by hand: 26 sections, 1,794 words',
        '275 documents in all: **234 for customers, 41 internal**',
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
    type: 'standard',
    content: {
      title: 'What is keyword search?',
      icon: 'search',
      points: [
        'Find the documents that **contain the words** you typed',
        'The oldest way to search, and still everywhere: websites, email, Elasticsearch, SQLite',
        'No model, no API, and **fast**',
        'The question: which documents come **first**?',
      ],
    },
  },
  {
    type: 'code',
    content: {
      title: 'How it works',
      code: `1. Split into words
   "Why is the heating already on before my alarm goes off?"
   → why, is, the, heating, already, on, before, my, alarm, goes, off

2. Build an index: each word → the documents that contain it
   geofencing → away-mode-and-geofencing-qa-report (18)
                set-up-geofencing (16)
                phone-location-privacy-policy (15)
                ... 37 documents in all

3. Score every document with a question word, and sort`,
      highlights: [
        '**Lower case**, letters and digits only. Real engines also cut words to their root',
        'An **inverted index**: like the index of a book, look up a word, get the pages',
        'Counting matches isn\'t enough: **"the" is in all 275 documents**',
      ],
    },
  },
  {
    type: 'equation',
    content: {
      title: 'BM25: the idea',
      mathml: `<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
  <mtext>score</mtext>
  <mo>=</mo>
  <munder><mo>∑</mo><mtext>question words</mtext></munder>
  <mtext>rarity</mtext>
  <mo>×</mo>
  <mtext>matches</mtext>
</math>`,
      points: [
        '**Rarity**: "the", in all 275 documents, 0.002; "geofencing", in 37, 2.00',
        '**Matches**: one mention scores 1.00, two 1.43, ten 2.17, never more than **2.5**',
        '**Length**: one mention scores 1.29 at half the average length, 0.69 at double',
      ],
      credit:
        'Robertson & Zaragoza (2009). "The Probabilistic Relevance Framework: BM25 and Beyond." Foundations and Trends in Information Retrieval 3(4)',
    },
  },
  {
    type: 'code',
    content: {
      title: 'BM25',
      code: `for word in set(words(question)):
    if word not in counts:
        continue
    rarity = math.log(1 + (len(texts) - appears_in[word] + 0.5)
                          / (appears_in[word] + 0.5))
    count = counts[word]
    score += rarity * count * (K1 + 1) / (
        count + K1 * (1 - B + B * len(text) / average_length))`,
      highlights: [
        '`rarity`: large when `appears_in[word]`, the number of documents with the word, is small',
        '`K1` (1.5): how fast repeats level off. The most a word can add is `K1 + 1` times its rarity',
        "`B` (0.75): how much a document's length counts against it",
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
      code: `=== The user guide: 26 sections ===
   7.64  Warm Wake
   6.98  Frost protection
   4.62  Energy reports

=== All the documentation: 275 documents ===
   7.02  Enter your boiler size for energy reports
   6.82  Web dashboard: Household screen guide
   6.56  Web dashboard: Energy screen guide`,
      highlights: [
        'User guide: Warm Wake is the only section that says **"already"**',
        'All 275 documents: Warm Wake comes **142nd**',
        '"why" is in 7 documents, "goes" in 1, **"alarm" in none**',
        'Keyword search matches **words, not meaning**',
      ],
    },
  },

  // ---- Section 2: Build an embeddings model ----
  {
    type: 'title',
    content: {
      title: '2. Build an embeddings model',
      subtitle: 'Words used in the same places',
      icon: 'brain',
    },
  },
  {
    type: 'standard',
    content: {
      title: 'What is an embedding?',
      icon: 'layers',
      points: [
        'A **vector**: a list of numbers that stands for a piece of text',
        'Texts that **mean** similar things get vectors that point the same way',
        'Module 1: 16 numbers per token, learned as a **side effect**',
        '**word2vec**: learn them on purpose, from the words around each word',
      ],
      credit:
        'Mikolov et al. (2013). "Efficient Estimation of Word Representations in Vector Space." arXiv:1301.3781',
    },
  },
  {
    type: 'standard',
    content: {
      title: 'How to build one',
      icon: 'wrench',
      points: [
        'The game: **are these two words near each other?**',
        '1. Keep the words that appear at least twice: **235**',
        '2. Give each word **20 random numbers**: its vector',
        '3. Make examples: real neighbours (1) and random words (0)',
        '4. Guess, compare with the answer, and **nudge the numbers**',
        '5. Repeat: 30 passes through the user guide',
      ],
    },
  },
  {
    type: 'code',
    content: {
      title: 'Step 3: examples from the text',
      code: `"... for your postcode. While Warm Wake is heating early,
 the display shows the sunrise symbol."

Real neighbours of "wake", up to 3 words either side:
  wake → your, while, warm, is, heating, early          answer 1

5 random words for each real pair (wake + warm, first pass):
  wake → connected, guide, current, frost, not          answer 0`,
      highlights: [
        'One pass through the guide: **9,498 real pairs**, 47,490 random ones',
        'Random words are almost never real neighbours',
        'The window ignores full stops: *your* comes from the sentence before',
      ],
    },
  },
  {
    type: 'code',
    content: {
      title: 'Step 4: guess, and nudge',
      code: `samples = [(tokens[j], 1)] + [(random.choice(noise), 0)
                              for _ in range(NEGATIVES)]
for other, is_neighbour in samples:
    neighbour = neighbours[other]
    guess = sigmoid(sum(a * b for a, b in zip(vector, neighbour)))
    error = is_neighbour - guess
    for k in range(SIZE):
        change[k] += rate * error * neighbour[k]
        neighbour[k] += rate * error * vector[k]`,
      highlights: [
        'Multiply and add: the bigger the total, the more it thinks **neighbours**',
        '`sigmoid` turns that into a guess from 0 to 1. At the start, every guess is **0.5**',
        '`error` = answer − guess: **nudge both** words, more when the guess was further off',
        'Skip-gram with negative sampling: 30 passes, **1.7 million guesses**, about 11 seconds',
      ],
    },
  },
  {
    type: 'title',
    content: {
      title: 'Demo — Build an embeddings model',
      subtitle: 'Switch to terminal: python demo/02_word_vectors.py',
      icon: 'rocket',
    },
  },
  {
    type: 'code',
    content: {
      title: 'The closest words',
      code: `=== Trained on the user guide: 1,794 words, 235 different words ===
  warm       wake, sunrise, heat, early, power
  password   sign, network, link, account, cleaning
  heating    hours, switch, early, protection, for
  alarm      never seen`,
      highlights: [
        'Nobody told it what any word means',
        '*warm* → *wake*, *sunrise*, *early*: words the guide **uses together**',
        'Every word and its 20 numbers: `demo/output/02_word_vectors.txt`',
      ],
    },
  },
  {
    type: 'description',
    content: {
      title: 'Why this breaks',
      icon: 'warning',
      description:
        '*Heating* is closest to *hours*, *switch* and *for*: **1,794 words is far too little text**. The model only knows the **235 words** that appear twice, and **"alarm" isn\'t one of them**. And it gives one vector **per word**: our question is 11 words, and a document is hundreds.',
    },
  },

  // ---- Section 3: Turn a document into numbers ----
  {
    type: 'title',
    content: {
      title: '3. Turn a document into numbers',
      subtitle: 'One vector for a whole text',
      icon: 'hash',
    },
  },
  {
    type: 'comparison',
    content: {
      title: 'Two ways',
      left: {
        label: 'Average our word vectors',
        code: `known = [word_vectors[w]
         for w in words(text)
         if w in word_vectors]
vector = [sum(column) / len(known)
          for column in zip(*known)]`,
      },
      right: {
        label: 'An embeddings model',
        code: `response = client.embeddings.create(
    model="text-embedding-3-small",
    input=texts,
)
vectors = [item.embedding
           for item in response.data]`,
      },
    },
  },
  {
    type: 'standard',
    content: {
      title: 'text-embedding-3-small',
      icon: 'layers',
      points: [
        'Trained to embed **whole passages**, word order included',
        'Up to 8,191 tokens in, **1,536 numbers** out',
        'A separate **embeddings** endpoint, not the Responses API',
        'All 275 documents: 179,993 tokens, **under half a cent**',
      ],
    },
  },
  {
    type: 'title',
    content: {
      title: 'Demo — Turn a document into numbers',
      subtitle: 'Switch to terminal: python demo/03_document_vectors.py',
      icon: 'rocket',
    },
  },
  {
    type: 'code',
    content: {
      title: 'The numbers',
      code: `=== Our model: the average of the word vectors ===
  Q: Why is the heating already on before my alarm goes off?
    20 numbers: [-0.61, -0.77, 0.33, 0.24, -0.31, 0.08, ...]
    left out 5 words it has never seen: alarm, already, goes, my, why
  Understand Warm Wake
    20 numbers: [-0.55, -0.97, 0.08, 0.21, -0.22, -0.23, ...]

=== text-embedding-3-small ===
  Q: Why is the heating already on before my alarm goes off?
    1,536 numbers: [-0.0109, 0.0147, -0.0659, -0.0318, ...]
  Understand Warm Wake
    1,536 numbers: [-0.0090, 0.0321, -0.0258, 0.0117, ...]`,
      highlights: [
        'Our model kept 6 of 11 words: **is, the, heating, on, before, off**',
        'Averaging also **loses the word order**',
        'No single number means anything you could name',
      ],
    },
  },
  {
    type: 'description',
    content: {
      title: 'Why this breaks',
      icon: 'warning',
      description:
        "Which document is closer to the question: **Warm Wake**, or keyword search's winner, **boiler size**? Look at the numbers: **you can't tell**. A list of numbers doesn't find anything on its own. We need a way to **measure** how close two vectors are.",
    },
  },

  // ---- Section 4: Find by similarity ----
  {
    type: 'title',
    content: {
      title: '4. Find by similarity',
      subtitle: 'The angle between two vectors',
      icon: 'compass',
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
        '1 means the same direction, 0 unrelated, −1 opposite',
        "Divide by the lengths: a long document **doesn't win by being long**",
      ],
    },
  },
  {
    type: 'code',
    content: {
      title: 'Search by similarity',
      code: `def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    length_a = math.sqrt(sum(x * x for x in a))
    length_b = math.sqrt(sum(y * y for y in b))
    return dot / (length_a * length_b)

results = sorted(
    ((cosine_similarity(question_vector, v), d)
     for v, d in zip(vectors, library)),
    key=lambda r: r[0], reverse=True)`,
      highlights: [
        '`dot`: multiply number by number, and add up',
        'Embed every document and the question, then **sort**',
        "OpenAI's vectors have length 1, near enough: `dot` alone gives **almost** the same order",
      ],
    },
  },
  {
    type: 'title',
    content: {
      title: 'Demo — Find by similarity',
      subtitle: 'Switch to terminal: python demo/04_similarity_search.py',
      icon: 'rocket',
    },
  },
  {
    type: 'code',
    content: {
      title: 'By meaning',
      code: `=== The user guide: 26 sections ===
  0.618  customer  Warm Wake
  0.420  customer  Boost
  0.408  customer  The boost button

=== All the documentation: 275 documents ===
  0.488  customer  Understand Warm Wake
  0.455  customer  Heating Starts Below Five Degrees
  0.427  customer  Set a heating schedule`,
      highlights: [
        'Warm Wake is **first**, in both libraries',
        'It shares only "heating" and "before": so do **100 other documents**',
        '0.488 sounds low: similarities only mean something **next to each other**',
      ],
    },
  },
  {
    type: 'comparison',
    content: {
      title: 'Where Warm Wake came',
      left: {
        label: 'Keyword search',
        items: ['User guide, 26 sections: **1st**', 'All 275 documents: **142nd**'],
      },
      right: {
        label: 'Cosine similarity',
        items: ['User guide, 26 sections: **1st**', 'All 275 documents: **1st**'],
      },
    },
  },
  {
    type: 'description',
    content: {
      title: 'Why this breaks',
      icon: 'warning',
      description:
        "Every run sends **all 275 documents** to the API again, and the vectors vanish when the script ends. Every search **compares with every document**: fine for 275, not for millions. And there's **no filter**: 41 documents are internal, and nothing stops a customer seeing them.",
    },
  },

  // ---- Section 5: A vector database ----
  {
    type: 'title',
    content: {
      title: '5. A vector database',
      subtitle: 'Store once, search fast, filter',
      icon: 'database',
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
    "dormouse-docs",
    configuration={"hnsw": {"space": "cosine"}},
    embedding_function=None,
)`,
      highlights: [
        'Runs inside our script: one folder, **9.7 MB** for 275 documents',
        'A **collection** is like a table. Compare by **cosine**',
        "`embedding_function=None`: **our** vectors, not Chroma's own model",
        'Telemetry off: no usage statistics sent',
      ],
    },
  },
  {
    type: 'code',
    content: {
      title: 'Store once, search with a filter',
      code: `collection.upsert(
    ids=[d["id"] for d in changed],
    embeddings=embed([d["text"] for d in changed]),
    documents=[d["text"] for d in changed],
    metadatas=[{"title": ..., "audience": ..., "checksum": ...}],
)

collection.query(query_embeddings=[vector], n_results=3,
                 where={"audience": "customer"})`,
      highlights: [
        '**Metadata**: facts about each document, to filter by',
        'A **checksum** of the text: embed only what has changed',
        '`where`: search only documents whose metadata matches',
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
        '**Approximate**: very occasionally it misses a slightly closer one',
      ],
      credit:
        'Malkov & Yashunin (2018). "Efficient and Robust Approximate Nearest Neighbor Search Using Hierarchical Navigable Small World Graphs." arXiv:1603.09320',
    },
  },
  {
    type: 'title',
    content: {
      title: 'Demo — A vector database',
      subtitle: 'Switch to terminal: python demo/05_vector_database.py',
      icon: 'rocket',
    },
  },
  {
    type: 'code',
    content: {
      title: 'Stored once, and filtered',
      code: `Stored 0 new or changed documents in chroma/

Q: Why is the heating already on before my alarm goes off?  (customers only)
  0.487  customer  Understand Warm Wake

Q: My thermostat makes a clicking noise  (every document)
  0.520  internal  Relay click on hardware revision C
  0.440  customer  Thermostat Does Not Respond to Dial Changes

Q: My thermostat makes a clicking noise  (customers only)
  0.440  customer  Thermostat Does Not Respond to Dial Changes
  0.424  customer  Thermostat Shows the Wrong Room Temperature`,
      highlights: [
        'Second run: **0** documents embedded',
        'Every document: an **internal engineering note** comes first',
        "Customers only: the note **can't come back**",
      ],
    },
  },
  {
    type: 'description',
    content: {
      title: 'Why this breaks',
      icon: 'warning',
      description:
        'The customer asked **why** the heating comes on early. We found the right document, and the answer is inside it. **Reading it and answering is Module 6: RAG.** And the search **always returns something**: no customer document is about the click, but we still got three.',
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
        '**Keyword search**: shared words, not meaning',
        '**An embeddings model**: words used together, but too little text',
        '**A document as numbers**: an average, or a model trained on passages',
        '**Similarity search**: the right document first, by meaning',
        '**A vector database**: stored once and filtered, but no answers',
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'What we learned',
      icon: 'award',
      points: [
        'An **embedding** turns text into a vector: close vectors, similar meaning',
        'Embeddings are learned from **where words are used**',
        '**Cosine similarity** compares directions, not lengths',
        'A **vector database** stores vectors with metadata to filter on',
        "Similarity **ranks**: it can't say that nothing fits",
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'Final exercise: further reading',
      icon: 'book',
      points: [
        '**Spärck Jones (1972)**: why rare words count for more',
        '**Mikolov et al. (2013)**: word2vec, the model we built',
        '**Reimers & Gurevych (2019)**: one vector for a whole sentence',
        'Pick a paper, connect it to a demo, then start an extension',
        'Everything is in `further-reading/`',
      ],
    },
  },
];
