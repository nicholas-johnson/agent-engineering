# Module 7 — AI-Assisted Development

> A survey of the AI tools that teams use to build software today, one section each. First the baseline: one prompt and a few lines of Python turn an idea into a page you can click. **Lovable** turns a description into a hosted app, with a database and sign-in. **Claude Code** is a coding agent in your terminal, with subagents, agent files, skills and connectors. **Cursor** is an editor with a mode for each job: ask, build, plan, debug, and several at once. **Cloud agents** take a ticket and hand back a pull request while you do something else. Last, the **company brain**: what your company knows, behind one MCP server that every tool can use. Each section ends with what the tool is known for, and what to watch out for.

## Learning goals

- Build a **prototype** from one prompt in Python, and see what an **app builder** adds
- Use **Lovable**: Plan, Build and Chat modes, **Instructions**, the **built-in backend**, the **security scan** and publishing
- Use **Claude Code**: permission modes, commands, `claude -p`, **subagents** defined in **agent files**, **skills** and **connectors**
- Use **Cursor**'s **Ask**, **Agent**, **Plan** and **Debug** modes, and run several agents at once with **/multitask**
- Hand a ticket to a **cloud agent**, and review the **pull request** it returns
- Put a **company brain** behind an **MCP server**, and attach it to Claude Code, Cursor and the Claude app
- Choose between app builders, AI editors, coding agents and general assistants

## The core idea

Every coding tool in this module is the same thing underneath: Module 3's **tool loop**, with tools for reading files, editing them and running commands. What differs is where the loop runs (a browser, your terminal, your editor, someone else's computer), how much it asks you before it acts, and where it reads what your company knows.

So this module is a survey. Each section shows one tool doing real work, with a run sheet to follow, then sums it up: what it is **known for**, and what to **watch out for**. The tools change every few months. The facts here were checked on 23 November 2026, and some will be out of date by the time you read this.

## The data

Dormouse is the smart thermostat from Modules 5 and 6. Everything here was written for this course.

| Path | What it is |
|------|------------|
| `data/project/` | A small stand-in for the Dormouse web dashboard's code: the settings, when Warm Wake switches the heating on, and the settings page. 16 tests, an `AGENTS.md`, a `CLAUDE.md`, and two saved homes in `homes/` that `python -m dormouse` runs. It has one real bug the tests don't catch (DOR-234) |
| `data/tickets/` | Four tickets, a stand-in for Jira: DOR-231 (choose how early Warm Wake starts), DOR-232 (let the week start on Saturday), DOR-233 (choose how long Boost lasts) and DOR-234 (the bug) |
| `data/agents/` | Three Claude Code agent files for reviewing a change: `ticket-checker`, `test-reviewer` and `customer-text` |
| `data/skills/` | Four skills, as `SKILL.md` files: release notes, test plan, change summary and help article |
| `data/brain/` | The company brain: six short Markdown files on the product, customers, voice, glossary, decisions and design |
| `data/feedback.json` | 30 pieces of customer feedback from September and October 2026. 14 are about the heating coming on early |
| `data/changes/DOR-231.diff`, `data/help/warm-wake.md` | A change a coding agent made for DOR-231, and the Warm Wake help article: material for the write-a-skill playground |
| `data/tools.json` | 29 AI tools in four kinds, with what they're known for, what to watch out for, a price and sources. Checked on 20 November 2026; the tools in sections 2 to 5 were rechecked on 23 November |

## Running the demos

Two sections have a Python script. From this folder:

```bash
uv run python demo/01_just_build_it.py
```

| Script | What it does |
|--------|--------------|
| `demo/01_just_build_it.py` | Builds a prototype from one request, and writes it to `demo/output/01_prototype.html`. Needs `OPENAI_API_KEY` |
| `demo/06_brain_server.py` | The company-brain MCP server. You don't run it yourself: Claude Code, Cursor or the Claude app starts it |

The other sections are live runs in the tools themselves. Each has a run sheet: what to set up, what to type, and what to point out.

| Section | Run sheet | Needs |
|---------|-----------|-------|
| 2. Lovable | [`demo/02_lovable.md`](demo/02_lovable.md) | A Lovable account (the free plan is enough) |
| 3. Claude Code | [`demo/03_claude_code.md`](demo/03_claude_code.md) | Claude Code, on a Claude plan or an API key |
| 4. Cursor | [`demo/04_cursor.md`](demo/04_cursor.md) | Cursor, on a paid plan for the whole run |
| 5. Cloud agents | [`demo/05_cloud_agents.md`](demo/05_cloud_agents.md) | The project on GitHub, and an account with each service |
| 6. The company brain | [`demo/06_company_brain.md`](demo/06_company_brain.md) | Claude Code, Cursor or the Claude desktop app |

