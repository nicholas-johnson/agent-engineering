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
      title: 'Day Two — Closing',
      subtitle: 'What to take home',
      icon: 'award',
    },
  },
  {
    type: 'code',
    content: {
      title: 'What is an embedding?',
      code: `Customers can't sign in after resetting their password
As 1,536 numbers: [0.0235, -0.0048, 0.0286, -0.0008, ...]

Keyword  11.04  TS-1879  Handle an expired password during sign-in
Vector   0.511  TS-1042  Log in with the new password after a password reset`,
      highlights: [
        'A vector that stands for what a piece of text **means**',
        'Close together means similar meaning: the right test came first, sharing only "after" and "password"',
        'A **vector database** stores them once, and filters by criteria such as the platform',
      ],
    },
  },
  {
    type: 'code',
    content: {
      title: 'Which search is best?',
      code: `A right script in the top 5, for 20 requests

                          Keyword   Vector   Hybrid
14 in everyday words            6       12        9
6 quoting an error code         6        6        6
All 20                         12       18       15`,
      highlights: [
        '**Hybrid search** did worse than vectors alone, on our requests',
        'It helps with exact terms the embeddings don’t know: part numbers, ticket IDs',
        'So **measure**, with your own requests and known answers',
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'What is RAG?',
      icon: 'book',
      points: [
        '**Retrieval-augmented generation**: look it up, then answer',
        'No documents: it guessed "early start". The feature is **Warm Wake**',
        'All 275 documents in the prompt: right, but 191,548 tokens a question',
        'Retrieve 5 chunks: 906 tokens, with the facts for 22 of 24 questions',
        'It misses when customers’ words aren’t the documentation’s',
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'What is a company brain?',
      icon: 'brain',
      points: [
        'Files an AI tool reads first: product, customers, voice, decisions',
        'Without it: a polished prototype in 30 seconds, all of it invented',
        'A **coding agent** builds it, and makes product decisions on its own',
        '**Plan first**: the right feature, and 61 changed lines nobody had read',
        '**Skills** automate the review. It missed the bug: people still read',
      ],
    },
  },
  {
    type: 'description',
    content: {
      title: 'The tools change',
      icon: 'compass',
      description:
        'This year alone, Cursor was bought, Windsurf became Devin Desktop and Gemini CLI was replaced. What lasts is the **context** you give the tools and the **checks** you put around them.',
    },
  },
  {
    type: 'code',
    content: {
      title: 'What is prompt injection?',
      code: `The former lodger's device name, 20 runs each

Injection             No defence   Marked   Detector
Obvious                     0/20
Helpful-looking            20/20     0/20       0/20
Written as a record         7/20     0/20       9/20`,
      highlights: [
        'Text someone else wrote, followed by the model as if it were an instruction',
        'The obvious attack failed. The one that looked **helpful** worked every time',
        'Defences are rates, not guarantees, and one success is enough',
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'What is the lethal trifecta?',
      icon: 'warning',
      points: [
        '**Private data**: Sam’s home and household',
        '**Untrusted content**: a device name somebody else wrote',
        '**A way out**: a tool that invites any email address',
        'All three: an injection can steal. Remove one, or confirm the way out',
      ],
      credit:
        'Simon Willison (2025). "The lethal trifecta for AI agents: private data, untrusted content, and external communication."',
    },
  },
  {
    type: 'standard',
    content: {
      title: 'Before you ship',
      icon: 'shield',
      points: [
        '**Access**: identity from the sign-in, permissions checked in code',
        '**Untrusted text**: find it, mark it, measure attacks as rates',
        '**Actions**: tiers, a person confirms the risky ones, all logged',
        '**Data**: know what the provider keeps; redact, retain, erase',
        '**Deployment**: the user’s own permissions, and limits on spend',
      ],
    },
  },
  {
    type: 'cards',
    content: {
      title: 'Two days',
      cards: [
        {
          heading: 'Day One: the agent',
          points: [
            '**1.** A language model from scratch',
            '**2.** A chatbot',
            '**3.** Tools and MCP',
            '**4.** Choosing a provider',
          ],
        },
        {
          heading: 'Day Two: putting it to work',
          points: [
            '**5.** Search by meaning',
            '**6.** RAG on your own documents',
            '**7.** AI-assisted development',
            '**8.** Security and deployment',
          ],
        },
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'Where next',
      icon: 'map',
      points: [
        'Every module has a **playground**: settings to change, scripts to run',
        'And **further reading**, with ⭐ on the best places to start',
        'The final exercise: read one, link it to a demo, start an extension',
        'Then try one idea on your own documents, code or customers',
      ],
    },
  },
  {
    type: 'title',
    content: {
      title: 'Thank you',
      subtitle: 'Questions?',
      icon: 'sparkles',
    },
  },
];
