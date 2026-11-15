# Playground

Things to play with between exercises: models, prices and providers, side by side. Each folder has a short script to run and a list of ideas to take it further. None of them are required, and there are no right answers.

From the module folder (`day-one/module-03-choosing-a-provider`):

```bash
uv run python playground/price-calculator/play.py
```

Or without `uv` (set up `.venv` once at the repo root with `python3 -m venv .venv && .venv/bin/pip install -e .`, or `".[local]"` if running `your-own-loop`):

```bash
source ../../.venv/bin/activate
python playground/price-calculator/play.py
```

| Folder | What it's about | Needs |
|--------|-----------------|-------|
| [price-calculator](price-calculator/) | What a real chatbot costs each month, on 32 models | Nothing |
| [model-catalogue](model-catalogue/) | Search all 469 models on OpenRouter by price, context, inputs and openness | Nothing |
| [local-models](local-models/) | Two sizes of small model on your laptop | Ollama, `qwen3:0.6b` and `qwen3:1.7b` |
| [open-vs-closed](open-vs-closed/) | A laptop model against a frontier model | Ollama, `OPENAI_API_KEY` |
| [content-policies](content-policies/) | What each model will say, refuse or sidestep | Ollama; more with `OPENAI_API_KEY` and `OPENROUTER_API_KEY` |
| [your-own-loop](your-own-loop/) | Module 1's generation loop, by hand, on a real open model | `uv sync --extra local` |

Everything a script writes goes into an `output/` folder next to it.
