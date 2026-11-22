# Ask your docs

A chat window over the Dormouse knowledge base. You'll ask your own questions and get demo 5's kind of answer: drawn only from the documentation, with quotes that are checked against the chunks they cite, and the five chunks the search found. Then you can point it at a folder of your own Markdown.

From the module folder (`day-two/module-06-rag-and-proprietary-knowledge`):

```bash
uv run python playground/ask-your-docs/play.py
```

Or without `uv` (set up `.venv` once at the repo root with `python3 -m venv .venv && .venv/bin/pip install -e .`):

```bash
source ../../.venv/bin/activate
python playground/ask-your-docs/play.py
```

Needs `OPENAI_API_KEY` in `.env`. The first run embeds all 1,823 chunks, which took about two minutes, and keeps them in a ChromaDB store in `playground/ask-your-docs/output/chroma`. After that, only new or changed chunks are embedded. Type a question and press Enter; an empty line stops. Every question, answer, citation and chunk is saved to `playground/ask-your-docs/output/transcript.json`.

You can also pipe the questions in:

```bash
printf 'How much does a Dormouse thermostat cost?\n\n' | uv run python playground/ask-your-docs/play.py
```

---

This is demos 3 and 5 joined into a loop. Each question is embedded, and the five nearest chunks go to `gpt-6-luna` with demo 5's instructions: use only the documentation, quote each sentence you rely on with its chunk's id, and say so if the documentation doesn't answer. Each quote is then looked for, word for word, in the chunk it names. `quote checked` means it's there; `NOT IN THAT CHUNK` means the model misquoted or cited the wrong chunk. Under each answer are the chunks the search found, with their **cosine similarity** to the question.

```text
275 documents, 1,823 chunks. Ask a question; an empty line stops.

You: Why does my Dormouse turn the heating on before the time I set?
Dormouse: The documentation doesn’t explain why Dormouse might turn the heating on before a scheduled time.
   (answered: false)
   Searched:
     0.667  create-a-smart-home-heating-routine.md#leave-temperature-control-to-dormouse
     0.633  create-a-smart-home-heating-routine.md#keep-temperature-schedules-on-dormouse
     0.627  use-a-smart-plug-alongside-dormouse.md#use-dormouse-for-heating
     0.611  use-a-smart-plug-alongside-dormouse.md#troubleshooting-the-separate-automation
     0.609  create-a-smart-home-heating-routine.md#troubleshoot-carefully

You: My partner didn't accept the invite in time and now the link doesn't work.
Dormouse: The invitation link expires after 7 days, so your partner can’t use it to join now. The home owner needs to send a new invitation from Settings > Household > Invite; the new link will work for 7 days.
   [invitation-to-join-a-household-has-expired.md#what-the-message-means] "A household invitation works for 7 days. After that, its link expires and cannot be used to join the home." (quote checked)
   [invite-someone-to-your-home.md#invitation-expiry] "If the person does not use the link in time, the owner needs to send a new invitation from Settings > Household > Invite." (quote checked)
   [invitation-to-join-a-household-has-expired.md#ask-the-owner-to-send-a-new-invitation] "The new invitation works for 7 days from when it is sent." (quote checked)
   Searched:
     0.469  invite-someone-to-your-home.md#invitation-expiry
     0.454  understand-household-invitation-expiry.md#what-happens-when-it-expires
     0.454  invitation-to-join-a-household-has-expired.md#ask-the-owner-to-send-a-new-invitation
     0.441  invitation-to-join-a-household-has-expired.md#what-the-message-means
     0.428  web-dashboard-household-screen-guide.md#invitation-status-and-expiry

You: How much does a Dormouse thermostat cost?
Dormouse: The documentation does not specify the price of a Dormouse Thermostat.
   (answered: false)
   Searched:
     0.639  thermostat-zone-capacity-and-device-compatibility.md#dormouse-thermostat
     0.627  check-the-thermostat-operating-temperature-range.md#operating-range
     0.625  thermostat-temperature-measurement-specification.md#specification-summary
     0.617  thermostat-physical-dimensions-and-display-specification.md#product
     0.615  add-dormouse-devices-to-a-home-automation-system.md#check-what-your-home-supports

You: Why does my thermostat click loudly when the heating comes on?
Dormouse: The click is the normal sound of the thermostat switching the boiler on and off.
   [internal-relay-click-revision-c.md#what-support-should-say] "Tell the customer the click is the normal sound of the thermostat switching the boiler on and off." (quote checked)
   Searched:
     0.579  internal-relay-click-revision-c.md#what-support-should-say
     0.527  internal-relay-click-revision-c.md#summary
     0.482  thermostat-does-not-respond-to-dial-changes.md#check-for-an-error-code
     0.476  heating-does-not-start-when-the-boiler-is-not-responding.md#heating-and-safety
     0.468  heating-starts-below-five-degrees.md#check-the-room-temperature

You:
```

