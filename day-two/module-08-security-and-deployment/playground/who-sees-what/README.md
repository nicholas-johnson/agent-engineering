# Who sees what

In demo 2, a customer's search only reached documents marked for customers, and the internal note on the relay click never reached the model. Here you'll search the same knowledge base as a customer and as a support agent, and see what each one gets back. Then you'll move the filter: search everything first and remove what the role mustn't see afterwards, which is what happens when the filter is added late. No model and no API key: it uses a small keyword search, so it runs in a moment.

From the module folder (`day-two/module-08-security-and-deployment`):

```bash
uv run python playground/who-sees-what/play.py
```

Or without `uv` (set up `.venv` once at the repo root with `python3 -m venv .venv && .venv/bin/pip install -e .`):

```bash
source ../../.venv/bin/activate
python playground/who-sees-what/play.py
```

Needs nothing but `data/kb/`. The results go in `playground/who-sees-what/output/results.json`.

---

Every document says who it is for in its front matter (`audience: customer` or `audience: internal`), and every chunk carries its document's audience. Each role lists the audiences it may read:

```python
ROLES = {
    "customer": ["customer"],
    "support agent": ["customer", "internal"],
}
FILTER = "before"  # "before": search only what the role may read. "after": search everything, then remove the rest.
```

The search scores each chunk by the words it shares with the question, weighting rare words ("click") above common ones ("thermostat"). It splits sections a little differently from the demos, so it finds 288 chunks rather than 258. Filtering before the search:

```text
288 chunks. Question: Why does my thermostat click so loudly? Can I have a replacement?
Filtering before the search.

As a customer (customer): 5 of 5 results
   3.4  customer  thermostat-electrical-safety-policy.md#Responding to errors
   3.4  customer  thermostat-electrical-safety-policy.md#Support and maintenance
   3.4  customer  thermostat-replacement-on-an-existing-wall-plate.md#Thermostat Replacement on an Existing Wall Plate
   3.4  customer  thermostat-replacement-on-an-existing-wall-plate.md#Before you begin
   3.4  customer  thermostat-replacement-on-an-existing-wall-plate.md#Check the existing installation

As a support agent (customer, internal): 5 of 5 results
  10.9  internal  internal-relay-click-revision-c.md#Summary
   7.9  internal  internal-relay-click-revision-c.md#What support should say
   4.6  internal  internal-relay-click-revision-c.md#Relay click on hardware revision C
   3.4  internal  temperature-sensor-fault-escalation-playbook.md#Purpose and scope
   3.4  internal  temperature-sensor-fault-escalation-playbook.md#Confirm the reported fault
```

And with `FILTER = "after"`:

```text
As a customer (customer): 0 of 5 results

As a support agent (customer, internal): 5 of 5 results
  10.9  internal  internal-relay-click-revision-c.md#Summary
  ...
```

## Things to notice

- **The support agent's top three are the relay note.** It's the only document about clicking. The customer gets the nearest thing they're allowed to see: replacing a thermostat, and electrical safety.
- **Filtering afterwards left the customer with nothing.** The top five were all internal, so removing them left an empty list. The model would then answer from nothing, and probably say the documentation doesn't cover clicking, which isn't quite true. Filtering before the search, in the query, always fills the top five with what the role may read.
- **Filtering afterwards is still safe.** Nothing internal got through either way. The difference is quality, not security. A filter in the prompt ("ignore internal documents") would be neither.
- **Every chunk here scored 3.4.** That's "thermostat" and "replacement" and nothing rarer. A keyword search can't tell which of these five is most useful. Module 5's embeddings would rank them by meaning.

## Try this

1. **Ask something else.** Change `QUESTION` to "Why can't my lodger invite people?" or "How long do you keep my heating history?". Which questions give the two roles the same results?
2. **Add an installer.** Installers need the wiring and installation documents, but not the support playbooks. Add an `installer` audience to a few documents' front matter (in a copy of `data/kb/`) and a role that can read it.
3. **Mislabel a document.** Change `internal-relay-click-revision-c.md` to `audience: customer` in a copy. How would you catch that before it ships? Write a check.
4. **Two audiences.** Let a document be `audience: customer, internal` and change the filter to cope. Is a list of audiences better than one?
5. **Filter after, but fetch more.** With `FILTER = "after"`, fetch the top 20 and keep the first 5 the role may see. When does that still fail?
6. **Per-customer documents.** Sam's tickets are for Sam and for staff, but not for Alex. Add a `customer` field to some chunks and filter on it as well. That's what a per-user vector search needs.

## Questions

For discussion. There are no right answers.

- A support agent asks the same question as a customer and gets a completely different answer. Is that what you want? What happens if the agent pastes their answer to the customer?
- Who decides each document's audience, and what happens when nobody does?
- Filtering after the search was safe but less useful. Would anyone notice that quality loss in testing?
- Should staff be able to search as a customer, to see what a customer would be told?

## Further reading

- **OWASP Top 10 for LLM Applications 2025**, LLM02:2025 "Sensitive Information Disclosure": https://genai.owasp.org/llm-top-10/. Its prevention list starts with access controls on the data the model can reach, which is this script.
