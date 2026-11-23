# Old code rescue

Pick an old project, yours or your team's, that nobody likes touching: no tests, out-of-date dependencies, a bug everyone works around. First pin down what it does today with tests, then bring it up to date, then fix the bug with Debug mode. It's the job AI editors are most often bought for, and the one where "it still works" needs proving.

**Build it in:** Cursor. **Time:** a day. **Needs:** Cursor, and an old project with a git history you can make a branch in.

## Start in Ask mode

> Explain what this project does, how to run it, and what it depends on. Which parts are the riskiest to change, and why?

## Then: tests before changes

In Agent mode:

> Write tests that pin down what this code does today, including its odd cases. Don't change the code. If something looks like a bug, write a test for the current behaviour anyway, and list it for me.

Run them. Commit them. Now you have something that tells you if the next step breaks anything.

## Then: bring it up to date

In Plan mode:

> Plan how to bring this project up to date: the language version, then each dependency, one at a time, running the tests after each. Stop at the first step that breaks a test and tell me why.

## Then: the bug everyone works around

In Debug mode, describe it the way a user would:

> When I export a report for a month with 31 days, the last day is missing. It's been like this for years.

Let it add its logging and ask you to reproduce it. Fix it, and turn the "current behaviour" test for it into a test for the right behaviour.

## Watch for

- **Tests that pass by changing the code.** You asked it not to touch the code while writing tests. Check the diff.
- **Upgrades that change behaviour.** A test that starts failing after an upgrade is the tests doing their job.
- **Its list of odd cases.** Some will be bugs, and some will be features someone relies on.

## Try this

1. Ask for a diagram of how the project fits together, as a Mermaid diagram in the README.
2. Give the bug-hunting step to Claude Code instead, asking it to prove the cause before changing anything. Compare with Debug mode.
3. Ask a cloud agent to do one dependency upgrade as a pull request, and review it.
4. Remove one piece of code the tests say nothing uses. Then check whether anything really did use it.
5. Write the README the project should have had, and ask someone who's never seen the project to follow it.

## Questions

For discussion. There are no right answers.

- "Pin down what it does today, including the bugs." Why might you want a test that checks for a bug?
- Who should decide which odd cases are bugs and which are features?
- If the tests were written by the same model that later changes the code, how much should they reassure you?
