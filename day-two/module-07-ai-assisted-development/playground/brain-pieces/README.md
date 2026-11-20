# Brain pieces

Demo 2 gave the model the whole company brain at once, so you can't tell which file did what. Here you'll build demo 2's prototype four times, each with a different part of the brain: nothing, then `product.md`, then the decisions, then the design and voice. You'll compare what ends up on each screen, and work out which file changed what.

From the module folder (`day-two/module-07-ai-assisted-development`):

```bash
uv run python playground/brain-pieces/play.py
```

Or without `uv` (set up `.venv` once at the repo root with `python3 -m venv .venv && .venv/bin/pip install -e .`):

```bash
source ../../.venv/bin/activate
python playground/brain-pieces/play.py
```

Needs `OPENAI_API_KEY` in `.env`. It builds the four prototypes at the same time, streaming each one, and took about 25 seconds. Each prototype is written to `playground/brain-pieces/output/` twice: as HTML to open in a browser, and as a `.txt` file of the words on its screen.

---

The request is demo 2's, word for word. What changes is the list of brain files that goes into the instructions:

```python
PIECES = {
    "nothing": [],
    "product": ["product.md"],
    "product, decisions": ["product.md", "decisions.md"],
    "product, decisions, design, voice": ["product.md", "decisions.md", "design.md", "voice.md"],
}
```

To skip demo 2's spec, the prototype is built straight from the request and the brain. For each prototype the script prints the brain files, the colours in its HTML (design is the one thing the screen's words can't show), and the words on the screen:

```text
Request: Build the settings screen for the Dormouse thermostat app, where customers choose how early Warm Wake starts the heating.

=== nothing ===
  Brain files: none
  Colours: #22251F, #4D633B, #666960, #667B53, #68775D, #72756C, #74776D, #77796F ...
  On the screen:
    dormouse
    .
    Living room
    Heating schedule
    A warmer
    welcome.
    Choose how early your home should start warming up before your day begins.
    Warm Wake
    Ready when you are.
    Start heating before your scheduled time
    15 min
    Just a little
    30 min
    Balanced
    45 min
    Extra cosy
    Tomorrow morning
    6:30
    → 7:00 am
    Heating starts 30 minutes before wake-up
    Warm Wake learns how your home heats up, so it can reach your comfort temperature right on time.
    Your morning, at a glance
    Tomorrow
    6:00
    Heat starts
    7:00
    Save preferences
    Your Warm Wake preference is saved.

=== product ===
  Brain files: product.md
  Colours: #1D4934, #202A24, #244A35, #285C43, #355442, #69736C, #83AE90, #849087 ...
  On the screen:
    d
    dormouse
    My home
    Settings
    ›
    Heating
    ›
    Warm Wake
    Warm Wake
    Wake up to a warm home. Dormouse learns how long your home takes to heat and starts the heating before your schedule.
    Warm Wake
    Warm your home in time for a scheduled temperature change.
    Start heating up to
    30 minutes early
    At schedule time
    90 minutes early
    It adapts to your home.
    Warm Wake learns how quickly your home heats up and starts only as early as needed, up to your chosen limit.
    Save changes
    Look for the sunrise
    Your thermostat display shows a sunrise symbol while Warm Wake is heating ahead of a schedule period.
    Warm Wake works with your Schedule and can start up to 90 minutes early.

=== product, decisions ===
  Brain files: product.md, decisions.md
  Colours: #194A36, #202522, #245C45, #626963, #696D66, #747A75, #93B7A0, #A9B0AA ...
  On the screen:
    ◒
    dormouse
    Settings
    ›
    Schedule
    Warm Wake
    Choose how early your heating can start so your home is warm when a scheduled period begins.
    Start heating up to
    30 minutes early
    A little extra time to warm up
    60 minutes early
    A balanced start for most homes
    Recommended
    90 minutes early
    The most time to reach your target
    It learns as it goes
    Warm Wake learns how long your home takes to heat. It starts only as early as needed, up to the limit you choose. The thermostat shows a sunrise while it’s warming up.
    Done

=== product, decisions, design, voice ===
  Brain files: product.md, decisions.md, design.md, voice.md
  Colours: #1E2A44, #555B64, #716F6B, #CFC7BB, #E6DFD3, #E8743B, #FBF7F0, #FFFDF9
  On the screen:
    ‹
    Dormouse
    Settings > Schedule
    Warm Wake
    Warm Wake learns how long your home takes to heat up, then starts the heating early so it is warm when your schedule says.
    When heating starts
    Start heating
    Choose how early Warm Wake can start before a scheduled period.
    Up to 30 minutes
    Up to 60 minutes
    Up to 90 minutes
    Changes save automatically.
    ☀
    The display shows a sunrise symbol while Warm Wake is heating your home early.

Open the prototypes in playground/brain-pieces/output/ in a browser.
```

