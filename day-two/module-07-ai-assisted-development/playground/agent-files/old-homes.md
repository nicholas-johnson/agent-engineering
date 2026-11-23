---
name: old-homes
description: Checks that a change still works for homes saved before it, whose settings may be missing a new setting or hold an old value. Use after a change to settings, before it is committed.
tools: Read, Grep, Glob, Bash
model: sonnet
---

Homes keep the settings they saved, sometimes for years. A change that adds a setting, or changes the values one allows, has to work for a home saved before it.

1. Run `git diff` and list every setting the change adds or changes.
2. For each one, find every place the code reads it. Would a home saved before the change, without the setting or with an old value, crash or do the wrong thing?
3. Prove it: copy a file in `homes/` to a new name, take out the new setting or put in an old value, and run `python -m dormouse` on the copy. Delete the copy afterwards.

Reply with each setting, what an old home would get, and whether that is right. Change no files except your temporary copies.
