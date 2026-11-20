# Playground

Things to play with between exercises: the choices you make when you build with AI, from the first idea to the launch. Which parts of the company brain matter, how a person stays in charge of a coding agent, whether tests written first keep it honest, how much one reviewer misses, how to write a skill of your own, how to find a feature in customer feedback, and how to check copy against the brand voice. Each folder has a short script to run and a list of ideas to take it further. None of them are required, and there are no right answers.

Every script follows the same feature as the demos, DOR-231: let customers choose how early Warm Wake starts the heating. Each one builds what it needs from `data/`, so you don't have to run the demos first. They all need your OpenAI API key in `.env` (see the module README).

From the module folder (`day-two/module-07-ai-assisted-development`):

```bash
uv run python playground/brain-pieces/play.py
```

Or without `uv` (set up `.venv` once at the repo root with `python3 -m venv .venv && .venv/bin/pip install -e .`):

```bash
source ../../.venv/bin/activate
python playground/brain-pieces/play.py
```

| Folder | What it's about | Needs |
|--------|-----------------|-------|
| [brain-pieces](brain-pieces/) | Demo 2's prototype, built with none, some or most of the company brain. Which file changes what? | `OPENAI_API_KEY` |
| [permissions](permissions/) | The coding agent asks before every change. Say no, say why, and steer it | `OPENAI_API_KEY` |
| [test-first](test-first/) | The agent writes failing tests from the ticket, then makes them pass without touching them | `OPENAI_API_KEY` |
| [second-opinion](second-opinion/) | The review skill on the same change, from three reviewers. Do they find the same problems? | `OPENAI_API_KEY`; `ANTHROPIC_API_KEY` for the third reviewer |
| [write-a-skill](write-a-skill/) | A skill runner, with a new skill to edit: a support reply in the Dormouse voice | `OPENAI_API_KEY` |
| [feedback-themes](feedback-themes/) | Before the ticket: group 30 pieces of feedback into themes, and count them | `OPENAI_API_KEY` |
| [voice-check](voice-check/) | Check customer copy against the voice twice: rules in code, and a model | `OPENAI_API_KEY` |

Everything a script writes goes into an `output/` folder next to it. `permissions` and `test-first` change a copy of `data/project` in their `output/project`, so every run starts from the same code.
