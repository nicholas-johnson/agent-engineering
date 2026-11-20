# Feedback themes

Every demo starts from DOR-231, and DOR-231 starts from a count: "14 of 30 pieces of feedback were about the heating coming on early". Here you'll go back a step and do that count with a model. It reads all 30 pieces of feedback from September and October and groups them into **themes**, problems or requests that one piece of work could deal with. Then the script counts each theme, lists them biggest first, and checks that every piece of feedback landed in exactly one.

From the module folder (`day-two/module-07-ai-assisted-development`):

```bash
uv run python playground/feedback-themes/play.py
```

Or without `uv` (set up `.venv` once at the repo root with `python3 -m venv .venv && .venv/bin/pip install -e .`):

```bash
source ../../.venv/bin/activate
python playground/feedback-themes/play.py
```

Needs `OPENAI_API_KEY` in `.env`. It makes one call, which took about 6 seconds. The themes, with a one-sentence summary of each, are written to `playground/feedback-themes/output/themes.json`.

---

A model asked for themes in plain text writes them however it likes, and its counts can be wrong. So the reply has to fit a **schema**: a list of themes, each with a name, a summary and the ids of its feedback. With `"strict": True`, the Responses API makes sure the reply matches it. The ids are an `enum` built from the data, so the model can only use ids that exist:

```python
"feedback_ids": {"type": "array", "items": {"type": "string", "enum": ids}},
...
text={"format": {"type": "json_schema", "name": "themes", "schema": SCHEMA, "strict": True}},
```

The counts come from the length of each list, in code, never from the model:

```text
30 pieces of feedback, 17 themes, biggest first:

  13  Heating starts too early
      F01 F02 F04 F06 F10 F12 F14 F16 F19 F22 F24 F27 F29
   1  Geofencing needs more distance
      F03
   1  Warm-up needs a middle setting
      F08
   1  Explain the energy estimate
      F09
   1  Heating use changed unexpectedly
      F17
   1  Add Apple Home support
      F11
   1  Add another thermostat
      F13
   1  Dim the display at night
      F15
   1  Pairing keeps timing out
      F18
   1  Set holiday dates
      F20
   1  Find out which batteries to use
      F23
   1  Share access without sharing a password
      F26
   1  App opens slowly
      F28
   1  Easy schedule setup
      F05
   1  Warm house at wake-up
      F21
   1  Radiator valves are worth it
      F25
   1  Quick, friendly support
      F30

In no theme: F07. In more than one: none.
```

The themes change from run to run: their names, how many there are, and where the edge cases go.

## Things to notice

- **13, not 14.** The ticket counts 14. The model put F08 ("I found the Warm Wake thing and turned it off, but now the house is freezing ... Is there no in-between?") in a theme of its own, "Warm-up needs a middle setting". Is that the same problem? The ticket seems to count it, since it mentions "one customer who turned it off found the house too cold", and it's the clearest request for How early there is. Where you draw a theme's edge decides how big it looks.
- **One piece of feedback vanished.** F07, the E-305 error code, is in no theme. The schema guarantees every id is real, and that the reply is the right shape. It can't make the model include all of them. Only the check at the end found it, and without it nobody would have known.
- **F04 and F19 were the hard ones.** F04 asks about a sun on the display, and F19 is a landlord asking whether to send an engineer. Neither says "too early" in so many words, and both are Warm Wake. The model got both. A keyword search for "early" wouldn't have.
- **Seventeen themes for 30 comments.** Most themes have one piece of feedback in them. Ask for fewer themes and you get bigger, vaguer ones; ask for more and you get a list. Neither is the right number.

## Try this

1. **Run it three times.** Write down the biggest theme's count each time. How steady is the number a ticket would quote?
2. **Fewer themes.** Add "Use no more than six themes" to `INSTRUCTIONS`. What gets merged, and does anything end up somewhere strange?
3. **Our names, not theirs.** Change the instruction to name themes after our features ("Warm Wake", "Geofencing"). Do F04 and F19 still land in the Warm Wake theme?
4. **Make it say why.** Add a `reason` to each theme in the schema: one sentence on what the feedback in it has in common. Does asking for a reason change the groups?
5. **Fix the gap.** If any feedback is in no theme, send the model a second message listing the missing ids and asking it to place them. Does it put F07 somewhere sensible?
6. **More feedback.** Write 20 more pieces of feedback of your own into a copy of `feedback.json`, including some about How early after it ships, and point the script at your copy. Does a new theme appear?

## Questions

For discussion. There are no right answers.

- The ticket says 14, and the model says 13. Which number would you put in front of the people deciding what to build?
- A theme with one piece of feedback might be one customer, or the only one who bothered to write. How would you tell?
- Customers called it "heating coming on early", never "Warm Wake". Should themes be named in the customer's words or the company's?
- A model that quietly drops one item in 30 would drop about 300 in 10,000. What else in this course would you now check for that?

## Further reading

- **Braun, V. & Clarke, V. (2006). "Using thematic analysis in psychology." _Qualitative Research in Psychology_, 3(2), 77–101.** The standard description of how people find themes in what others say, in six phases. Read the phases, then ask which ones the model did in this script, and which ones it skipped.
- **OpenAI. "Structured model outputs." _OpenAI API documentation_.** [developers.openai.com/api/docs/guides/structured-outputs](https://developers.openai.com/api/docs/guides/structured-outputs). What `strict` guarantees, and which parts of JSON Schema it supports. Look for the list of supported keywords, `enum` among them.
