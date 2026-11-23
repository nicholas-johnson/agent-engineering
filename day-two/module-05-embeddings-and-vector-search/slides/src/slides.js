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
      title: 'Dormouse',
      icon: 'question',
      description: `Dormouse is a fake company, making AI-controlled thermostats. It has **275 documents** across a wide range of functions. 
        
        Here, I've modelled these as markdown files, but in reality these might be Confluence docs, Office 365, Jira, Support tickets, etc. We have a fake user guide, support and troubleshooting articles, policies, and internal notes for staff. 
        
        A customer asks a question. The answer is in there somewhere. **How do we find it?**`,
    },
  },
  {
    type: 'code',
    content: {
      title: 'The data looks like this:',
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
        'The **user guide** has 26 sections, 1,794 words',
        '275 documents in all: **234 for customers, 41 internal**',
        'How to search it?',
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
        'No model, no API, and **fast**',
        'Which documents match, and in what order?',
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'Build the index',
      icon: 'book',
      points: [
        '1. **Split** every document into words: lower case, letters and digits only',
        '2. **Build an inverted index**: each word points to the documents that contain it, and how many times. Like the index of a book',
        "3. Note each document's length",
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'For each question',
      icon: 'search',
      points: [
        '1. **Split** the question the same way: *why, is, the, heating, already, on, before, my, alarm, goes, off*',
        '2. **Look up** each word in the index: the documents that contain it',
        '3. **Score**: each word adds to the score of every document that contains it. **Rare** words add more, each extra **mention** adds less, and **long** documents get less',
        "4. **Add up** each document's total, and **sort**, best first",
        '"the" is in all 275 documents, so it adds **almost nothing**',
      ],
    },
  },
  {
    type: 'equation',
    content: {
      title: 'BM25',
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
    type: 'title',
    content: {
      title: 'Demo — Keyword search',
      subtitle: 'Switch to terminal: python demo/01_keyword_search.py',
      icon: 'rocket',
    },
  },
  {
    type: 'description',
    content: {
      title: 'Why this breaks',
      icon: 'warning',
      description: `The question may not use the same words as the answer. The customer asks about the heating coming on **"before my alarm goes off"**. The answer, *Understand Warm Wake*, says it **"starts the heating before a schedule period"**.

        "alarm" is in **none** of the 275 documents, so it adds nothing. Across all the documentation, the answer comes **142nd**. In the user guide, Warm Wake came first only because it is the one section that says **"already"**.

        Keyword search matches **words, not meaning**.`,
    },
  },

  // ---- Section 2: Embeddings ----
  {
    type: 'title',
    content: {
      title: '2. Embeddings',
      subtitle: 'Grouping words that mean the same',
      icon: 'calculator',
    },
  },
  {
    type: 'standard',
    content: {
      title: 'What is an embedding?',
      icon: 'layers',
      points: [
        'A **vector**: a list of numbers that stands for a piece of text',
        'Words that **mean** similar things get vectors that point the same way',
      ],
      credit: 'Harris (1954). "Distributional Structure." Word 10(2–3):146–162',
    },
  },
  {
    type: 'code',
    content: {
      title: 'Count the neighbours',
      code: `vectors = [[0] * len(vocabulary) for _ in vocabulary]
for i, word in enumerate(tokens):
    for j in range(max(0, i - WINDOW), min(len(tokens), i + WINDOW + 1)):
        if j != i:
            vectors[word][tokens[j]] += 1`,
      highlights: [
        '1. Keep the words that appear at least twice: **235**',
        '2. For each word, count every word up to **3 places away**',
        "3. Each **row** is a word's vector: 235 numbers",
      ],
    },
  },
  {
    type: 'code',
    content: {
      title: 'Neighbouring words tend to be related',
      code: `=== Counted in the user guide: 1,794 words, 235 different words ===
  warm       wake, sunrise, early, heat, is
  password   link, schedules, your, choose, and
  heating    thermostat, when, temperature, and, dial
  alarm      never seen`,
      highlights: [
        "*warm*'s row: *wake* 10, *is* 4, *the* 3, *heating* 3, *sunrise* 2, ...",
        `Nobody told it what any word means. It's just looking for words that tend to be found together.`,
      ],
    },
  },
  {
    type: 'word-line',
    content: {
      title: 'The counts on a line',
      // From "picked" in demo/output/02_word_line.json, written by demo/02_count_vectors.py.
      words: {
        sunrise: -0.43,
        wake: -0.39,
        warm: -0.35,
        early: -0.18,
        frost: -0.17,
        heat: -0.12,
        temperature: 0.03,
        app: 0.08,
        schedule: 0.09,
        router: 0.12,
        boiler: 0.13,
        radiator: 0.22,
        account: 0.25,
        password: 0.25,
        phone: 0.3,
        email: 0.39,
      },
      steps: [
        {
          caption: 'Sixteen words from the user guide, in **alphabetical order**',
        },
        {
          caption:
            '**One number each**: every word pulled towards the words it is most like',
          placed: true,
        },
        {
          caption: "Warm Wake's words end up **together**",
          highlight: ['sunrise', 'wake', 'warm', 'early', 'heat'],
        },
        {
          caption: 'Signing in is at the **other end**',
          highlight: ['phone', 'email', 'account', 'password'],
        },
        {
          caption: 'But **boiler** is closer to **password** than to **heat**',
          highlight: ['boiler', 'password', 'heat'],
        },
      ],
      note: 'We picked the 16 words. Each starts anywhere and moves, again and again, halfway towards the others, weighted by how alike their counts are (spectral ordering).',
    },
  },
  {
    type: 'title',
    content: {
      title: 'Demo — Embeddings',
      subtitle: 'Switch to terminal: python demo/02_count_vectors.py',
      icon: 'rocket',
    },
  },
  {
    type: 'description',
    content: {
      title: 'Why this breaks',
      icon: 'warning',
      description: `We have assigned one number per word so they fit on a line. This means that words that want to be in two places have no way to do this.
        
        What if we increased the number of vector dimensions to 2?`,
    },
  },

  // ---- Section 3: A map of meaning ----
  {
    type: 'title',
    content: {
      title: '3. A map of meaning',
      subtitle: 'Two numbers per word',
      icon: 'map',
    },
  },
  {
    type: 'standard',
    content: {
      title: 'Two numbers per word',
      icon: 'compass',
      points: [
        'The same pull as the line, on **two lines at once**',
        'The second line is kept **at right angles** to the first',
        'Each word is a **point on a map**, and the middle is the average word',
        'An arrow from the middle: its **direction** says what the word is like',
      ],
    },
  },
  {
    type: 'word-map',
    content: {
      title: 'The map',
      // From demo/output/03_word_map.json, written by demo/03_word_map.py.
      words: {
        account: [0.25, 0.09],
        password: [0.25, 0.126],
        phone: [0.295, 0.223],
        email: [0.394, 0.379],
        router: [0.118, 0.512],
        frost: [-0.171, 0.443],
        wake: [-0.392, 0.159],
        warm: [-0.351, 0.128],
        sunrise: [-0.43, 0.048],
        early: [-0.179, -0.079],
        heat: [-0.12, -0.156],
        temperature: [0.035, -0.249],
        app: [0.084, -0.305],
        schedule: [0.091, -0.281],
        boiler: [0.125, -0.108],
        radiator: [0.221, -0.06],
      },
      groups: {
        account: 1,
        password: 1,
        phone: 1,
        email: 1,
        router: 1,
        radiator: 1,
        frost: 2,
        wake: 2,
        warm: 2,
        sunrise: 2,
        early: 2,
        heat: 3,
        temperature: 3,
        app: 3,
        schedule: 3,
        boiler: 3,
      },
      steps: [
        { caption: 'Sixteen words, **two numbers each**' },
        {
          caption:
            'An **arrow** from the middle. Short ones, like *boiler*, point nowhere much',
          arrows: true,
        },
        {
          caption: '**Only the direction counts**: push every word out to the circle',
          circle: true,
        },
        {
          caption: '**Three groups** by direction: signing in, Warm Wake, the schedule',
          grouped: true,
        },
        {
          caption: '*warm* and *wake*: **2°** apart, a similarity of **1.00**',
          angle: ['warm', 'wake'],
          highlight: ['warm', 'wake'],
        },
        {
          caption: '*warm* and *password*: **133°** apart, a similarity of **−0.68**',
          angle: ['warm', 'password'],
          highlight: ['warm', 'password'],
        },
      ],
      note: 'The same 16 words as the line. The first number is the line from section 2; the second is a line at right angles to it. Groups found by k-means.',
    },
  },

  {
    type: 'equation',
    content: {
      title: 'The angle says how alike',
      mathml: `<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
  <mtext>similarity</mtext>
  <mo>=</mo>
  <mi>cos</mi>
  <mo>(</mo>
  <mtext>angle</mtext>
  <mo>)</mo>
</math>`,
      points: [
        '**1** for the same direction, **0** at right angles, **−1** opposite',
        'This is **cosine similarity**: demo 2 used it to find the closest words',
        'On the circle, distance² = 2 − 2 × similarity: grouping by distance **is** grouping by angle',
      ],
      credit:
        'Ng, Jordan & Weiss (2001). "On Spectral Clustering: Analysis and an algorithm." NIPS 14:849–856',
    },
  },
  {
    type: 'title',
    content: {
      title: 'Demo — A map of meaning',
      subtitle: 'Switch to terminal: python demo/03_word_map.py',
      icon: 'rocket',
    },
  },
  {
    type: 'description',
    content: {
      title: 'Why this breaks',
      icon: 'warning',
      description: `It only works on **words we picked**: 16 words from three topics, so three directions were enough. Give all 235 words two numbers each and the map holds nothing clear. The words pointing the same way as *warm* are *network*, *protection*, *for*, *510* and *while*.

        And it gives one vector **per word**. Our question is 11 words, and a document is hundreds: to search, we need **one vector per text**.`,
    },
  },

  // ---- Section 4: Sentences from words ----
  {
    type: 'title',
    content: {
      title: '4. Sentences from words',
      subtitle: 'Add up the word vectors',
      icon: 'calculator',
    },
  },
  {
    type: 'standard',
    content: {
      title: 'One vector per sentence',
      icon: 'layers',
      points: [
        'Our question is **11 words**, and a document is hundreds. A search needs **one vector** for each',
        'The simplest way: **add up** the vectors of its words',
        "A word that isn't on the map **adds nothing**",
        'Then compare two sentences by their **angle**, just as we compared words',
      ],
    },
  },
  {
    type: 'word-map',
    content: {
      title: 'Add up the arrows',
      // The words and numbers from demo/output/03_word_map.json, as on "The map".
      words: {
        account: [0.25, 0.09],
        password: [0.25, 0.126],
        phone: [0.295, 0.223],
        email: [0.394, 0.379],
        router: [0.118, 0.512],
        frost: [-0.171, 0.443],
        wake: [-0.392, 0.159],
        warm: [-0.351, 0.128],
        sunrise: [-0.43, 0.048],
        early: [-0.179, -0.079],
        heat: [-0.12, -0.156],
        temperature: [0.035, -0.249],
        app: [0.084, -0.305],
        schedule: [0.091, -0.281],
        boiler: [0.125, -0.108],
        radiator: [0.221, -0.06],
      },
      groups: {
        account: 1,
        password: 1,
        phone: 1,
        email: 1,
        router: 1,
        radiator: 1,
        frost: 2,
        wake: 2,
        warm: 2,
        sunrise: 2,
        early: 2,
        heat: 3,
        temperature: 3,
        app: 3,
        schedule: 3,
        boiler: 3,
      },
      sentences: {
        'warm wake early': ['warm', 'wake', 'early'],
        'frost sunrise heat': ['frost', 'sunrise', 'heat'],
        'email password account': ['email', 'password', 'account'],
      },
      steps: [
        {
          caption: 'Every word is an **arrow** from the middle',
          arrows: true,
          grouped: true,
        },
        {
          caption:
            '*warm wake early*: put its arrows **tip to tail**. Where they end is the sum',
          sentences: ['warm wake early'],
          highlight: ['warm', 'wake', 'early'],
        },
        {
          caption: '*frost sunrise heat*: different words, **almost the same direction**',
          sentences: ['warm wake early', 'frost sunrise heat'],
          highlight: ['warm', 'wake', 'early', 'frost', 'sunrise', 'heat'],
        },
        {
          caption: '**12°** apart: a similarity of **0.98**',
          angle: ['warm wake early', 'frost sunrise heat'],
        },
        {
          caption: '*email password account* adds up to **another direction**',
          sentences: ['warm wake early', 'email password account'],
          highlight: ['warm', 'wake', 'early', 'email', 'password', 'account'],
          angle: null,
        },
        {
          caption: '**134°** apart: a similarity of **−0.69**',
          angle: ['warm wake early', 'email password account'],
        },
      ],
      note: "The 16 words from section 3. Demo 4 adds up the two numbers from demo 3's map of all 235 words.",
    },
  },
  {
    type: 'code',
    content: {
      title: 'Add up, then compare',
      code: `def sentence_vector(text, word_vectors):
    known = [word_vectors[w] for w in words(text)
             if w in word_vectors]
    return [sum(column) for column in zip(*known)]

cosine_similarity(sentence_vector(a, word_vectors),
                  sentence_vector(b, word_vectors))`,
      highlights: [
        "`word_vectors`: demo 3's **two numbers** for each of the 235 words",
        '`zip(*known)`: every first number, then every second number…',
        'Sum or average, the **angle** is the same: cosine similarity, as in demo 2',
      ],
    },
  },
  {
    type: 'title',
    content: {
      title: 'Demo — Sentences from words',
      subtitle: 'Switch to terminal: python demo/04_sentence_vectors.py',
      icon: 'rocket',
    },
  },

  {
    type: 'description',
    content: {
      title: 'Why this breaks',
      icon: 'warning',
      description: `**Two numbers are too few.** With two, every text is just a direction round a circle, and 275 documents share 360°. **19 of them** are within 8° of the question, a similarity of 0.99 or more. The pairs worked because the heating words and the password words happen to point different ways.

        And the map needs **every pair** of words first: 27,495 for 235 words, about 5 billion for 100,000. What if a model **learned** more numbers for each word?`,
    },
  },

  // ---- Section 5: Build an embeddings model ----
  {
    type: 'title',
    content: {
      title: '5. Build an embeddings model',
      subtitle: 'Learn 20 numbers instead with word2vec',
      icon: 'brain',
    },
  },

  {
    type: 'standard',
    content: {
      title: 'How to build one',
      icon: 'wrench',
      points: [
        '1. Keep the same **235** words',
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
      title: 'Check results against the text',
      code: `"... for your postcode. While Warm Wake is heating early,
 the display shows the sunrise symbol."

Real neighbours of "wake", up to 3 words either side:
  wake → your, while, warm, is, heating, early          answer 1

5 random words for each real pair (wake + warm, first pass):
  wake → connected, guide, current, frost, not          answer 0`,
      highlights: [
        'One pass through the guide: **9,498 real pairs**, 47,490 random ones',
        'Random words are almost never real neighbours',
      ],
    },
  },
  {
    type: 'code',
    content: {
      title: 'Guess. Nudge the weights. Repeat until it works',
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
      subtitle: 'Switch to terminal: python demo/05_word_vectors.py',
      icon: 'rocket',
    },
  },

  {
    type: 'description',
    content: {
      title: 'Why this breaks',
      icon: 'warning',
      description: `On this little text, word2vec is **no better at neighbours** than counting: *heating* is closest to *hours*, *switch* and *for*. **1,794 words is far too little text**, and *alarm*, the word the question turns on, isn't in it at all.

        And adding up still **loses the order**: "The heating is off and frost protection is on" and its opposite score **1.000**, the same words in any order. *The* gets as much say as *heating*. We need a model that reads **the whole text**.`,
    },
  },

  // ---- Section 6: A commercial embedding model ----
  {
    type: 'title',
    content: {
      title: '6. A commercial embedding model',
      subtitle: 'OpenAI text-embedding-3-small',
      icon: 'compass',
    },
  },
  {
    type: 'code',
    content: {
      title: 'An embeddings model',
      code: `response = client.embeddings.create(
    model="text-embedding-3-small",
    input=texts,
)
vectors = [item.embedding for item in response.data]`,
      highlights: [
        '`text-embedding-3-small`: trained to embed **whole passages**, word order included',
        'Up to 8,191 tokens in, **1,536 numbers** out',

        'Cost: All 275 documents: 179,993 tokens, **under half a cent**',
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
        'The same angle as demos 4 and 5, now for vectors with **1,536 numbers**',
        'Cosine similarity works in any number of dimensions',
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
      title: 'Demo — A commercial embedding model',
      subtitle: 'Switch to terminal: python demo/06_similarity_search.py',
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
    type: 'three-way',
    content: {
      title: 'Where Warm Wake came',
      columns: [
        {
          label: 'Keyword search',
          items: ['User guide, 26 sections: **1st**', 'All 275 documents: **142nd**'],
        },
        {
          label: 'Two numbers, added up',
          items: ['User guide, 26 sections: **9th**', 'All 275 documents: **71st**'],
        },
        {
          label: '20 numbers, added up',
          items: ['User guide, 26 sections: **3rd**', 'All 275 documents: **8th**'],
        },
        {
          label: 'text-embedding-3-small',
          items: ['User guide, 26 sections: **1st**', 'All 275 documents: **1st**'],
        },
      ],
    },
  },
  {
    type: 'description',
    content: {
      title: 'Why this breaks',
      icon: 'warning',
      description: `The customer asked **why** the heating comes on early. We found the right document, and the answer is inside it. **Reading it and answering is Module 6: RAG.**

        And every run sends **all 275 documents** to the API again, and the vectors vanish when the script ends. Every search **compares with every document**, and there's **no filter**: 41 documents are internal. Module 6 keeps the vectors in a **vector database**.`,
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
        '**Counting**: neighbours counted, but on a line each word has only one place',
        '**A map**: two numbers per word, but only for words we picked',
        '**Sentences from words**: add up the arrows, but two numbers are too few',
        '**An embeddings model**: 20 learned numbers, but too little text, and no word order',
        '**A commercial embedding model**: reads the whole text, and puts the right document first',
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
        'Embeddings come from **where words are used**: counted or learned',
        '**Cosine similarity** compares directions, not lengths',
        'Adding up its words gives a sentence **one vector**, but loses the order',
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
