# Playground

Things to play with between exercises: embeddings, and the choices behind a search that runs on them. You'll retrain the word2vec model with more text and other settings, compare sentences and distance measures, choose what text stands for each document, search in other languages, and shrink the vectors. Each folder has a short script to run and a list of ideas to take it further. None of them are required, and there are no right answers.

Most of them score a search with `data/questions.json`: 20 questions in customers' own words, each with the documents that answer it. The scripts that embed the whole documentation save the vectors in their `output/` folder, so the second run doesn't call the API for them again.

From the module folder (`day-two/module-05-embeddings-and-vector-search`):

```bash
uv run python playground/word-vectors/play.py
```

Or without `uv` (set up `.venv` once at the repo root with `python3 -m venv .venv && .venv/bin/pip install -e .`):

```bash
source ../../.venv/bin/activate
python playground/word-vectors/play.py
```

| Folder | What it's about | Needs |
|--------|-----------------|-------|
| [word-vectors](word-vectors/) | Demo 5's word2vec model with every setting exposed. Feed it more text and watch the neighbours change | Nothing: plain Python, offline |
| [similarity-explorer](similarity-explorer/) | Type sentences and see how similar their embeddings are. Opposites, translations and error codes all surprise | `OPENAI_API_KEY` |
| [distance-measures](distance-measures/) | Cosine similarity, dot product and straight-line distance, on word counts and on embeddings | `OPENAI_API_KEY` |
| [what-to-embed](what-to-embed/) | The whole document, the title, the headings or the opening: which finds the right document? | `OPENAI_API_KEY` |
| [other-languages](other-languages/) | Ask four questions in six languages and search the English documentation, by keywords and by vectors | `OPENAI_API_KEY` |
| [shrink-the-vectors](shrink-the-vectors/) | 1,536 numbers per vector, or 64? What shorter vectors save and lose | `OPENAI_API_KEY` |

Everything a script writes goes into an `output/` folder next to it.
