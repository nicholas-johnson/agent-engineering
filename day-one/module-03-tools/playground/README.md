# Playground

Things to play with between exercises: an agent that calls tools, and the messages those calls are made of. Each folder has a short script to run and a list of ideas to take it further. None of them are required, and there are no right answers.

From the module folder (`day-one/module-04-tools`):

```bash
uv run python playground/calculator/play.py
```

Or without `uv` (set up `.venv` once at the repo root with `python3 -m venv .venv && .venv/bin/pip install -e .`):

```bash
source ../../.venv/bin/activate
python playground/calculator/play.py
```

| Folder | What it's about | Needs |
|--------|-----------------|-------|
| [calculator](calculator/) | Six maths tools: watch the agent plan a calculation | `OPENAI_API_KEY` |
| [tool-descriptions](tool-descriptions/) | Does a tool's description change what the model does? | `OPENAI_API_KEY` |
| [raw-protocol](raw-protocol/) | Talk MCP by hand: the JSON messages the package hides | Nothing |
| [lying-tools](lying-tools/) | A buggy tool, and a tool whose result carries instructions | `OPENAI_API_KEY` |
| [parallel-calls](parallel-calls/) | Five lookups at once, in one round | `OPENAI_API_KEY`, internet |
| [weather-server](weather-server/) | A second API server, to copy when you write your own | `OPENAI_API_KEY`, internet |

Everything a script writes goes into an `output/` folder next to it.
