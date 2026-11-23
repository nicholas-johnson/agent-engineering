# Playground

Things to try between exercises, in the tools themselves. You'll write an agent file and a skill for Claude Code, add hooks that run the tests after every edit, give Cursor the company's rules, hunt a bug with Debug mode, add a tool to the company-brain server, and give the same ticket to two tools to compare what comes back. None of them are required, and there are no right answers.

Then leave Dormouse behind. [Projects to build](#projects-to-build), below, has fourteen things to build of your own, one folder each, from a pub quiz in Lovable to an MCP server for your team. They need no Python: each folder is a brief, the first prompts to use, what to watch for, and ideas to take it further.

## Exercises on the Dormouse project

These seven folders are exercises in a tool: a README with the steps, and the files to drop into the project. Three have a Python script. Each one builds what it needs from `data/`, so you don't have to run the demos first.

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

## Projects to build

The exercises above all work on Dormouse. These don't: they're things to build for yourself, your team or your friends, to find out what each tool is like on a problem you care about. Each folder has only a README: what to build, the prompts to start with, what to watch for, ideas to take it further, and questions to talk about. Pick one that sounds fun, not one that sounds useful.

A few habits help in every tool:

- **Say who it's for and what they do**, not what the screens look like. Let the tool propose the screens, then change them.
- **Plan first** for anything bigger than an afternoon, and read the plan before you approve it.
- **Say how to check it**: "Run the tests", "Open it in a browser and try it on a phone-sized screen".
- **Keep your own data private.** Anything you paste or attach goes to the tool's provider (Module 8). Use made-up data until you know where it goes.

| Folder | What you'll build | Build it in | Time |
|--------|-------------------|-------------|------|
| [pub-quiz](pub-quiz/) | A quiz night: the host's big screen, players on their phones, a live leaderboard | Lovable | An evening |
| [court-booking](court-booking/) | A booking page for four tennis courts, with rules, roles and no double bookings | Lovable | An evening |
| [chores-board](chores-board/) | A family chores board with points, photo proof and rewards, usable by a seven-year-old | Lovable | An evening |
| [event-rsvp](event-rsvp/) | An RSVP site for a wedding or conference, with meal choices and an export for the caterer | Lovable | An evening |
| [photo-tidy](photo-tidy/) | A script that sorts photos by the date taken, with a dry run and a hook that blocks deletes | Claude Code | An afternoon |
| [word-game](word-game/) | A two-player word game of your own design, in one HTML file | Claude Code or Cursor | An afternoon |
| [spending-chart](spending-chart/) | A page that charts your spending from a bank export, and never sends it anywhere | Claude Code | An afternoon |
| [browser-extension](browser-extension/) | A Chrome extension that adds a reading time to articles, with as few permissions as possible | Claude Code or Cursor | An afternoon |
| [spreadsheet-to-code](spreadsheet-to-code/) | A team spreadsheet rebuilt as a program, with tests that match it to the penny | Claude Code | A day |
| [first-contribution](first-contribution/) | A pull request to an open-source project you use, for a "good first issue" | Cursor | A day or two |
| [old-code-rescue](old-code-rescue/) | Tests for old code, an upgrade, and the bug everyone works around, fixed in Debug mode | Cursor | A day |
| [backlog-afternoon](backlog-afternoon/) | Five small issues handed to cloud agents, and five pull requests to review | Cloud agents | An afternoon |
| [team-brain](team-brain/) | An MCP server for what your team knows, attached to Claude Code, Cursor and the Claude app | Claude Code | A day |
| [prototype-to-product](prototype-to-product/) | One idea through every tool: Lovable, GitHub, Cursor, a cloud agent and a review | All of them | A weekend |

### More ideas

Smaller ones, with no folder of their own:

- **A recipe box** in Lovable: paste a recipe from anywhere, scale it, and build a shopping list for the week.
- **A portfolio from your CV** in Lovable: paste the CV in Plan mode, then change the site by pointing at it with the preview toolbar.
- **A team bot** for Slack or Discord that answers questions from your team's FAQ, with Module 6's document search behind it.
- **Your old project, explained**: point Claude Code at code you wrote years ago and ask for the README it should have had.
- **A reading-list server**: your books in a spreadsheet, behind a small MCP server, attached to the Claude app. "What should I read next?"
- **A public API as an MCP server**: train times, a library catalogue or a football table, like Module 3's weather server.
- **Module 1 in a browser**: the word-pair model as a web page that completes your sentence one word at a time.
