# Voice check

Demo 6 checked the launch copy for banned words and savings figures with a few lines of code. The rest of `voice.md` (plain and calm, be exact, sentence case) was left to a person. Here you'll check a piece of customer copy two ways at once: with rules in code, and with a model that reads the whole of `voice.md`. You'll paste in your own copy, or use the bad sample that comes with the script, and see what each way catches that the other misses.

From the module folder (`day-two/module-07-ai-assisted-development`):

```bash
uv run python playground/voice-check/play.py
```

Or without `uv` (set up `.venv` once at the repo root with `python3 -m venv .venv && .venv/bin/pip install -e .`):

```bash
source ../../.venv/bin/activate
python playground/voice-check/play.py
```

Needs `OPENAI_API_KEY` in `.env`. Paste the copy and press Enter on an empty line, or press Enter straight away to check the sample. It makes one call, which took about 4 seconds. The copy, both lists of problems and the model's rewrite are written to `playground/voice-check/output/check.json`.

You can also pipe the copy in. An empty line checks the sample:

```bash
printf '\n' | uv run python playground/voice-check/play.py
printf 'Good news! Warm Wake is now even smarter.\n\n' | uv run python playground/voice-check/play.py
```

---

The rules in code are the ones simple enough to write as a pattern. The banned words are read from `voice.md`, as in demo 6, and the rest are regular expressions:

```python
problems += [f'"{m}" is a savings figure' for m in re.findall(r"\d+ ?%|\d+ per ?cent", copy, re.IGNORECASE)]
# 6:30 AM, 7am, 7 p.m.
times = re.findall(r"\b\d{1,2}(?:[:.]\d{2})? ?(?:[ap]\.m\.|[ap]m\b)", copy, re.IGNORECASE)
problems += [f'"{m}" uses the degree symbol' for m in re.findall(r"\d+ ?°[CF]?", copy)]
```

The model gets the whole of `voice.md` and a schema to fill in: a list of problems, each with a quote, the rule it breaks and a fix, and then a rewrite. Here is the sample:

```text
The sample:

Introducing the all-new Warm Wake: a revolutionary, seamless way to wake up to a cosy home!
Our smart AI now lets you choose exactly when your heating kicks in, so you could save up to 20% on your gas bill.
Want it 21°C by 6:30 AM? Just head to Settings → Heating → Warm Wake and Unlock Your Perfect Morning.

Rules in code found 7:
  - "revolutionary" is on the list of words we don't use
  - "seamless" is on the list of words we don't use
  - "unlock" is on the list of words we don't use
  - "smart AI" is on the list of words we don't use
  - "20%" is a savings figure
  - "6:30 AM" uses the 12-hour clock
  - "21°C" uses the degree symbol

The model found 10:
  - "all-new": Use a plain, calm tone and focus on what the feature does for the customer, not promotional claims.
      Fix: Introducing Warm Wake:
  - "revolutionary": Do not use the word “revolutionary”.
      Fix: Remove it.
  - "seamless": Do not use the word “seamless”.
      Fix: Remove it.
  - "a cosy home!": Keep the tone calm and avoid promotional phrasing.
      Fix: a warmer home.
  - "Our smart AI": Do not use the phrase “smart AI”.
      Fix: Warm Wake
  - "so you could save up to 20% on your gas bill": Never promise a saving you can't show. Point customers to the Energy tab instead.
      Fix: Check your energy use in the Energy tab.
  - "21°C": Write temperatures as “21 degrees” in customer text, never with a symbol.
      Fix: 21 degrees
  - "6:30 AM": Use the 24-hour clock.
      Fix: 06:30
  - "Settings → Heating → Warm Wake": Use “>” for menu paths.
      Fix: Settings > Heating > Warm Wake
  - "Unlock Your Perfect Morning": Do not use “unlock”. Use sentence case for headings and buttons.
      Fix: Choose when your heating starts.

Rewritten:

Introducing Warm Wake. Choose when your heating starts, so your home reaches 21 degrees by 06:30. Go to Settings > Heating > Warm Wake. Check your energy use in the Energy tab.
```

