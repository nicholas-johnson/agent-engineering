# Temperature

The `temperature` setting from Module 1, now on a real model. You'll ask the same question eight times at each temperature from 0 to 2.

From the module folder (`day-one/module-02-building-a-chatbot`):

```bash
uv run python playground/temperature/play.py
```

Or without `uv` (set up `.venv` once at the repo root with `python3 -m venv .venv && .venv/bin/pip install -e .`):

```bash
source ../../.venv/bin/activate
python playground/temperature/play.py
```

Needs `OPENAI_API_KEY` in `.env`.

---

This asks `gpt-6-luna`. Temperature 2 is as high as the API allows. The answers go to `playground/temperature/output/temperatures.txt`.

```text
0.0  Otter, Otter, Otter, Otter, Otter, Otter, Otter, Otter
0.5  Otter, Otter, Otter, Otter, Otter, Otter, Otter, Otter
1.0  Otter, Otter, Otter, Otter, Otter, Otter, Otter, Otter
1.5  Otter, Elephant, Otter, Elephant, Otter, Otter, Otter, Otter
2.0  Elephant, Otter, Otter, Otter, Otter, Otter, Otter, Otter
```

Asked for "one animal", the model is so sure about "Otter" that it takes temperature 1.5 before anything else appears. Temperature reshapes the probabilities exactly as in Module 1, but when one answer has nearly all the probability, even a big reshape leaves it on top. The `logprobs` playground shows how sure the model usually is.

## Things to notice

- **Temperature needs reasoning effort `"none"`.** With any other reasoning effort the API says *"Unsupported parameter: 'temperature' is not supported with this model."* The message blames the model, but the cause is the reasoning setting.
- **Temperature 0 is not a guarantee.** For a sentence rather than one word, even temperature 0 gives slightly different answers each time. The way models are run on GPUs adds tiny variations.

## Try this

1. **A longer answer.** Change the prompt to *"Write the opening line of a story about a cat who can disappear."* Can you tell the temperatures apart? (We couldn't, much.)
2. **Top-p.** The API also has `top_p`, which keeps only the most likely tokens that add up to that much probability (Module 1's top-p, built in). Try `temperature=2.0, top_p=1.0`, then `top_p=0.1`.
3. **More tries.** Set `TRIES = 30` at temperature 2. What is the full list of animals it ever says? Why so few, out of all the animals there are?
4. **Find a prompt temperature does affect.** What kind of question has many equally good answers? Try a few and see which one makes temperature matter most.

## Questions

For discussion. There are no right answers.

- Training to be a helpful assistant has made the model very sure of itself: "Otter" almost every time. Is that a good thing?
- Even temperature 0 doesn't give exactly the same answer every time. What does that mean for testing an application built on a model?
- When would you want a chatbot to give the same answer every time, and when wouldn't you?

## Further reading

- **Holtzman, A., Buys, J., Du, L., Forbes, M. & Choi, Y. (2020). "The Curious Case of Neural Text Degeneration." *ICLR 2020*.** [arXiv:1904.09751](https://arxiv.org/abs/1904.09751). How temperature and top-p reshape the probabilities. The top-p exercise is this paper's sampling method, on a real model.
- **OpenAI (2023). "GPT-4 Technical Report."** [arXiv:2303.08774](https://arxiv.org/abs/2303.08774). Figure 8. After training to be an assistant, the model is much more sure of itself than its hit rate justifies. That is why "Otter" survives until the temperature is high.
