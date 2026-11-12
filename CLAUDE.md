# Agent Engineering

Course materials for _Agent Engineering_, a hands-on Python course on building AI agents from the ground up: a language model from scratch, embeddings, vector stores, RAG, then agents.

## Repository

- **Python**: managed with uv (`pyproject.toml`). Dependencies so far: `openai` and `python-dotenv` (Module 2), `anthropic` and `google-genai` (Module 3), `mcp` (Module 4; version 2, where the server class is `MCPServer` from `mcp.server.mcpserver`). An optional `local` extra adds `transformers` and PyTorch for self-hosting (`uv sync --extra local`). Run scripts with `uv run python ...`; the system `python3` is too old.
- **API keys**: read from `.env` at the repo root (gitignored; copy `.env.example`). `OPENAI_API_KEY` from Module 2; Module 3 also uses `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`, `XAI_API_KEY` and `OPENROUTER_API_KEY` when present.
- **Local models**: Module 3 uses Ollama with `qwen3:1.7b` (and `qwen3:0.6b` in a playground), and `Qwen/Qwen3-1.7B` from Hugging Face.
- **Slides**: a pnpm workspace. `slide-deck/` is the shared React slide components; each module's `slides/` is a Vite app that uses it.
- **Commands**:
  - `pnpm slides:NN`: run module NN's slides
  - `pnpm slides:pdf`: export every deck to `pdf/`
  - `pnpm format:slides`: format the slides with Prettier

## Building or changing a module

Follow the module guide. Module 1 (`day-one/module-01-intro-to-language-models/`) is the reference example.

@MODULE_GUIDE.md
