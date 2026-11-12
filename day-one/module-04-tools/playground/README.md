# Playground

Things to play with between exercises. Each folder has a short script to run and a list of ideas to take it further. None of them are required, and there are no right answers.

Run each one from inside its folder:

```bash
cd calculator
uv run python play.py
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
