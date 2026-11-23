# Cursor rules

Cursor reads the project's `AGENTS.md` by itself, but the company brain isn't in the project. Here you'll turn two brain files into **Cursor rules**, one that always applies and one Cursor picks when the job needs it, and ask the same questions with and without them.

From the module folder (`day-two/module-07-ai-assisted-development`), with the project copied as in the [playground README](../README.md):

```bash
MODULE="$PWD"
cd ~/dormouse-dashboard
mkdir -p .cursor/rules
{ printf -- '---\ndescription: Product decisions Dormouse has made, and why\nalwaysApply: true\n---\n\n'; cat "$MODULE/data/brain/decisions.md"; } > .cursor/rules/decisions.mdc
{ printf -- '---\ndescription: How Dormouse writes anything a customer reads: labels, explanations, messages\nalwaysApply: false\n---\n\n'; cat "$MODULE/data/brain/voice.md"; } > .cursor/rules/voice.mdc
```

Needs Cursor. Open `~/dormouse-dashboard` in Cursor.

---

A rule is a `.mdc` file in `.cursor/rules/`: Markdown with a few lines at the top that say when it applies. Cursor ignores plain `.md` files there.

| `decisions.mdc` | `voice.mdc` |
|-----------------|-------------|
| `alwaysApply: true`: in every conversation | `alwaysApply: false`: Cursor reads the `description` and decides |

The other two kinds are rules for certain files (`globs: tests/**`) and rules you only use by name (`@voice`). The difference matters because every rule that applies is context the model reads before your question: the always-on ones cost tokens in every conversation.

Before you add the rules, ask in Ask mode:

> Where should a new setting for how long Boost lasts go, and what should its choices be?

Then add them, start a new conversation, and ask again. Then, in Agent mode, paste `data/tickets/DOR-233.md` and read the labels it writes.

_Output to come: recorded answers from Cursor, with and without the rules._

## Things to notice

- **Which rule was used?** Did it pick up `voice.mdc` for the labels without being told? Look for the voice's rules in what it wrote: sentence case, the 24-hour clock, none of the banned words.
- **Rules against the ticket.** DOR-233 puts Boost length under Heating. Decisions say settings about *when* the heating runs live under Schedule. Is Boost length about when, or how warm? Does Cursor notice the question?
- **A copy.** These rules are copies of the brain. Change `decisions.md` in the module, and the rules don't change.

## Try this

1. **Glob it.** Make a rule for `tests/**` only: "Never change an existing test without saying why." Edit a test and see if it's used.
2. **By name.** Set `voice.mdc` to apply manually, and use it with `@voice` in a question.
3. **Too much.** Make all six brain files always-apply rules. Ask something small. Does the answer get better, or just longer?
4. **The same rules in Claude Code.** Put the same text in `CLAUDE.md`, or as files Claude Code imports with `@`. What's different?
5. **One source.** Replace the copies with the company-brain MCP server from section 6 (`demo/06_company_brain.md`). Which is better for a rule that applies every time?

## Questions

For discussion. There are no right answers.

- Every tool has its own place for rules. How would you keep five copies of the brain the same?
- An always-on rule is read before every question. What deserves that, and what should wait to be asked for?
- When a rule and a ticket disagree, which should win, and who should the agent ask?

## Further reading

- **Cursor. "Rules." _Cursor documentation_.** [cursor.com/docs/rules](https://cursor.com/docs/rules). The four kinds of rule, and where Cursor reads `AGENTS.md`. Read the part on how Cursor decides to apply a rule from its description.
