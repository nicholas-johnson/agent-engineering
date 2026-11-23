# Hooks

`AGENTS.md` asks a coding agent to run the tests before it finishes, and to change a test only when the ticket needs it. Asking isn't making. Here you'll add two **hooks** to Claude Code: commands that run at fixed points whether the model remembers or not. One runs the tests after every edit. The other stops any edit to a test until Claude explains itself.

From the module folder (`day-two/module-07-ai-assisted-development`), with the project copied as in the [playground README](../README.md):

```bash
MODULE="$PWD"
cd ~/dormouse-dashboard
mkdir -p .claude/hooks
cp "$MODULE"/playground/hooks/settings.json .claude/settings.json
cp "$MODULE"/playground/hooks/hooks/*.sh .claude/hooks/
claude
```

Needs Claude Code. Then paste `data/tickets/DOR-232.md` (let the week start on Saturday), which needs a test changed.

---

`settings.json` says when each hook runs. `PreToolUse` runs before a tool, and `PostToolUse` after it; the matcher picks the tools, here any edit:

```json
"PostToolUse": [
  {
    "matcher": "Edit|Write",
    "hooks": [{ "type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/run-tests.sh" }]
  }
]
```

A hook talks back through its **exit code**. 0 means carry on. 2 means stop, and whatever the hook wrote to stderr goes to Claude. `run-tests.sh` exits 2 when a test fails, so Claude sees the failures straight after the edit that caused them. `protect-tests.sh` reads the edit Claude is about to make, as JSON on stdin, and exits 2 if the file is in `tests/`:

```sh
if grep -q '"file_path": *"[^"]*/tests/'; then
  echo "Don't change a test without asking. Say which test, and why the ticket needs the change." >&2
  exit 2
fi
```

Both scripts were checked by hand, without Claude Code, by feeding them what it would send:

```text
$ echo '{"tool_name":"Edit","tool_input":{"file_path":"/x/dormouse-dashboard/tests/test_settings.py"}}' | sh hooks/protect-tests.sh
Don't change a test without asking. Say which test, and why the ticket needs the change.
tests edit -> exit 2

$ echo '{"tool_name":"Edit","tool_input":{"file_path":"/x/dormouse-dashboard/dormouse/settings.py"}}' | sh hooks/protect-tests.sh
code edit -> exit 0
```

With a test broken on purpose, `run-tests.sh` printed the failure and exited 2; with the tests passing it printed nothing and exited 0.

In Claude Code, paste DOR-232 and add: "Build this. If you need to change a test, tell me which one and why first." Watch for the moment the hook blocks its first edit to `tests/`, and what it says next.

## Things to notice

- **The rule moved from a request to a guarantee.** The sentence in `AGENTS.md` still matters: it tells Claude why. The hook makes sure.
- **Blocked isn't stopped.** When `protect-tests.sh` blocks an edit, Claude reads the message and has to explain. DOR-232 really does need a test changed, so the explanation should be easy.
- **Every edit costs a test run.** Sixteen tests take a few milliseconds here. In a real project, think about which hook belongs after every edit and which only at the end (the `Stop` event).

## Try this

1. **Quieter.** Change `run-tests.sh` to run only the test file that matches the file Claude edited.
2. **At the end, not after every edit.** Move the test run from `PostToolUse` to `Stop`, which runs when Claude thinks it's finished. What changes?
3. **Format on save.** Add a `PostToolUse` hook that runs a formatter on the file just edited.
4. **Guard the brain.** Block edits to `AGENTS.md` and `CLAUDE.md`, so the agent can't rewrite its own rules.
5. **Log it.** Add a hook that appends every command Claude runs (the `Bash` tool) to a log file, with the time. Read it after a session.
6. **Cursor too.** Cursor has hooks of its own, in `.cursor/hooks.json`. Write the same two for Cursor, using its documentation.

## Questions

For discussion. There are no right answers.

- Which of your team's rules should be a sentence in `AGENTS.md`, and which should be a hook?
- A hook can block the agent. Who decides what it blocks, and who can change the hook?
- Running the tests after every edit makes the agent slower and more careful. When is that the wrong trade?
- Hooks run on your machine, with your permissions. What could go wrong with a hook someone else committed to the project?

## Further reading

- **Anthropic. "Hooks reference." _Claude Code documentation_.** [code.claude.com/docs/en/hooks](https://code.claude.com/docs/en/hooks). Every event a hook can run on, and what a hook can send back. Read the section on exit codes, and on what `PreToolUse` receives on stdin.
