# Further reading and extensions

Our chatbot is a next-token predictor, given instructions and a conversation. How did a next-token predictor learn to be a helpful assistant? How does it see? And what happens when the conversation gets long?

## The exercise

1. **Pick one paper** from the reading list. If you're not sure, start with one marked ⭐.
2. **Read the part that matters.** You don't need to read it all. Each description says what to look for.
3. **Connect it to a demo.** Write two or three sentences: what problem was the paper solving, and which of our demos or playgrounds does it relate to?
4. **Pick one extension** from the list at the end and start it. Most will take longer than a break, so take them home.

---

## Reading list

### From next-token predictor to assistant: why instructions work

A model trained only to predict the next token of web text doesn't follow instructions. Asked a question, it is just as likely to continue with three more questions. These papers are how it learned to answer.

**⭐ Ouyang, L. et al. (2022). "Training language models to follow instructions with human feedback." *NeurIPS 2022*. [arXiv:2203.02155](https://arxiv.org/abs/2203.02155)**

InstructGPT, the direct ancestor of ChatGPT. Look at figure 2: first show the model examples of good answers, then have people rank its answers, train a second model to predict those rankings, and use that to train the first model further. This is **reinforcement learning from human feedback (RLHF)**. Their 1.3-billion-parameter model's answers were preferred to those of the original 175-billion-parameter GPT-3.

**Christiano, P. et al. (2017). "Deep reinforcement learning from human preferences." *NeurIPS 2017*. [arXiv:1706.03741](https://arxiv.org/abs/1706.03741)**

Where RLHF came from, before language models: teaching a simulated robot to do a backflip from people choosing which of two video clips looked better. Read the introduction for the idea.

**Wei, J. et al. (2022). "Finetuned Language Models Are Zero-Shot Learners." *ICLR 2022*. [arXiv:2109.01652](https://arxiv.org/abs/2109.01652)**

"Instruction tuning": fine-tune a model on many tasks, each described as an instruction, and it gets much better at following instructions it has never seen. The other half of how `instructions=` became something a model pays attention to.

**Bai, Y. et al. (2022). "Constitutional AI: Harmlessness from AI Feedback." [arXiv:2212.08073](https://arxiv.org/abs/2212.08073)**

Instead of people ranking every answer, give the model a short list of principles and let it critique and revise its own answers. Compare with the `personas` playground: a persona is a set of principles too.

### Instructions, and breaking them

**Perez, F. & Ribeiro, I. (2022). "Ignore Previous Prompt: Attack Techniques For Language Models." *NeurIPS ML Safety Workshop*. [arXiv:2211.09527](https://arxiv.org/abs/2211.09527)**

**Prompt injection**: getting a model to ignore its instructions by what you type. Read it after trying to break the characters in the `personas` playground.

**Wallace, E. et al. (2024). "The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions." [arXiv:2404.13208](https://arxiv.org/abs/2404.13208)**

Why should the instructions beat whatever the user types? Because models are now trained to rank them: instructions from the developer above messages from the user, and both above text the model happens to read. This is why our Cheshire Cat stays a cat even when you ask it not to — mostly.

**Wei, J. et al. (2022). "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models." *NeurIPS 2022*. [arXiv:2201.11903](https://arxiv.org/abs/2201.11903)**

Ask a model to work through a problem step by step before answering, and it gets much better at maths and logic. Reasoning models build this in: the `reasoning={"effort": ...}` setting controls how many "thinking" tokens they write before the answer. See the reasoning tokens in the `model-shootout` playground.

### Long conversations

**⭐ Liu, N. F. et al. (2024). "Lost in the Middle: How Language Models Use Long Contexts." *Transactions of the ACL* 12:157–173. [arXiv:2307.03172](https://arxiv.org/abs/2307.03172)**

Hide the answer to a question somewhere in a long context, and models find it easily at the start or the end, but often miss it in the middle. Look at figure 1, the U-shaped curve. Worth knowing before you send a very long conversation, as in the `cost-of-memory` playground.

**Packer, C. et al. (2023). "MemGPT: Towards LLMs as Operating Systems." [arXiv:2310.08560](https://arxiv.org/abs/2310.08560)**

If the conversation won't fit, manage it like an operating system manages memory: keep the recent part in the context window, move the rest out to storage, and let the model fetch it back when needed. A more ambitious version of the summarising idea in the `cost-of-memory` playground.

### Streaming: why replies come one token at a time

**Pope, R. et al. (2023). "Efficiently Scaling Transformer Inference." *MLSys 2023*. [arXiv:2211.05102](https://arxiv.org/abs/2211.05102)**

How big models are actually run to generate text. Look for the difference between the two phases: reading the prompt can be done all at once, but writing the reply has to happen one token after another, because each token depends on the last. That's what you watch in demo 4.

**Leviathan, Y., Kalman, M. & Matias, Y. (2023). "Fast Inference from Transformers via Speculative Decoding." *ICML 2023*. [arXiv:2211.17192](https://arxiv.org/abs/2211.17192)**

A clever way round the one-at-a-time problem: let a small, fast model guess the next few tokens, and have the big model check them all at once. The output follows exactly the same probabilities as the big model on its own, just faster.

### How a language model sees

**⭐ Dosovitskiy, A. et al. (2021). "An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale." *ICLR 2021*. [arXiv:2010.11929](https://arxiv.org/abs/2010.11929)**

The Vision Transformer. Look at figure 1: cut an image into 16×16 patches, turn each patch into a vector, and feed them to a transformer exactly as if they were word tokens. This is the idea behind demo 5.

**Radford, A. et al. (2021). "Learning Transferable Visual Models From Natural Language Supervision." *ICML 2021*. [arXiv:2103.00020](https://arxiv.org/abs/2103.00020)**

CLIP: train an image model and a text model together on 400 million pictures and their captions, so that a picture and a description of it end up with similar vectors. A preview of embeddings, which are coming up later in the course.

**Alayrac, J.-B. et al. (2022). "Flamingo: a Visual Language Model for Few-Shot Learning." *NeurIPS 2022*. [arXiv:2204.14198](https://arxiv.org/abs/2204.14198)**

How to plug an image model into an existing language model so that pictures and text can be mixed freely in one conversation, as in demo 5.

**Liu, H., Li, C., Wu, Q. & Lee, Y. J. (2023). "Visual Instruction Tuning." *NeurIPS 2023*. [arXiv:2304.08485](https://arxiv.org/abs/2304.08485)**

LLaVA: a surprisingly simple recipe for a chatbot that can see. Connect an image model to a language model with one small layer, then teach it with conversations about pictures. Instruction tuning, again, for images.

### Does it know what it knows?

**Kadavath, S. et al. (2022). "Language Models (Mostly) Know What They Know." [arXiv:2207.05221](https://arxiv.org/abs/2207.05221)**

When a model gives an answer a 70% probability, is it right 70% of the time? Mostly, yes. Read it alongside the `logprobs` playground.

**OpenAI (2023). "GPT-4 Technical Report." [arXiv:2303.08774](https://arxiv.org/abs/2303.08774)**

Look for figure 8. Before instruction training, GPT-4's probabilities were well calibrated: when it was 70% sure, it was right about 70% of the time. After training to be an assistant, it became much more sure of itself than it should be. Compare with how often the `logprobs` playground shows 100%.

---

## Guides, books and videos

- **OpenAI API guides.** The official guides to the things in this module: [Text generation](https://developers.openai.com/api/docs/guides/text), [Conversation state](https://developers.openai.com/api/docs/guides/conversation-state), [Streaming](https://developers.openai.com/api/docs/guides/streaming-responses), [Images and vision](https://developers.openai.com/api/docs/guides/images-vision), [Reasoning](https://developers.openai.com/api/docs/guides/reasoning) and [Prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching).
- **The OpenAI Cookbook**, [cookbook.openai.com](https://cookbook.openai.com/): worked examples of almost everything the API can do.
- **Andrej Karpathy, "Intro to Large Language Models"** ([video](https://www.youtube.com/watch?v=zjkBMFhNj_g), 2023). An hour-long talk for a general audience: what a model is, how it becomes an assistant, and where it goes wrong.
- **Andrej Karpathy, "Deep Dive into LLMs like ChatGPT"** ([video](https://www.youtube.com/watch?v=7xTGNNLPyMI), 2025). Three and a half hours on everything between the raw text and the chatbot: tokens, pre-training, instruction tuning, RLHF and reasoning.
- **Chip Huyen, *AI Engineering* (O'Reilly, 2025).** A book on building real applications on top of models like this one: prompting, evaluation, cost and latency.

---

## Extensions

Bigger projects than the playground. ★ is an afternoon, ★★★ is a weekend.

**★ Tell the story from the pictures.** Send all five Tenniel illustrations in this module (`data/` and `playground/vision/images/`) in one message, in book order, and ask the model to tell the story they illustrate. How close does it get to Carroll's? Does it know where they come from?

**★ A stop button.** While a reply is streaming, pressing Ctrl-C should stop the reply but not the chatbot. Keep what was written so far in the conversation, and carry on. (Catch `KeyboardInterrupt` inside the streaming loop.)

**★★ No SDK.** Rewrite demo 4 using only Python's standard library: `urllib.request` to call the API, and your own code to read the stream of server-sent events. You'll see exactly what the `openai` package does for you.

**★★ Needle in a haystack.** Put the whole of *Alice* (from Module 1) into the instructions, hide one made-up fact somewhere in it ("The Dormouse's favourite number is 37"), and ask for it. Move the fact from the start to the middle to the end. Do you see Liu et al.'s U-shape? What does each attempt cost?

**★★ The secret keeper.** Write instructions for a bot that guards a password and must never reveal it. Then challenge other people to get it out. Every time someone succeeds, harden the instructions. Read Perez & Ribeiro and Wallace et al. for ideas on both sides.

**★★ Does it know what it knows?** Ask the model 50 multiple-choice quiz questions, answering with a single letter, and record the probability it gave its answer (see the `logprobs` playground). Group the answers by confidence and check how often each group was right. Is it well calibrated?

**★★ Memory that lasts.** At the end of each chat, ask the model to write down anything worth remembering about the user as a short list, and save it to a file. Next time, put that list in the instructions. Now it remembers you between chats.

**★★★ A web chatbot.** Put the chatbot in a web page. Use Python's `http.server` (or a small framework) to serve a page with a text box, and stream the reply to the browser as it is generated, using server-sent events. This is how every chatbot website works.
