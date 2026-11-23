# First contribution

Make your first contribution to an open-source project you use. Find a small issue labelled "good first issue", learn the code in Cursor's Ask mode, plan the change in Plan mode, then build it, test it and open a pull request that follows the project's own rules. It's the real test of an AI editor: a codebase you didn't write, conventions you didn't choose, and maintainers who will read every line.

**Build it in:** Cursor. **Time:** a day or two. **Needs:** Cursor, a GitHub account, and a project with open "good first issue" labels.

## Start in Ask mode

Fork the project, clone your fork, open it in Cursor, and choose Ask mode:

> Explain how this project is organised, how to set it up, and how to run its tests. Then read CONTRIBUTING.md and tell me its rules in five bullet points.

Get the tests passing on your machine before you change anything. Then paste the issue:

> Here's the issue I want to fix: (paste it). Which files would I need to change, and what tests already cover this area?

## Then, in Plan mode

> Plan the smallest change that fixes this issue, in the project's existing style, with a test that fails before the fix and passes after. Ask me anything the issue doesn't say.

Read the plan against `CONTRIBUTING.md`. Then build it, run the tests, and read every line of the diff before you commit.

## Watch for

- **Style.** Does the change look like the code around it, or like the model's own habits?
- **Size.** Maintainers like small changes. Did it touch anything the issue didn't ask about?
- **Disclosure.** Some projects ask you to say when AI helped, and a few don't accept AI-written code at all. Read their policy before you open the pull request.

## Try this

1. Turn `CONTRIBUTING.md` into a Cursor rule, `.cursor/rules/contributing.mdc`, set to always apply, so every conversation follows it. Keep it out of your pull request.
2. Before you open the pull request, ask in Ask mode: "What would a maintainer push back on in this change?"
3. Write the pull request description yourself, then ask Cursor to improve it. Which is better?
4. When a maintainer asks for changes, paste their comment into Agent mode and make them. Did it understand what they meant?
5. Pick a second issue, harder than the first, and do it with Claude Code instead.

## Questions

For discussion. There are no right answers.

- If an AI wrote most of your contribution, whose contribution is it?
- Maintainers now get many AI-written pull requests. What would make yours easy to review?
- You learned the codebase in Ask mode. How much of it do you understand now, and does that matter?
