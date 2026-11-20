# Live demos

Each section has a Python demo that runs on the course's OpenAI key, and a live run in a real tool. This is the run sheet for the live runs. Record each one beforehand: Lovable takes a few minutes, and agents do something different every time.

Before the coding runs, copy the project somewhere outside the course repository, so the tools can change it and use git:

```bash
cp -R data/project ~/dormouse-dashboard && cd ~/dormouse-dashboard && git init -q && git add . && git commit -qm "Start"
```

To start again: `git reset --hard && git clean -fd`.

## 1. Just build it: Lovable

1. New project. Paste the same request as demo 1:

   > Build the settings screen for the Dormouse thermostat app, where customers choose how early Warm Wake starts the heating.

2. Point out: it works, it looks finished, and it has invented the settings, the wording and the design.

## 2. The company brain: Lovable again

1. In the project's settings, open **Knowledge** (Lovable now calls it **Instructions**) and paste in `data/brain/product.md`, `voice.md`, `decisions.md` and `design.md`.
2. Ask it to rebuild the screen. Compare it with the first one and with `demo/output/02_prototype.html`.
3. Show where the same brain lives in the other tools: `AGENTS.md` and `CLAUDE.md` in the project, Cursor's rules, Claude Projects.

## 3. The coding agent: Claude Code and Cursor

In `~/dormouse-dashboard`:

1. Run `claude`, then type the same request as demo 3:

   > Let customers choose how early Warm Wake starts the heating.

2. Let it run. Point out that it read `CLAUDE.md`, which points at `AGENTS.md`, and ran the tests.
3. `git diff`, and compare with `demo/output/03_changes.diff`: what did it decide on its own?
4. Reset, and do the same in Cursor's agent.

## 4. Plan, review, then implement: plan mode

1. Reset. In Claude Code, press Shift+Tab until it says **plan mode**. In Cursor, pick **Plan** from the mode menu.
2. Paste the contents of `data/tickets/DOR-231.md` and ask for a plan.
3. Read the plan aloud. Push back on one step, and watch it change the plan.
4. Approve it, and let it build.

## 5. Review and automate: skills

1. Copy the skills into the project: `mkdir -p .claude/skills && cp -R <module>/data/skills/review .claude/skills/`.
2. In Claude Code: "Review the change in `git diff` against DOR-231." It picks the review skill from its description.
3. Show the same thing running without a person, in a pull request: `claude -p` in a script, or the `anthropics/claude-code-action` GitHub Action. Codex has `codex exec` and `openai/codex-action`.

## 6. Out the door: Claude, ChatGPT or Gemini

1. Start a Claude Project (or a ChatGPT Project, or a NotebookLM notebook) and add the brain files, the ticket and the help article.
2. Ask for the launch email in the Dormouse voice. Then the sales sheet.
3. Point out: no code, the same brain, the same checks.
