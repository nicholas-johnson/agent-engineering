# Playground

Things to try between exercises, in the tools themselves. You'll write an agent file and a skill for Claude Code, add hooks that run the tests after every edit, give Cursor the company's rules, hunt a bug with Debug mode, add a tool to the company-brain server, and give the same ticket to two tools to compare what comes back. None of them are required, and there are no right answers.

Most folders are exercises in a tool: a README with the steps, and the files to drop into the project. Three have a Python script. Each one builds what it needs from `data/`, so you don't have to run the demos first.

The exercises work on a copy of the Dormouse project, outside the course repository so the tools can change it. From the module folder (`day-two/module-07-ai-assisted-development`):

```bash
MODULE="$PWD"
cp -R data/project ~/dormouse-dashboard && cd ~/dormouse-dashboard && git init -q && git add . && git commit -qm "Start"
```

To start again: `git reset --hard && git clean -fd` in `~/dormouse-dashboard`.

The Python scripts run from the module folder:

```bash
uv run python playground/brain-tools/play.py
```

Or without `uv` (set up `.venv` once at the repo root with `python3 -m venv .venv && .venv/bin/pip install -e .`):

```bash
source ../../.venv/bin/activate
python playground/brain-tools/play.py
```

| Folder | What it's about | Needs |
|--------|-----------------|-------|
| [agent-files](agent-files/) | Write a subagent for Claude Code, and run it alongside the module's three | Claude Code |
| [write-a-skill](write-a-skill/) | A skill runner, with a new skill to edit: a support reply in the Dormouse voice | `OPENAI_API_KEY`; Claude Code or Cursor to use it there |
| [hooks](hooks/) | Make Claude Code run the tests after every edit, and ask before it changes a test | Claude Code |
| [cursor-rules](cursor-rules/) | Turn the company brain into Cursor rules, and see what changes | Cursor |
| [debug-hunt](debug-hunt/) | A customer's saved home that shows a bug. Find it with Debug mode | Cursor (or Claude Code) |
| [brain-tools](brain-tools/) | Add a tool to the company-brain MCP server, and try it with no API key | Nothing; Claude Code or Cursor to attach it |
| [same-ticket](same-ticket/) | Give one ticket to two tools, and compare the changes | Two of Claude Code, Cursor and a cloud agent |

Everything a script writes goes into an `output/` folder next to it.
