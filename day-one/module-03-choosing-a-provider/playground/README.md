# Playground

Things to play with between exercises. Each folder has a short script to run and a list of ideas to take it further. None of them are required, and there are no right answers.

Run each one from inside its folder:

```bash
cd price-calculator
uv run python play.py
```

| Folder | What it's about | Needs |
|--------|-----------------|-------|
| [price-calculator](price-calculator/) | What a real chatbot costs each month, on 32 models | Nothing |
| [model-catalogue](model-catalogue/) | Search all 469 models on OpenRouter by price, context, inputs and openness | Nothing |
| [local-models](local-models/) | Two sizes of small model on your laptop | Ollama, `qwen3:0.6b` and `qwen3:1.7b` |
| [open-vs-closed](open-vs-closed/) | A laptop model against a frontier model | Ollama, `OPENAI_API_KEY` |
| [content-policies](content-policies/) | What each model will say, refuse or sidestep | Ollama; more with `OPENAI_API_KEY` and `OPENROUTER_API_KEY` |
| [your-own-loop](your-own-loop/) | Module 1's generation loop, by hand, on a real open model | `uv sync --extra local`; run demo 5 first |

Everything a script writes goes into an `output/` folder next to it.
