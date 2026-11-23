# Run sheet: Cursor

The live demo for section 4. Cursor is a code editor built around an agent, with a mode for each kind of job: Ask, Agent, Plan and Debug, plus `/multitask` to run several agents at once. Try it once before the session: agents do something different every time.

You need Cursor and an account. The free plan is limited, so use a paid one for the whole run. Checked against Cursor's documentation on 23 November 2026.

## Set up

Copy the project somewhere outside the course repository, so Cursor can change it and you can use git. From the module folder:

```bash
cp -R data/project ~/dormouse-dashboard && cd ~/dormouse-dashboard && git init -q && git add . && git commit -qm "Start"
```

Open `~/dormouse-dashboard` in Cursor, then open the agent panel with Cmd+I (Ctrl+I on Windows). Shift+Tab cycles through the modes, or use the mode picker under the input. Each mode starts with a fresh context.

To start again between steps:

```bash
git reset --hard && git clean -fd
```

## 1. Ask mode

1. Choose **Ask** and type: "How does Warm Wake decide when to switch the heating on?"

Point out: Ask mode can read the code but can't change it, so it's a safe way into code you don't know. It also read `AGENTS.md` without being asked.

## 2. Agent mode

1. Choose **Agent** and paste the contents of `data/tickets/DOR-232.md` (let the week start on Saturday).
2. Let it work. Approve the commands it wants to run, such as the tests.
3. Read the changes in the editor before you keep them.

Point out: it reads, edits several files and runs the tests, the same loop as Claude Code, next to the code you are reading.

## 3. Plan mode

1. Start again. Choose **Plan** and paste the contents of `data/tickets/DOR-231.md` (let customers choose how early Warm Wake starts).
2. Answer its questions. Read the plan, edit one step, then build it.

Point out: a plan is a dozen lines to read, and changing it costs nothing. The plan opens like a file you can edit, and **Save to workspace** keeps it in the project. For a plan with independent steps, **Build in Parallel** gives each step its own agent.

## 4. Debug mode

1. Start again. Choose **Debug** and paste the contents of `data/tickets/DOR-234.md` (Warm Wake starts 90 minutes early in small homes).
2. It lists a few hypotheses, adds logging to the code, and asks you to reproduce the bug. Run what it asks, which will be something like:

   ```bash
   python -m dormouse homes/flat-3b.json
   ```

3. It reads the logs and makes a small fix. Run the command again: Flat 3B's heating should now come on at 06:36. When you confirm it works, it removes the logging.

Point out: it worked from evidence, the values in the running code, not from reading alone. The bug is real: `learned_rate` returns degrees a minute, not degrees an hour, and none of the 16 tests check it.

## 5. Multitask

1. Start again. Open the Agents Window: Cmd+Shift+P (Ctrl+Shift+P), then **Open Agents Window**.
2. Type `/multitask`, then paste the contents of `data/tickets/DOR-232.md` and `data/tickets/DOR-233.md` (let Boost last 30 minutes, 1 hour or 2 hours).
3. Watch two agents work at once. Read each change when they finish.

Point out: two tickets in the time of one, but two diffs to read. Both touch `settings.py` and `pages.py`, so look at how they were combined.
