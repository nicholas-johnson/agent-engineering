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
      title: 'Day One — Closing',
      subtitle: 'What to take home',
      icon: 'award',
    },
  },
  {
    type: 'standard',
    content: {
      title: 'What is a token?',
      icon: 'hash',
      points: [
        'A piece of text: common words are one token, rare words split into pieces',
        'Single characters are tokens too, so **any text** can be written',
        'Module 1 built 500 tokens; real tokenizers have 100,000–200,000',
        'A model reads tokens and predicts the **next token**',
        'You pay per token, input **and** output',
      ],
    },
  },
  {
    type: 'code',
    content: {
      title: 'What is a context window?',
      code: `Turn   Input tokens   Output tokens
   1             56              29
   2             96              19
   3            127              34`,
      highlights: [
        'The tokens a model can see at once: hundreds of thousands in real models',
        'The model has no memory: a chat resends the **whole conversation** every turn',
        'So every turn costs more, and a long chat eventually runs out of room',
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'What is a vector?',
      icon: 'layers',
      points: [
        'A list of numbers',
        'Module 1: the next-token probabilities, a vector with 2,676 entries',
        '**Embeddings**: a vector for each token (16 numbers in Module 1), learned in training',
        'Module 2: image patches become vectors too, so a picture is just more tokens',
        'Tomorrow: vectors are what **vector stores** and **RAG** search',
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'What is an MCP server?',
      icon: 'server',
      points: [
        'MCP is the **Model Context Protocol**: an open standard for sharing tools',
        'An **MCP server** offers tools and runs them on request',
        'An **MCP client** connects to servers and uses their tools',
        'Write a server once: Claude, ChatGPT, Cursor, VS Code and our agent can all use it',
        'Module 3: the maths server and the cards server, two servers in one loop',
      ],
    },
  },
  {
    type: 'cards',
    content: {
      title: 'Who are the main AI providers?',
      cards: [
        {
          heading: 'The big labs',
          points: [
            '**OpenAI**: GPT',
            '**Anthropic**: Claude',
            '**Google**: Gemini',
            '**xAI**: Grok',
          ],
        },
        {
          heading: 'Open weights',
          points: [
            '**DeepSeek**: very cheap',
            '**Alibaba**: Qwen',
            'Download and run them anywhere',
          ],
        },
        {
          heading: 'OpenRouter',
          points: ['Many labs, one API', 'Your data passes through it as well'],
        },
        {
          heading: 'Ollama',
          points: ['A model on your own laptop', 'Free and private, gets more wrong'],
        },
      ],
    },
  },
  {
    type: 'title',
    content: {
      title: 'See you tomorrow',
      subtitle: 'Day Two: embeddings, vector stores and RAG',
      icon: 'rocket',
    },
  },
];
