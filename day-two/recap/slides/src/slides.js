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
    type: 'description',
    content: {
      title: 'One idea under everything',
      icon: 'brain',
      description:
        'A language model predicts the **next token**. Everything we built yesterday, from counting word pairs in *Alice* to an agent calling a live API, was that one idea, given more context and more to do.',
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
      title: 'What is a language model?',
      icon: 'brain',
      points: [
        'A **next-token predictor**: given some tokens, how likely is each possible next token?',
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
    type: 'code',
    content: {
      title: 'Module 1: a language model from scratch',
      code: `' the queen said to' (seen in the book)
  ' the' 16%, ' alice' 13%, ' "' 8%, ' herself' 5%
' the mouse said to' (never seen in the book)
  ' the' 15%, ' alice' 12%, ' "' 7%, ' herself' 5%`,
      highlights: [
        'Word pairs, windows, letters, tokens: always **too many contexts** to count',
        'A neural network **learns a function**, so it predicts for contexts it has never seen',
        '"mouse" and "queen" got similar **embeddings**. Today, vectors like these become search',
      ],
    },
  },
  {
    type: 'code',
    content: {
      title: 'Module 2: a chatbot',
      code: `You: Hello! My name is Nick.
Cat: Hello, Nick! ... Shall I call you Nick?

You: What is my name?
Cat: I don't know your name—you haven't told me.`,
      highlights: [
        'The API is **stateless**: the model only sees what you send in that call',
        'So a chat resends the **whole conversation**: 56, then 96, then 127 input tokens',
        'Then streaming, and images: a picture is just more tokens',
      ],
    },
  },
  {
    type: 'code',
    content: {
      title: 'Module 3: tools',
      code: `Model: ... is 2,766.6443672823.
Model: ... is 2,766.6443839608.
Model: ... is 2,766.6442826149.

  [tool] square_root({"number":7654321}) -> 2766.644357339772
Agent: ... is 2766.6443573398.`,
      highlights: [
        'Asked directly, the model guesses digits: confidently, and differently each time',
        'A **tool loop**: the model asks for a tool, our code runs it, the model uses the result',
        'An **MCP server** shares tools with any client: Claude, ChatGPT, Cursor and our agent',
        'Text from outside is not instructions: **prompt injection** comes back in Module 8',
      ],
    },
  },
  {
    type: 'code',
    content: {
      title: 'Module 4: choosing a provider',
      code: `Model                          Total   Per 1,000 chats
gpt-6-luna                      2.1s           $0.0493
anthropic/claude-haiku-5.5      1.2s           $0.0932
anthropic/claude-opus-5.5       3.0s           $5.7320
x-ai/grok-4.7                  11.5s           $7.8760
deepseek/deepseek-v4.1-flash    0.6s           $0.0786
qwen3:1.7b                      1.0s              free`,
      highlights: [
        'One logic puzzle, one piece of code: from free to $7.88 per 1,000 chats',
        'Haiku got the tins the wrong way round. A 1.7B model on a laptop got them right',
        'Also ask where your data goes, and what it will and won’t say',
        'Which provider? *It depends a good deal on where you want to get to*',
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'What yesterday’s agent couldn’t do',
      icon: 'warning',
      points: [
        'It only knows what it was **trained on**, plus what its tools return',
        'It can’t search **your** documents, tickets or test scripts',
        'So its answers about your product are guesses, however confident',
        'And nobody has asked yet **who it works for**, or what it may do',
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'Five questions from yesterday',
      icon: 'question',
      points: [
        'Why did the Cat forget Nick’s name?',
        'Why does every turn of a chat cost more than the last?',
        'When an agent uses a tool, who runs it: the model or your code?',
        'What does an MCP server give you that a plain function doesn’t?',
        'Name one thing to ask a provider that isn’t the price',
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'Answers',
      icon: 'check',
      points: [
        'The API is stateless: each call sees only what you send',
        'Every turn resends the whole conversation, and you pay for all of it',
        'Your code. The model only asks',
        'Write it once, and any MCP client can use it',
        'Where your data goes, what it will say, and how fast it is',
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
