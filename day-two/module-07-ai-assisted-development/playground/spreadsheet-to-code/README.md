# Spreadsheet to code

Every team has a spreadsheet that does real work: a quote calculator, a holiday rota, a pricing sheet with formulas nobody dares touch. Rebuild one as a small program, with tests that prove it gives exactly the same answers as the spreadsheet. It's a lesson in checks: the spreadsheet is the specification, and the tests are how you know the agent matched it.

**Build it in:** Claude Code. **Time:** a day. **Needs:** Claude Code, and a spreadsheet with formulas in it. Use a copy, or make one up, if the real one holds anything private.

## Start in plan mode

Save the spreadsheet as `quote.xlsx` in an empty folder (or describe a made-up one, below). Start `claude` there, and switch to plan mode:

> quote.xlsx works out a price for a job from the hours, materials, the customer type and a discount table. Read every formula in it. Plan a small program that does the same calculation, with a test for every row of the examples sheet that checks the program gives exactly the spreadsheet's answer, to the penny. List anything in the spreadsheet you don't understand before you plan.

No spreadsheet to hand? Ask it to make one: "Make a quote calculator spreadsheet for a window cleaner: price by number of windows, floors and customer type, with a discount table and ten examples."

## Then

- "Build it. Run the tests after every change."
- "Find three inputs where the spreadsheet does something odd, like a negative discount, and write tests that show it."
- "Add a command so I can type the inputs and get a quote."

## Make the tests run every time

Add hooks, so the tests run after every edit whether Claude remembers or not, and it has to ask before changing a test:

> Add a PostToolUse hook that runs the tests after every Edit or Write and shows Claude any failures, and a PreToolUse hook that blocks edits to the tests folder until I agree.

## Watch for

- **Formulas it misread.** Rounding, dates and percentages are where the answers drift by a penny.
- **Tests that bend.** If a test fails, did it fix the code or change the test? The hook should make it ask.
- **The odd cases.** Were they bugs in the spreadsheet? Who decides whether the program copies them?

## Try this

1. Add an agent file, `.claude/agents/penny-check.md`, that compares the program with the spreadsheet on 100 random inputs and reports every difference.
2. Ask for a short explanation of the calculation for the people who use the spreadsheet today, with no code in it.
3. Turn the program into a one-page web form for the team.
4. Do the same with a second spreadsheet that has macros in it. What's harder?
5. Hand it to the spreadsheet's owner and ask them to try to break it.

## Questions

For discussion. There are no right answers.

- The spreadsheet had a bug, and the program copies it exactly. Is that a success?
- Who in your team would have to agree before the program replaced the spreadsheet?
- A spreadsheet is something everyone can open and change. What does the team lose when it becomes code?
