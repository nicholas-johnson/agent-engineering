# Redact

Demo 5 took Sam's name, address, phone number and email out of a support message before logging it, using what Dormouse knew about Sam and three regular expressions. Here you'll run just the regular expressions over ten messages that real customers might write, and count how much personal data gets through. Then you'll add patterns, and write messages that beat them. No model and no API key.

From the module folder (`day-two/module-08-security-and-deployment`):

```bash
uv run python playground/redact/play.py
```

Or without `uv` (set up `.venv` once at the repo root with `python3 -m venv .venv && .venv/bin/pip install -e .`):

```bash
source ../../.venv/bin/activate
python playground/redact/play.py
```

Needs nothing. The results go in `playground/redact/output/redacted.json`.

---

Each message comes with the personal data that should come out of it, so the script can count what it missed. The patterns run in order, and each match is replaced by its label:

```python
PATTERNS = [
    ("[EMAIL]", r"[\w.+-]+@[\w-]+(\.[\w-]+)+"),
    ("[PHONE]", r"(\+44 ?|\b0)7\d{3} ?\d{6}\b"),
    ("[POSTCODE]", r"\b[A-Z]{1,2}\d[A-Z\d]? ?\d[A-Z]{2}\b"),
]
```

Lines starting `!` still have personal data in them:

```text
  Call me on [PHONE] if you need to.
  My email is [EMAIL].
! We're at 14 Elm Grove, Leeds [POSTCODE].
    missed: 14 Elm Grove
! Postcode ls62ab, if that helps.
    missed: ls62ab
  My mobile is [PHONE].
! It's sam dot taylor at example dot com.
    missed: sam dot taylor at example dot com
! Ring me on oh seven seven double oh, nine double oh one two three.
    missed: oh seven seven double oh, nine double oh one two three
! This is Sam Taylor, the owner.
    missed: Sam Taylor
! Jo's phone is the one ending 124.
    missed: Jo
    missed: ending 124
! We're away until the 30th, the house is empty.
    missed: away until the 30th

Took out 4 of 12 pieces of personal data.
```

## Things to notice

- **The patterns caught what they were written for**, and only that: the email, both phone numbers and the postcode in capitals.
- **Names and street addresses got straight through.** There's no pattern for "Sam Taylor" or "14 Elm Grove". Demo 5 caught them because it already knew Sam's name and address; a stranger's name in Sam's message would get through there too.
- **People write numbers in words when they're dictating, or dodging a filter.** "Oh seven seven double oh" is a phone number to a person and nothing to a regular expression.
- **"Away until the 30th" is personal data too.** With the address, it tells someone when a house is empty. No pattern for emails or phone numbers will ever catch it.

## Try this

1. **Fix the postcode.** Make the postcode pattern ignore case and allow a missing space. Does it start catching things that aren't postcodes, like serial numbers?
2. **Names.** Add a pattern for "This is Firstname Lastname" or "my name's ...". How many names in real messages would it miss?
3. **Spelled-out emails.** Catch "at" and "dot" emails. Then write a message where "at" and "dot" are ordinary words, and see whether you redacted too much.
4. **Add messages.** Write three messages of your own that beat every pattern, with the personal data listed, and add them to `MESSAGES`.
5. **Use a model.** Ask a model to rewrite each message with personal data replaced by labels, and compare its count with the patterns'. What does it cost you to send the unredacted message to a model to redact it?
6. **Try Presidio.** Install `presidio-analyzer` and `presidio-anonymizer` and run them on `MESSAGES`. Which messages does it fix, and which does it still miss?

## Questions

For discussion. There are no right answers.

- The patterns took out 4 of 12. Is that better than nothing, or worse, because people now trust the log is clean?
- "Away until the 30th" isn't on any list of personal data types, but it's the most dangerous line here. How would you find things like it?
- Redacting with a model means sending the personal data to the model first. When is that acceptable?
- If you can't redact reliably, what else could you do: keep less, keep it for less time, or restrict who can read the log?

## Further reading

- **UK ICO, "Guidance on AI and data protection"**, the chapter "How should we assess security and data minimisation in AI?": https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/artificial-intelligence/guidance-on-ai-and-data-protection/. It explains why keeping less in the first place beats cleaning it up later.

## Rabbit holes

- **Presidio.** Presidio (https://github.com/data-privacy-stack/presidio, formerly Microsoft's) finds personal data with patterns, named-entity models and checksums, and replaces it with labels, fake values or hashes. Add a recogniser for Dormouse serial numbers (`DMC-260417`), then run it over demo 4's audit log.
- **Reversible pseudonyms.** Replace each name with a stable token (`[NAME-1]`) and keep the mapping in a separate, locked store, so support can reverse it when they must and nobody else can. Build it, then work out what erasing one customer means when their data is in two places.
