# Prototype to product

Take one idea through every tool in the module. Prototype it in Lovable, move the code to GitHub, add the feature Lovable struggled with in Cursor, hand the next job to a cloud agent, and have an agent review its pull request. At the end, write down where each tool was best. It's the closest the playground gets to how a small team might really work.

**Build it in:** Lovable, Cursor or Claude Code, and a cloud agent. **Time:** a weekend. **Needs:** an account with each, and a GitHub account.

## Pick an idea

Something small enough for a weekend, with a few people using it. For example:

> A lunch rota for a small office: who's buying the sandwiches each Friday, who owes whom, and a reminder on Thursday afternoon.

## 1. Prototype it in Lovable

Plan mode, then Build mode, as in section 2. Stop when people could use it, not when it's perfect. Write down the one thing you couldn't get Lovable to do well.

## 2. Move it to GitHub

Connect GitHub from the Lovable project. It makes a new repository and keeps it in sync both ways.

## 3. Take it further in Cursor or Claude Code

Clone the repository and open it. Start in Ask mode, or by asking Claude Code:

> Explain how this app is built: the pages, the database tables, and where sign-in happens. What would you change before more people use it?

Then add the thing Lovable struggled with, in Plan mode first. Add an `AGENTS.md` with how to run it and what not to touch.

## 4. Hand the next job to a cloud agent

Write the next feature as an issue (see [backlog-afternoon](../backlog-afternoon/) for a pattern) and give it to a cloud agent. Ask `@claude` to review its pull request against the issue. Merge it only after you've read it.

## 5. Write down what you learned

A short table: each tool, what it was best at in this project, and where you had to take over.

## Watch for

- **Two tools editing one repository.** Lovable syncs both ways. What happened when you changed code in Cursor and then asked Lovable for something?
- **Where the context lives.** By the end, Lovable's Instructions, `AGENTS.md` and your issues all describe the project. Do they agree?
- **Security.** Run Lovable's deep scan at the end, after everyone's changes. Did anything new turn up?

## Try this

1. Put what the project knows behind a small MCP server, as in [team-brain](../team-brain/), and attach it to every tool.
2. Ask someone who's never seen it to use it for a week, and turn their complaints into issues for cloud agents.
3. Do the same idea again, starting in Claude Code instead of Lovable. Which route got further in the same time?
4. Write a skill that sets up a new project the way you'd now like every project to start.

## Questions

For discussion. There are no right answers.

- Which tool would you drop if you could only keep three? Why that one?
- At which step did you stop understanding every line of your own project? Does that worry you?
- If this had been a real product, which step would have needed a person who isn't you?
