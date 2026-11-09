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
      title: 'Module 1 — Intro to Language Models',
      subtitle: 'Building a language model from scratch, in five steps',
      icon: 'brain',
    },
  },
  {
    type: 'description',
    content: {
      title: 'What is a language model?',
      icon: 'question',
      description:
        'Given some text, predict what comes next. A language model takes a **context** and returns a **probability for every possible next token**. To generate text, pick one, add it to the context, and ask again.',
    },
  },
  {
    type: 'standard',
    content: {
      title: 'Our corpus',
      icon: 'book',
      points: [
        "*Alice's Adventures in Wonderland*, Lewis Carroll (Project Gutenberg)",
        '**Small:** chapter 1, *Down the Rabbit-Hole* — about 2,200 words',
        '**Large:** the whole book — about 27,000 words',
        'Plain Python, no libraries, no GPU',
        'Every demo writes what it learned to `demo/output/`',
      ],
    },
  },

  // ---- Section 1: Word pairs ----
  {
    type: 'title',
    content: {
      title: '1. Word pairs',
      subtitle: 'The simplest possible language model',
      icon: 'link',
    },
  },
  {
    type: 'standard',
    content: {
      title: 'Count what comes next',
      icon: 'calculator',
      points: [
        'Split the text into words',
        'For every word, count the words that come straight after it',
        'Divide by the total to get a probability for each next word',
        'That is a language model — a **bigram model**',
      ],
    },
  },
  {
    type: 'code',
    content: {
      title: 'The whole model',
      code: `counts = defaultdict(Counter)
for word, next_word in zip(words, words[1:]):
    counts[word][next_word] += 1`,
      highlights: [
        '`zip(words, words[1:])` gives every pair of neighbouring words',
        'Then divide each count by the total for that word',
      ],
    },
  },
  {
    type: 'code',
    content: {
      title: 'A vector of probabilities',
      code: `"the": {
  "queen": 0.0396,
  "king": 0.0365,
  "mock": 0.0323,
  "gryphon": 0.0323,
  ...
}`,
      highlights: [
        'One probability for every word that can follow "the"',
        'The full vector has 2,676 entries — almost all zero',
        'The model is only as good as the text it counted',
      ],
    },
  },
  {
    type: 'title',
    content: {
      title: 'Demo — Word pairs',
      subtitle: 'Switch to terminal: python demo/01_word_pairs.py',
      icon: 'rocket',
    },
  },
  {
    type: 'description',
    content: {
      title: 'Why this breaks',
      icon: 'warning',
      description:
        '*"alice was beginning to get into the people that very tired of tumbling down the second time , she could see , and there was now , now only knew how late !"* — every **pair** makes sense, the sentence doesn\'t. The model only ever sees **one word of context**.',
    },
  },

  // ---- Section 2: Context window ----
  {
    type: 'title',
    content: {
      title: '2. The context window',
      subtitle: 'More context, more counting',
      icon: 'layers',
    },
  },
  {
    type: 'standard',
    content: {
      title: 'Look further back',
      icon: 'eye',
      points: [
        'Slide a window of **five words** along the text',
        'For each five-word context, count the word that comes next',
        'The number of tokens a model can see is its **context window**',
        'Real models: hundreds of thousands of tokens',
      ],
    },
  },
  {
    type: 'code',
    content: {
      title: 'A sliding window',
      code: `for i in range(len(words) - WINDOW):
    context = " ".join(words[i : i + WINDOW])
    counts[context][words[i + WINDOW]] += 1`,
      highlights: [
        'The window moves one word at a time — every position is an example',
        'The context is now five words, not one',
      ],
    },
  },
  {
    type: 'title',
    content: {
      title: 'Demo — Context window',
      subtitle: 'Switch to terminal: python demo/02_context_window.py',
      icon: 'rocket',
    },
  },
  {
    type: 'description',
    content: {
      title: 'Perfect English?',
      icon: 'eye',
      description:
        '*"alice was beginning to get very tired of sitting by her sister on the bank , and of having nothing to do ..."* — the first paragraph of the book, **word for word**. 99% of five-word contexts have only one possible next word. The model isn\'t predicting, it\'s **reciting**.',
    },
  },
  {
    type: 'equation',
    content: {
      title: 'The combinatorial problem',
      mathml: `<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
  <mtext>possible contexts</mtext>
  <mo>=</mo>
  <msup><mi>V</mi><mi>n</mi></msup>
</math>`,
      points: [
        '*V* is the vocabulary size, *n* is the window',
        'Whole book: 2,676⁵ = **137 quadrillion** possible contexts',
        'We have seen **30,350** of them',
        'More text barely helps — contexts grow far faster than text',
      ],
    },
  },
  {
    type: 'description',
    content: {
      title: 'Never seen it',
      icon: 'ban',
      description:
        '*"The Queen was beginning to get very cross with the Hatter."* — seven five-word contexts. The model has seen **one**. For the rest, it has nothing to say at all.',
    },
  },

  // ---- Section 3: Letters ----
  {
    type: 'title',
    content: {
      title: '3. Letters',
      subtitle: 'A tiny vocabulary, a longer window',
      icon: 'hash',
    },
  },
  {
    type: 'standard',
    content: {
      title: 'Shrink the vocabulary',
      icon: 'scissors',
      points: [
        'The problem is *V* — thousands of words',
        'Predict **letters** instead: about 40 characters',
        'A smaller vocabulary means we can afford a longer window',
        'Use **eight letters** of context',
      ],
    },
  },
  {
    type: 'comparison',
    content: {
      title: 'Words vs letters',
      left: {
        label: 'Five words',
        items: [
          'Vocabulary: 2,676',
          'Window: 5 words',
          'Possible contexts: 137 quadrillion',
          'Recites the book',
        ],
      },
      right: {
        label: 'Eight letters',
        items: [
          'Vocabulary: 41',
          'Window: 8 letters',
          'Possible contexts: 8 trillion',
          'Invents new sentences',
        ],
      },
    },
  },
  {
    type: 'title',
    content: {
      title: 'Demo — Letters',
      subtitle: 'Switch to terminal: python demo/03_letters.py',
      icon: 'rocket',
    },
  },
  {
    type: 'description',
    content: {
      title: 'Why this breaks',
      icon: 'warning',
      description:
        '*"alice was beginning to get us dry would be of very like having found out a new kind of rule, "and i\'ll tell you just now."* — eight letters is only about **a word and a half**. Each step carries very little meaning, so the model rambles. Letters are too small; words are too many.',
    },
  },

  // ---- Section 4: Tokens ----
  {
    type: 'title',
    content: {
      title: '4. Tokens',
      subtitle: 'Somewhere between letters and words',
      icon: 'blocks',
    },
  },
  {
    type: 'standard',
    content: {
      title: 'What is a token?',
      icon: 'puzzle',
      points: [
        'A common chunk of text: `" the"`, `" caterpillar"`, `"ing"`, `"a"`',
        'Common words get one token, rare words get split into pieces',
        'Single letters are tokens too, so **any text** can be written',
        'Every modern language model works in tokens',
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'Byte-pair encoding',
      icon: 'recycle',
      points: [
        'Start with every single character as a token',
        'Count every pair of neighbouring tokens in the text',
        'Merge the most common pair into a new token',
        'Repeat until you have enough — we stop at **500**',
        'First merges: `" t"`, `"he"`, `" a"`, `" s"`, then `" the"`',
      ],
    },
  },
  {
    type: 'code',
    content: {
      title: 'Splitting text into tokens',
      code: `alice was beginning to get very tired of sitting by her sister

['al', 'ice', ' was', ' begin', 'ning', ' to', ' get', ' very',
 ' ti', 'red', ' of', ' s', 'it', 'ting', ' by', ' her', ' s',
 'ist', 'er']`,
      highlights: [
        'Take the longest token that matches, then move on',
        'Real tokenizers: 100,000–200,000 tokens, same idea',
      ],
    },
  },
  {
    type: 'title',
    content: {
      title: 'Demo — Tokens',
      subtitle: 'Switch to terminal: python demo/04_tokens.py',
      icon: 'rocket',
    },
  },
  {
    type: 'description',
    content: {
      title: 'Why this breaks',
      icon: 'warning',
      description:
        "Four-token contexts: 500⁴ = **62.5 billion** possible. The book has about 50,000 tokens. 92% of the contexts we have seen still have only one possible next token. Counting can't get us any further — we need a model that can guess about a context it has **never seen**.",
    },
  },

  // ---- Section 5: A neural language model ----
  {
    type: 'title',
    content: {
      title: '5. A neural language model',
      subtitle: 'Learn a function instead of counting',
      icon: 'brain',
    },
  },
  {
    type: 'standard',
    content: {
      title: 'Stop counting',
      icon: 'lightbulb',
      points: [
        'Instead of a table of every context, **learn a function**',
        'Context in, vector of next-token probabilities out',
        'A function works for **any** context — even ones it never saw',
        'Based on Bengio et al. (2003), shrunk to fit in plain Python',
      ],
      credit:
        'Bengio, Ducharme, Vincent & Jauvin (2003). "A Neural Probabilistic Language Model." JMLR 3:1137–1155',
    },
  },
  {
    type: 'code',
    content: {
      title: 'The model',
      code: `last 3 tokens
   │
   ▼
a vector of 16 numbers for each token    ← embeddings
   │  (3 × 16 = 48 numbers)
   ▼
hidden layer: 32 neurons, tanh
   │
   ▼
one score for each of the 500 tokens
   │
   ▼
softmax → probabilities`,
      highlights: ['26,068 parameters, all starting random'],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'Training',
      icon: 'refresh',
      points: [
        'Pick a random context from the book, and the token that really came next',
        'Run it forward to get probabilities',
        '**Loss** = `-log(probability of the right token)`',
        '**Backpropagation**: work out how each parameter affected the loss',
        '**Gradient descent**: nudge every parameter to reduce it',
        'Repeat 30,000 times',
      ],
    },
  },
  {
    type: 'code',
    content: {
      title: 'Where backpropagation starts',
      code: `score_grads = probabilities[:]
score_grads[target] -= 1`,
      highlights: [
        'For softmax with this loss: **predicted minus actual**',
        'Everything after this is the chain rule, by hand',
        'Loss starts at 6.21 (random guessing) and falls to around 4.5',
      ],
    },
  },
  {
    type: 'title',
    content: {
      title: 'Demo — A neural language model',
      subtitle: 'Switch to terminal: python demo/05_neural_model.py',
      icon: 'rocket',
    },
  },
  {
    type: 'code',
    content: {
      title: 'A context it has never seen',
      code: `' the queen said to' (seen in the book)
  ' the' 16%, ' alice' 13%, ' "' 8%, ' herself' 5%

' the mouse said to' (never seen in the book)
  ' the' 15%, ' alice' 12%, ' "' 7%, ' herself' 5%`,
      highlights: [
        'A counting model has nothing for "the mouse said to"',
        'The neural model learned that mouse and queen are used alike',
        'The generated text is rough — 26,000 parameters, two minutes, one book',
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'Embeddings',
      icon: 'compass',
      points: [
        'Each token gets a learned vector of 16 numbers',
        'Nobody told the model what any token means',
        'Tokens used in similar ways end up with **similar vectors**',
        'See `demo/output/05_neural_model_embeddings.txt`',
        'We come back to embeddings later in the course',
      ],
    },
  },

  // ---- Wrap-up ----
  {
    type: 'title',
    content: {
      title: 'Wrap-up',
      subtitle: 'From counting to learning',
      icon: 'check',
    },
  },
  {
    type: 'comparison',
    content: {
      title: 'Our model vs a modern LLM',
      left: {
        label: 'Our model',
        items: [
          '500 tokens',
          '3-token context',
          '26,068 parameters',
          'One book',
          'One hidden layer',
          'Two minutes, one CPU core',
        ],
      },
      right: {
        label: 'A modern LLM',
        items: [
          '100,000–200,000 tokens',
          'Hundreds of thousands of tokens of context',
          'Billions to trillions of parameters',
          'Trillions of tokens of text',
          'A deep transformer',
          'Months, thousands of GPUs',
        ],
      },
    },
  },
  {
    type: 'standard',
    content: {
      title: 'What we learned',
      icon: 'award',
      points: [
        'A language model maps a context to **next-token probabilities**',
        'Counting works, but contexts grow as *V*ⁿ — the **combinatorial problem**',
        'Tokens balance vocabulary size against sequence length',
        'A neural network **generalises** to contexts it has never seen',
        'Along the way it learns **embeddings**',
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'Final exercise: further reading',
      icon: 'book',
      points: [
        '**Shannon (1948)** — demos 1–3, done by hand',
        '**Sennrich et al. (2016)** — byte-pair encoding comes to language',
        '**Bengio et al. (2003)** — demo 5, at full size',
        '**Vaswani et al. (2017)** — the transformer',
        'Pick a paper, connect it to a demo, then start an extension',
        'Everything is in `further-reading/`',
      ],
    },
  },
];
