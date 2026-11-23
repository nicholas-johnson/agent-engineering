# Same ticket, two tools

The module shows each tool on its own. Here you'll give the same ticket to two of them and compare what comes back: the files they changed, the tests they wrote, the words they chose, and the decisions they made that the ticket didn't.

From the module folder (`day-two/module-07-ai-assisted-development`), make two copies of the project:

```bash
MODULE="$PWD"
for tool in first second; do
  cp -R data/project ~/dormouse-$tool && (cd ~/dormouse-$tool && git init -q && git add . && git commit -qm "Start")
done
```

Needs two of: Claude Code, Cursor, or a cloud agent (which needs the project on GitHub, as in `demo/05_cloud_agents.md`). Open `~/dormouse-first` in one tool and `~/dormouse-second` in the other. Paste the same ticket, `data/tickets/DOR-233.md` (let customers choose how long Boost lasts), into each, in the same mode. When both have finished:

```bash
cd ~/dormouse-first && git add -A && git diff --cached --stat
cd ~/dormouse-second && git add -A && git diff --cached --stat
diff -ru --exclude=.git ~/dormouse-first ~/dormouse-second
```

---

DOR-233 is small, but it leaves real choices open: what the setting is called in the code, whether it's stored as minutes or as a name, how the three choices are drawn on the page, which tests change, and what an existing customer without the setting gets. Two tools, or one tool twice, rarely make all the same ones.

## Things to notice

- **Same tests passing, different code.** Both will probably finish with every test passing. Passing tests say each one did what it meant to, not that they meant the same thing.
- **Labels.** The ticket names the choices "30 minutes, 1 hour and 2 hours". Did both use those words exactly?
- **Saved homes.** Run `python -m dormouse homes/flat-3b.json` in each copy. Flat 3B was saved before Boost length existed.

## Try this

1. **One tool twice.** Give the ticket to the same tool in both copies. Are the two runs more alike than two tools?
2. **Plan both.** Repeat in plan mode in both tools. Compare the plans before you build. Do the differences show up there first?
3. **With the brain.** Attach the company-brain server (`demo/06_company_brain.md`) to both, and repeat. Do the two get closer together?
4. **Score them.** Use the `ticket-checker` agent from `data/agents/` to check both changes against the ticket. Do you agree with its scores?
5. **Merge them.** Take the best parts of each into one change by hand. How long did that take compared with writing it yourself?

## Questions

For discussion. There are no right answers.

- If two tools make different, reasonable choices, whose job was it to make that choice?
- Would you rather a tool that's predictable, or one that's sometimes brilliant?
- What would your team need to see before it standardised on one tool?

## Further reading

- **Jimenez, C. E., Yang, J., Wettig, A., Yao, S., Pei, K., Press, O. & Narasimhan, K. (2024). "SWE-bench: Can Language Models Resolve Real-World GitHub Issues?" _ICLR 2024_.** [arXiv:2310.06770](https://arxiv.org/abs/2310.06770). How coding agents are usually compared: real issues, checked by tests. Read how a task counts as solved, and think about what that leaves out compared with what you just did.
