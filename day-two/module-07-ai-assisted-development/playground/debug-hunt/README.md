# Debug hunt

The module's Debug mode demo fixes one bug. Here's another. A customer chose Sunday as the first day of the week, and the dashboard keeps showing Monday. You'll set up a fresh copy of the project with their saved home, then find the cause with Cursor's Debug mode, or with Claude Code, from evidence rather than guesswork.

From the module folder (`day-two/module-07-ai-assisted-development`):

```bash
uv run python playground/debug-hunt/play.py
```

Or without `uv` (set up `.venv` once at the repo root with `python3 -m venv .venv && .venv/bin/pip install -e .`):

```bash
source ../../.venv/bin/activate
python playground/debug-hunt/play.py
```

It needs nothing else, and makes a fresh copy every time you run it, in `playground/debug-hunt/output/project`. Open that folder in Cursor (or start `claude` in it).

---

The script copies `data/project`, adds the customer's saved home as `homes/house-7.json`, and prints what support sent:

```text
Bug report from support:

  A customer at 7 Orchard Close chose Sunday for "Week starts on" in the app.
  On the web dashboard's settings page it shows Monday. They changed it back to
  Sunday in the app twice, and the dashboard still shows Monday.

  To reproduce, from the project folder:
    python -m dormouse homes/house-7.json
  then open homes/house-7.html in a browser.

A fresh copy of the project is in playground/debug-hunt/output/project.
Open it in Cursor, choose Debug mode, and paste the bug report.
```

Reproducing it shows the page with nothing selected, which a browser draws as Monday:

```text
<select name="week_starts_on"><option>Monday</option><option>Sunday</option></select>
```

Paste the bug report into Debug mode. It should list a few hypotheses, add logging, ask you to run the command and reload the page, then read what the logging caught.

_Output to come: a recorded Debug mode session._

## Things to notice

- **The code isn't wrong for any value it allows.** `settings.check` only accepts "Monday" or "Sunday". The bug is in what was saved before that check existed. Does Debug mode find the value, or the line?
- **Two fixes.** Change the page to compare without case, or clean the saved value when a home is loaded. Which did it choose, and did it ask?
- **The other bug is still there.** This copy still has the heat-up rate bug from the demo: 7 Orchard Close's heating comes on 90 minutes early too. Did Debug mode notice, or stay on the ticket?

## Try this

1. **No Debug mode.** Reset the copy (run the script again) and paste the report into Agent mode. Does it find the same cause, as fast, and is it as sure?
2. **Claude Code.** Do the same in Claude Code. Ask it to prove the cause before changing anything.
3. **A test first.** Ask for a failing test that shows the bug, before any fix. Then the fix.
4. **Your own bug.** Change one line of the project to break it, say `MAX_MINUTES_EARLY` in a way the tests don't catch, write a bug report as a customer would, and give it to a partner to find.
5. **Both bugs.** Give Debug mode both reports, the week and DOR-234, in one go. Does it keep them apart?

## Questions

For discussion. There are no right answers.

- The bug lives in old data, not new code. Who on your team would have caught it, and how?
- Debug mode adds logging to your code and takes it out again. What would you want to check before you trust that it's all gone?
- An agent that can read logs from a running app can read whatever is in them. What should never be logged?
- Is a fix that's right for this customer the right fix for every customer saved before the check existed?

## Further reading

- **Cursor. "Debug Mode." _Cursor documentation_.** [cursor.com/docs/agent/debug-mode](https://cursor.com/docs/agent/debug-mode). The steps Debug mode follows. Read the part on reproducing a bug, and why it asks you to do it rather than guessing from the code.
