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
      title: 'Module 2 — Building a Chatbot',
      subtitle: 'Talking to a real language model',
      icon: 'bot',
    },
  },

  // ---- Section 1: One response ----
  {
    type: 'title',
    content: {
      title: '1. One response',
      subtitle: 'Ask a real model a question',
      icon: 'mail',
    },
  },
  {
    type: 'code',
    content: {
      title: 'One call',
      code: `client = OpenAI()

response = client.responses.create(
    model="gpt-6-luna",
    reasoning={"effort": "none"},
    instructions=INSTRUCTIONS,
    input="Would you tell me, please, which way I ought to go from here?",
)
print(response.output_text)`,
      highlights: [
        '`input`: what you say',
        '`instructions`: who to be and how to behave — the **system prompt**',
        '`output_text`: the reply',
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'Our chatbot',
      icon: 'bot',
      points: [
        'The instructions make it **the Cheshire Cat**',
        'Mischievous and fond of riddles, but always answers the question',
        'Two or three sentences per reply',
        "`gpt-6-luna`: OpenAI's fast, low-cost GPT-6 model",
        'Reasoning effort `"none"`: answer straight away, no thinking first',
      ],
    },
  },
  {
    type: 'comparison',
    content: {
      title: 'The older API',
      left: {
        label: 'Responses API (this course)',
        items: [
          '`client.responses.create(...)`',
          '`instructions=` and `input=`',
          '`response.output_text`',
          'Recommended by OpenAI',
        ],
      },
      right: {
        label: 'Chat Completions (older)',
        items: [
          '`client.chat.completions.create(...)`',
          '`messages=` only',
          '`completion.choices[0].message.content`',
          'Still supported, and in lots of existing code',
        ],
      },
    },
  },
  {
    type: 'title',
    content: {
      title: 'Demo — One response',
      subtitle: 'Switch to terminal: python demo/01_one_response.py',
      icon: 'rocket',
    },
  },
  {
    type: 'code',
    content: {
      title: 'The response object',
      code: `"model": "gpt-6-luna",
"output": [
  { "type": "message", "role": "assistant",
    "content": [{ "type": "output_text", "text": "That depends a good deal..." }] }
],
"usage": {
  "input_tokens": 65,
  "output_tokens": 49,
  "total_tokens": 114
}`,
      highlights: [
        'Open `demo/output/01_response.json` to see it all',
        '`output` is a list — a response can contain more than one item',
        'You pay for input **and** output tokens',
      ],
    },
  },
  {
    type: 'description',
    content: {
      title: 'Why this breaks',
      icon: 'warning',
      description:
        '*"That depends a good deal on where you want to get to."* — Carroll\'s own words, from a real model. But it answers **one question**, then stops. To ask another, you have to run it again.',
    },
  },

  // ---- Section 2: A chat loop ----
  {
    type: 'title',
    content: {
      title: '2. A chat loop',
      subtitle: 'Keep the conversation going',
      icon: 'refresh',
    },
  },
  {
    type: 'code',
    content: {
      title: 'Put it in a loop',
      code: `while True:
    question = input("You: ")
    if not question:
        break
    response = client.responses.create(..., input=question)
    print(f"Cat: {response.output_text}")`,
      highlights: ["That's a chatbot", 'Press Enter on an empty line to stop'],
    },
  },
  {
    type: 'title',
    content: {
      title: 'Demo — A chat loop',
      subtitle: 'Switch to terminal: python demo/02_chat_loop.py',
      icon: 'rocket',
    },
  },
  {
    type: 'code',
    content: {
      title: 'Why this breaks',
      code: `You: Hello! My name is Nick.
Cat: Hello, Nick! ... Shall I call you Nick?

You: What is my name?
Cat: I don't know your name—you haven't told me.`,
      highlights: [
        'The API is **stateless**: every call is completely separate',
        'The model only sees what you send in that call',
        "Module 1's context window again — it has no memory of its own",
      ],
    },
  },

  // ---- Section 3: The context window ----
  {
    type: 'title',
    content: {
      title: '3. The context window',
      subtitle: 'Send the whole conversation, every time',
      icon: 'database',
    },
  },
  {
    type: 'code',
    content: {
      title: 'Keep a list',
      code: `messages.append({"role": "user", "content": question})
response = client.responses.create(..., input=messages)
messages.append({"role": "assistant", "content": response.output_text})`,
      highlights: [
        '`user`: what you said. `assistant`: what the model said',
        'The model reads it all and predicts what the assistant says next',
        'Or pass `previous_response_id` and let the API keep the list',
      ],
    },
  },
  {
    type: 'title',
    content: {
      title: 'Demo — The context window',
      subtitle: 'Switch to terminal: python demo/03_conversation.py',
      icon: 'rocket',
    },
  },
  {
    type: 'code',
    content: {
      title: 'Why this breaks',
      code: `Cat: Your name is Nick—unless you've wandered into a
     very convincing disguise.

Turn   Input tokens   Output tokens
   1             56              29
   2             96              19
   3            127              34`,
      highlights: [
        'It remembers — but you **wait** for the whole reply',
        'And **every turn costs more**: each one resends everything before it',
        'See `demo/output/03_conversation.txt`',
      ],
    },
  },

  // ---- Section 4: Streaming ----
  {
    type: 'title',
    content: {
      title: '4. Streaming',
      subtitle: 'Watch the reply being written',
      icon: 'zap',
    },
  },
  {
    type: 'code',
    content: {
      title: 'A stream of events',
      code: `stream = client.responses.create(..., input=messages, stream=True)
for event in stream:
    if event.type == "response.output_text.delta":
        print(event.delta, end="", flush=True)`,
      highlights: [
        'Each `delta` is the next piece of the reply',
        'Other events: `response.created`, `response.completed`, ...',
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'One token at a time',
      icon: 'clock',
      points: [
        "Streaming isn't a special effect",
        'The model really does write one token at a time',
        'Each token predicted from everything before it',
        'Exactly like the generation loop in every Module 1 demo',
        'Streaming just lets you **watch**',
      ],
    },
  },
  {
    type: 'title',
    content: {
      title: 'Demo — Streaming',
      subtitle: 'Switch to terminal: python demo/04_streaming.py',
      icon: 'rocket',
    },
  },
  {
    type: 'description',
    content: {
      title: 'Why this breaks',
      icon: 'warning',
      description:
        'Our Cat can chat, remember, and reply as it writes. But it can only **read text**. What if we showed it a picture?',
    },
  },

  // ---- Section 5: Images ----
  {
    type: 'title',
    content: {
      title: '5. Images',
      subtitle: 'A model that can see',
      icon: 'image',
    },
  },
  {
    type: 'code',
    content: {
      title: 'Text and pictures',
      code: `image = base64.b64encode(Path("mad-tea-party.png").read_bytes()).decode()
messages = [{
    "role": "user",
    "content": [
        {"type": "input_text", "text": "What is going on in this picture?"},
        {"type": "input_image", "image_url": f"data:image/png;base64,{image}"},
    ],
}]`,
      highlights: [
        'Content can be a list of parts: some text, some images',
        'The image travels inside the request as **base64** text — or as a URL',
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'How a language model sees',
      icon: 'eye',
      points: [
        "OpenAI doesn't publish the details, but the usual approach:",
        'Cut the image into small square **patches**',
        "Turn each patch into a vector, like a token's embedding",
        'To the model, the picture is just **more tokens** in the context',
        'You pay for them as input tokens',
      ],
    },
  },
  {
    type: 'image',
    content: {
      title: 'What we will show it',
      src: '/mad-tea-party.png',
      alt: "John Tenniel's illustration of the Mad Tea Party",
      credit: 'John Tenniel (1865). Project Gutenberg #114, public domain',
    },
  },
  {
    type: 'title',
    content: {
      title: 'Demo — Images',
      subtitle: 'Switch to terminal: python demo/05_images.py',
      icon: 'rocket',
    },
  },
  {
    type: 'code',
    content: {
      title: 'What the Cat saw',
      code: `You: What is going on in this picture?
Cat: Alice has stumbled upon the Mad Hatter's tea party: she sits
     at a crowded table with the Hatter, the March Hare, and the
     Dormouse.

You: Who is the one with the big hat?
Cat: That's the Mad Hatter—the one wearing the enormous hat
     marked "In this style 10/6."`,
      highlights: ["It read the price ticket in the Hatter's hat"],
    },
  },

  // ---- Wrap-up ----
  {
    type: 'title',
    content: {
      title: 'Wrap-up',
      subtitle: 'From one question to a chatbot that can see',
      icon: 'check',
    },
  },
  {
    type: 'standard',
    content: {
      title: 'What we built',
      icon: 'blocks',
      points: [
        '**One response** — a single call, with instructions',
        '**A chat loop** — which forgot everything',
        '**The context window** — send the whole conversation every time',
        '**Streaming** — watch the reply being written',
        '**Images** — a model that can see',
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'What we learned',
      icon: 'award',
      points: [
        'A chat model still just predicts the **next token**',
        '**Instructions** shape who it is and how it behaves',
        'The API is **stateless** — memory means sending the history',
        'Every turn resends everything, so **long chats cost more**',
        'Images become **tokens** too',
      ],
    },
  },

  {
    type: 'standard',
    content: {
      title: 'Getting set up',
      icon: 'key',
      points: [
        'Create an API key at **platform.openai.com**',
        'Copy `.env.example` to `.env` and put your key in it',
        '`load_dotenv()` reads it — `.env` is never committed',
        'Two packages: `openai` and `python-dotenv`',
      ],
    },
  },
];
