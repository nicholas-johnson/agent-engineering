# Agent files

The module gave Claude Code three agent files to review a change: one checks the ticket, one the tests, one the words customers see. Here you'll add a fourth, `old-homes`, which checks that a change still works for homes saved before it. You'll run all four at once, then write one of your own.

From the module folder (`day-two/module-07-ai-assisted-development`), set up the project and make a change to review (see the [playground README](../README.md) for the copy):

```bash
MODULE="$PWD"
cd ~/dormouse-dashboard
mkdir -p .claude/agents && cp "$MODULE"/data/agents/*.md "$MODULE"/playground/agent-files/old-homes.md .claude/agents/
claude
```

Needs Claude Code. In Claude Code, paste `data/tickets/DOR-233.md` (let customers choose how long Boost lasts) and let it build. Then ask:

> Check this change with the ticket-checker, test-reviewer, customer-text and old-homes agents, all at the same time. Here is the ticket: (paste it again)

---

An agent file is a page of Markdown in `.claude/agents/`. The top says who the agent is and what it may do; the rest is its instructions:

```markdown
---
name: old-homes
description: Checks that a change still works for homes saved before it, whose settings may be missing a new setting or hold an old value. Use after a change to settings, before it is committed.
tools: Read, Grep, Glob, Bash
model: sonnet
---
```

The **description** is what Claude reads when it decides which agent to use, so it says when, not just what. The **tools** line keeps a reviewer from editing. Each subagent starts with a fresh context of its own: it doesn't see your conversation, only the job Claude hands it, and it sends back a summary rather than everything it read. That is why four can run at once without filling up the main conversation.

`old-homes` is there because of a real kind of bug. Every home in `homes/` keeps the settings it saved. A change that adds `boost_minutes` and reads `settings["boost_minutes"]` works in every test, which use the new defaults, and crashes for every customer who saved before it.

_Output to come: a recorded Claude Code run of the four agents on DOR-233._

## Things to notice

- **Did they really run at once?** Claude Code starts subagents in the background. Watch the order their reports come back in.
- **Did old-homes prove it, or guess?** Its instructions say to copy a saved home and run it. Look for the copy in its report.
- **Overlap.** The test reviewer is told to look for "settings saved before the change" too. Do the two agents agree?

## Try this

1. **Cheaper.** Change `old-homes` to `model: haiku`. Does it still find the problem, if there is one?
2. **Ask by description.** Don't name the agents. Ask "Is this change safe for existing customers?" Which agent does Claude pick?
3. **Your own.** Write `security-reviewer.md`: it checks a change for anything that reads files, runs commands or uses input a customer typed. Give it only `Read, Grep, Glob`.
4. **One that can fix.** Write an agent with `Edit` in its tools that fixes only the problems the others found, and nothing else. Is that better than letting the main conversation fix them?
5. **Share it.** Commit `.claude/agents/` to the project. Start a cloud session (section 5) on the repository: does it find the agents?
6. **For every project.** Move `old-homes.md` to `~/.claude/agents/`. It's now yours in every project. Which of your agents belong to a project, and which to you?

## Questions

For discussion. There are no right answers.

- Four reviewers that never get tired. Does that make a person's review more or less important?
- An agent file is easy to write and easy to trust. Who on your team should be allowed to add one to the project?
- `old-homes` checks for a mistake someone has already made. What mistakes has your team made that a page of instructions could check for?
- When four agents agree a change is fine, what haven't they checked?

## Further reading

- **Anthropic. "Create custom subagents." _Claude Code documentation_.** [code.claude.com/docs/en/sub-agents](https://code.claude.com/docs/en/sub-agents). Every field an agent file can have. Read the part on running subagents in the background, and on what a subagent does and doesn't see.
