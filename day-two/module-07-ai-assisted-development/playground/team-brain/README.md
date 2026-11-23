# Team brain

Build an MCP server for something your team knows, and attach it to the tools everyone uses. Section 6 did it for Dormouse's product, decisions and voice. Do it for your own team: how you work, what you've decided, what your words mean, the questions new people always ask. You won't write the server yourself: you'll ask a coding agent to, starting from the module's.

**Build it in:** Claude Code (to write the server), then Claude Code, Cursor and the Claude app (to use it). **Time:** a day. **Needs:** Claude Code, and a few pages of your team's knowledge, with nothing secret in them.

## Start with the knowledge

Write, or collect, four or five short Markdown files:

- `how-we-work.md`: meetings, reviews, releases, who to ask about what
- `decisions.md`: decisions you've made, with the reason for each
- `glossary.md`: your team's words and acronyms
- `faq.md`: what new people ask in their first month

Keep each under a page. If it's long, it's two files.

## Then, the server

Make a folder with your files in `brain/`, copy the module's `demo/06_brain_server.py` into it as an example, and start `claude` there:

> Read 06_brain_server.py: it's an example. Write a server like it for the files in brain/: one tool to read a topic, one to search all of them for words, and a description for each that says when to use it. Then tell me how to attach it to Claude Code, Cursor and the Claude desktop app.

Attach it to Claude Code with `claude mcp add`, then ask something only your team would know:

> What did we decide about code reviews, and why?

## Watch for

- **The descriptions.** They're all the model knows about your tools. Read them as if you were the model: would you know when to call each one?
- **What it answers without asking.** Does it call the tool, or guess from what it already knows?
- **Stale answers.** Change a decision in `decisions.md`. Does the next answer change, without restarting anything?

## Try this

1. Attach it to Cursor and the Claude app too. Ask all three the same question.
2. Give it to a new colleague on their first day, and ask them to write down every question it couldn't answer. Those are your next files.
3. Add a tool that lists what changed in the brain this week.
4. Put your team's calendar or ticket system behind it as well, with a ready-made connector, and ask questions that need both.
5. Ask Claude Code to write a test for each tool, so you know it still works after the next change.

## Questions

For discussion. There are no right answers.

- Who should be allowed to change the brain, and who should check what they wrote?
- Some of what your team knows isn't written down anywhere. What gets lost when only the written part reaches the tools?
- Once every tool reads the brain, a mistake in it is repeated by every tool. How would you catch one?
