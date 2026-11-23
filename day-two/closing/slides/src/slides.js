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
    type: 'title',
    content: {
      title: 'Thank you',
      subtitle: 'Questions?',
      icon: 'sparkles',
    },
  },
];
