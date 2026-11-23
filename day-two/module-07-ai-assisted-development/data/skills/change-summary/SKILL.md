---
name: change-summary
description: Summarise a code change in plain English for people who don't read code, and write the comment for its ticket. Use when a change is merged.
---

# Summarise a change

Work from the ticket and the change that implements it. If you weren't given them, ask which ticket it is, and read the change with `git diff`. Write for support, product and marketing, who don't read code.

Reply in Markdown with two parts:

## What changed

Three to six short bullet points: what customers will notice, where they will find it, and what the default is. Then one line on anything that has NOT changed that people might ask about.

## Ticket comment

A comment for the ticket, of no more than four lines: what was done, how it was tested, and anything left to do.

No code, file names or function names in "What changed".