The model's answers change from run to run, so yours will be worded differently.

## Things to notice

- **The module's own question fails.** "Why does my Dormouse turn the heating on before the time I set?" is answered by the user guide's Warm Wake section, but the five nearest chunks are all about smart-home routines and smart plugs. The model, told not to guess, says the documentation doesn't explain it. That's an honest answer and a wrong one: the failure is in the search, not the model. Searching demo 4's customer-style questions is one way to close that gap.
- **The similarities don't tell you whether it worked.** The failed search's best match scored 0.667; the invitation question, which worked, scored 0.469. A score only ranks the chunks for one question. It says nothing about whether the right chunk is among them.
- **Three quotes, all checked.** The invitation answer rests on three sentences from two documents, and each is really in the chunk it names. When a quote isn't, you'll see `NOT IN THAT CHUNK`.
- **An internal document answered a customer.** The click question was answered from `internal-relay-click-revision-c.md`, a note for support staff. Its `#summary` chunk, also in the top five, names the supplier batch that the note says never to mention. This time the model kept to the scripted line. Nothing in the search stopped it from doing otherwise.

## Try this

1. **Ask it everything.** Try the questions in `data/questions.json`, then your own. Find a question it gets wrong with the right chunk in the top five, and one where the right chunk is missing.
2. **More or fewer chunks.** Set `TOP = 1`, then `TOP = 20`. Does the Warm Wake question come right? What else changes?
3. **Customers only.** Keep internal documents out of a customer's search. Add `audience` to each chunk's metadata, next to `document`, fill it from each document's front matter, and pass `where={"audience": "customer"}` to `collection.query`. Ask about the click again.
4. **Follow-up questions.** Ask "How do I invite someone?", then "How long does it last?". The second search only sees "How long does it last?". Pass the last few turns to the model and ask it to rewrite the question so it stands alone, then search with that. This is called **query rewriting**.
5. **Your own documents.** Point `DOCS` at a folder of your own Markdown files: a project's `docs/`, or this course's module READMEs. Change the first line of `INSTRUCTIONS` to match. Front matter is optional; without a title, the file name is used.
6. **Show the source.** Print each cited chunk's heading line (its first line) under the quote, so a reader can see "Dormouse Thermostat User Guide > Heating > Boost" rather than a chunk id.

## Questions

For discussion. There are no right answers.

- "The documentation doesn't explain this" was true of the five chunks the model saw, and false of the knowledge base. Is that a good answer to give a customer? What should happen next?
- Every quote was checked, but a checked quote only proves the sentence is in the chunk. What would it take to check that the quotes support the answer?
- An internal note was one search away from a customer. Whose job is it to keep internal documents out: the search, the instructions, or the people who decide what goes in the knowledge base?
- If you pointed this at your team's documents, which questions would you trust it with, and which would you never let it answer?

## Further reading

- **Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Küttler, H., Lewis, M., Yih, W., Rocktäschel, T., Riedel, S. & Kiela, D. (2020). "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks." _NeurIPS 2020_.** [arXiv:2005.11401](https://arxiv.org/abs/2005.11401). The paper that named RAG. Read the introduction for the argument this script rests on: knowledge kept in documents can be inspected and updated, and knowledge kept in a model's weights can't.
- **Gao, T., Yen, H., Yu, J. & Chen, D. (2023). "Enabling Large Language Models to Generate Text with Citations." _EMNLP 2023_.** [arXiv:2305.14627](https://arxiv.org/abs/2305.14627). Measures whether citations really support what they're attached to. Look for their two measures, **citation recall** and **citation precision**: a step beyond this script's word-for-word check.
