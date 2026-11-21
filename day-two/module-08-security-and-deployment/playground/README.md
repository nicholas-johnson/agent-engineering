# Playground

Things to play with between exercises: attacks and defences around an assistant in front of customers. You'll try to get a secret out of an assistant, write your own prompt injection and count how often it works, search the knowledge base as a customer and as staff, beat a redaction script, check agents for the lethal trifecta, and put limits on a customer who won't stop typing. Each folder has a short script to run and a list of ideas to take it further. None of them are required, and there are no right answers.

Every script follows the same thread as the demos: Sam, the clicking thermostat, and Ask Dormouse. Each one builds what it needs from `data/`, so you don't have to run the demos first.

From the module folder (`day-two/module-08-security-and-deployment`):

```bash
uv run python playground/secret-keeper/play.py
```

Or without `uv` (set up `.venv` once at the repo root with `python3 -m venv .venv && .venv/bin/pip install -e .`):

```bash
source ../../.venv/bin/activate
python playground/secret-keeper/play.py
```

| Folder | What it's about | Needs |
|--------|-----------------|-------|
| [secret-keeper](secret-keeper/) | Get a discount code out of an assistant told to keep it, at three levels of defence | `OPENAI_API_KEY` |
| [injection-lab](injection-lab/) | Rename Sam's thermostat to an attack of your own, and count how often the assistant follows it | `OPENAI_API_KEY` |
| [who-sees-what](who-sees-what/) | Search the knowledge base as a customer and as a support agent, and filter before or after the search | Nothing |
| [redact](redact/) | Take the personal data out of support messages before logging them, and count what gets through | Nothing |
| [lethal-trifecta](lethal-trifecta/) | Check six agents' tools for private data, untrusted content and a way to send data out | Nothing |
| [spend-limits](spend-limits/) | One customer, ten messages, and the limits that keep a public assistant affordable | `OPENAI_API_KEY` |

Everything a script writes goes into an `output/` folder next to it.
