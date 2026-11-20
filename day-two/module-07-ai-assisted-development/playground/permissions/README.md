# Permissions

Demo 3's coding agent changed files as soon as it decided to. Claude Code and Cursor don't, unless you let them: they show you each change and wait. Here you'll be the developer at that prompt. The agent gets demo 3's vague request, and before every file it writes you see the diff of that one change and answer `y` or `n`. Say `n`, type a reason, and the agent gets your reason back instead of a written file. You'll see whether a few words at the right moment steer it as well as a ticket does.

From the module folder (`day-two/module-07-ai-assisted-development`):

```bash
uv run python playground/permissions/play.py
```

Or without `uv` (set up `.venv` once at the repo root with `python3 -m venv .venv && .venv/bin/pip install -e .`):

```bash
source ../../.venv/bin/activate
python playground/permissions/play.py
```

Needs `OPENAI_API_KEY` in `.env`. The agent works on a fresh copy of `data/project` in `playground/permissions/output/project`. The run below took about 50 seconds, plus however long you spend reading. Every change it made is in `output/changes.diff`, and the conversation and your answers are in `output/transcript.json`.

You can also pipe the answers in. This refuses the first change with a reason, then allows the rest:

```bash
{ printf 'n\nThree choices only: 30, 60 or 90 minutes, with 60 as the default. And it belongs under Schedule, not Heating.\n'; yes y | head -30; } | uv run python playground/permissions/play.py
```

---

It's demo 3's agent with one change, in `run_tool`. Before `write_file` touches the disk, the developer is asked:

```python
def ask_permission(path, content):
    ...
    if input(f"\n  Allow this change to {path}? (y/n) ").strip().lower() == "y":
        return None
    reason = input("  Why not? ").strip()
    return f"The developer refused this change: {reason}"
```

A refusal goes back to the model as the tool's result, like any other. The agent never sees the file change, only your words. This run refused the first change and allowed the rest. The answers typed at the prompts are shown as they'd appear in a terminal; five of the eight changes are left out in the middle:

```text
Request: Let customers choose how early Warm Wake starts the heating.

  list_files 
  read_file  dormouse/settings.py
  read_file  dormouse/warm_wake.py
  read_file  dormouse/pages.py
  list_files 
  read_file  tests/test_settings.py
  read_file  tests/test_warm_wake.py
  read_file  tests/test_pages.py
  read_file  README.md
  read_file  AGENTS.md
  read_file  CLAUDE.md
  write_file dormouse/settings.py
      --- a/dormouse/settings.py
      +++ b/dormouse/settings.py
      @@ -3,6 +3,7 @@
       DEFAULTS = {
           "boost_temperature": 21.0,
           "warm_wake": True,
      +    "warm_wake_minutes": 90,
           "week_starts_on": "Monday",
           "away_temperature": 16.0,
           "geofencing": False,
      @@ -27,6 +28,9 @@
           elif name in ("warm_wake", "geofencing"):
               if not isinstance(value, bool):
                   raise ValueError(f"{name} must be on or off")
      +    elif name == "warm_wake_minutes":
      +        if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= 90:
      +            raise ValueError("warm_wake_minutes must be from 0 to 90 minutes")
           elif name == "week_starts_on":
               if value not in ("Monday", "Sunday"):
                   raise ValueError("week_starts_on must be Monday or Sunday")

  Allow this change to dormouse/settings.py? (y/n) n
  Why not? Three choices only: 30, 60 or 90 minutes, with 60 as the default. And it belongs under Schedule, not Heating.
  write_file dormouse/settings.py
      --- a/dormouse/settings.py
      +++ b/dormouse/settings.py
      @@ -3,6 +3,7 @@
       DEFAULTS = {
           "boost_temperature": 21.0,
           "warm_wake": True,
      +    "warm_wake_minutes": 60,
           "week_starts_on": "Monday",
           "away_temperature": 16.0,
           "geofencing": False,
      @@ -27,6 +28,9 @@
           elif name in ("warm_wake", "geofencing"):
               if not isinstance(value, bool):
                   raise ValueError(f"{name} must be on or off")
      +    elif name == "warm_wake_minutes":
      +        if isinstance(value, bool) or value not in (30, 60, 90):
      +            raise ValueError("warm_wake_minutes must be 30, 60 or 90 minutes")
           elif name == "week_starts_on":
               if value not in ("Monday", "Sunday"):
                   raise ValueError("week_starts_on must be Monday or Sunday")

  Allow this change to dormouse/settings.py? (y/n) y
  write_file dormouse/warm_wake.py
  ...

  Allow this change to dormouse/settings.py? (y/n) y
  run_tests  

Agent: Added a Warm Wake start-time setting, defaulting to 60 minutes, with choices of 30, 60 or 90 minutes. It appears under Schedule and caps how early Warm Wake starts the heating.

Updated settings, Warm Wake and settings-page tests for the new behaviour. All 19 tests pass.

You allowed 7 changes and refused 1.
Tests: Ran 19 tests, OK
The changes are in playground/permissions/output/changes.diff
```

