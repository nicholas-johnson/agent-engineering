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
      title: 'Day One — Recap',
      subtitle: 'Where we got to yesterday',
      icon: 'refresh',
    },
  },

  {
    type: 'code',
    content: {
      title: 'What is a token?',
      code: `alice was beginning to get
['al', 'ice', ' was', ' begin', 'ning', ' to', ' get']`,
      highlights: [
        'A piece of text: common words are one token, rarer words split into pieces',
        'Single letters are tokens too, so **any text** can be written',
        'Module 1 built 500 tokens; real tokenizers have 100,000–200,000',
        'You pay per token, input **and** output',
      ],
    },
  },
  {
    type: 'code',
    content: {
      title: 'What is a vector?',
      code: `"the": {
  "queen": 0.0396,
  "king": 0.0365,
  "mock": 0.0323,
  "gryphon": 0.0323,
  ...
}`,
      highlights: [
        'A **list of numbers**',
        'What comes after "the": one probability for every word, 2,676 numbers',
        '**Embeddings**: a vector for each token, 16 numbers in Module 1, learned in training',
        'Tokens used in similar ways end up with **similar vectors**',
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'What is a context window?',
      icon: 'eye',
      points: [
        'The tokens a model can see at once',
        'Module 1’s neural model saw 3 tokens; `gpt-6-luna` sees 1,050,000',
        'Everything you send in one call: instructions, the whole chat, tool results',
        'No memory: if it isn’t in the window, the model doesn’t know it',
        'You pay for every token in it, on every call',
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'What is a language model?',
      icon: 'brain',
      points: [
        'A **next-token predictor**: given a vector of tokens (a context window), how likely is each possible next token?',
        'The answer is a vector of probabilities, one for every token it knows',
        'Pick a token, add it to the text, and ask again: that’s how it writes',
        'Module 1 learned from one book; real models from trillions of tokens',
        'A chatbot is a language model continuing a conversation',
      ],
    },
  },

  {
    type: 'standard',
    content: {
      title: 'Today',
      icon: 'rocket',
      points: [
        '**5. Embeddings and Vector Search**: find things by meaning',
        '**6. RAG and Proprietary Knowledge**: answer from your documents',
        '**7. AI-Assisted Development**: build with agents, from product to sales',
        '**8. Security and Commercial Deployment**: put it in front of customers',
      ],
    },
  },
];