Agents do something different every time, so instead of quoting one run, each section says what to build, the kind of prompts to use, and what to look for. Try each one before the session: an app takes minutes to build, and a cloud agent longer.

## 1. Just build it

**Demo:** `demo/01_just_build_it.py`

The quickest way from an idea to something people can click is to ask a model for it. Underneath every app builder is one request like this:

```python
INSTRUCTIONS = "You build prototypes. Reply with one complete, self-contained HTML file and nothing else."
REQUEST = "Build the settings screen for the Dormouse thermostat app, where customers choose how early Warm Wake starts the heating."
```

The demo streams the reply, so a long file shows progress as it arrives, and writes it to `01_prototype.html`. It prints the words a customer would see:

```text
Building... 14,237 characters

Request: Build the settings screen for the Dormouse thermostat app, where customers choose how early Warm Wake starts the heating.

On the screen:
  d
  dormouse
  A softer start
  Warm Wake
  Wake up to a home that’s already just right.
  Start heating before you wake
  Choose how much time your home needs.
  On
  30
  min early
  At wake-up
  2 hours early
  Your next wake-up
  Warm Wake will begin at
  6:30 AM
  Dormouse learns how quickly your home warms up, so it can make every morning feel comfortable.
  Save changes
  You can change this anytime in your settings.
  Warm Wake settings saved
```

It took 30 seconds, and it looks finished: a dark green card, a large "30 min early", a slider and a Save button. It is also all invented. The model has never heard of Dormouse, so it wrote the most likely screen for a thermostat app: a slider to "2 hours early" where Warm Wake has never gone past 90 minutes, a Save button where our app saves as you go, and "6:30 AM" where we use the 24-hour clock.

**Known for / watch out for:** cheap, fast and entirely yours: a few lines of code, any model, no account with anyone else. But you get one page, with no database, no sign-in and nowhere to host it, and everything on it is a guess. A prototype this polished is also risky in a meeting: people react to the made-up details as if they were decisions.

## 2. Lovable

**Run sheet:** [`demo/02_lovable.md`](demo/02_lovable.md)

**Lovable** is an **app builder**: you describe an app in a chat, and it writes a whole web app, runs it in a preview next to the chat, and hosts it when you publish. Others in the same group are v0, Bolt.new, Replit Agent, Figma Make and Google AI Studio. The run sheet builds a feedback board where Dormouse customers post problems and vote for each other's.

The mode picker next to the chat input has three modes:

| Mode | What it does | Changes code? |
|------|--------------|---------------|
| **Plan** | Looks at the project, asks questions, and writes a plan you can edit. Approving it switches to Build. The plan is kept in `.lovable/plan/` | No |
| **Build** | The default, formerly called Agent mode. Builds features, fixes bugs and reads logs, for as long as the job takes | Yes |
| **Chat** | Answers questions about the code and the data. If you ask for a change, it offers to start building | No |

Around the chat:

- **The built-in backend** (Lovable Cloud) is on by default: a database, sign-in, file storage and server functions, run on Supabase. That is what turns a page into an app.
- **The preview toolbar** lets you select an element and describe a change to it, edit text in place, draw on the page, and leave comments.
- **Instructions** (formerly Knowledge) are what Lovable reads before every message: up to 10,000 characters each for the workspace, the project and you. The run sheet pastes the company brain in here.
- **Security**: a quick scan of the database rules and packages runs on every publish, and a deep scan of the code (3 to 15 minutes) runs when you ask.
- **Publish** puts the app at `your-app.lovable.app`. **GitHub sync** creates a repository and keeps it in step both ways, so a developer can carry on in another tool.
- **Connectors** link the chat to other services, including your own MCP server, given its URL.

Prices on 23 November 2026: free with 5 credits a day (30 a month); Pro from $25 a month for 100 credits.

**Try it.** Build the feedback board from the run sheet, or something small from your own work: a sign-up form, an internal tool, a dashboard over a spreadsheet. Describe who uses it and what they do, not the screens, and start in Plan mode:

- Plan: "Build a feedback board for customers of Dormouse, a smart thermostat. Customers sign in, post a problem, and vote for other people's posts. Our support team can mark a post as answered, with a reply."
- Build, one change at a time: "Only support staff can mark a post answered." "Sort posts by votes, and newest first when two are tied."
- With the brain in Instructions: "Rewrite every piece of text on the board in our voice."
- Chat: "Who can see a customer's email address?" "What happens if someone votes twice?"

Look for what it decided that you didn't say: the pages, the colours, who can see what. Then run the deep security scan and read what it finds.

**Known for / watch out for:** the fastest way from a paragraph to a hosted app with a database and sign-in, for people who don't write code, and a real React app you can take away. But it's Lovable's choice of stack, not your product's code; credits run out quickly on a big build; and publishing is one click whether or not the app is safe. In February 2026 an app showcased by Lovable [leaked 18,697 user records](https://www.theregister.com/2026/02/27/lovable_app_vulnerabilities), and Lovable says fixing what its scan finds is up to the app's owner. Module 8 picks this up.

## 3. Claude Code

**Run sheet:** [`demo/03_claude_code.md`](demo/03_claude_code.md)

### What it is

**Claude Code** is Anthropic's **coding agent**. You start it with `claude` in a project folder, in a terminal, and type what you want. It reads the code, edits files, runs commands and the tests, and keeps going until the job is done or it needs you. The same agent runs in VS Code and JetBrains, in the Claude desktop app, and in the cloud (section 5).

Under the polish it is Module 3's tool loop. In outline:

```python
TOOLS = [read_file, edit_file, search, run_command]

while True:
    response = model(instructions, conversation, tools=TOOLS)
    calls = [item for item in response.output if item.type == "function_call"]
    if not calls:
        break                      # no more tools: the job is done
    for call in calls:
        conversation.append(run(call))   # read, edit, run the tests...
```

Before your first message it reads `CLAUDE.md`, the project's instructions. The Dormouse project's `CLAUDE.md` is one line, `@AGENTS.md`, which imports the file Cursor, Codex and Copilot read, so every tool gets the same test command and rules.

### Using it

- **Permission modes** say how much it asks first. Shift+Tab cycles through them: manual (it asks before each edit and command), accept edits, **plan** (it only reads and proposes, until you approve), and auto, where a check decides what is safe to do without asking. `/permissions` shows the rules for what's always allowed or never allowed.
- **Commands** start with `/`: `/clear` for a fresh conversation, `/mcp` for connectors, `/permissions`, and any skill by name.
- **`claude -p "..."`** runs the same agent with no person: from a script, a scheduled job or CI. It prints the answer and stops.

### Subagents and agent files

A **subagent** is a separate agent that Claude Code starts to do part of the job. It has its own context: it gets only the task Claude hands it, does the work, and sends back a summary. So the main conversation stays short, and several subagents can work at once. Claude Code has some built in, such as **Explore**, which searches a codebase without changing it, and **Plan**.

An **agent file** defines your own. It is a page of Markdown in `.claude/agents/`, committed with the project so the whole team has it. The module has three, in `data/agents/`, for reviewing a change:

```markdown
---
name: ticket-checker
description: Checks a change against its ticket's acceptance criteria, one by one. Use after a change is made, before it is committed.
tools: Read, Grep, Glob, Bash
model: sonnet
---

You check a change against the ticket it is for. You are given the ticket, or its text.

1. Read the change: run `git diff` and `git status`, and read any new files.
2. Go through the ticket's acceptance criteria one at a time. ...
```

The **description** is what Claude reads to decide when to use it. **tools** limits what it can do: these reviewers can't edit. **model** picks the model: `customer-text` runs on Haiku, because checking labels doesn't need a bigger one. The run sheet builds DOR-232, then asks for all three reviewers at once. They start in the background, side by side, and report back separately.

### Skills

A **skill** is a folder with a `SKILL.md`: a name and a description at the top, then instructions. Claude Code reads only the descriptions until a job matches one, then loads that skill's instructions. You can also run one by name, as `/release-notes`. The module's four skills are in `data/skills/`; the run sheet copies them into `.claude/skills/`. Skills are an open format: Cursor, Codex and Copilot read the same files.

### Connectors

A **connector** is an MCP server (Module 3) that gives Claude Code tools from another service: GitHub, Linear, Google Drive, a database. `/mcp` lists them. Connectors you add at claude.ai appear in Claude Code too when you sign in with the same account, and `claude mcp add` adds one to a project. Section 6 builds one of our own.

Prices on 23 November 2026: Claude Code comes with Claude Pro, $17 a month billed annually or $20 monthly, and above. The free plan doesn't include it.

**Try it.** On a copy of the Dormouse project, as in the run sheet. Talk to it the way you'd brief a colleague: say what you want, how to check it, and what not to touch.

- "What does this project do, and how do I run it?"
- Paste DOR-232, then: "Build this. Run the tests before you finish, and tell me which files you changed."
- Shift+Tab to plan mode, paste DOR-233: "Plan this. Ask me about anything the ticket doesn't say."
- After a change: "Check the change against this ticket with the ticket-checker, test-reviewer and customer-text agents, all at the same time."
- "Write the release notes for this change." Then `/test-plan`.
- From a script: `claude -p "Run the tests and tell me how many pass."`

Look for: it reads `AGENTS.md` before anything else; it asks before editing in manual mode; three subagents running at once, each coming back with a short report; the skill picked from its description.

**Known for / watch out for:** a strong agent that works anywhere a terminal does, with the most ways to shape it: agent files, skills, hooks, connectors, plan mode, and `claude -p` for scripts and CI. But it acts on your real files and runs real commands, so the permission mode matters, and a long session can use a lot of your plan's allowance. It reads `AGENTS.md` only if there is no `CLAUDE.md`, unless `CLAUDE.md` imports it. And there's no editor: you read its changes with `git diff` or your own.

## 4. Cursor

**Run sheet:** [`demo/04_cursor.md`](demo/04_cursor.md)

**Cursor** is a code editor, based on VS Code, built around an agent. Its agent panel (Cmd+I) has a **mode** for each kind of job. Shift+Tab cycles through them, and each one starts with a fresh context:

| Mode | What it's for | Changes code? |
|------|---------------|---------------|
| **Ask** | Questions about the code: how it works, where something lives | No |
| **Agent** | The default: build a feature, fix a bug, refactor | Yes |
| **Plan** | Asks questions, writes a plan you can edit, then builds it when you say | After you approve |
| **Debug** | Bugs you can reproduce but can't explain | Yes, with evidence first |

The run sheet uses one ticket per mode: Ask about Warm Wake, Agent mode for DOR-232, Plan mode for DOR-231, and Debug mode for DOR-234.

### Debug mode

DOR-234 is a real bug in the project. Support says small homes get their heating 90 minutes early, although they warm up in under half an hour:

```text
$ python -m dormouse homes/flat-3b.json
Flat 3B: the room is at 18 degrees. The next period starts at 07:00, at 20 degrees.
Warm Wake switches the heating on at 05:30, 90 minutes early.
Settings page: homes/flat-3b.html
```

Flat 3B warms at about 5 degrees an hour, so 2 degrees needs about 24 minutes, and the heating should come on at 06:36. The cause is one line in `dormouse/warm_wake.py`:

```python
def learned_rate(heat_ups):
    """How fast the home warms, in degrees an hour, from its recent heat-ups: (degrees gained, minutes taken) pairs."""
    ...
    return degrees / minutes
```

That is degrees a minute, 60 times too small, so every home looks slow and Warm Wake always starts as early as it may. In a big house that's 90 minutes anyway, which is why it looks right there. All 16 tests pass, because none of them check `learned_rate`.

Debug mode doesn't guess from the code. It lists a few **hypotheses**, adds logging that reports to Cursor, and asks you to **reproduce** the bug. It reads what the logging caught, makes a small fix, asks you to check, then takes the logging out again.

### Several at once

`/multitask` runs several agents at once instead of one after another. Type it in the Agents Window with two tickets, DOR-232 and DOR-233, and each gets its own agent working in parallel. From a plan, **Build in Parallel** does the same with the plan's independent steps.

### What it reads

Cursor reads `AGENTS.md` in the project, its own **rules** in `.cursor/rules/` (`.mdc` files that apply always, by file, when relevant, or when you ask), and skills from `.cursor/skills/`, `.agents/skills/` and `.claude/skills/`. MCP servers go in `.cursor/mcp.json` (section 6).

Prices on 23 November 2026: free with limited use of Cursor's own and Grok models; Plus $8 a month; Premium $30, which adds cloud agents and other companies' models at their API prices. SpaceX bought Cursor in August, and OpenAI said it would stop supplying its models; on 16 November a Cursor forum post said access had been extended to 25 November.

**Try it.** One job per mode, on a copy of the Dormouse project:

- Ask: "How does Warm Wake decide when to switch the heating on?" "Where would a setting for how long Boost lasts go?"
- Agent: paste DOR-232 and let it build.
- Plan: paste DOR-231, then: "Ask me anything the ticket doesn't say before you plan." Edit one step of the plan before you build it.
- Debug: paste DOR-234. When it asks you to reproduce the bug, run `python -m dormouse homes/flat-3b.json`.
- In the Agents Window: `/multitask`, then DOR-232 and DOR-233.

Look for: Debug mode's hypotheses before any fix, and whether the logging finds `learned_rate`. After the fix, Flat 3B's heating should come on at 06:36 and 14 Mill Lane's still at 05:00. With `/multitask`, see how two agents changing `settings.py` at once were combined.

**Known for / watch out for:** an agent next to the code you're reading, with a mode for each job: Ask to learn the code safely, Plan to agree before building, Debug to work from evidence, and `/multitask` for parallel work. But changes arrive fast and need reading in the editor before you keep them; parallel agents can change the same files; and its prices and model supply have changed more than any other tool's this year.

## 5. Cloud agents

**Run sheet:** [`demo/05_cloud_agents.md`](demo/05_cloud_agents.md)

A **cloud agent** runs the same tool loop on a computer in the cloud. You hand it a task, close the tab, and come back to a branch or a **pull request**: a proposed change, with its diff, waiting for review. It starts from a fresh copy of the repository, so it needs the project on GitHub (some support GitLab and others), and it reads the same instruction files as the local tools.

| Cloud agent | Start a task from | Hands back | Reads | Plan needed |
|-------------|-------------------|------------|-------|-------------|
| **Claude Code on the web** | claude.ai/code, the Claude app, `claude --cloud "..."`, Slack | A branch, then a pull request when you ask | `CLAUDE.md`, agents, skills, `.mcp.json` | Claude Pro and above |
| **Copilot in the cloud** | Assigning an issue to Copilot, `@copilot` in a pull request, the Agents tab | One pull request per task | `AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md` | Any paid Copilot plan, from $10 |
| **Codex cloud** | The Codex app (**Work in → Cloud**), `codex cloud`, Linear | A diff, to commit or open as a pull request | `AGENTS.md` | ChatGPT Plus and above |
| **Cursor Cloud Agents** | cursor.com/agents, Cursor's **Cloud** option, `@cursor` in Slack, GitHub or Linear | A branch and a pull request, with screenshots and logs | Rules and `AGENTS.md` | Cursor Premium and above |
| **Devin** | app.devin.ai, `@Devin` in Slack or Teams, `/devin` on a pull request | Pull requests | `AGENTS.md` | Pro, from $20 |

Google's **Jules** became read-only on 11 November 2026 and closes on 31 December; Google points its users to Antigravity.

The run sheet puts the project on GitHub, with DOR-232 to DOR-234 as issues, and gives one to each agent. Then it closes the loop: `/install-github-app` adds Anthropic's GitHub Action to the repository, and a comment starting `@claude` on any pull request gets it reviewed.

**Try it.** Put the project on GitHub with the tickets as issues, and give each cloud agent one. Nobody will be there to answer its questions, so write the task as a complete ticket, and say how to check it:

- "Fix DOR-234. Add a test that would have caught it. Run `python -m unittest` before you finish; every test must pass."
- Assign DOR-233 to Copilot, then on its pull request: "@copilot Name the choices 30 minutes, 1 hour and 2 hours, as the ticket says."
- On any pull request: "@claude Review this against the issue it fixes."

Look for: how long each took; whether it ran the tests, and says so; what it wrote in the pull request description; and what you'd have to check before merging.

**Known for / watch out for:** work that happens while you do something else, several tasks at once, and results that arrive where your team already reviews code. But nobody is watching it work, so the pull request is the only place to catch a mistake, and review becomes the bottleneck. It runs with whatever the cloud machine can reach, so check what secrets and internet access you give it (Module 8). And setup matters: an agent that can't install the project or run its tests will hand back code it never ran.

## 6. The company brain

**Demo:** `demo/06_brain_server.py` · **Run sheet:** [`demo/06_company_brain.md`](demo/06_company_brain.md)

Asked cold, every tool in this module writes the most likely answer for a company like yours. A **company brain** is what your company knows, written down once, in plain files:

| File | What it says |
|------|--------------|
| `product.md` | What we sell, every feature, and where each setting lives |
| `customers.md` | Who our customers are and what they care about |
| `voice.md` | How we write, and the words we don't use |
| `glossary.md` | What our terms mean, and what customers call them |
| `decisions.md` | Product decisions we've made, and why. "Give customers a choice of three, not a number." "Settings about when the heating runs live under Schedule." |
| `design.md` | Colours, type, and how a settings screen is laid out |

Every tool has its own place for this: Lovable's Instructions, `CLAUDE.md`, Cursor's rules, `AGENTS.md`, a Claude or ChatGPT Project. Five tools means five copies, each pasted in by someone at some point, and they drift apart. Tickets and feedback change every day, and don't belong in a file in every repository at all.

So put the brain behind one **MCP server**, and give every tool the same connection. `demo/06_brain_server.py` is under 50 lines, with three tools:

```python
server = MCPServer("dormouse-brain", log_level="WARNING")


@server.tool()
def read_brain(topic: str) -> str:
    """Read one part of Dormouse's company brain. `topic` is one of: product (every feature, and where each
    setting lives), customers (...), voice (...), glossary (...), decisions (product decisions we've
    made, and why) or design (...). Read decisions before making any product decision, and voice before
    writing anything a customer will read."""
    ...

@server.tool()
def get_ticket(ticket_id: str) -> str:
    """Read one ticket, such as DOR-231: the problem, what we're building, and its acceptance criteria."""
    ...

@server.tool()
def search_feedback(words: str) -> str:
    """Customer feedback from September and October 2026 that contains any of these words, as JSON..."""
    ...
```

Modules 3 and 6 built servers like this and wrote their own client. Here the clients are the real tools. Each one starts the server itself:

| Tool | How to attach it |
|------|------------------|
| Claude Code | `claude mcp add --transport stdio dormouse-brain -- uv run --directory <module folder> python demo/06_brain_server.py` |
| Cursor | A `dormouse-brain` entry in `.cursor/mcp.json`, with the same command |
| The Claude desktop app | The same entry in `claude_desktop_config.json` (**Settings → Developer → Edit Config**) |

Then ask each one something only the brain knows: "What have we decided about where settings go, and why?", "Build DOR-233", or "Write a reply to a customer whose heating comes on at 5:40 for a 7:00 period." The [brain-tools](playground/brain-tools/) playground calls the same three tools without a model, so you can see exactly what comes back.

**Try it.** Attach the server, then ask things only the brain knows:

- Claude Code: "What have we decided about where settings go, and why?" Then: "Build DOR-233. Read our decisions and voice first."
- Cursor, in Ask mode: "What did customers say about the heating coming on early?"
- The Claude app: "Write a two-line reply to a customer who asks why their heating comes on at 5:40 for a 7:00 period."

Look for: which tool it calls, and whether it asks first; whether DOR-233's labels and placement change once it has read the decisions and the voice; and the same answers in three different tools.

**Known for / watch out for:** one source of truth that every tool reads, kept up to date in one place, for developers and for the people in support, product and marketing who never open a code editor. But a local server only reaches tools on your own computer: Lovable and the cloud agents need it on the internet, at a URL, with sign-in in front of it, which is Module 8. A tool's description decides when a model uses it, so it needs writing as carefully as the brain itself. And anything the brain says is now said to every tool: a mistake in `decisions.md` spreads everywhere at once.

## Choosing tools

The tools fall into four kinds. `data/tools.json` has 29 of them, with what each is known for, what to watch out for, a price and a source.

| Kind | For | Examples |
|------|-----|----------|
| **Build an app from a prompt** | Product managers, designers and founders who want something clickable | Lovable, v0, Bolt.new, Replit Agent, Figma Make, Google AI Studio |
| **AI editors** | Developers who want an agent inside the editor they use every day | Cursor, GitHub Copilot in VS Code, Devin Desktop (formerly Windsurf), Kiro, Google Antigravity, JetBrains, Zed |
| **Coding agents** | Developers who hand over a task and review the result, in the terminal, the cloud or CI | Claude Code, OpenAI Codex, Antigravity CLI (which replaced Gemini CLI), Copilot in the cloud, Devin, and the open source Aider, Cline and OpenCode |
| **For everyone else** | Product, marketing and sales, working with documents, meetings and research | Claude (Projects, Cowork), ChatGPT, Gemini and NotebookLM, Microsoft 365 Copilot, Notion AI, Glean, Granola |

What they share matters more than what separates them:

| | Claude Code | Cursor | Codex | GitHub Copilot |
|---|---|---|---|---|
| Reads the project's instructions from | `CLAUDE.md` (or `AGENTS.md` if there is none) | `AGENTS.md`, rules | `AGENTS.md` | `AGENTS.md` and others |
| Plan first | Plan mode | Plan mode | Plan mode (`/plan`) | Plan agent |
| Skills (`SKILL.md`) | Yes | Yes | Yes | Yes |
| MCP servers | Yes | Yes | Yes | Yes |
| Runs without a person | `claude -p`, cloud, GitHub Action | Cloud agents | `codex exec`, cloud, GitHub Action | Copilot in the cloud |

Things worth knowing this year:

- SpaceX [bought Cursor](https://thenextweb.com/news/spacex-cursor-acquisition-completed-gpu-fleet) in August 2026. OpenAI then [said it would stop supplying its models](https://openai.com/index/our-decision-on-cursor-following-its-acquisition-by-spacex/) to Cursor, with a proposed cut-off of 12 November, since extended.
- Google [replaced Gemini CLI with Antigravity CLI](https://developers.googleblog.com/en/an-important-update-transitioning-gemini-cli-to-antigravity-cli/) for individual users in June, and is [closing Jules](https://jules.google/docs/changelog/2026-10-29/) at the end of the year.
- Windsurf [became Devin Desktop](https://docs.devin.ai/desktop/devin-desktop-faq) in June.
- GitHub Copilot [moved to usage-based billing](https://github.blog/2026-05-01-github-copilot-is-moving-to-usage-based-billing/) in June, and its cloud agent became [Copilot in the cloud](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent) in October.
- App builders have had real security incidents. In February 2026 an app showcased by Lovable [leaked 18,697 user records](https://www.theregister.com/2026/02/27/lovable_app_vulnerabilities), and a flaw in Lovable's own API [exposed other users' projects](https://thenextweb.com/news/lovable-vibe-coding-security-crisis-exposed). Module 8 picks this up.

### How this course was built

This course is a real example. Its repository has a `CLAUDE.md`, 24 lines, which imports `MODULE_GUIDE.md`: how a module is put together, the demo rules, the README sections, British English. That is the course's company brain, and every agent that worked on it read it first. Promotional clips are made with a skill, `.claude/skills/social-clip/SKILL.md`. A test, `tests/test_structure.py`, checks every module against the guide. And each module's outline is agreed before anything is built: plan first. This module was rebuilt in Claude Code, in a git worktree of its own, while other agents worked on other modules in theirs.

## Summary

| Tool | Known for | Watch out for |
|------|-----------|---------------|
| 1. A prompt in Python | A clickable page in 30 seconds, and all yours | One page, no backend, and everything on it invented |
| 2. Lovable | A hosted app with a database and sign-in, from a paragraph | Its stack, not your code; credits; publishing apps that aren't safe |
| 3. Claude Code | A terminal agent you can shape: agent files, skills, hooks, connectors, `claude -p` | It acts on real files and commands; no editor to read changes in |
| 4. Cursor | A mode for each job, next to the code: Ask, Agent, Plan, Debug, `/multitask` | Fast changes need reading; prices and model supply keep changing |
| 5. Cloud agents | Tasks done while you're away, delivered as pull requests | Nobody watching; review becomes the bottleneck; what the machine can reach |
| 6. The company brain | One source of truth every tool reads | Local only until deployed; mistakes spread everywhere at once |

## Playground

The [playground](playground/) has exercises in the tools: write an agent file and a skill, add hooks that run the tests after every edit, give Cursor the company's rules, hunt a second bug with Debug mode, add a tool to the company-brain server, and give the same ticket to two tools. It also has [projects to build](playground/README.md#projects-to-build) of your own in each tool, from a pub quiz in Lovable to an MCP server for your team.

## Further reading and extensions

[Further reading](further-reading/) is the final exercise: papers on coding agents, on giving them context, and on whether AI tools make people faster, and bigger projects to try.

## Slides

```bash
pnpm slides:07
```