The agent decides differently from run to run, so you'll be asked about different changes.

## Things to notice

- **One refusal did most of a ticket's work.** Left alone, the agent chose any number of minutes from 0 to 90, with a default of 90, like demo 3's. One sentence at the prompt, and its very next attempt had 30, 60 or 90 with a default of 60. Every later change followed the reason too: the page offers the three choices, and the tests check them.
- **"It" was read one way.** The reason said "it belongs under Schedule". The agent moved its new setting there and left Warm Wake itself under Heating, with the old test that checks it's there. DOR-231 moves both. A reason is short, and short is easy to read two ways.
- **It named things for itself.** The setting is `warm_wake_minutes`, labelled "Warm Wake start time" on the page. The ticket calls it How early. Nothing at the prompt said so, so nothing changed it.
- **Saying yes got easy.** After the refusal, this run said `y` seven times. One of those changes edited an existing test, `test_never_more_than_90_minutes_early`, to set the new setting to 90 so it still passes. The project's `AGENTS.md` asks agents to say which tests they changed and why. The summary says only "Updated ... tests for the new behaviour". Reading every diff is the whole point of the prompt, and it's the first thing people stop doing.
- **The agent read `AGENTS.md` itself.** It was already in its instructions. Agents often check the file anyway; it costs a step and a few hundred tokens.

## Try this

1. **Refuse with no reason.** Answer `n`, then press Enter at "Why not?". What does the agent do with "The developer refused this change: " and nothing after it?
2. **Steer harder.** Refuse the first change with the whole of DOR-231's "What we're building" list pasted in as the reason. How close does it get to demo 4's result?
3. **Allow by file.** Add a constant like `ALWAYS_ALLOW = ["tests/"]`, and skip the prompt for paths that start with one of them. Claude Code's permission rules do the same for tools and paths. Which folders would you trust it with?
4. **Ask before running, too.** `run_tests` runs code the agent wrote. Ask before that as well. Is it more annoying, or more reassuring?
5. **Edit instead of refusing.** Add a third answer, `e`, that opens the proposed content in your editor (save it to a file and wait for Enter), then writes your version and tells the model what you changed.
6. **Count the cost of a refusal.** Print `response.usage.input_tokens` on every call. How many tokens did the refused attempt cost, and how many did the agent spend reading before its first write?

## Questions

For discussion. There are no right answers.

- One sentence at the right moment fixed the default and the choices. Was that cheaper than writing the ticket first, or did it only work because you already knew what the ticket would say?
- The agent took "it" to mean its new setting, not Warm Wake. Whose mistake was that?
- After a few good changes, most people start pressing `y` without reading. What would make you keep reading, or should the tool stop asking about some changes?
- Claude Code can be told to stop asking altogether. When, if ever, would you let it?

## Further reading

- **Anthropic. "Configure permissions." _Claude Code documentation_.** [code.claude.com/docs/en/permissions](https://code.claude.com/docs/en/permissions). How the real prompt works: allow, ask and deny rules for tools and paths, and the permission modes. Compare its rules with what this script asks about.

## Rabbit holes

- **Do it with a hook.** Claude Code runs [hooks](https://code.claude.com/docs/en/hooks), your own scripts, before and after each tool call. Write a `PreToolUse` hook that refuses any edit to an existing test file, with a reason the model can read. Then let Claude Code loose on DOR-231 and see whether it works around you.
- **Watch someone else's agent.** Turn on permission prompts in Cursor or Claude Code and give it demo 3's request in a copy of `data/project` (see `demo/LIVE.md`). Count how many prompts you see, and how many you'd have refused if you'd read them carefully.
