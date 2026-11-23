# Run sheet: Claude Code

The live demo for section 3. Claude Code is a coding agent that runs in your terminal, in the folder you start it in. Try it once before the session: agents do something different every time.

You need Claude Code and a Claude plan that includes it (Pro or above), or an API key. Checked against Claude Code's documentation on 23 November 2026.

## Set up

Copy the project somewhere outside the course repository, so Claude Code can change it and you can use git. From the module folder:

```bash
MODULE="$PWD"
cp -R data/project ~/dormouse-dashboard && cd ~/dormouse-dashboard && git init -q && git add . && git commit -qm "Start"
```

To start again between steps:

```bash
git reset --hard && git clean -fd
```

## 1. Start it

1. In `~/dormouse-dashboard`, run `claude`.
2. Ask: "What does this project do, and how do I run it?"

Point out: it read `CLAUDE.md` first, which imports `AGENTS.md`, so it already knows the test command and the rules.

## 2. Use it

1. Paste the contents of `$MODULE/data/tickets/DOR-232.md` (let the week start on Saturday).
2. Watch it read, edit and run the tests. Depending on the permission mode, it asks before each edit and command.
3. Press Shift+Tab to show the modes: manual (it asks first), accept edits, plan, and auto. Say which one you're in.
4. Type `/` to show the commands: `/clear`, `/permissions`, `/mcp` and more.
5. Leave it, and in another terminal show the same agent with no person: `claude -p "Run the tests and tell me how many pass."`

Point out: under the polish this is Module 3's tool loop, with tools to read, edit, search and run commands.

## 3. Subagents, from agent files

1. Leave the change in place. Quit Claude Code, copy in the three agent files, and start it again (agent files load when it starts):

   ```bash
   mkdir -p .claude/agents && cp "$MODULE"/data/agents/*.md .claude/agents/
   claude
   ```

2. Ask: "Check the change against this ticket with the ticket-checker, test-reviewer and customer-text agents, all at the same time." Paste DOR-232 after it.
3. Watch three subagents start at once. Each has its own context and tools, and reports back a summary.

Point out: each agent file is a page of Markdown: a name, a description that says when to use it, the tools it may use, a model, and its instructions. They live in the project, so the whole team gets them. `customer-text` runs on Haiku, because checking labels doesn't need a bigger model.

## 4. Skills

1. Copy in the skills:

   ```bash
   mkdir -p .claude/skills && cp -R "$MODULE"/data/skills/* .claude/skills/
   ```

2. Ask: "Write the release notes for this change." It picks the `release-notes` skill from its description.
3. Then type `/test-plan` to run a skill by name.

Point out: a skill is a folder with a `SKILL.md`: instructions loaded only when the job matches. Cursor, Codex and Copilot read the same format.

## 5. Connectors

1. Type `/mcp` to list the MCP servers Claude Code can use.
2. If you are signed in with a Claude account, the connectors you added at claude.ai (such as GitHub, Linear or Google Drive) appear here too, named like `claude.ai Linear`.

Point out: a connector is an MCP server (Module 3), here to someone else's service. Section 6 adds one of our own.
