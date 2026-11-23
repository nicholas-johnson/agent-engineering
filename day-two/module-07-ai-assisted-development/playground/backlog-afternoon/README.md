# Backlog afternoon

Clear five small jobs from a repository's backlog without writing any of the code. Write five clear issues, hand each one to a cloud agent, go and do something else, then come back and review five pull requests. You'll find out how much of the work is in writing the issue, and how much in reading what comes back.

**Build it in:** cloud agents: Claude Code on the web, Copilot in the cloud, Codex cloud or Cursor's Cloud Agents. **Time:** an afternoon, most of it spent elsewhere. **Needs:** a GitHub repository you own, and at least one cloud agent's paid plan.

## Start with the issues

Pick five small, different jobs in one of your repositories:

1. A typo or broken link in the README.
2. A missing test for a function that has none.
3. An error message that doesn't say what to do.
4. A small feature: a new option, a new column, a new flag.
5. A README section that's out of date.

Write each one as a GitHub issue that someone who's never seen the project could finish alone. A pattern that works:

> **What's wrong:** the error when the config file is missing says "KeyError: 'path'".
> **What it should do:** say "No config file found at ~/.tool/config.toml. Run tool init to make one."
> **How to check:** run `tool run` with no config file; run the tests; all must pass.
> **Don't:** change anything else.

## Then, hand them out

Give each issue to a cloud agent: assign it to Copilot, paste it into Claude Code on the web or Codex, or mention `@cursor`. Give one issue to two different agents.

Come back in an hour, and review each pull request as if a new colleague wrote it.

## Watch for

- **The unclear issue.** Which one did you write worst? A person would have asked. What did the agent do?
- **Did it run the tests?** Look for the evidence in the pull request, not the claim.
- **The issue given to two agents.** Same fix? Same size? Which would you merge?

## Try this

1. Write a skill, `.claude/skills/write-issue/SKILL.md`, that turns a one-line complaint into an issue in the pattern above. Use it for the next five.
2. Add an `AGENTS.md` to the repository with how to run the tests and what never to change, and give the agents five more issues. Fewer surprises?
3. Install the Claude GitHub app and ask `@claude` to review each pull request before you do. What did it catch that you'd have missed, and the other way round?
4. Time yourself: writing issues, waiting, reviewing. Compare with doing the five jobs yourself.
5. Try an issue that's too big on purpose. What comes back?

## Questions

For discussion. There are no right answers.

- If the agent does the coding, what is your job now?
- Which of the five would you have been faster doing yourself? Why give it to an agent anyway?
- A pull request from an agent that nobody watched: what would you need to see before you merged it on a Friday afternoon?
