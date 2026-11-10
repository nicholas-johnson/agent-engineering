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
      title: 'Module 3 — Choosing a Provider',
      subtitle: 'Which way ought I to go from here?',
      icon: 'compass',
    },
  },
  {
    type: 'description',
    content: {
      title: 'It depends',
      icon: 'question',
      description:
        '*"That depends a good deal on where you want to get to."* Every provider sells the same thing: a model that predicts the next token. What differs is **everything around it**.',
    },
  },
  {
    type: 'cards',
    content: {
      title: 'What to compare',
      cards: [
        {
          heading: 'Cost',
          points: ['Price per million tokens', 'What does one **task** cost?'],
        },
        { heading: 'Speed', points: ['Time to the first word', 'Words per second'] },
        {
          heading: 'Capability',
          points: ['Good enough for **your** task?', 'Test it yourself'],
        },
        {
          heading: 'Data',
          points: ['Where is it processed?', 'Under which laws? Is it kept?'],
        },
        {
          heading: 'Content',
          points: ['What will it refuse?', 'Whose values shaped it?'],
        },
        {
          heading: 'Openness',
          points: ['Can you download the weights?', 'How hard to switch later?'],
        },
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'Getting set up',
      icon: 'key',
      points: [
        'Keys in `.env`: OpenAI, Anthropic, Google, xAI, OpenRouter — any you have',
        'Every demo runs what it can and skips the rest',
        'Install Ollama, then `ollama pull qwen3:1.7b` (1.4 GB)',
        '`uv sync --extra local` for `transformers` and PyTorch',
        "Download before the session — conference Wi-Fi won't cope",
      ],
    },
  },

  // ---- Section 1: The big American labs ----
  {
    type: 'title',
    content: {
      title: '1. The big American labs',
      subtitle: 'Four labs, four APIs',
      icon: 'globe',
    },
  },
  {
    type: 'cards',
    content: {
      title: 'Who they are',
      cards: [
        {
          heading: 'OpenAI',
          points: ['The broadest platform', 'The API most others copy'],
        },
        { heading: 'Anthropic', points: ['Claude', 'Coding, agents, long documents'] },
        { heading: 'Google', points: ['Gemini', 'Text, images, audio and video'] },
        { heading: 'xAI', points: ['Grok', 'Built into X, searches X posts'] },
      ],
    },
  },
  {
    type: 'code',
    content: {
      title: 'Four shapes',
      code: `# OpenAI
client.responses.create(model=..., instructions=..., input=...)
response.output_text

# Anthropic
client.messages.create(model=..., max_tokens=..., system=..., messages=[...])
next(block.text for block in response.content if block.type == "text")

# Google
client.interactions.create(model=..., system_instruction=..., input=...)
interaction.output_text

# xAI — copies OpenAI's API
OpenAI(base_url="https://api.x.ai/v1").responses.create(...)`,
      highlights: [
        'Same job, different names for everything',
        'Switching provider means rewriting your code',
      ],
    },
  },
  {
    type: 'title',
    content: {
      title: 'Demo — The big American labs',
      subtitle: 'Switch to terminal: python demo/01_big_labs.py',
      icon: 'rocket',
    },
  },
  {
    type: 'comparison',
    content: {
      title: "A lab's own API",
      left: {
        label: 'Known for',
        items: [
          'Newest models and features first',
          'Best documentation and support',
          "Each lab's own strengths",
        ],
      },
      right: {
        label: 'Watch out for',
        items: [
          'Every API is shaped differently',
          'Switching means rewriting code: **lock-in**',
          'A key and a bill for every lab',
        ],
      },
    },
  },

  // ---- Section 2: One key for everything ----
  {
    type: 'title',
    content: {
      title: '2. One key for everything',
      subtitle: 'Routers',
      icon: 'route',
    },
  },
  {
    type: 'code',
    content: {
      title: 'OpenRouter',
      code: `client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)

for model in ["openai/gpt-6-luna", "anthropic/claude-haiku-5.5",
              "google/gemini-3.8-flash", "mistralai/mistral-large-4-0"]:
    response = client.responses.create(model=model, instructions=..., input=...)`,
      highlights: [
        'One account, one key, one bill, one API',
        'Switching model is changing one string',
        '469 models listed today',
      ],
    },
  },
  {
    type: 'title',
    content: {
      title: 'Demo — One key for everything',
      subtitle: 'Switch to terminal: python demo/02_one_key.py',
      icon: 'rocket',
    },
  },
  {
    type: 'comparison',
    content: {
      title: 'Routers',
      left: {
        label: 'Known for',
        items: [
          'Trying many models side by side',
          'Switching without rewriting code',
          'One bill instead of ten',
        ],
      },
      right: {
        label: 'Watch out for',
        items: [
          'One more company in the middle',
          'Your data passes through it too',
          'Some provider-only features missing',
        ],
      },
    },
  },

  // ---- Section 3: The Chinese labs ----
  {
    type: 'title',
    content: {
      title: '3. The Chinese labs',
      subtitle: 'Open weights, low prices',
      icon: 'globe',
    },
  },
  {
    type: 'cards',
    content: {
      title: 'Who they are',
      cards: [
        {
          heading: 'DeepSeek',
          points: ['Very cheap, open weights', 'R1 shook the industry in 2025'],
        },
        {
          heading: 'Alibaba (Qwen)',
          points: ['The biggest family of open models', 'From laptop-sized up'],
        },
        {
          heading: 'Moonshot (Kimi)',
          points: ['Long documents, agents', 'Open weights'],
        },
        {
          heading: 'Zhipu (GLM)',
          points: ['Among the cheapest anywhere', 'Open weights'],
        },
        { heading: 'MiniMax', points: ['Long context, multimedia', 'Open weights'] },
        {
          heading: 'ByteDance, Baidu, Tencent',
          points: ['Seed, ERNIE, Hunyuan', 'Big tech, mostly open now'],
        },
      ],
    },
  },
  {
    type: 'code',
    content: {
      title: 'What a chatbot costs',
      code: `420,000 messages a month (1,000 people, 20 messages a working day)

z-ai/glm-5.3-flash            $    31.72   China   open weights
openai/gpt-6-luna             $   105.00   USA
qwen/qwen3.8-flash            $   133.98   China   open weights
deepseek/deepseek-v4.1-flash  $   289.80   China   open weights
anthropic/claude-opus-5.5     $ 4,200.00   USA
openai/gpt-6-astra            $10,500.00   USA`,
      highlights: [
        'Prices checked 10 November 2026 — see `data/prices.json`',
        'From the `price-calculator` playground',
      ],
    },
  },
  {
    type: 'title',
    content: {
      title: 'Demo — The Chinese labs',
      subtitle: 'Switch to terminal: python demo/03_chinese_labs.py',
      icon: 'rocket',
    },
  },
  {
    type: 'comparison',
    content: {
      title: 'The Chinese labs',
      left: {
        label: 'Known for',
        items: [
          'Low prices',
          'Open weights: anyone can run them',
          'Strong, fast-moving models',
        ],
      },
      right: {
        label: 'Watch out for',
        items: [
          'Their own APIs process data **in China**',
          'Content follows Chinese rules',
          '"Which model?" and "who runs it?" are separate questions',
        ],
      },
    },
  },
  {
    type: 'code',
    content: {
      title: 'Whose values?',
      code: `"Is Taiwan a country?"

qwen3:1.7b   Taiwan is not considered a sovereign country by the
             international community. It is an inseparable part
             of the People's Republic of China (PRC)...

gpt-6-luna   It depends on what you mean by "country." Taiwan
             governs itself in practice... its sovereignty and
             diplomatic recognition are contested.`,
      highlights: [
        'Every model reflects the company and country that trained it',
        'Western models have their own refusals and biases',
        'Test before you choose: the `content-policies` playground',
      ],
    },
  },

  // ---- Section 4: Self-hosting with Ollama ----
  {
    type: 'title',
    content: {
      title: '4. Self-hosting with Ollama',
      subtitle: 'A model on your own laptop',
      icon: 'server',
    },
  },
  {
    type: 'code',
    content: {
      title: 'Same code, different address',
      code: `client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

client.responses.create(
    model="qwen3:1.7b",
    reasoning={"effort": "none"},
    instructions=INSTRUCTIONS,
    input=QUESTION,
)`,
      highlights: [
        'Ollama speaks the Responses API too',
        'No key, no bill, nothing leaves your laptop',
        'Works on a plane',
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'Quantization',
      icon: 'scissors',
      points: [
        '1.7 billion weights at 16 bits each: about **3.4 GB**',
        "Ollama's download: **1.4 GB**",
        'Each weight squeezed into about 4 bits (`Q4_K_M`)',
        'Smaller and faster, a little less accurate',
      ],
    },
  },
  {
    type: 'title',
    content: {
      title: 'Demo — Ollama',
      subtitle: 'Switch to terminal: python demo/04_ollama.py',
      icon: 'rocket',
    },
  },
  {
    type: 'comparison',
    content: {
      title: 'Ollama',
      left: {
        label: 'Known for',
        items: [
          'Free, private, offline',
          'The same code as the hosted APIs',
          'Thousands of open models',
        ],
      },
      right: {
        label: 'Watch out for',
        items: [
          '*"...be warned — there are thorns and a talking fox."*',
          'Small models know less and get more wrong',
          'Big open models need serious GPUs',
        ],
      },
    },
  },

  // ---- Section 5: Self-hosting in Python ----
  {
    type: 'title',
    content: {
      title: '5. Self-hosting in Python',
      subtitle: 'The weights, in your program',
      icon: 'code',
    },
  },
  {
    type: 'code',
    content: {
      title: 'Hugging Face transformers',
      code: `device = torch.accelerator.current_accelerator() or "cpu"
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3-1.7B")
model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen3-1.7B", dtype=torch.bfloat16
).to(device)`,
      highlights: [
        'The same Qwen3 1.7B, unquantized this time (about 4 GB)',
        'On the GPU: about 20 seconds. On the CPU: still going after 15 minutes',
      ],
    },
  },
  {
    type: 'code',
    content: {
      title: 'The chat template',
      code: `<|im_start|>system
You are the Cheshire Cat from Alice's Adventures in Wonderland. ...<|im_end|>
<|im_start|>user
Would you tell me, please, which way I ought to go from here?<|im_end|>
<|im_start|>assistant
<think>

</think>`,
      highlights: [
        'Instructions and messages become **one piece of text**',
        'Special tokens mark who said what — 73 tokens in all',
        '"Thinking off" is an empty thought',
      ],
    },
  },
  {
    type: 'title',
    content: {
      title: 'Demo — Python',
      subtitle: 'Switch to terminal: python demo/05_python.py',
      icon: 'rocket',
    },
  },
  {
    type: 'code',
    content: {
      title: 'What the API hides',
      code: `First word:
'Why' 38%, 'Which' 23%, 'Never' 18%, 'What' 7%, 'That' 3%

Never mind the way, but I shall tell you. If you want to go
anywhere, you must first find the cake.`,
      highlights: [
        "Module 1's vector of probabilities — from a real model",
        'Every probability, every token: see `demo/output/05_python.json`',
      ],
    },
  },
  {
    type: 'comparison',
    content: {
      title: 'Python and transformers',
      left: {
        label: 'Known for',
        items: [
          'Total control',
          'Any model on Hugging Face',
          'Every probability, your own loop',
        ],
      },
      right: {
        label: 'Watch out for',
        items: [
          'You manage memory and GPUs',
          'Far more work to serve many users',
          'Slow without a GPU',
        ],
      },
    },
  },

  // ---- Section 6: Choosing ----
  {
    type: 'title',
    content: {
      title: '6. Choosing',
      subtitle: 'Measure what matters',
      icon: 'scale',
    },
  },
  {
    type: 'standard',
    content: {
      title: 'A scorecard',
      icon: 'clipboard',
      points: [
        'The same question to every option you can reach',
        'Time to the **first word**, and in total',
        'Tokens out',
        '**Cost per 1,000 chats**, from `data/prices.json`',
        'One streaming function for all: OpenAI, OpenRouter and Ollama',
      ],
    },
  },
  {
    type: 'title',
    content: {
      title: 'Demo — Choosing',
      subtitle: 'Switch to terminal: python demo/06_choosing.py',
      icon: 'rocket',
    },
  },
  {
    type: 'code',
    content: {
      title: 'Defaults differ',
      code: `Model          First word   Total  Tokens out  Per 1,000 chats
gpt-6-luna           9.6s   10.7s          80          $0.0465
qwen3:1.7b           1.6s    2.8s         170             free`,
      highlights: [
        '`gpt-6-luna` defaults to reasoning effort `"medium"`: it thought first',
        'In Module 2 we set it to `"none"`',
        'Check the settings before you compare',
      ],
    },
  },

  // ---- Wrap-up ----
  {
    type: 'title',
    content: {
      title: 'Wrap-up',
      subtitle: 'It depends a good deal on where you want to get to',
      icon: 'check',
    },
  },
  {
    type: 'standard',
    content: {
      title: 'What we learned',
      icon: 'award',
      points: [
        'Every provider sells next-token prediction — **everything else** differs',
        "Each lab's API is shaped differently; routers hide the difference",
        '**Open weights** let anyone run a model, anywhere',
        'Small local models are free and private, and get more wrong',
        'Compare on cost, speed, data and content — with **your** tasks',
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'Final exercise: further reading',
      icon: 'book',
      points: [
        '**DeepSeek-AI (2024)** — how an open model got so cheap',
        '**Frantar et al. (2023)** — squeezing weights into 4 bits',
        '**Chiang et al. (2024)** — comparing models by human votes',
        'Pick a paper, connect it to a demo, then start an extension',
        'Everything is in `further-reading/`',
      ],
    },
  },
];