The prototypes change from run to run, so yours will look and read differently.

## Things to notice

- **Each file did a different job.** With nothing, the model invented the choices (15, 30 or 45 minutes) and a default of 30. `product.md` gave it the real limit of 90 minutes and the real menu path, Settings > Heating; it built a slider from 0 to 90 in steps of 5, set to 30. `decisions.md` moved it to Schedule, cut it to three choices and picked 60 as the default ("Recommended"), because the default should use less gas. Nobody told it 30, 60 or 90: it worked those out from "three choices" and "up to 90 minutes".
- **The colours only arrived with `design.md`.** The first three prototypes are all in greens the model chose itself. The last uses cream `#FBF7F0`, night blue `#1E2A44`, ember orange `#E8743B` and the line colour `#E6DFD3`, straight from the file. Open the HTML to see the segmented control it asks for.
- **The Save button went too.** The first two have "Save preferences" and "Save changes" buttons. `design.md` says changes save as soon as they're made, and the last prototype says "Changes save automatically." instead.
- **The voice is easier to see in what's missing.** No "A warmer welcome.", no "Extra cosy", no 12-hour "7:00 am". The last screen is plainer than the others, and in sentence case.
- **Some things never arrived.** The ticket's "How early" name isn't in any of them, because the ticket isn't in the brain. Neither is the feedback that started it all. Demo 2 had both.

## Try this

1. **The other two files.** Add `customers.md` and `glossary.md` to the last list. Does anything on the screen change? If not, what are those files for?
2. **One file at a time.** Replace `PIECES` with one entry per brain file, each on its own. Which single file changes the screen most?
3. **Break a decision.** In a copy of `decisions.md`, change "three named choices" to "a number to type". Point one entry at your copy instead. Does the prototype follow the new decision?
4. **Add the ticket.** Put `data/tickets/DOR-231.md` in the instructions as well (you'll need to read it from a different folder). Does "How early" appear? Does anything else change?
5. **Order matters?** Put `design.md` first, then last, in the same list. Does the order of the files change what you get?
6. **Count the cost.** Print `response.usage.input_tokens` for each build. How many tokens does each brain file add to every request, and is each one worth it?

## Questions

For discussion. There are no right answers.

- `decisions.md` is six short paragraphs, and it changed the default, the choices and where the setting lives. Who in your organisation writes that kind of thing down, and where does it live today?
- With only `product.md`, the model put the setting under Heating, which was true when the file was written. What happens when the brain is out of date?
- None of the prototypes is wrong for the brain it was given. If a prototype is only as good as what you wrote down, what's the most useful thing your team hasn't written down?
- A designer would pick the colours from `design.md` without being told. What else does your team know that a model would have to be told?

## Rabbit holes

- **Put the brain where the tools look.** The same files go in a Lovable project's Knowledge, a Claude Project, Cursor's rules (`.cursor/rules/`, see [Cursor's rules documentation](https://cursor.com/docs/rules)) or an [`AGENTS.md`](https://agents.md) at the top of a repository. Pick one, add the four files from the last run, and ask it for the same screen. Do you get the same prototype as here?
- **Make the brain smaller.** Write a single page that says everything the four files did for this screen, in as few words as you can. Build with it instead. What could you leave out, and what turned out to matter?
