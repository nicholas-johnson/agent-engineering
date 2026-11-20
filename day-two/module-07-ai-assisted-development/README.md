# Module 7 — AI-Assisted Development

> We follow one small feature through a company: Dormouse customers keep asking why their heating comes on early, so product decides to let them choose how early Warm Wake starts. First we just ask for it, and get a polished screen that invents everything. Giving the model the **company brain**, a few files on our product, customers, voice and decisions, makes it ours. A **coding agent** builds it in the real code and passes its tests, but makes product decisions nobody asked it to make. Making it **plan first** against the agreed ticket gets the feature right, but leaves 61 changed lines nobody has read. **Skills** review it, write the test plan and the summary, and catch some of what a person would. The same brain and skills then write the release notes, help article, email, social posts and sales sheet. The tools change every few months. What lasts is the context you give them and the checks you put around them.

## Learning goals

- Build a working **prototype** from one prompt, and see why it isn't the product
- Write a **company brain**: the few files every AI tool should read, and where each tool reads them (`AGENTS.md`, `CLAUDE.md`, rules, project knowledge)
- Understand what a **coding agent** is: Day One's tool loop with tools to read, write and test code
- Use **plan mode**: plan, review, then implement, against an agreed **spec**
- Review AI-written code properly, and know what an AI **reviewer** misses
- Turn repeated work into **skills**, and run them without a person, in **CI**
- Use the same brain for marketing and sales, with **automatic checks** on what goes out
- Choose between **app builders**, **AI editors**, **coding agents** and general assistants

## The core idea

AI tools now help at every step of shipping a feature: working out what to build, prototyping, writing the code, reviewing it, testing it, and telling customers. Each of them, asked cold, writes the most likely answer for a company like yours. That is generic, and a little bit wrong in ways that are hard to spot.

Two things make the output yours, and they work the same in every tool. **Context**: what your company knows, written down once where every tool can read it. **Checks**: a plan agreed before the work, and a review, tests and rules after it. The tools are interchangeable, and change every few months. The context and the checks are yours to keep.

## The data

Dormouse is the smart thermostat from Modules 5 and 6. Everything here was written for this course.

| Path | What it is |
|------|------------|
| `data/brain/` | The company brain: six short Markdown files on the product, customers, voice, glossary, decisions and design |
| `data/feedback.json` | 30 pieces of customer feedback from September and October 2026. 14 are about the heating coming on early |
| `data/tickets/DOR-231.md` | The agreed ticket for the feature, with acceptance criteria. A stand-in for Jira |
| `data/project/` | A small stand-in for the web dashboard's code: settings, Warm Wake and the settings page, with 16 tests, an `AGENTS.md` and a `CLAUDE.md` |
| `data/changes/DOR-231.diff` | The change one run of demo 4 made, saved so demos 5 and 6, and everyone in the room, look at the same one |
| `data/skills/` | Eight skills, as `SKILL.md` files: review, test plan, change summary, release notes, help article, launch email, social posts, sales sheet |
| `data/help/warm-wake.md` | The Warm Wake help article as it is today, from Module 6's user guide |
| `data/tools.json` | 29 AI tools in four kinds, with what they're known for, what to watch out for, a price and sources. Checked on 20 November 2026 |

## Running the demos

From this folder:

```bash
uv run python demo/01_just_build_it.py
```

Each demo takes under a minute. Demo 4 asks you to approve its plan. To run it without typing: `printf 'y\n' | uv run python demo/04_plan_first.py`.

| Demo | Writes to `demo/output/` |
|------|--------------------------|
| `01_just_build_it.py` | `01_prototype.html` |
| `02_company_brain.py` | `02_spec.md`, `02_prototype.html` |
| `03_coding_agent.py` | `03_project/` (the changed copy), `03_changes.diff`, `03_transcript.json` |
| `04_plan_first.py` | `04_plan.md`, `04_project/`, `04_changes.diff`, `04_transcript.json` |
| `05_skills.py` | `05_review.md`, `05_test-plan.md`, `05_change-summary.md` |
| `06_out_the_door.py` | `06_launch/` with five Markdown files |

The output is different every run. The agents in demos 3 and 4 make different choices each time, so expect your diff to differ from the one quoted here.

