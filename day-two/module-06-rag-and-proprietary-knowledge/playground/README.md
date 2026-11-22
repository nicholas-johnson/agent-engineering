# Playground

Things to play with between exercises: the choices inside a RAG system, and what each one costs. How to cut the documents into chunks, what to put at the top of each chunk, how many chunks to send, what to tell the model, and what happens when a fact changes. Each folder has a short script to run and a list of ideas to take it further. None of them are required, and there are no right answers.

They all need your OpenAI API key in `.env` (see the module README). Each script builds what it needs from `data/`, so you don't have to run the demos first. The scripts that embed the knowledge base keep the vectors in a ChromaDB store in their own `output/` folder, so only the first run waits for the embeddings.

From the module folder (`day-two/module-06-rag-and-proprietary-knowledge`):

```bash
uv run python playground/ask-your-docs/play.py
```

Or without `uv` (set up `.venv` once at the repo root with `python3 -m venv .venv && .venv/bin/pip install -e .`):

```bash
source ../../.venv/bin/activate
python playground/ask-your-docs/play.py
```

| Folder | What it's about | Needs |
|--------|-----------------|-------|
| [ask-your-docs](ask-your-docs/) | A chat over the knowledge base, with checked quotes. Then point it at your own Markdown | `OPENAI_API_KEY` |
| [chunk-sizes](chunk-sizes/) | Cut at the headings, or every 50, 150 or 400 words: what does retrieval find, and how many tokens does it send? | `OPENAI_API_KEY` |
| [chunk-headings](chunk-headings/) | Embed each chunk with and without its "Title > Heading" line | `OPENAI_API_KEY` |
| [how-many-chunks](how-many-chunks/) | The top 1 to the top 20: what each extra chunk finds, and what it costs | `OPENAI_API_KEY` |
| [grounding-rules](grounding-rules/) | Three sets of instructions, the same chunks. Which one stops the model making things up? | `OPENAI_API_KEY` |
| [stale-copies](stale-copies/) | One fact changes. Find every chunk that still states the old one | `OPENAI_API_KEY` |
| [long-context-or-rag](long-context-or-rag/) | The whole knowledge base in every prompt, or the top five chunks: the bill per day | `OPENAI_API_KEY`, only to count tokens |

Everything a script writes goes into an `output/` folder next to it.
