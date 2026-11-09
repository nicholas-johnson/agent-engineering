# Agent Engineering

Course materials for _Agent Engineering_, a hands-on Python course on building AI agents from the ground up: a language model from scratch, embeddings, vector stores, RAG, then agents.

## Repository

- **Python**: managed with uv (`pyproject.toml`), standard library only so far. Run scripts with `uv run python ...`; the system `python3` is too old.
- **Slides**: a pnpm workspace. `slide-deck/` is the shared React slide components; each module's `slides/` is a Vite app that uses it.
- **Commands**:
  - `pnpm slides:NN`: run module NN's slides
  - `pnpm slides:pdf`: export every deck to `pdf/`
  - `pnpm format:slides`: format the slides with Prettier

## Building or changing a module

Follow the module guide. Module 1 (`day-one/module-01-intro-to-language-models/`) is the reference example.

@MODULE_GUIDE.md
