# Module 3 — Choosing a Provider

> In Module 2, Alice asked the Cheshire Cat which way she ought to go, and the Cat said *"That depends a good deal on where you want to get to."* That is also the honest answer to "which AI provider should I use?" This module is a survey. We send the same Cheshire Cat to the big American labs, to a router that reaches hundreds of models with one key, to the Chinese labs, and to two models running on your own laptop, one through Ollama and one in plain Python. Along the way we look at what each is known for, what it costs, where your data goes, and what it will and won't say. We finish with a scorecard.

## Learning goals

- Name the main **model providers** (American, Chinese and European) and what each is known for.
- Call several providers from Python, and see that each one's **API** is shaped differently.
- Use a **router** (OpenRouter) to reach hundreds of models with one key and one API.
- Explain **open weights**, and what it does and doesn't mean.
- Run an open model on your own machine, with **Ollama** and with Hugging Face **`transformers`**, and explain **quantization**.
- Compare providers on **cost per task**, **speed**, **where your data goes** and **content policies**, not just on how clever they are.

---

## The question

Every provider sells the same thing: a model that predicts the next token. What differs is everything around it.

| | Questions to ask |
|-|------------------|
| **Cost** | Price per million input and output tokens. What does one *task* cost? |
| **Speed** | How long until the first word? How many words per second? |
| **Capability** | Is it good enough for *your* task? (Test it. Don't trust the leaderboard.) |
| **Context** | How much text can it read at once? |
| **Inputs** | Text only, or images, audio and video too? |
| **Data** | Where is your data processed, under which country's laws, and is it kept? |
| **Content** | What will it refuse to say, and whose values shaped it? |
| **Openness** | Can you download the weights and run it yourself? Under what licence? |
| **Lock-in** | How hard is it to switch to someone else later? |

## The map

Prices are from [OpenRouter's public model list](https://openrouter.ai/api/v1/models), **checked 10 November 2026**, in US dollars per million tokens. They are usually the same as each lab's own price. They change often: run `data/build_prices.py` to refresh them.

"Open weights" means OpenRouter links the model to a Hugging Face repository where the weights can be downloaded.

### American labs

| Lab | Known for |
|-----|-----------|
| **OpenAI** | The broadest platform: text, images, audio, built-in tools. The API most others copy. |
| **Anthropic** | Claude. Known for coding, agents and long documents, and for its safety research. |
| **Google** | Gemini. Reads text, images, audio and video, with million-token context windows. |
| **xAI** | Grok. Built into X (Twitter), with search over X posts. |
| **Meta** | Its newer Muse models are mostly closed, with one open-weight model. Its older Llama models are open. |
| **Amazon** | Nova models, mainly used inside Amazon Bedrock. |

| Lab | Model | Input $/M | Output $/M | Context | Open weights | Takes |
|-----|-------|----------:|-----------:|--------:|:------------:|-------|
| OpenAI | `gpt-6-astra` | 10 | 50 | 1.1M |  | image, text |
| OpenAI | `gpt-6.1-sol` | 2 | 10 | 1.1M |  | image, text |
| OpenAI | `gpt-6.1-terra` | 1 | 5 | 1.1M |  | image, text |
| OpenAI | `gpt-6-luna` | 0.1 | 0.5 | 1.1M |  | image, text |
| Anthropic | `claude-fable-5.2` | 8 | 40 | 1M |  | text, image |
| Anthropic | `claude-opus-5.5` | 4 | 20 | 1M |  | text, image |
| Anthropic | `claude-sonnet-5.5` | 2 | 10 | 1M |  | text, image |
| Anthropic | `claude-haiku-5.5` | 0.1 | 0.5 | 1M |  | text, image |
| Google | `gemini-4-carbon` | 2 | 10 | 1M |  | audio, image, text, video |
| Google | `gemini-4-argon` | 2 | 10 | 1M |  | audio, image, text, video |
| Google | `gemini-3.8-flash` | 0.825 | 4.125 | 1M |  | text, image, video, audio |
| Google | `gemini-3.5-flash-lite` | 0.3 | 2.5 | 1M |  | text, image, video, audio |
| xAI | `grok-4.7` | 2 | 6 | 500K |  | text, image |
| xAI | `grok-build-0.1` | 1 | 2 | 256K |  | text, image |
| Meta | `muse-wonder` | 4 | 20 | 1M |  | text, image, video, audio |
| Meta | `muse-spark-open` | 1.25 | 4.25 | 1M | yes | text, image, video, audio |
| Amazon | `nova-2-lite-v1` | 0.3 | 2.5 | 1M |  | text, image, video |

### Chinese labs

| Lab | Known for |
|-----|-----------|
| **DeepSeek** | Very low prices and open weights. Its 2025 reasoning model, R1, shook the industry. |
| **Alibaba (Qwen)** | The biggest family of open models, from 0.6 billion parameters up. Many small Qwen models run on a laptop. |
| **Moonshot (Kimi)** | Long documents and agent work. Open weights. |
| **Zhipu (GLM)** | Some of the cheapest capable models anywhere. Open weights. |
| **MiniMax** | Long context and multimedia. Open weights. |
| **ByteDance** | Seed models, behind the Doubao chatbot that is huge in China. Closed. |
| **Baidu, Tencent, Xiaomi** | ERNIE, Hunyuan and MiMo. Big Chinese tech companies, now publishing open weights too. |

| Lab | Model | Input $/M | Output $/M | Context | Open weights | Takes |
|-----|-------|----------:|-----------:|--------:|:------------:|-------|
| DeepSeek | `deepseek-v4-pro-0813` | 0.111 | 4.44 | 1M | yes | text |
| DeepSeek | `deepseek-v4.1-flash` | 0.3 | 1.2 | 1M | yes | text, image |
| Alibaba (Qwen) | `qwen3.8-max-0902` | 2 | 6 | 1M |  | text, image, video |
| Alibaba (Qwen) | `qwen3.8-flash` | 0.15 | 0.47 | 1M | yes | text, image, video |
| Moonshot (Kimi) | `kimi-k3.1-pro` | 2 | 10 | 1M | yes | text, image, video |
| Zhipu (GLM) | `glm-5.3` | 0.07 | 1.4 | 1M | yes | text |
| Zhipu (GLM) | `glm-5.3-flash` | 0.04 | 0.078 | 1M | yes | text, image, video |
| MiniMax | `minimax-m3` | 0.3 | 1.2 | 1M | yes | text, image, video |
| ByteDance | `seed-2-1-turbo` | 0.5 | 2.5 | 262K |  | text, image, video |
| Baidu | `ernie-5.5-flash-preview` | 0.28 | 1.13 | 1M | yes | text |
| Tencent | `hy4` | 0.417 | 1.25 | 1M | yes | text, image |
| Xiaomi | `mimo-v2.6-pro` | 0.435 | 0.87 | 1.1M | yes | text, image, video, audio |

### Elsewhere

| Lab | Known for |
|-----|-----------|
| **Mistral** (France) | Europe's leading lab. Open weights, and a European company for those who need one. |
| **Cohere** (Canada) | Business use: search, retrieval and models that cite their sources. |

| Lab | Model | Input $/M | Output $/M | Context | Open weights | Takes |
|-----|-------|----------:|-----------:|--------:|:------------:|-------|
| Mistral | `mistral-large-4-0` | 0.7 | 2.1 | 1M | yes | text, image |
| Mistral | `mistral-small-2603` | 0.15 | 0.6 | 262K | yes | text, image |
| Cohere | `command-a-plus` | 0.3 | 1.5 | 192K |  | text, image |

### Routers, hosts, clouds and local tools

| Kind | Examples | What they do |
|------|----------|--------------|
| **Routers** | OpenRouter | One key and one API for hundreds of models from every lab. |
| **Fast hosts** | Groq, Cerebras, Together, Fireworks | Run open-weight models, often much faster or cheaper than the lab itself. Groq and Cerebras build their own chips. |
| **Clouds** | AWS Bedrock, Microsoft Azure (Foundry), Google Vertex AI | Many labs' models inside a big cloud. Chosen when a company's data, contracts and security already live there. |
| **Local** | Ollama, LM Studio, llama.cpp, vLLM | Run open-weight models on your own laptop or server. |

---

## Setting up

You won't have every key, and you don't need them all. Each demo runs whatever it can and skips the rest.

| Key in `.env` | For | Get one at |
|---------------|-----|-----------|
| `OPENAI_API_KEY` | OpenAI | platform.openai.com |
| `ANTHROPIC_API_KEY` | Anthropic | platform.claude.com |
| `GEMINI_API_KEY` | Google | aistudio.google.com |
| `XAI_API_KEY` | xAI | console.x.ai |
| `OPENROUTER_API_KEY` | Everything else, including the Chinese labs | openrouter.ai |

For the self-hosting sections:

1. Install [Ollama](https://ollama.com) and download the model (1.4 GB): `ollama pull qwen3:1.7b`
2. Install the optional Python packages, `transformers` and PyTorch: `uv sync --extra local`. The first run of demo 5 downloads the model from Hugging Face (about 4 GB).

Do both before the session: conference Wi-Fi won't cope with everyone downloading at once.

## The data

| File | What | Source |
|------|------|--------|
| `data/prices.json` | Prices, context windows and inputs for 32 models | [OpenRouter model list](https://openrouter.ai/api/v1/models), checked 10 November 2026 |
| `data/build_prices.py` | Rebuilds `prices.json` with today's prices | — |

## Running the demos

From this folder, for example:

```bash
uv run python demo/01_big_labs.py
```

Demo 5 needs the optional packages: `uv run --extra local python demo/05_python.py`.

| Demo | Needs | Writes |
|------|-------|--------|
| `01_big_labs.py` | Any of the four lab keys | `01_big_labs.json` |
| `02_one_key.py` | `OPENROUTER_API_KEY` | `02_one_key.json` |
| `03_chinese_labs.py` | `OPENROUTER_API_KEY` | `03_chinese_labs.json` |
| `04_ollama.py` | Ollama | `04_ollama.txt` |
| `05_python.py` | `uv sync --extra local` | `05_python.json` |
| `06_choosing.py` | Whatever you have | `06_scorecard.json` |

Replies are random, so yours will differ from the examples below.

> **Note for this version of the course:** the outputs below marked *Output to come* need keys we didn't have when this module was written. The code follows each provider's documentation; the output will be added once it has been run.

---

## 1. The big American labs

**Demo:** `demo/01_big_labs.py`

The same instructions and the same question, sent to four labs using each lab's own Python package. Put the four functions side by side and the differences jump out:

| | OpenAI | Anthropic | Google | xAI |
|-|--------|-----------|--------|-----|
| Package | `openai` | `anthropic` | `google-genai` | `openai`, pointed at `api.x.ai` |
| Call | `client.responses.create` | `client.messages.create` | `client.interactions.create` | `client.responses.create` |
| Instructions | `instructions=` | `system=` | `system_instruction=` | `instructions=` |
| Question | `input=` | `messages=[...]` | `input=` | `input=` |
| Reply | `response.output_text` | the `text` block in `response.content` | `interaction.output_text` | `response.output_text` |
| Must set | — | `max_tokens` | — | — |

xAI doesn't have its own API shape at all: it copies OpenAI's, so the `openai` package works with a different `base_url`. Many providers do this, which is part of why OpenAI's API is the closest thing to a standard.

The models: `gpt-6-luna`, `claude-opus-5-5`, `gemini-3.8-flash` and `grok-4.7`. The Anthropic call also turns on Anthropic's **refusal fallback** (`fallbacks="default"`): if the model declines a request for safety reasons, the API retries it on another Claude model.

> **OpenAI:** That depends a good deal on where you want to get to. If you don't much care where, then any road will do—but if you do, tell me your destination, and I'll help you choose.

*Output to come* from Anthropic, Google and xAI.

**Known for / watch out for:** each lab's own package gives you its newest features first. But every one is shaped differently, so switching provider means rewriting your code.

## 2. One key for everything

**Demo:** `demo/02_one_key.py`

A **router** sits between you and the labs. One account, one key, one bill, and one API (OpenAI's) for hundreds of models:

```python
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.environ["OPENROUTER_API_KEY"])

for model in MODELS:
    response = client.responses.create(model=model, instructions=INSTRUCTIONS, input=QUESTION)
```

Switching model is changing one string: `"anthropic/claude-haiku-5.5"`, `"google/gemini-3.8-flash"`, `"mistralai/mistral-large-4-0"`. The demo sends the Cat to seven models from six labs.

*Output to come.*

**Known for / watch out for:** perfect for trying models side by side, and for switching without rewriting code. But it's one more company in the middle, OpenRouter's Responses API is stateless (no `previous_response_id`), the newest provider-only features may not be there, and your data passes through OpenRouter as well as the lab.

## 3. The Chinese labs

**Demo:** `demo/03_chinese_labs.py`

The same router, six Chinese labs: DeepSeek, Qwen, Kimi, GLM, MiniMax and ERNIE.

*Output to come.*

Look back at the map. Most of these models have **open weights**, and many cost a fraction of their American equivalents: `glm-5.3-flash` is $0.04 per million input tokens, against $0.10 for `gpt-6-luna` and $4 for `claude-opus-5.5`.

**Known for / watch out for:**

- **Where your data goes.** Using a Chinese lab's own API generally means your prompts are processed in China, under Chinese law. Many companies' policies don't allow that. But the *same open weights* can be run by an American or European host, or on your own machine. "Which model?" and "who runs it?" are separate questions.
- **Content policies.** Models trained in China must follow Chinese rules on generated content, and they often follow the Chinese government's position on political topics. Western models have their own refusals and biases too. The `content-policies` playground shows the difference, and why you should test before you choose.

## 4. Self-hosting with Ollama

**Demo:** `demo/04_ollama.py`

**Ollama** downloads open-weight models and runs them on your own machine. It speaks OpenAI's Responses API too, so the code is the same as calling OpenAI. Only the address changes:

```python
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
```

No key, no bill, and nothing leaves your laptop. It works on a plane.

The demo streams the Cat's reply from `qwen3:1.7b`, a 1.7-billion-parameter model from Alibaba's Qwen family:

> Which way shall I tell you? Well, you might go whichever way your heart points, but I must say, the path is not clear. Let me see... Ah, yes! The garden is ahead, but be warned—there are thorns and a talking fox.

It's in character, and it's fast. It's also clearly a much smaller model: there are no talking foxes in *Alice*.

The download is 1.4 GB, but 1.7 billion parameters at 16 bits each would be about 3.4 GB. Ollama's copy is **quantized**: each weight is squeezed into about 4 bits (`ollama show qwen3:1.7b` says `Q4_K_M`). Quantized models are smaller and faster, and a little less accurate.

Small models think too: Qwen3 writes hidden "thinking" before it answers, unless you turn it off with `reasoning={"effort": "none"}`. With thinking on, the same question took 4.4 seconds; with it off, 0.8 seconds.

**Known for / watch out for:** free, private and offline. But a model small enough for a laptop knows far less and gets far more wrong than a frontier model (see the `local-models` and `open-vs-closed` playgrounds). The big open models need hundreds of gigabytes of GPU memory.

## 5. Self-hosting in Python

**Demo:** `demo/05_python.py`

Ollama hides the model behind an API. Hugging Face's **`transformers`** library loads the weights straight into your Python program, which means you can see everything:

```python
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3-1.7B")
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen3-1.7B", dtype=torch.bfloat16).to(device)
```

These are the same Qwen3 1.7B weights that Ollama ran, unquantized this time (about 4 GB). The demo runs on the GPU if there is one (Apple silicon or NVIDIA), and takes about 20 seconds on a recent Mac. Our first attempt, on the CPU with full-size 32-bit weights, was still going after a quarter of an hour.

`demo/output/05_python.json` shows three things an API hides:

**The chat template.** Instructions and messages aren't sent to the model separately. They are joined into one piece of text with special tokens marking who said what:

```text
<|im_start|>system
You are the Cheshire Cat from Alice's Adventures in Wonderland. ...<|im_end|>
<|im_start|>user
Would you tell me, please, which way I ought to go from here?<|im_end|>
<|im_start|>assistant
<think>

</think>
```

That's 73 tokens. The empty `<think></think>` is how "thinking off" works: the template writes an empty thought for the model.

**The next-token probabilities.** Module 1's vector, from a real model. The first word of the reply:

```text
'Why' 38%, 'Which' 23%, 'Never' 18%, 'What' 7%, 'That' 3%
```

**The reply:**

> Never mind the way, but I shall tell you. If you want to go anywhere, you must first find the cake.

(PyTorch prints a harmless `Redirects are currently not supported in MacOs` warning on a Mac.)

**Known for / watch out for:** complete control: any model on Hugging Face, every probability, your own generation loop (see the `your-own-loop` playground). But you manage memory, GPUs and speed yourself, and it's far more work to serve many users than Ollama or a hosted API.

## 6. Choosing

**Demo:** `demo/06_choosing.py`

Send the same question to every option you can reach, and measure what matters: how long until the first word, how long in total, how many tokens, and what 1,000 such chats would cost at the prices in `data/prices.json`.

Every option uses the same streaming code, because OpenAI, OpenRouter and Ollama all speak the Responses API. Each model runs with its own default settings.

```text
Model                            First word   Total Tokens out  Per 1,000 chats
gpt-6-luna                             9.6s   10.7s         80          $0.0465
anthropic/claude-haiku-5.5                                  skipped: no API key
anthropic/claude-opus-5.5                                   skipped: no API key
google/gemini-3.8-flash                                     skipped: no API key
x-ai/grok-4.7                                               skipped: no API key
deepseek/deepseek-v4.1-flash                                skipped: no API key
qwen/qwen3.8-flash                                          skipped: no API key
mistralai/mistral-small-2603                                skipped: no API key
qwen3:1.7b                             1.6s    2.8s        170             free
```

*Full scorecard to come.* Even this much has a lesson in it: `gpt-6-luna`'s default reasoning effort is `"medium"`, so it thought for nine seconds before writing a word. In Module 2 we set it to `"none"`. **Defaults differ, and they matter.**

The scorecard is a starting point, not an answer. Add the questions from the start of this module, and the answer to "which provider?" is the Cat's: it depends a good deal on where you want to get to.

---

## Summary

| Option | Good for | Watch out for |
|--------|----------|---------------|
| A lab's own API | Newest features, best support | Every API is different: lock-in |
| A router | Trying many models, one key, easy switching | One more company in the middle; some features missing |
| Chinese labs | Price, open weights | Where data is processed; content policies |
| Ollama | Free, private, offline, same code as the APIs | Small models know less and get more wrong |
| Python + `transformers` | Total control, see every probability | You manage memory, GPUs and speed |

## Playground

[`playground/`](playground/) has six things to play with: a price calculator, a searchable catalogue of every model on OpenRouter, small local models side by side, open versus closed, content policies, and your own generation loop on a real open model.

## Further reading and extensions

The final exercise is in [`further-reading/`](further-reading/): papers on how open models are built and why they are cheap, how to make big models small enough to run yourself, and how models are compared, plus extension projects to take home.

## Slides

```bash
pnpm slides:03
```
