# Further reading and extensions

Why did open models get so good and so cheap? How do you squeeze a model onto a laptop? What does "open" really mean? And how do you tell which model is best?

## The exercise

1. **Pick one paper** from the reading list. If you're not sure, start with one marked ⭐.
2. **Read the part that matters.** You don't need to read it all. Each description says what to look for.
3. **Connect it to a demo.** Write two or three sentences: what problem was the paper solving, and which of our demos or playgrounds does it relate to?
4. **Pick one extension** from the list at the end and start it. Most will take longer than a break, so take them home.

---

## Reading list

### Why open models got cheap

**⭐ DeepSeek-AI (2024). "DeepSeek-V3 Technical Report." [arXiv:2412.19437](https://arxiv.org/abs/2412.19437)**

The open model that showed frontier performance could be trained for a fraction of what anyone expected. Look at the abstract and the cost table near the start: the training run's cost, in dollars. Then look for **mixture of experts**: the model has hundreds of billions of parameters, but only a small fraction of them is used for each token, which is a big part of why it is cheap to run. This is why the Chinese labs in demo 3 can charge so little.

**Shazeer, N. et al. (2017). "Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer." *ICLR 2017*. [arXiv:1701.06538](https://arxiv.org/abs/1701.06538)**

Where mixture of experts came from. Instead of one big layer that every token passes through, many smaller "experts", and a small network that picks a few of them for each token. Look at figure 1.

**Fedus, W., Zoph, B. & Shazeer, N. (2022). "Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity." *Journal of Machine Learning Research* 23(120):1–39. [arXiv:2101.03961](https://arxiv.org/abs/2101.03961)**

Mixture of experts made simple: send each token to just one expert. Read it to understand what "280 billion total parameters" in a model card does and doesn't mean.

**DeepSeek-AI (2025). "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning." [arXiv:2501.12948](https://arxiv.org/abs/2501.12948)**

The open reasoning model that shook the industry in January 2025. It learned to "think" before answering mostly through reinforcement learning, then that ability was copied into small models. The "thinking" Qwen3 does in demo 4 comes from this line of work.

**Hinton, G., Vinyals, O. & Dean, J. (2015). "Distilling the Knowledge in a Neural Network." *NIPS Deep Learning Workshop*. [arXiv:1503.02531](https://arxiv.org/abs/1503.02531)**

**Distillation**: train a small model to copy a big one's probabilities, not just its answers. Most small open models, including the Qwen3 models we ran, are made partly this way.

**Qwen Team (2025). "Qwen3 Technical Report." [arXiv:2505.09388](https://arxiv.org/abs/2505.09388)**

The family we ran in demos 4 and 5. Look for how one family covers sizes from 0.6 billion parameters up, how the small models learn from the big ones, and how thinking is switched on and off: the empty `<think></think>` in demo 5's chat template.

### Making models small enough to run

**⭐ Frantar, E., Ashkboos, S., Hoefler, T. & Alistarh, D. (2023). "GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers." *ICLR 2023*. [arXiv:2210.17323](https://arxiv.org/abs/2210.17323)**

How to squeeze each weight of a trained model into 3 or 4 bits with little loss in quality, without retraining. Ollama's `Q4_K_M` files use llama.cpp's own method, but the idea is the same: it's why `qwen3:1.7b` was a 1.4 GB download, not 3.4 GB.

**Dettmers, T., Lewis, M., Belkada, Y. & Zettlemoyer, L. (2022). "LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale." *NeurIPS 2022*. [arXiv:2208.07339](https://arxiv.org/abs/2208.07339)**

Why quantizing large models is harder than it looks: a few "outlier" values in each layer matter far more than the rest. Look at the section on emergent outliers.

**Lin, J. et al. (2024). "AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration." *MLSys 2024*. [arXiv:2306.00978](https://arxiv.org/abs/2306.00978)**

A simpler idea: protect the 1% of weights that matter most, and quantize the rest. Many of the 4-bit models on Hugging Face are AWQ models.

**Kwon, W. et al. (2023). "Efficient Memory Management for Large Language Model Serving with PagedAttention." *SOSP 2023*. [arXiv:2309.06180](https://arxiv.org/abs/2309.06180)**

The paper behind vLLM, the most widely used way to serve open models to many users at once. Ollama is for one person on a laptop; this is how you serve a whole company. Look at the explanation of the memory each conversation needs while it is being generated.

### What "open" means

**⭐ Liesenfeld, A. & Dingemanse, M. (2024). "Rethinking open source generative AI: open washing and the EU AI Act." *FAccT 2024*, 1774–1787. [doi:10.1145/3630106.3659005](https://doi.org/10.1145/3630106.3659005)**

"Open weights" is not "open source". This paper scores dozens of "open" models on what they really share: weights, training data, code, documentation, licence. Many share only the weights. Read it before trusting the "open weights" column in the map.

**Solaiman, I. (2023). "The Gradient of Generative AI Release: Methods and Considerations." *FAccT 2023*. [arXiv:2302.04844](https://arxiv.org/abs/2302.04844)**

Release isn't open or closed: it's a scale, from fully closed to API-only to downloadable weights to fully open. Look at figure 1, then place each lab from the map on it.

**Touvron, H. et al. (2023). "Llama 2: Open Foundation and Fine-Tuned Chat Models." [arXiv:2307.09288](https://arxiv.org/abs/2307.09288)**

The release that started the open-weights boom. Read the introduction for why Meta published the weights, then look up the Llama licence: free to use, but with conditions. "Open" models come with licences, and you should read them.

### Comparing models

**⭐ Chiang, W.-L. et al. (2024). "Chatbot Arena: An Open Platform for Evaluating LLMs by Human Preference." *ICML 2024*. [arXiv:2403.04132](https://arxiv.org/abs/2403.04132)**

The famous leaderboard: people ask two anonymous models the same question and vote for the better answer. Hundreds of thousands of votes become a ranking. Look at how votes become scores.

**Singh, S. et al. (2025). "The Leaderboard Illusion." [arXiv:2504.20879](https://arxiv.org/abs/2504.20879)**

The case against trusting that leaderboard too much: some labs test many private versions and publish only the best, and some models get far more votes than others. Read it straight after Chiang et al.

**Liang, P. et al. (2023). "Holistic Evaluation of Language Models." *Transactions on Machine Learning Research*. [arXiv:2211.09110](https://arxiv.org/abs/2211.09110)**

HELM: compare models on many things at once (accuracy, robustness, fairness, bias, toxicity, efficiency), not one score. Compare with the questions at the start of this module.

---

## Sites, courses and docs

- **[OpenRouter documentation](https://openrouter.ai/docs)** and its [public model list](https://openrouter.ai/api/v1/models), which `data/build_prices.py` reads.
- **[Ollama documentation](https://docs.ollama.com)** and its [model library](https://ollama.com/library).
- **[Hugging Face LLM course](https://huggingface.co/learn/llm-course)**: free, hands-on, and the best introduction to `transformers`.
- **[Artificial Analysis](https://artificialanalysis.ai)**: independent measurements of models' quality, speed and price, updated continuously.
- **[LMArena](https://lmarena.ai)**: the Chatbot Arena leaderboard. Vote on a few comparisons yourself.
- **[vLLM documentation](https://docs.vllm.ai)**: for serving open models to many users.

---

## Extensions

Bigger projects than the playground. ★ is an afternoon, ★★★ is a weekend.

**★ Price watch.** Run `data/build_prices.py` every day for a week (a cron job, or a scheduled task), keeping each day's file. Which prices changed? Which models appeared or disappeared? Prices in this field move fast.

**★ Where does my data go?** For every lab in `data/prices.json`, find its data policy: where requests are processed, whether they're stored, for how long, and whether they're used for training. Make a table. Which could your organisation use?

**★ Never go down.** Write a function that tries a list of providers in order: if one fails or takes more than ten seconds, try the next. Test it by giving the first provider a wrong API key. Every production chatbot needs this.

**★★ A smart router.** Send easy questions to a cheap model and hard ones to an expensive one. Use the cheap model itself to decide which is which. Run fifty questions through it and work out how much you saved compared with always using the expensive model, and how many answers got worse.

**★★ Your own arena.** Build a small Chatbot Arena: show two anonymous answers to the same question side by side, let people vote, and turn the votes into a ranking (look up the Elo rating system). Run it with your colleagues on questions from your own work. Does your ranking match the public one?

**★★ Serve it properly.** Run an open model with vLLM or llama.cpp's server instead of Ollama, and point the Module 2 chatbot at it. Then have ten copies of the chatbot ask questions at the same time. How do Ollama and the server compare?

**★★★ Quantize it yourself.** Use llama.cpp's tools to convert Qwen3 1.7B from Hugging Face into its own file format, then quantize it to 8, 4 and 2 bits. Measure the file size, the speed and the answers to the `local-models` questions at each size. Where does it fall apart?

**★★★ Distil a Cheshire Cat.** Use a big model to write 1,000 Cheshire Cat replies to 1,000 questions. Fine-tune `Qwen3-0.6B` on them (look up LoRA and the `peft` library). Does the tiny model become a convincing Cat? Is it better than giving the tiny model instructions?
