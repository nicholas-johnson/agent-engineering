# Playground

Things to try between exercises, in the tools themselves. You'll write an agent file and a skill for Claude Code, add hooks that run the tests after every edit, give Cursor the company's rules, hunt a bug with Debug mode, add a tool to the company-brain server, and give the same ticket to two tools to compare what comes back. None of them are required, and there are no right answers.

Then leave Dormouse behind: [Projects to build](#projects-to-build), below, has ideas for building something of your own in each tool, from a pub quiz to an MCP server for your team.

Most folders are exercises in a tool: a README with the steps, and the files to drop into the project. Three have a Python script. Each one builds what it needs from `data/`, so you don't have to run the demos first.

The exercises work on a copy of the Dormouse project, outside the course repository so the tools can change it. From the module folder (`day-two/module-07-ai-assisted-development`):

```bash
MODULE="$PWD"
cp -R data/project ~/dormouse-dashboard && cd ~/dormouse-dashboard && git init -q && git add . && git commit -qm "Start"
```

To start again: `git reset --hard && git clean -fd` in `~/dormouse-dashboard`.

The Python scripts run from the module folder:

```bash
uv run python playground/brain-tools/play.py
```

Or without `uv` (set up `.venv` once at the repo root with `python3 -m venv .venv && .venv/bin/pip install -e .`):

```bash
source ../../.venv/bin/activate
python playground/brain-tools/play.py
```

| Folder | What it's about | Needs |
|--------|-----------------|-------|
| [agent-files](agent-files/) | Write a subagent for Claude Code, and run it alongside the module's three | Claude Code |
| [write-a-skill](write-a-skill/) | A skill runner, with a new skill to edit: a support reply in the Dormouse voice | `OPENAI_API_KEY`; Claude Code or Cursor to use it there |
| [hooks](hooks/) | Make Claude Code run the tests after every edit, and ask before it changes a test | Claude Code |
| [cursor-rules](cursor-rules/) | Turn the company brain into Cursor rules, and see what changes | Cursor |
| [debug-hunt](debug-hunt/) | A customer's saved home that shows a bug. Find it with Debug mode | Cursor (or Claude Code) |
| [brain-tools](brain-tools/) | Add a tool to the company-brain MCP server, and try it with no API key | Nothing; Claude Code or Cursor to attach it |
| [same-ticket](same-ticket/) | Give one ticket to two tools, and compare the changes | Two of Claude Code, Cursor and a cloud agent |

Everything a script writes goes into an `output/` folder next to it.

## Projects to build

The folders above all work on Dormouse. These don't: they're things to build for yourself, your team or your friends, to find out what each tool is like on a problem you care about. Pick one that sounds fun, not one that sounds useful. Each has a first prompt to get going. Expect to change it after the first answer.

A few habits help in every tool:

- **Say who it's for and what they do**, not what the screens look like. Let the tool propose the screens, then change them.
- **Plan first** for anything bigger than an afternoon, and read the plan before you approve it.
- **Say how to check it**: "Run the tests", "Open it in a browser and try it on a phone-sized screen".
- **Keep your own data private.** Anything you paste or attach goes to the tool's provider (Module 8). Use made-up data until you know where it goes.

### In Lovable: an app other people can use

No code to write. The interesting part is the backend: sign-in, a database, and who can see what.

1. **A pub quiz night.** The host shows questions on a big screen; players join on their phones with a code and answer against the clock; scores update live.
   > Build a quiz app for a pub quiz night. The host makes a quiz of picture and text questions, then runs it on a big screen. Players join on their phones with a four-letter code, answer each question before a timer runs out, and see a live leaderboard.
2. **A booking page for a club.** Four tennis courts (or meeting rooms, or allotment tools), members book an hour, nobody can double-book.
   > Build a booking page for a tennis club with four courts. Members sign in and book a court for an hour, up to a week ahead, at most two bookings each. The club secretary can block courts for matches.

   Watch for: two people booking the same court at the same moment. Ask it how it stops that.
3. **A family chores board.** Chores with points, a weekly leaderboard, and rewards the parents set.
   > Build a chores board for a family of five. Parents add chores with points; children tick them off with a photo; at the end of the week the points turn into rewards the parents choose.
4. **An RSVP site for an event.** A wedding, a reunion or a conference: invitations by link, meal choices, dietary needs, and a spreadsheet export for the caterer.
5. **A recipe box.** Paste a recipe from anywhere; it tidies it up, scales it to any number of people, and builds a shopping list across the week's meals.
6. **A portfolio from your CV.** Paste your CV in Plan mode and ask for a one-page site. Then use the preview toolbar to change it by pointing, not typing.

### In Claude Code: tools that run on your own computer

Claude Code is at its best on things that live in files and folders: scripts, small programs and the projects you already have.

1. **Tidy a folder of photos.** Rename every photo by the date it was taken, sort them into a folder per month, and find the duplicates.
   > Write a Python script that renames the photos in a folder by the date they were taken, moves them into a folder per month, and lists likely duplicates. It must never delete anything, and it should print what it would do unless I pass --apply. Test it on the sample photos in test-photos/.

   Watch for: anything that moves or deletes files. Use plan mode, and try it on a copy first.
2. **A game in one HTML file.** A word game, a puzzle or a small arcade game of your own design, that runs in any browser with no install.
   > Make a two-player word game in a single HTML file: each player gets seven letters, and they take turns making words for points. Keep score, and work on a phone.
3. **Your spending, as a chart.** Export a few months of transactions from your bank as a CSV, and build a local page that groups and charts them.
   > Read transactions.csv and make a single HTML page that charts my spending by category and by month. Guess the categories from the descriptions, and let me correct them. Everything must stay on this computer.
4. **A team bot.** A Slack or Discord bot that answers questions from your team's FAQ, with Module 6's retrieval behind it.
5. **A browser extension.** Something small that changes pages you visit: reading time on articles, a word count on any text box, or a button that copies a page as Markdown.
6. **A spreadsheet, rebuilt.** Take a spreadsheet that does real work in your team (a quote calculator, a rota) and turn it into a small Python program with tests that prove it gives the same answers as the spreadsheet.
7. **A project of your own, explained.** Point it at code you wrote years ago: "Explain this project to someone who's joining it. Then write the README it should have had."

### In Cursor: code that already exists

Cursor is at its best next to code you're reading and changing, including code that isn't yours.

1. **Your first open-source contribution.** Find a project you use with a "good first issue". Learn the code in Ask mode, plan the change in Plan mode, then follow the project's own contributing guide.
   > (Ask mode) Explain how this project is organised, how to run its tests, and which files I'd need to change for this issue: (paste the issue)
2. **Tests for code nobody tested.** Pick an old project with no tests. Ask for tests that describe what the code does now, before you change anything.
   > Write tests that pin down what this module does today, including its odd cases. Don't change the module. If something looks like a bug, write a test for the current behaviour and tell me about it.
3. **Bring something old up to date.** A Python 2 script, a jQuery page, a project whose dependencies are five years old. Plan the upgrade, then use Debug mode on whatever breaks.
4. **Take a Lovable app further.** Sync one of your Lovable apps to GitHub, open it in Cursor, and add the feature Lovable struggled with.
5. **Hunt a bug you've been ignoring.** Every project has one. Describe it to Debug mode the way a user reported it, and let it ask you to reproduce it.

### With a cloud agent: work that happens while you're away

1. **A backlog afternoon.** Write five small, clear issues on one of your repositories: a typo, a missing test, a confusing error message, a docs gap, a small feature. Give each to a cloud agent, go and do something else, then review five pull requests.
2. **The README that was never written.** Give an agent a repository with no documentation: "Write a README that explains what this does, how to install it and how to run the tests. Check every command works before you write it down."
3. **A dependency upgrade.** "Update every dependency to its latest version, one at a time, running the tests after each. Stop and report the first one that breaks something."

Watch for: what each agent did when the issue was unclear. A person would have asked; did it guess?

### With MCP: a brain of your own

The company-brain server is 47 lines. Write one for something you know.

1. **Your team's knowledge.** Your team's decisions, glossary and how-tos, as a server everyone attaches to their tools. Start by copying `brain-tools/server.py`.
2. **A spreadsheet you look things up in.** Your reading list, a product catalogue, the office plant-watering rota: a CSV behind two or three tools, attached to the Claude app.
   > (In the Claude app) What should I read next? I liked the last three books I gave five stars to.
3. **A public API.** Train times, the weather, a library catalogue, a football league table: like Module 3's weather server, but for something you check every day.
4. **This course.** The course's modules, as a brain. Attach it and ask: "Which module explains why a model makes things up, and what's the demo?"

### Put them together

1. **From prototype to product.** Build an app in Lovable, sync it to GitHub, add a feature in Cursor, hand the next issue to a cloud agent, and review its pull request with `@claude`. Write down where each tool was best.
2. **Module 6 as an app.** A chat page in front of Module 6's document search, built in Claude Code or Cursor, so customers can ask the Dormouse manual questions and see the sources. Then think about what Module 8 says it needs before it goes on the internet.
3. **Module 1 in a browser.** Module 1's word-pair model as a web page: type the start of a sentence, and watch it complete it one word at a time, with the choices it was weighing.
