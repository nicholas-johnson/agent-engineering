# Write a skill

The module's skills were written for you. Here you'll write your own. A **skill** is a folder with a `SKILL.md` in it: a name and a description at the top, which a tool like Claude Code reads to decide when to use it, then the instructions. This folder comes with a new one, `support-reply`, which answers a customer who asks why the heating comes on early, now that DOR-231 has shipped. You'll run it, change it, and then write one of your own. The script can run any skill in `data/skills/` too.

From the module folder (`day-two/module-07-ai-assisted-development`):

```bash
uv run python playground/write-a-skill/play.py
```

Or without `uv` (set up `.venv` once at the repo root with `python3 -m venv .venv && .venv/bin/pip install -e .`):

```bash
source ../../.venv/bin/activate
python playground/write-a-skill/play.py
```

Needs `OPENAI_API_KEY` in `.env`. It makes one call, which took about 3 seconds. The reply is written to `playground/write-a-skill/output/`, named after the skill: `support-reply.md` for the one that ships here.

---

Two constants say what to run:

```python
SKILL = HERE / "support-reply"   # a folder with a SKILL.md; try DATA / "skills" / "release-notes"
REQUEST = (
    "Reply to this customer: Is it normal for the heating to switch on at 5:30 for a 7:00 period? "
    "My neighbour has the same thermostat and hers doesn't."
)
```

The skill's instructions go in as the model's instructions. Everything any of the module's skills might need goes in as the input: the ticket, `AGENTS.md`, the change, the help article and the company brain, then your request. That's how a skill can be short: it says what to do and in what order, and leaves the facts to the materials. Here is [`support-reply/SKILL.md`](support-reply/SKILL.md)'s list of steps:

```markdown
1. Answer their question first, in one sentence. If the heating comes on before their schedule, that is Warm Wake, and it is working as it should.
2. Say what Warm Wake does for them, in one or two sentences.
3. Tell them how to change it: the exact menu path, the choices, and the default, all from the ticket.
4. If they would rather it didn't start early at all, tell them how to turn Warm Wake off, and what happens then.
5. If their message points to a real fault, such as an error code or no heat at all, don't explain Warm Wake. Say you'll look into it, and ask for what you need.
```

The request is F29 from `data/feedback.json`, word for word:

```text
Skill: support-reply
  Reply to a customer who asks why the heating comes on before their schedule, now that Warm Wake has a How early setting. Use when answering support chats and emails about early heating.

Request: Reply to this customer: Is it normal for the heating to switch on at 5:30 for a 7:00 period? My neighbour has the same thermostat and hers doesn't.

Hi, yes—if the heating comes on before your schedule, that’s Warm Wake, and it’s working as it should.

Warm Wake learns how long your home takes to heat up and starts early so it’s warm when the period begins. Yours is starting up to 90 minutes early.

You can change this in Settings > Schedule > How early. Choose 30, 60 or 90 minutes; the default is 60 minutes. To stop it starting early, turn Warm Wake off in Settings > Schedule. The heating will then start at the scheduled time.

Dormouse support

(93 words, written to playground/write-a-skill/output/support-reply.md)
```

Set `SKILL = DATA / "skills" / "social-post"` and `REQUEST = "Write the social posts."`, and the same script runs a module skill instead. The replies change from run to run.

## Things to notice

- **It followed the order.** Answer, what it does, how to change it, how to turn it off, then the sign-off, in 93 words. The skill's numbered steps are the reply's paragraphs.
- **It ignored the neighbour.** The customer's real puzzle is why her neighbour's thermostat doesn't do it. The answer is in the brain (Warm Wake learns each home's heat-up rate) but the skill never says to answer every question the customer asks, so it didn't.
- **"Up to 90 minutes" isn't quite right.** 05:30 for a 07:00 period is exactly 90 minutes, so the reply is right for this customer. But it says "Yours is starting up to 90 minutes early" as a fact about their home, and after the update their default will be 60. The skill didn't say what to assume about a customer's settings.
- **The times disappeared.** The skill says to use the 24-hour clock "even when the customer used something else". The reply avoided the problem by not mentioning a time at all. A rule that's never triggered is never tested.
- **The menu path is the model's own.** "Settings > Schedule > How early" is a fair guess from the ticket, which only says How early is in Settings > Schedule. A support reply sends a customer to a real screen, so it's worth checking.

## Try this

1. **Answer the neighbour.** Add a step to `SKILL.md` that makes sure every question in the message gets an answer. Run it again. Does the reply explain why homes differ, and does it stay under 120 words?
2. **A real fault.** Change `REQUEST` to F07 from `data/feedback.json`: "Display says E-305, boiler pressure looks fine at 1.2 bar. What next?". Does step 5 stop it explaining Warm Wake?
3. **Check the voice.** Copy the reply into [voice-check](../voice-check/). Does it pass both ways?
4. **Write your own.** Copy `support-reply/` to a new folder, say `landlord-faq/`, and write a skill that answers F19 (the landlord whose tenant thinks the heating is faulty). Write the description first: when should a tool pick this skill and not `support-reply`?
5. **Description only.** Give the model just the `name` and `description` of every skill in `data/skills/` and this folder, and a request like "Can you tell customers about this?". Ask it which skill to use. That's what Claude Code does before it reads a skill's instructions. Is your description good enough to be picked?
6. **A skill with a script.** Real skills can carry files next to `SKILL.md`, such as a checklist or a script. Add a `banned.txt` of words to your skill's folder, and change `load_skill` to append any `.txt` files in the folder to the instructions.

## Questions

For discussion. There are no right answers.

- The skill told the model what to do, but not to answer every question. How do you write instructions for the things you didn't think to say?
- Support replies go to customers. Would you let this skill send its reply, draft it for a person, or neither?
- A skill is a page of Markdown, so anyone on the support team could write or change one. Is that a strength, or a risk?
- What does your team do the same way every week that could be a skill? What would be lost by writing it down?

## Further reading

- **Agent Skills. "Specification."** [agentskills.io/specification](https://agentskills.io/specification). The open format the module's skills follow. Read the section on the `SKILL.md` front matter: what goes in `name` and `description`, and why the description is what a tool reads first.
- **Anthropic. "Agent Skills." _Claude documentation_.** [platform.claude.com/docs/en/agents-and-tools/agent-skills/overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview). How Claude loads skills a little at a time: the description always, the instructions only when the skill is used, and the extra files only when the instructions point to them. Compare it with this script, which loads everything every time.

## Rabbit holes

- **Use it in Claude Code.** Copy `support-reply/` into a project's `.claude/skills/` folder, as `demo/LIVE.md` does with the review skill. Paste in a customer message and ask Claude Code to answer it, without naming the skill. Does it pick yours?
- **A skill library.** Write three more skills a Dormouse support team would use (refund questions, installer questions, landlord questions), with descriptions that don't overlap. Then write ten customer messages and check whether a model, given only the descriptions, picks the right skill for each.