Each section also has a live run in a real tool: Lovable, Claude Code, Cursor, and a Claude or ChatGPT project. [`demo/LIVE.md`](demo/LIVE.md) is the run sheet.

## 1. Just build it

**Demo:** `demo/01_just_build_it.py`

The quickest way from an idea to something people can click is to ask for it. Tools like Lovable, v0 and Bolt turn a sentence into a working app. Underneath, it is one request:

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

It took 30 seconds, and it looks finished: a dark green card, a large "30 min early", a slider, a Save button. Then do the same in Lovable, and get a whole app.

### Why this breaks

Nothing on that screen is ours. The model has never heard of Dormouse, so it wrote the most likely screen for a thermostat app. It invented a slider from "At wake-up" to "2 hours early", where Warm Wake has never gone past 90 minutes. It put the setting on a screen of its own, called "A softer start". It added a Save button, where our app saves as you go, and wrote the time as "6:30 AM", where we use the 24-hour clock. The copy sounds like an advert.

None of that is the model's fault: we didn't tell it any of it. A prototype that looks this finished is also risky in a meeting: people react to the made-up details as if they were decisions.

So tell it what we know.

## 2. The company brain

**Demo:** `demo/02_company_brain.py`

A **company brain** is what your company knows, written down once, in plain files every tool can read:

| File | What it says |
|------|--------------|
| `product.md` | What we sell, every feature, and where each setting lives |
| `customers.md` | Who our customers are and what they care about |
| `voice.md` | How we write, and the words we don't use |
| `glossary.md` | What our terms mean, and what customers call them |
| `decisions.md` | Product decisions we've made, and why. "Give customers a choice of three, not a number." "Settings about when the heating runs live under Schedule." |
| `design.md` | Colours, type, and how a settings screen is laid out |

Every tool has a place for this. Coding tools read `AGENTS.md` at the top of the code (Codex, Cursor, GitHub Copilot and many others), or `CLAUDE.md` (Claude Code, which reads `AGENTS.md` only when there is no `CLAUDE.md`; ours is one line, `@AGENTS.md`, to import it). Lovable calls it Instructions, Cursor has rules, Claude and ChatGPT have Projects. For things that change every day, like tickets and documents, **MCP** (Module 3) connects the tool to Jira, Confluence or Google Drive instead. Module 6's RAG is the same idea at scale.

The demo makes two calls. First, a product manager's spec, from the brain and the 30 pieces of customer feedback. Then the prototype, from the brain and that spec:

```python
brain = "\n\n".join(path.read_text() for path in sorted((DATA / "brain").glob("*.md")))
spec = ask(f"{SPEC_INSTRUCTIONS}\n\n{brain}\n\n# Customer feedback, September and October\n\n{feedback}", f"The request: {REQUEST}", ...)
html = html_only(ask(f"{PROTOTYPE_INSTRUCTIONS}\n\n{brain}\n\n# The spec\n\n{spec}", REQUEST, ...))
```

```text
Request: Build the settings screen for the Dormouse thermostat app, where customers choose how early Warm Wake starts the heating.

On the screen:
  Schedule
  dormouse
  Settings
  Schedule
  Warm Wake start time
  Choose how early Warm Wake can start before a schedule period.
  Up to 30
  minutes
  Up to 60
  minutes
  Up to 90
  minutes
  Saved automatically
  Warm Wake may start later if your home needs less time to reach its target temperature.
```

The spec, in `02_spec.md`, quotes the feedback by its ids. It picks the same answer product had already agreed in the ticket, from the decisions alone:

```text
Customers choose how early Warm Wake can start, using three named choices:

- **Up to 30 minutes**
- **Up to 60 minutes** — default
- **Up to 90 minutes**
```

| | Demo 1: the request alone | Demo 2: with the brain |
|---|---|---|
| Where | A screen of its own, "A softer start" | Settings > Schedule |
| Choices | A slider, "At wake-up" to "2 hours early" | Up to 30, 60 or 90 minutes |
| Default | 30 minutes | Up to 60 minutes |
| Saving | A Save button | Saved automatically |
| Look | Dark green | Dormouse cream, night blue and ember orange |
| Time | 30 seconds | 23 seconds, spec and prototype |

The same model, the same request. The only difference is about 1,300 words of context.

