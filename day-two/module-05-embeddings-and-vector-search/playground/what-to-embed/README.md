# What to embed

Before you can search by meaning, you have to decide what text stands for each script. You'll embed the library three ways and see where the right script lands for twenty requests.

From the module folder (`day-two/module-05-embeddings-and-vector-search`):

```bash
uv run python playground/what-to-embed/play.py
```

Or without `uv` (set up `.venv` once at the repo root with `python3 -m venv .venv && .venv/bin/pip install -e .`):

```bash
source ../../.venv/bin/activate
python playground/what-to-embed/play.py
```

Needs `OPENAI_API_KEY` in `.env`. The first run embeds the library three times (about 3,000 texts) and keeps the vectors in `playground/what-to-embed/output/vectors.db`, so later runs take a couple of seconds. The rank of the right script, and the top five for each way, are written to `playground/what-to-embed/output/ranks.json`.

---

Demo 2 embedded each script's title and expected result, and left out the preconditions and steps, because the steps mostly say "open the app, tap this". This playground tests that choice. Each script is turned into text three ways:

```python
WAYS = {"full text": full_text, "title": title, "title + expected": title_and_expected}
```

- **full text**: title, preconditions, steps and expected result, as demo 1's keyword search uses
- **title**: the title alone
- **title + expected**: what the demos embed

Then every request in `data/requests.json` is compared with all 1,000 scripts, and the table shows where the best right script lands: 1 means first. The module's own request comes first, on its own.

```text
Where the right script lands (1 = first), searching all 1,000 scripts:

  Request                                                      full text             title  title + expected
  Customers can't sign in after resetting their p...                   4                 1                 1

  Customer changed the temperature while the ther...                   5                 6                 2
  Can someone still see the household's details o...                   1                 1                 1
  The same thermostat shows up twice in the home ...                   1                 1                 1
  Energy use for just the bedroom, not the whole ...                  17               255               569
  Did last night's software update keep my heatin...                  13                98                 4
  Holding the knob down for a while makes the tem...                   1               130                 9
  What happens when someone tries to add more roo...                   5                 6                 9
  A family member who isn't the owner managed to ...                  12                14                10
  Someone taken off the household can still see t...                   1                98                14
  A partially sighted user can't read the schedul...                   1                 3                 3
  Closed the app halfway through updating the the...                   5                38                 1
  Screen reader users can't tell which room's con...                   8                29                16
  A thermostat that hasn't been given a room is c...                  12                 3                 2
  The thermostat says 21 but the room feels colde...                   2                 5                 1
  Customer sees E-217 on the thermostat                                1                 1                 1
  E-221 showing on the display                                         1                 2                 1
  E-104 came up while setting up a new thermostat                      1                 1                 1
  E-101 on the screen after moving house                               2                 5                 1
  Display says E-312                                                   1                 2                 1
  E-510 after last night's update                                      1                 1                 1

  A right script in the top 5, of 20                                  15                11                14
```

A tie counts as a draw. TS-1042 and its iOS twin TS-1187 have exactly the same text, so they share first place.

## Things to notice

- **On the module's request, the module's choice wins.** With title + expected, TS-1042 "Log in with the new password after a password reset" comes first. With the full text it comes fourth. In `output/ranks.json`, the three ahead of it are TS-1047 "Preserve sign-in email after a password error", TS-1877 "Request a password reset for a registered email" and TS-1437 "Reject an incorrect password". Their steps are full of emails and passwords too, so they look like it.
- **On twenty requests, the full text wins, just.** 15 against 14. Look at "Holding the knob down for a while makes the temperature jump". Its script, TS-1958, is titled "Check dial operation after a long press", and the request's meaning is in the steps: "Press and hold the dial for five seconds", and check the target hasn't changed. With the full text it comes first; without the steps, ninth. The steps aren't always "open the app, tap".
- **The title alone is worst** (11). A dozen words isn't much to go on.
- **"Energy use for just the bedroom"** lands 17th, 255th and 569th. Its script, TS-1568, is "View report for a selected zone". The customer says bedroom; the script says zone. No choice of text closes a gap like that.
- **The platform filter hides most of the difference.** With `FILTER_BY_PLATFORM = True`, so each request is only compared with its own platform's scripts as in demo 4, the counts are 18, 14 and 18. That 18 is demo 4's vector search.

## Try this

1. **Steps alone.** Add a fourth way that embeds only the steps. How far behind does it come?
2. **Name the feature.** Add a way that puts the component first: `f"{script['component']}: {script['title']}. {script['expected']}"`. Does it help "Energy use for just the bedroom"?
3. **Different cut-offs.** Set `TOP = 1`, then `TOP = 10`. Which way is best at putting the right script first?
4. **Your own requests.** Add five requests to the list, with the IDs of the scripts that answer them. Use words the scripts don't use, as the bedroom request does. Does the order of the three ways hold?
5. **Two vectors per script.** Embed title + expected and the steps separately, and score each script by the better of its two similarities. Does it beat both?
6. **Write what people will ask.** Ask `gpt-6-luna` to write, for each script, the question a tester would type to find it, and embed that. This is called **document expansion**. It costs 1,000 model calls once, and none per search.

## Questions

For discussion. There are no right answers.

- One request said title + expected; twenty said the full text, by one request. How many requests would you want to see before trusting a choice like this?
- The best text to embed depends on how people will search. How could you find out how your testers search before you build anything?
- The title alone did worst, yet the title is what people read in a list of results. Should a test script be written for people, for search, or both?
- Searching one platform made two of the three ways look the same. When does a filter hide a weakness you would want to know about?
