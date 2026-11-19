# Local models

How small can a model be and still be useful? You'll ask the same three questions of two Qwen models running on your laptop.

From the module folder (`day-one/module-04-choosing-a-provider`):

```bash
ollama pull qwen3:0.6b
ollama pull qwen3:1.7b
uv run python playground/local-models/play.py
```

Or without `uv` (set up `.venv` once at the repo root with `python3 -m venv .venv && .venv/bin/pip install -e .`):

```bash
ollama pull qwen3:0.6b
ollama pull qwen3:1.7b
source ../../.venv/bin/activate
python playground/local-models/play.py
```

Needs Ollama running (`qwen3:0.6b` is 523 MB; `qwen3:1.7b` is 1.4 GB). The answers are written to `playground/local-models/output/answers.txt`.

---

One model has 0.6 billion parameters, the other 1.7 billion. Both run in Ollama.

```text
=== Who wrote Alice's Adventures in Wonderland, and in what year was it published? ===
qwen3:0.6b    0.4s  Alice's Adventures in Wonderland was written by **Lewis Carroll** and was published in **1865**.
qwen3:1.7b    0.7s  *Alice's Adventures in Wonderland* was written by **Charles Lutwidge Dickens** (also known as **Charles Dodgson**), and it was published in **1865**.

=== If Alice is 7 and her sister is twice her age, how old will her sister be in 3 years? ===
qwen3:0.6b    0.7s  ... **Alice's sister will be 17 years old**.
qwen3:1.7b    1.2s  ... ### Final Answer: **17**
```

## Things to notice

- **Bigger isn't always right.** The 1.7B model blended Charles Dickens with Charles Dodgson (Lewis Carroll's real name). On an earlier run it got the name right but gave the year as 1871, which is when _Through the Looking-Glass_ came out. Small models know facts loosely and get them wrong with complete confidence.
- **Both are fast.** Under a second for a short answer, on a laptop, for free.

## Try this

1. **Bigger models.** `ollama pull qwen3:4b` (2.5 GB) and `qwen3:8b` (5.2 GB), and add them to `MODELS`. Where does the answer get reliably right? How much slower is it?
2. **Run it again.** Run the script three times. Do the small models make the same mistakes each time?
3. **Thinking.** Remove `reasoning={"effort": "none"}`. With thinking on, does the 0.6B model get more right? How much slower is it?
4. **Other families.** Try models from other labs: `ollama pull gemma3:1b` (Google) or `llama3.2:1b` (Meta). Same questions, same size: which family is best?
5. **Quantization.** The tags page for each model (for example [ollama.com/library/qwen3/tags](https://ollama.com/library/qwen3/tags)) lists versions with 8-bit or 16-bit weights instead of 4-bit. Pull one and compare: bigger download, slower, more accurate?
6. **Your questions.** Write ten questions about something you know well. What's the smallest model that gets eight right?

## Questions

For discussion. There are no right answers.

- The 1.7B model got the author wrong, and the 0.6B model got it right. How would you test whether a small model is good enough for a job?
- When is "free, private and offline" worth "knows less and gets more wrong"?
- Would you let a small local model answer customers' questions? Your colleagues' questions? What's the difference?

## Further reading

- **Qwen Team (2025). "Qwen3 Technical Report."** [arXiv:2505.09388](https://arxiv.org/abs/2505.09388). The family in this playground. Look for how one family covers sizes from 0.6 billion parameters up, and how the small models learn from the big ones.
- **Frantar, E., Ashkboos, S., Hoefler, T. & Alistarh, D. (2023). "GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers." _ICLR 2023_.** [arXiv:2210.17323](https://arxiv.org/abs/2210.17323). How a trained model's weights are squeezed into a few bits. This is why `qwen3:1.7b` is a 1.4 GB download rather than 3.4 GB.

## Rabbit holes

Optional extensions and interesting things to look at.

1. **The modelfile.** `ollama show qwen3:1.7b --modelfile`. It names the quant, the chat template, and the stop tokens. The template is why thinking is on or off.
2. **The file format.** The [GGUF spec](https://github.com/ggml-org/ggml/blob/master/docs/gguf.md) is what that quant name means: which weights were stored, and at how many bits. Pull a second quant from the [tags page](https://ollama.com/library/qwen3/tags), ask the same three questions, and note where the answers change.