### Why this breaks

The prototype is ours now, but it is still a guess at a screen: this one even dropped the switch that turns Warm Wake off, which its own spec says must stay. And it isn't the product. The real settings live in a codebase, with its own structure and tests. Changing that takes more than one call: read the code, decide where the change goes, edit several files, run the tests, fix what broke. That is a job for an agent.

## 3. The coding agent

**Demo:** `demo/03_coding_agent.py`

Claude Code, Cursor's agent, Codex and Copilot are **coding agents**. Under the polish, each one is Day One's tool loop, with tools for working on code:

```python
TOOLS = [
    tool("list_files", "List every file in the project."),
    tool("read_file", "Read a file.", path="Path from the project folder"),
    tool("write_file", "Replace a file with new content, or create it.", path=..., content=...),
    tool("run_tests", "Run the project's tests, and see what passed and failed."),
]

for step in range(MAX_STEPS):
    response = client.responses.create(model=MODEL, instructions=instructions, input=conversation, tools=TOOLS)
    conversation += response.output
    calls = [item for item in response.output if item.type == "function_call"]
    if not calls:
        return response.output_text, conversation
    ...
```

The project is `data/project/`, and the agent works on a copy in `demo/output/`, so every run starts from the same code. Like the real tools, it reads the project's `AGENTS.md` first: how to run the tests, and rules such as "Change an existing test only when the change you were asked to make changes the behaviour it checks". We give it one line, the way a developer would type it:

```text
Request: Let customers choose how early Warm Wake starts the heating.

  list_files 
  read_file  dormouse/settings.py
  read_file  dormouse/warm_wake.py
  read_file  dormouse/pages.py
  read_file  tests/test_settings.py
  read_file  tests/test_warm_wake.py
  read_file  tests/test_pages.py
  read_file  README.md
  read_file  AGENTS.md
  write_file dormouse/settings.py
  write_file dormouse/warm_wake.py
  write_file dormouse/pages.py
  write_file tests/test_settings.py
  write_file tests/test_warm_wake.py
  write_file tests/test_pages.py
  run_tests  
  write_file tests/test_pages.py
  run_tests  

Agent: Added a Warm Wake lead-time setting, with choices from 15 to 90 minutes. The heating start now respects the selected limit, and the settings page lets customers choose it.

Updated settings, Warm Wake and settings-page tests to cover the new behaviour. All 19 tests pass.

Changed 6 files: 31 lines added, 3 removed
Tests: Ran 19 tests, OK
The changes are in demo/output/03_changes.diff
```

