# Playground

Things to play with between exercises. Each folder has a short script to run and a list of ideas to take it further. None of them are required, and there are no right answers.

They all need your OpenAI API key in `.env` (see the module README). Each run costs a fraction of a cent.

From the module folder (`day-one/module-02-building-a-chatbot`):

```bash
uv run python playground/chatbot/play.py
```

Or without `uv` (set up `.venv` once at the repo root with `python3 -m venv .venv && .venv/bin/pip install -e .`):

```bash
source ../../.venv/bin/activate
python playground/chatbot/play.py
```

| Folder | What it's about |
|--------|-----------------|
| [chatbot](chatbot/) | A complete chatbot with every setting at the top: model, reasoning effort, temperature, length, instructions |
| [personas](personas/) | Same model, same question, different instructions |
| [temperature](temperature/) | What temperature does to a real model, and why it does less than you'd think |
| [model-shootout](model-shootout/) | The same questions to four models: speed, tokens and answers |
| [cost-of-memory](cost-of-memory/) | How the cost of a conversation grows with every turn |
| [logprobs](logprobs/) | A real model's next-token probabilities, like Module 1's |
| [vision](vision/) | Describe a folder of pictures, and see where it goes wrong |

Everything a script writes goes into an `output/` folder next to it.
