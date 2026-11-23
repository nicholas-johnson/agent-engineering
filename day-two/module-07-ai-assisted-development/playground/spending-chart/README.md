# Spending chart

Build a page that charts where your money goes, from the transactions your bank lets you download. It sorts them into categories, lets you correct its guesses, and charts each category by month. It's useful, it's quick, and it's built from some of the most private data you have, so it's also a lesson in keeping data on your own computer.

**Build it in:** Claude Code. **Time:** an afternoon. **Needs:** Claude Code, and a CSV export from your bank, or a made-up one.

## Start with made-up data

Don't start with your real statement. Ask for a fake one first:

> Make a CSV called transactions.csv of three months of made-up bank transactions for one person, in the same columns as my bank's export: Date, Description, Amount. Include rent, supermarkets, takeaways, transport, subscriptions and a few refunds.

Then:

> Read transactions.csv and make a single HTML page that charts spending by category and by month. Guess each category from the description, and let me correct a guess by clicking it; remember my corrections in a file next to the page. Everything must work offline, on this computer. Nothing is sent anywhere.

## Then

- "Show the ten biggest payments, and anything that looks like a new subscription."
- "Compare this month with the average of the last three, by category."
- "Refunds are showing as spending. Fix it, and add a test with a refund in it."

## Before your real data

Ask it to check its own work:

> List every place this page loads anything from the internet, or sends anything anywhere. Then remove them all.

Open the page with your Wi-Fi off. Only then swap in your real CSV, and run it from a folder that isn't backed up somewhere you don't expect.

## Watch for

- **Where your data goes.** The page runs on your computer, but Claude Code reads the CSV to build it, which sends it to the model's provider. That's why you started with made-up data. Module 8 says more.
- **The categories.** Which guesses were wrong, and why? "AMZN MKTP" isn't obvious.
- **Libraries from the internet.** A chart library loaded from a website is the most likely thing to break "offline".

## Try this

1. Add a second account, a credit card, with its own export format.
2. Set a budget for each category and show how close you are.
3. Turn the category rules into a file you edit by hand, instead of the model's guesses.
4. Ask for the same page in Cursor, with the same prompts. Which did you prefer to work with, and why?
5. Make it a small program you run once a month that writes the page, so the model is never involved again.

## Questions

For discussion. There are no right answers.

- The finished page sends nothing anywhere, but building it did. Where's the line between the tool seeing your data and the app sending it?
- Would you trust the model's category guesses for your taxes? For a budget?
- What's the most private thing you'd let a coding agent read, and what would you need to know first?
