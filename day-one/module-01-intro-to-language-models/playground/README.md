# Playground

Things to play with between exercises. Each folder has a short script to run and a list of ideas to take it further. None of them are required, and there are no right answers.

From the module folder (`day-one/module-01-intro-to-language-models`):

```bash
uv run python playground/finish-my-sentence/play.py
```

Or without `uv` (standard library only, no packages needed):

```bash
python3 playground/finish-my-sentence/play.py
```

| Folder | What it's about |
|--------|-----------------|
| [finish-my-sentence](finish-my-sentence/) | Type a prompt, watch all four counting models finish it |
| [temperature](temperature/) | The `temperature` setting every LLM API has, and what it does to the probabilities |
| [backoff](backoff/) | When a five-word context is unknown, fall back to four, three, two, one |
| [score-a-sentence](score-a-sentence/) | Run a model backwards: how likely is this sentence? |
| [other-books](other-books/) | The letter model on *Through the Looking-Glass*, and on Python code |
| [tokenizer-lab](tokenizer-lab/) | Vocabularies of 100, 500 and 2,000 tokens, and why LLMs can't spell strawberry |
| [neural-knobs](neural-knobs/) | Retrain the neural model with different settings, then save and reuse it |

Everything a script writes goes into an `output/` folder next to it.
