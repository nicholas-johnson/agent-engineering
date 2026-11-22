# Stale copies

Demo 6 updated the user guide and re-embedded only the chunks that changed. But the user guide isn't the only document that states each fact. Here one fact changes, household invitations now last 14 days instead of 7, and you'll hunt down every chunk in the knowledge base that still says 7: with a vector search, with a plain text search, and with both. The result is the list of documents an editor would need to open.

From the module folder (`day-two/module-06-rag-and-proprietary-knowledge`):

```bash
uv run python playground/stale-copies/play.py
```

Or without `uv` (set up `.venv` once at the repo root with `python3 -m venv .venv && .venv/bin/pip install -e .`):

```bash
source ../../.venv/bin/activate
python playground/stale-copies/play.py
```

Needs `OPENAI_API_KEY` in `.env`. The first run embeds all 1,823 chunks and keeps them in a ChromaDB store in `playground/stale-copies/output/chroma`; after that a run takes a few seconds. Every document to update, with each chunk's place in the vector search and the exact sentences that state the old fact, is written to `playground/stale-copies/output/stale-copies.json`.

---

The change sits at the top of the file:

```python
OLD_FACT = "A household invitation works for 7 days."  # what the documents say now
NEW_FACT = "A household invitation works for 14 days."  # what is true from today
OLD_WORDINGS = ["7 days", "seven days", "7-day", "seven-day"]  # every way of writing it you can think of
NEAREST = 20  # how many chunks the vector search returns
```

Two searches look for it:

- **Plain text**: every chunk that contains one of `OLD_WORDINGS`, using the same `contains_facts` check as the demos. It finds the words, whatever the chunk is about.
- **Vectors**: `OLD_FACT` is embedded and every chunk is ranked by how close it is, as in demo 3. A real search would return the first `NEAREST`. Ranking them all shows how far down the rest are.

```text
The fact "A household invitation works for 7 days." is now "A household invitation works for 14 days."

  Plain text search for 7 days, seven days, 7-day, seven-day: 30 chunks in 18 documents
  Vector search for the old fact: 20 of them are in the nearest 20
  The furthest is number 738 of 1,823

  The documents to update, and where their chunks came in the vector search:

  Vector rank         Type             Audience  Document
  1, 4, 9             support          customer  understand-household-invitation-expiry.md
  2, 7, 10            troubleshooting  customer  invitation-to-join-a-household-has-expired.md
  3                   support          customer  invite-someone-to-your-home.md
  5, 13               app              customer  android-app-household-screen-guide.md
  6, 14               app              customer  web-dashboard-household-screen-guide.md
  8, 17               app              customer  ios-app-household-screen-guide.md
  11, 18, 19, 21, 22  internal         internal  household-roles-and-invitation-qa-report.md
  12                  release notes    customer  firmware-3-3-release-notes.md
  15                  integration      customer  manage-household-access-for-connected-controls.md
  16                  support          customer  understand-who-can-manage-a-dormouse-home.md
  20                  internal         internal  household-notification-preferences-support-notes.md
  23                  guide            customer  user-guide.md
  25                  policy           customer  phone-location-privacy-policy.md
  36                  app              customer  android-app-account-settings-screen-guide.md
  37                  internal         internal  thermostat-firmware-release-history.md
  39                  app              customer  web-dashboard-account-settings-screen-guide.md
  47                  support          customer  manage-household-member-permissions.md
  98, 738             internal         internal  thermostat-firmware-4-1-baseline.md
```

## Things to notice

- **Eighteen documents state one fact.** Thirty chunks say invitations last 7 days. Update the user guide alone, as demo 6 did for Warm Wake, and 29 stale copies stay in the index, waiting to be retrieved.
- **The search doesn't prefer the source of truth.** The user guide comes 23rd, outside the top 20. Its "Household sharing" section is also about owners, members and permissions, so the invitation sentence is one of several. In [ask-your-docs](../ask-your-docs/), the question "My partner didn't accept the invite in time" was answered from two other documents, and the user guide wasn't in its top five. Fixing only the user guide would have changed nothing for that customer.
- **Vector search is precise but stops short.** All 20 of its results say 7 days, but 10 of the 30 chunks are further down. The furthest, 738th, is a row in a release history table: `| 3.3 | 2025-08-11 | Support for eight household members; invitations expire after 7 days.` Long chunks about something else, with the fact in passing, sink.
- **Text search finds everything you thought to spell.** It found all 30, because the documents happen to use only the four wordings in the list. A document that said "a week" would have been missed, and you'd never know.
- **Not every match should change.** Four of the chunks are history: the firmware 3.3 release notes ("Invitations to join a household now expire after 7 days."), the release history, the table row above, and the QA report's "Release context" section ("Firmware 3.3 ... changed invitations to expire after seven days."). They were true when written. Change them and the history is wrong instead. Neither search can tell history from a statement about today. The document's `type` in the front matter is a clue, but the QA report and the baseline document mix both.
- **Internal documents count too.** Four of the eighteen are internal. Customers never see them, but support staff do, and in this knowledge base so does the search.

## Try this

1. **Another fact.** The backup batteries keep the schedules for 48 hours. Set `OLD_FACT` and `OLD_WORDINGS` to find every copy. Then try the password reset link's 30 minutes. Which facts are copied most?
2. **Search further.** Set `NEAREST = 50`. How many of the 30 does the vector search find now, and what else comes back with them?
3. **A wording you didn't think of.** Add `"a week"` to `OLD_WORDINGS`. What does it find? (Look at what the firmware rollout plans say.)
4. **Ask a model.** Take the text matches and the vector search's top 50, and ask `gpt-6-luna` about each chunk: "Does this chunk say how long a household invitation lasts? If so, quote the sentence, and say whether it describes the product today or its history." Compare its list with the script's.
5. **Make the change.** Copy `data/docs/` to `output/docs/`, replace the old sentences (from `output/stale-copies.json`) with the new fact, but leave the history alone. Point [ask-your-docs](../ask-your-docs/) at the copy and ask about an expired invitation.
6. **Say it once.** Instead of finding copies after the fact, write `{invitation_days}` in the documents and fill it in when they're loaded. What would that take for a real documentation team, and what would it break?

## Questions

For discussion. There are no right answers.

- The user guide is the source of truth, but it came 23rd. Should a RAG system know which documents to trust most? How would you tell it?
- Four of the thirty chunks record history. When the fact changes, should the knowledge base keep them? What would a customer make of them?
- 18 documents repeat one fact, most of them written from the user guide. Is repeating a fact in every document that needs it good writing, or a maintenance problem waiting to happen?
- Who should be told when a fact changes: the people who own the documents, the people who own the search, or both? How would they find out?
