# Playground

Things to play with between exercises. Each folder has a short script to run and a list of ideas to take it further. None of them are required, and there are no right answers.

Run each one from inside its folder:

```bash
cd finish-my-sentence
uv run python play.py
```

| Folder | What it's about | Needs the demos first? |
|--------|-----------------|------------------------|
| [finish-my-sentence](finish-my-sentence/) | Type a prompt, watch all four counting models finish it | Yes, demos 1–4 |
| [temperature](temperature/) | The `temperature` setting every LLM API has, and what it does to the probabilities | Yes, demo 1 |
| [backoff](backoff/) | When a five-word context is unknown, fall back to four, three, two, one | No |
| [score-a-sentence](score-a-sentence/) | Run a model backwards: how likely is this sentence? | No |
| [other-books](other-books/) | The letter model on *Through the Looking-Glass*, and on Python code | No |
| [tokenizer-lab](tokenizer-lab/) | Vocabularies of 100, 500 and 2,000 tokens, and why LLMs can't spell strawberry | No |
| [neural-knobs](neural-knobs/) | Retrain the neural model with different settings, then save and reuse it | No |

Everything a script writes goes into an `output/` folder next to it.
