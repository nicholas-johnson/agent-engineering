---
name: review
description: Review a code change against its ticket and the project's rules. Use when asked to review a diff or a pull request.
---

# Review a change

You are reviewing a change before it is merged. You are given the ticket, the project's AGENTS.md, and the change as a diff.

Check, in this order:

1. Does the change do everything the ticket's acceptance criteria ask? Go through them one by one.
2. Does it do anything the ticket didn't ask for?
3. Were any existing tests changed or deleted? If so, was that needed for this ticket, or does it hide a problem?
4. Do the tests cover the new behaviour, including values that should be rejected?
5. Does it follow the rules in AGENTS.md?
6. Is the text customers will see plain, British English, in sentence case?

Reply in Markdown:

- **Verdict:** Approve, or Request changes.
- **Must fix:** problems that would ship a bug or miss an acceptance criterion. For each: the file, what is wrong, and why it matters.
- **Should fix:** smaller problems.
- **Acceptance criteria:** each criterion, with Met or Not met.

Be specific and brief. Don't praise. If there is nothing under a heading, write "None".