And a quieter piece of copy, typed in, with only one thing code can catch:

```text
Rules in code found 1:
  - "7am" uses the 12-hour clock

The model found 4:
  - "Good news!": Use a plain, calm tone.
      Fix: Remove the exclamation and start with the update.
  - "even smarter": Say what a feature does for the customer, not how clever it is.
      Fix: Describe the change directly.
  - "a little earlier": Be exact about timing.
      Fix: State how many minutes earlier it starts, if known.
  - "7am": Use the 24-hour clock for times.
      Fix: Write “07:00”.

Rewritten:

Warm Wake now starts the heating earlier, so your home is warm by 07:00.
```

The model's findings and rewrites change from run to run. The rules in code don't.

## Things to notice

- **The model found everything the rules did.** All seven rule findings are among its ten. It also found what no pattern could: "all-new", the exclamation mark, the arrows in the menu path, and the title case in "Unlock Your Perfect Morning".
- **And missed what a person wouldn't.** "Kicks in" is the vague kind of phrase "be exact" is about, and the model let it through. It caught "a little earlier" in the second copy, so it knows the rule; it just didn't apply it everywhere.
- **The rewrite kept the old menu path.** "Settings > Heating > Warm Wake" follows the voice and is wrong after DOR-231, which moves Warm Wake to Schedule. The checker only had `voice.md`. A voice check can't catch a wrong fact.
- **The fix can break a rule too.** In an earlier run on the second copy, the model's fix for "7am" was "7:00". The voice guide's example is "06:30", with a leading zero. The rule in code would have passed "7:00" as well: it only looks for am and pm.
- **The rules were wrong once, too.** An earlier version of the time pattern reported "7am." with the full stop, because it allowed for "a.m." with a dot at the end. Patterns are exact, which is what makes their mistakes easy to see and fix.

## Try this

1. **A rule for menu paths.** Add a rule that catches `→` or `->` in the copy. Then one for "Settings > Heating > Warm Wake", which DOR-231 makes out of date. Which of the two belongs in a voice check?
2. **Check the launch kit.** Paste in demo 6's social post, or the reply from [write-a-skill](../write-a-skill/). Does anything get through both checks?
3. **Make it fail on purpose.** Write copy that breaks one rule in a way a pattern can't see: "twenty per cent" in words, or "21 deg". Which check catches it?
4. **Use rules to check the model.** Run `rule_problems` on the model's rewrite. Does the rewrite pass the rules? Print a warning if it doesn't.
5. **Give it the brain.** Add `product.md` and `decisions.md` to the model's instructions as well as `voice.md`. Does it catch the old menu path now? Does it start finding other things?
6. **Many pieces of copy.** Read every `.md` file in a folder (demo 6 writes five), check each one both ways, and print a table: file, rule problems, model problems.

## Questions

For discussion. There are no right answers.

- The rules in code found seven problems, and the model ten. Would you drop the rules and keep the model?
- The model let "kicks in" through once, and might not next time. Is a check you can't repeat exactly still a check?
- The rewrite reads well, and sends customers to the wrong menu. Who should catch that, and when?
- Some of the voice is taste: is "a cosy home" too much? Should a model be deciding that, or only pointing at it?

## Rabbit holes

- **Vale.** [Vale](https://vale.sh) is a prose linter that writers' teams run like a code linter: rules in YAML files, run on every change. Write a small Dormouse style for it (the banned words, the degree symbol, 12-hour times) and run it over demo 6's launch kit.
- **Check every pull request.** Put both checks in a script that fails when it finds a problem, and run it in GitHub Actions on any change to customer-facing text. The rules can block a change; decide whether the model's findings should block it too, or only leave a comment.
