# Playground

Things to play with between exercises: embeddings, and the choices behind a search that runs on them. What text to embed, how long the vectors should be, how to merge two searches, and what similarity does and doesn't notice. Each folder has a short script to run and a list of ideas to take it further. None of them are required, and there are no right answers.

They all need your OpenAI API key in `.env` (see the module README). The scripts that embed the whole library save the vectors in their `output/` folder, so the second run doesn't call the API for them again.

From the module folder (`day-two/module-05-embeddings-and-vector-search`):

```bash
uv run python playground/similarity-explorer/play.py
```

Or without `uv` (set up `.venv` once at the repo root with `python3 -m venv .venv && .venv/bin/pip install -e .`):

```bash
source ../../.venv/bin/activate
python playground/similarity-explorer/play.py
```

| Folder | What it's about | Needs |
|--------|-----------------|-------|
| [similarity-explorer](similarity-explorer/) | Type sentences and see how similar their embeddings are. Opposites score high | `OPENAI_API_KEY` |
| [what-to-embed](what-to-embed/) | The full script, the title, or the title and expected result: which finds the right script? | `OPENAI_API_KEY` |
| [duplicate-finder](duplicate-finder/) | Find near-duplicate scripts in the library, a real clean-up job | `OPENAI_API_KEY` |
| [other-languages](other-languages/) | Search the English library in French, German, Spanish, Polish and Japanese | `OPENAI_API_KEY` |
| [shrink-the-vectors](shrink-the-vectors/) | 1,536 numbers per vector, or 64? What shorter vectors save and lose | `OPENAI_API_KEY` |
| [fusion-knobs](fusion-knobs/) | Demo 4's hybrid search with every setting exposed. Can any of them rescue it? | `OPENAI_API_KEY` |

Everything a script writes goes into an `output/` folder next to it.
