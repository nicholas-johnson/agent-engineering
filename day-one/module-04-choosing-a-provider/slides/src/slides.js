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
      title: 'Module 4 — Choosing a Provider',
      subtitle: 'Which model?',
      icon: 'compass',
    },
  },
  {
    type: 'description',
    content: {
      title: 'It depends',
      icon: 'question',
      description:
        'Every provider sells the same thing: a model that predicts the next token. What differs are the tokens you get, the APIs you call, and the prices you pay.',
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
          points: [
            '**ChatGPT** for conversation',
            '**Codex** for writing code',
            'The API the others copy',
          ],
        },
        {
          heading: 'Anthropic',
          points: [
            '**Claude**, in a desktop app',
            '**Claude Code** for software',
            '**Claude Cowork** for the rest',
          ],
        },
        {
          heading: 'Google',
          points: [
            '**Gemini**, inside Search and Android',
            '**Gemini Notebook** for your sources',
            '**Antigravity**, their coding IDE',
          ],
        },
        {
          heading: 'xAI',
          points: [
            '**Grok**, the new contender',
            '**Grok Bot**, with its own computer',
            '**Cursor**, the code editor',
          ],
        },
      ],
    },
  },
  {
    type: 'cards',
    content: {
      title: 'Cost: Input / output, $ per million tokens',
      cards: [
        {
          heading: 'OpenAI',
          points: [
            '**Astra** $10 / $50',
            '**Sol** $2 / $10',
            '**Terra** $1 / $5',
            '**Luna** $0.10 / $0.50',
          ],
        },
        {
          heading: 'Anthropic',
          points: [
            '**Fable** $8 / $40',
            '**Opus** $4 / $20',
            '**Sonnet** $2 / $10',
            '**Haiku** $0.10 / $0.50',
          ],
        },
        {
          heading: 'Google',
          points: [
            '**Carbon** $2 / $10',
            '**Argon** $2 / $10',
            '**3.8 Flash** $0.80 / $4',
            '**Flash Lite** $0.30 / $2.50',
          ],
        },
        {
          heading: 'xAI',
          points: ['**Grok 4.7** $2 / $6', '**Grok Build** $1 / $2'],
        },
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'OpenAI — scale and reach',
      icon: 'globe',
      points: [
        'Mission: build **AGI that benefits all of humanity**',
        'First mover — **ChatGPT** made AI mainstream',
        'The API every other lab copies',
        'Huge consumer reach and the biggest developer ecosystem',
        'Backed by Microsoft; enormous compute',
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'Anthropic — safety',
      icon: 'shield',
      points: [
        'Founded in 2021 by researchers who **left OpenAI**',
        '**Safety and alignment** are the stated mission',
        '**Constitutional AI**: trained against a written set of principles',
        'Careful, deliberate releases',
        'Claude is strong at coding and long, careful reasoning',
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'Google — research and reach',
      icon: 'search',
      points: [
        "**DeepMind's** deep research pedigree",
        'Runs on its own chips (**TPUs**), not just Nvidia',
        'Built into **Search, Android, Gmail, Workspace**',
        'Enormous data and distribution',
        'Gemini is natively multimodal — text, images, audio, video',
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'xAI — free speech',
      icon: 'message-square',
      points: [
        'Founded by **Elon Musk** in 2023',
        'A **"truth-seeking"** AI, less filtered than its rivals',
        'Willing to answer where others refuse',
        'Trained on its own giant GPU cluster (**Colossus**)',
        'The newest of the four, moving fast',
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
    type: 'standard',
    content: {
      title: 'AWS Bedrock',
      icon: 'server',
      points: [
        'One API to **many models** — Claude, Llama, Mistral, Amazon Nova',
        'The models run **inside your AWS account and region**',
        'Your prompts are not used to train the models',
        'Enterprise plumbing: IAM, VPC, logging, compliance',
        'Amazon is a major Anthropic backer — Claude is first-class here',
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'Google Cloud — Vertex AI',
      icon: 'cpu',
      points: [
        '**Gemini** plus third-party models (Claude, Llama) in Model Garden',
        'Runs in **your GCP project**, with data-residency controls',
        'Backed by Google infrastructure and **TPUs**',
        'Enterprise plumbing: IAM, VPC Service Controls, audit logs',
        'Tight fit if you already live in Google Cloud',
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'Microsoft Azure — Foundry',
      icon: 'layers',
      points: [
        '**Microsoft Foundry** (renamed from Azure AI Foundry, late 2025)',
        'The enterprise home for **OpenAI** models (Azure OpenAI)',
        'A wider catalogue too — Llama, Mistral, DeepSeek, xAI, and more',
        'Runs in **your Azure tenant and region**',
        'Enterprise plumbing: Entra ID, private networking, compliance',
        'Tight fit with the Microsoft stack — Copilot, Microsoft 365',
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

  // ---- Section 2: The Chinese labs ----
  {
    type: 'title',
    content: {
      title: '2. The Chinese labs',
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
    type: 'code',
    content: {
      title: 'Through OpenRouter',
      code: `client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)

client.responses.create(model="deepseek/deepseek-v4.1-flash", ...)`,
      highlights: [
        'One key reaches these labs',
        'Your data passes through OpenRouter as well as the lab',
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

  // ---- Section 3: Self-hosting with Ollama ----
  {
    type: 'title',
    content: {
      title: '3. Self-hosting with Ollama',
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

  // ---- Section 4: Self-hosting in Python ----
  {
    type: 'title',
    content: {
      title: '4. Self-hosting in Python',
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

  // ---- Section 5: Choosing ----
  {
    type: 'title',
    content: {
      title: '5. Choosing',
      subtitle: 'Measure what matters',
      icon: 'scale',
    },
  },
  {
    type: 'standard',
    content: {
      title: 'Cost',
      icon: 'calculator',
      points: [
        'Priced per million tokens, **input and output** separately',
        'Output usually costs several times more than input',
        'What matters is **cost per task**, not cost per token',
        'A chatty, reasoning-heavy model can beat a cheaper one on cost',
        'Semantic Caching can cut the bill',
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'Speed',
      icon: 'zap',
      points: [
        '**Latency**: time to the first word',
        '**Throughput**: words per second after that',
        'Reasoning models think before they speak — slower to start',
        'Does a person wait on it, or is it a background job?',
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'Capability',
      icon: 'target',
      points: [
        'Is it good enough for your task?',
        'Golden Tests let you know how well it performs',
        'Large agents can improve smaller agents',
        "Bigger isn't always better; small models win on narrow jobs",
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'Data',
      icon: 'database',
      points: [
        '**Where** is it processed, and under **whose laws**?',
        'Is your data **kept**, or used to train the next model?',
        'Cloud hosts keep it in **your** account and region',
        'Sensitive data may force you to self-host',
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'Content',
      icon: 'message-square',
      points: [
        'What will it refuse? Whose values shaped it?',
        'Every model carries the biases of its makers and country',
        'Over-refusal breaks real tasks as surely as under-refusal',
        'Test with the prompts you actually expect to send (Golden Tests)',
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'Openness',
      icon: 'package',
      points: [
        'Can you **download the weights** and run them yourself?',
        'Open: no lock-in, runs offline, total control',
        'Closed: newest features first, nothing to operate',
        'How hard would it be to **switch later**?',
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
      title: 'Not the same answer',
      code: `claude-haiku-5.5
  mixed tin: treacle. marmalade tin: the mixture.

qwen3:1.7b
  mixed tin: marmalade. marmalade tin: treacle.

gemini-3.8-flash
  "…the tin labelled 'tre"`,
      highlights: [
        'Haiku swaps the tins. The small local model does not',
        'Gemini spends the 500 token cap and never finishes',
        'Grok cannot turn reasoning off: 11s and 874 tokens',
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
        "Each lab's API is shaped differently",
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