In 56 seconds it read the code, changed six files and added three tests. When one of its new tests failed, it rewrote the test, not the code, and finished with everything passing. The tool landscape is in [Choosing tools](#choosing-tools): editors like Cursor put this loop next to your code, terminal agents like Claude Code run it in your project, and cloud agents run it on a server and open a pull request.

### Why this breaks

It works, and it is wrong. Every gap below was a decision, and the agent made each one on its own without asking:

- Six choices, from 15 to 90 minutes in 15-minute steps. We decided on three.
- A default of 90 minutes. The ticket says 60.
- Under Heating. We decided settings about *when* the heating runs live under Schedule.
- Called "Warm Wake lead time": jargon.
- Shown even when Warm Wake is off.

The tests pass because the agent wrote them to match its own decisions. Passing tests tell you the code does what the agent meant, not what you meant. The request was one line; the missing detail was in the ticket and the brain, which it never saw. A person who knew less than they needed to would ask. The agent didn't, because nothing asked it to.

## 4. Plan, review, then implement

**Demo:** `demo/04_plan_first.py`

Two changes. Give the agent the agreed ticket, `DOR-231.md`, with its acceptance criteria, instead of one line. And split the work: a **plan** first, with tools that can only look, then a person reads it, then the agent builds exactly that. This is **plan mode** in Claude Code, Cursor, Codex and Copilot (Shift+Tab in most of them). Kiro and GitHub's Spec Kit go further, with **spec-driven development**: requirements, then a design, then a task list, each reviewed before the next.

```python
plan, _ = run_agent(f"{ticket}\n\n{PLAN}", instructions, TOOLS[:2])  # list_files and read_file only
print(plan)
if input("Go ahead with this plan? (y/n) ").strip().lower() != "y":
    sys.exit()
summary, conversation = run_agent(f"{ticket}\n\n# Your plan\n\n{plan}\n\n{BUILD}", instructions, TOOLS)
```

```text
1. **`dormouse/settings.py`** — Add a `how_early` setting with a default of 60 and allow only 30, 60 or 90.
   **Tests:** Add tests in `tests/test_settings.py` for the default and allowed values, and rejection of other values. ...

2. **`dormouse/warm_wake.py`** — Use `how_early` as the maximum number of minutes Warm Wake can start before a schedule period, ...
   **Tests:** Update the existing 90-minute cap test in `tests/test_warm_wake.py` to reflect the new default of 60, and add coverage for all three choices. ...

3. **`dormouse/pages.py`** — Move the Warm Wake row from Heating to Schedule, add How early there, and show How early only when Warm Wake is on. ...

**Uncertainties:** The ticket doesn’t specify the exact customer-facing label or explanatory wording for How early. I’d use “How early” ...

Go ahead with this plan? (y/n) y

Building:
  ...
Changed 6 files: 51 lines added, 10 removed
Tests: Ran 21 tests, OK
```

The plan names every file, every test it will change and why, and the one thing it is unsure about. That is the cheapest moment to catch a mistake: a plan is a dozen lines to read, and changing it costs nothing.

| | Demo 3: one line | Demo 4: the ticket, and a plan |
|---|---|---|
| Choices | 15, 30, 45, 60, 75 or 90 minutes | 30, 60 or 90 minutes |
| Default | 90 minutes | 60 minutes |
| Where | Heating | Schedule |
| Hidden when Warm Wake is off | No | Yes |
| Name | Warm Wake lead time | How early |
| Lines added and removed | 31 and 3 | 51 and 10 |
| Tests | 19, all pass | 21, all pass |
| Time | 56 seconds | 53 seconds |

### Why this breaks

The plan was right, the tests pass, and every acceptance criterion looks met. You approved a plan; you haven't read the 61 changed lines that came out of it, and the agent wrote all of them, and all of their tests, in under a minute. Merging that because it passes is **vibe coding**: accepting code you haven't understood because it seems to work.

And there is a bug in it. A home's settings saved before firmware 4.2 have no `how_early` in them, so for every existing customer:

```python
saved_before_4_2 = {"boost_temperature": 21.0, "warm_wake": True, "week_starts_on": "Monday", "away_temperature": 16.0, "geofencing": False}
heating_start(datetime(2026, 11, 20, 7, 0), 10, 21, 2, saved_before_4_2)  # KeyError: 'how_early'
```

The ticket said existing customers get 60 minutes. The agent's tests only ever use the new defaults, so they can't see it. Somebody has to review the change properly.

## 5. Review and automate

**Demo:** `demo/05_skills.py`

Reviewing AI-written code is the same job as reviewing anyone's, done more often: read the diff, check it against the ticket, look hard at any test that was changed, and ask what it doesn't cover. Some of that can be automated, and the steps you repeat on every change are worth writing down.

A **skill** is a folder with a `SKILL.md` file: a name and a description at the top, then instructions. An agent loads it when the description matches the job. Claude Code started the format, and Codex, Copilot, Cursor and others read it too. Ours are in `data/skills/`: a **review** against the ticket and `AGENTS.md`, a **test plan** for a tester, and a **change summary** for support and product, with a ticket comment.

```python
def load_skill(name):
    """A skill is a Markdown file of instructions, with its name and description at the top."""
    _, front, body = (DATA / "skills" / name / "SKILL.md").read_text().split("---", 2)
    return body.strip()
```

The demo runs the three skills, at the same time, over the change from demo 4 (saved as `data/changes/DOR-231.diff`):

```text
=== review ===

**Verdict:** Request changes.

**Must fix:**
- `dormouse/settings.py`: `check` accepts values such as `60.0` for `how_early`. The ticket says any other value must be rejected; enforce the allowed integer values, not just equality with them.
- `dormouse/pages.py`: The new “How early” setting has no row in the page when Warm Wake is off. This conflicts with AGENTS.md, which requires every new setting to have a row on the settings page. ...

**Acceptance criteria:**
- With How early set to 30, 60 or 90, the heating never starts more than that many minutes before the period. — **Met**
- Any other value for How early is rejected. — **Not met** (`60.0` is accepted).
- A new customer, and an existing customer who has never changed it, gets 60 minutes. — **Met** (default is 60).
...

=== change-summary ===

## What changed

- Customers can choose how early Warm Wake starts heating: up to 30, 60 or 90 minutes before a schedule period.
- The default is 60 minutes for new and existing customers who haven’t changed this setting.
- Warm Wake and How early are now under **Settings > Schedule**, rather than **Settings > Heating**.
- How early is shown only when Warm Wake is on.
- Warm Wake still starts heating on time when switched off.
...
```

The three skills took 7 seconds together. The review caught one real gap: `60.0` gets through. It raised one false alarm: hiding How early is what the ticket asked for. And it marked existing customers as **Met**, missing the crash, because it reasoned from the defaults just as the agent did. The test plan did better: its test 3 is "Sign in as an existing customer whose How early setting has never been changed", which is exactly where a tester would hit the `KeyError`.

So an AI review is a second opinion, not a sign-off. It is quick and tireless, and it is good at the things you can list. It shares the author's blind spots, especially when the same model wrote the code. A different model, or a reviewer told to look for one kind of problem, helps. A person who knows that saved settings exist is still the one who catches this.

Once the steps are skills, they don't need a person to start them. `claude -p "..."` and `codex exec "..."` run an agent from a script, and the `anthropics/claude-code-action` and `openai/codex-action` GitHub Actions run one on every pull request: review the change, write the test plan, summarise it in plain English, update the ticket, explain why a build failed.

### Why this breaks

It doesn't, quite: this is where the code is done. But a feature isn't shipped when it's merged. Customers need telling, the help centre is wrong, support needs to know what changed, and sales will be asked about it. That is a lot of writing, by people who weren't in the room.

## 6. Out the door

**Demo:** `demo/06_out_the_door.py`

The same brain, the same ticket and the same change, and five more skills: **release notes**, the **help article** updated, a **launch email**, **social posts** and a **sales sheet**. Then a check on everything that goes out, from rules in the brain: none of the words in "Words we don't use", and no savings figures, because of the decision "No savings figures in marketing".

```python
def check(text):
    """Problems a person would otherwise have to spot: banned words, and savings figures."""
    problems = [f'"{word}"' for word in banned_words() if re.search(rf"\b{re.escape(word)}\b", text, re.IGNORECASE)]
    problems += [f'a savings figure, "{m}"' for m in re.findall(r"\d+ ?%|\d+ per ?cent", text)]
    return problems
```

```text
Launch kit for DOR-231, in demo/output/06_launch/:

  release-notes.md     voice check passed
  help-article.md      voice check passed
  launch-email.md      voice check passed
  social-post.md       voice check passed
  sales-sheet.md       voice check passed

=== social-post ===

**Short**  
Warm Wake now starts the heating no more than 30, 60 or 90 minutes before a schedule period. The default is 60 minutes. Choose how early it starts in Settings > Schedule.

**LinkedIn**  
Warm Wake helps your home reach its target temperature when a schedule period starts. Now you can choose how early it starts: up to 30, 60 or 90 minutes. The default is 60 minutes, and you’ll find the setting in Settings > Schedule. It’s there only while Warm Wake is on.
```

The whole kit took about 10 seconds. The email's subject is "Choose how early Warm Wake starts". The sales sheet's "What not to say" comes straight from the decisions: "Don't promise a particular gas saving or percentage. Point customers to their Energy tab." Every menu path and number matches the ticket, because they all came from it.

### Where this stops

The check only catches what somebody wrote down as a rule. The sales sheet calls How early a "shorter lead time", the agent's jargon from demo 3, and passed. On one run the social post came back twice, run together, and passed too. And it all describes the change as written, so it would have announced the existing-customer behaviour that crashes. A person still reads it before it goes out. What has changed is that they are reading and correcting, not writing from a blank page.

## Choosing tools

The tools fall into four kinds. `data/tools.json` has 29 of them, with what each is known for, what to watch out for, a price and a source, checked on 20 November 2026. They change monthly: recheck before you rely on any of it.

| Kind | For | Examples |
|------|-----|----------|
| **Build an app from a prompt** | Product managers, designers and founders who want something clickable | Lovable, v0, Bolt.new, Replit Agent, Figma Make, Google AI Studio |
| **AI editors** | Developers who want an agent inside the editor they use every day | Cursor, GitHub Copilot in VS Code, Devin Desktop (formerly Windsurf), Kiro, Google Antigravity, JetBrains, Zed |
| **Coding agents** | Developers who hand over a task and review the result, in the terminal, the cloud or CI | Claude Code, OpenAI Codex, Antigravity CLI (which replaced Gemini CLI), GitHub Copilot cloud agent, Devin, Jules, and the open source Aider, Cline and OpenCode |
| **For everyone else** | Product, marketing and sales, working with documents, meetings and research | Claude (Projects, Cowork), ChatGPT, Gemini and NotebookLM, Microsoft 365 Copilot, Notion AI, Glean, Granola |

What they share matters more than what separates them:

| | Claude Code | Cursor | Codex | GitHub Copilot |
|---|---|---|---|---|
| Reads the brain from | `CLAUDE.md` (or `AGENTS.md` if there is none) | `AGENTS.md`, rules | `AGENTS.md` | `AGENTS.md` and others |
| Plan first | Plan mode | Plan mode | Plan mode (`/plan`) | Plan agent |
| Skills (`SKILL.md`) | Yes | Yes | Yes | Yes |
| Runs without a person | `claude -p`, GitHub Action | Cloud agents | `codex exec`, GitHub Action | Cloud agent |

Things worth knowing this year:

- SpaceX [bought Cursor](https://thenextweb.com/news/spacex-cursor-acquisition-completed-gpu-fleet) in August 2026. OpenAI then [said it would stop supplying its models](https://openai.com/index/our-decision-on-cursor-following-its-acquisition-by-spacex/) to Cursor, with a proposed cut-off of 12 November.
- Google [replaced Gemini CLI with Antigravity CLI](https://developers.googleblog.com/en/an-important-update-transitioning-gemini-cli-to-antigravity-cli/) for individual users in June.
- Windsurf [became Devin Desktop](https://docs.devin.ai/desktop/devin-desktop-faq) in June.
- GitHub Copilot [moved to usage-based billing](https://github.blog/2026-05-01-github-copilot-is-moving-to-usage-based-billing/) in June.
- App builders have had real security incidents. In February 2026 an app showcased by Lovable [leaked 18,697 user records](https://www.theregister.com/2026/02/27/lovable_app_vulnerabilities), and a flaw in Lovable's own API [exposed other users' projects](https://thenextweb.com/news/lovable-vibe-coding-security-crisis-exposed). Module 8 picks this up.

## How this course was built

This course is a real example. Its repository has a `CLAUDE.md`, 24 lines, which imports `MODULE_GUIDE.md`, 185 lines on how a module is put together: the story structure, the demo rules, the README sections, British English. That is the course's company brain, and every agent that worked on it read it first. Promotional clips are made with a skill, `.claude/skills/social-clip/SKILL.md`. A test, `tests/test_structure.py`, checks every module against the guide: the automated check. And each module's outline is agreed before anything is built: plan first.

## Summary

| Step | What it gave us | What was wrong |
|------|-----------------|----------------|
| 1. Just build it | A polished prototype in 30 seconds | Everything on it was invented |
| 2. The company brain | A spec and prototype that are ours | Still a guess at a screen, not the product |
| 3. The coding agent | The feature in real code, tests passing, in a minute | It made the product decisions itself |
| 4. Plan first | The right feature, from the ticket | 61 lines nobody had read, with a bug |
| 5. Review and automate | A review, a test plan and a summary in 7 seconds | The review missed the bug; a person is still needed |
| 6. Out the door | Release notes, help, email, posts and a sales sheet | The checks only catch what's written down |

## Playground

The [playground](playground/) has small scripts to try between exercises: see which brain file changes what, approve each change an agent makes, make an agent write failing tests first, get a second opinion on a review, write your own skill, find themes in customer feedback, and check copy against the voice.

## Further reading and extensions

[Further reading](further-reading/) is the final exercise: papers on coding agents and on whether AI tools make people faster, and bigger projects to try.

## Slides

```bash
pnpm slides:07
```
