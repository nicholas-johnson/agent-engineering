# Grounding rules

Demo 3 told the model "Use our documentation". Demo 6 told it to use only the documentation, and to say when the documentation doesn't answer. Here you'll find out how much those words matter. The same five chunks go to the model with three sets of instructions, for 29 questions: the 24 the documentation answers and the 5 it doesn't. You'll count how often each set gets the answer right, and how often it makes something up.

From the module folder (`day-two/module-06-rag-and-proprietary-knowledge`):

```bash
uv run python playground/grounding-rules/play.py
```

Or without `uv` (set up `.venv` once at the repo root with `python3 -m venv .venv && .venv/bin/pip install -e .`):

```bash
source ../../.venv/bin/activate
python playground/grounding-rules/play.py
```

Needs `OPENAI_API_KEY` in `.env`. The first run embeds all 1,823 chunks and keeps them in a ChromaDB store in `playground/grounding-rules/output/chroma`. After that, a run makes 174 model calls, eight at a time, and took about a minute and a half. Every question, rule, reply and verdict is written to `playground/grounding-rules/output/results.json`.

---

The three sets of instructions sit in a dictionary at the top of the file. Each goes between demo 3's first line ("You are the support assistant for Dormouse...") and the chunks:

```python
RULES = {
    "plain": "Use our documentation:",
    "only the docs": "Use only the documentation below, never what you know from elsewhere.",
    "only, and say so": "Use only the documentation below, never what you know from elsewhere.\n"
    "If the documentation does not answer the question, say so. Do not guess.",
}
```

Unlike demo 6, the answers are plain text, with no `answered` field to fill in, so the model isn't nudged towards refusing by the shape of its reply. That means something else has to decide whether a reply answered the question. A second call to `gpt-6-luna`, a **judge**, reads each question and reply and says whether it gave the information asked for. Then:

- for the 24 answerable questions, a reply that answered is **right** if it contains the question's facts (the demos' `contains_facts`), and **wrong** if it doesn't
- for the 5 questions the documentation doesn't answer, any reply that answered **made something up**

```text
                                         plain     only the docs  only, and say so
  Of the 24 the documentation answers:
    answered right                          19                20                21
    answered wrong                           5                 3                 3
    said it didn't know                      0                 1                 0
  Of the 5 it doesn't:
    made something up                        0                 0                 0
    said it didn't know                      5                 5                 5
```

The answers change from run to run. A second run gave 19, 21 and 20 right, and again made nothing up.

## Things to notice

- **Nothing was made up, under any rules.** Not a price, a founder, a launch date, a discount or a phone number, in either run. With the chunks in front of it, `gpt-6-luna` says it doesn't know even when told only to "use our documentation". Compare demo 1, with no documentation at all.
- **The plain rules still reach outside.** Asked the price, the plain set said "Please check the Dormouse store or contact support for current pricing." There is no Dormouse store in the documentation. In the second run it suggested "Dormouse's official announcements". Neither counts as making something up, but both send a customer somewhere that may not exist.
- **Stricter rules got one or two more right.** 19 for plain both times; 20 or 21 for the others. That's within what changes between runs, so don't read much into the order of the last two.
- **Wrong answers start in the search.** The Warm Wake and geofencing questions were wrong under every set, because their chunks weren't in the top five (see [how-many-chunks](../how-many-chunks/)). Under plain rules, the first run explained Warm Wake from general knowledge: "Dormouse may start heating before a scheduled time so the room reaches the scheduled temperature by then". Right in spirit, from nowhere in the chunks. "Only, and say so" blamed frost protection in the first run, and said "I can't tell from the information provided" in the second.
- **Some "wrong" answers are right.** "Open the **Energy** tab" fails the check for "energy tab", because of the Markdown `**` around the word. "It will automatically try again ... tomorrow night" fails the check for "next night". The checker is part of what you're measuring. Read `output/results.json` before believing a count.
- **The judge is a model too.** Under "only the docs", the first run's Warm Wake reply gave schedule advice without saying it didn't know, and the judge counted it as not answering. You might not.

## Try this

1. **Tempt it.** Add "Always give the customer a specific, helpful answer." to the plain rule. Does anything get made up now?
2. **Harder questions.** The five unanswerable questions are far from the documentation. Write five that sit just beside it: the warranty on a radiator valve bought separately, the price of a replacement front cover, whether it works with an oil boiler. Do the rules differ more?
3. **A fairer check.** Strip `*` in `plain()`, and add `"next night|tomorrow night"` to the E-510 question's facts in a copy of `questions.json`. How many "wrong" answers were right?
4. **No chunks.** Send no documentation at all, as demo 1 does, but keep "only, and say so". Does it refuse all 29?
5. **Check the judge.** Read every verdict in `output/results.json` and mark the ones you disagree with. How often is it wrong, and in which direction? Then add "Answer in one word" to `JUDGE` or reword it, and see if it changes.
6. **Rules for internal documents.** Add a fourth set: "Some chunks are internal notes for staff. Never repeat anything from them that the notes say not to share." Ask the relay click question from `questions.json` (kind `internal`). Does it hold?

## Questions

For discussion. There are no right answers.

- No set of rules made anything up. Does that mean grounding instructions aren't needed, or that these five questions were too easy?
- "Check the Dormouse store" isn't a made-up fact, but it might be a made-up place. Where's the line between being helpful and inventing?
- Under "only, and say so", the model blamed frost protection for early heating once, and said it couldn't tell the next time. Which is worse for a customer?
- A model judged a model's answers here. When would you trust that, and when would you want a person to read them?

## Further reading

- **Kalai, A. T., Nachum, O., Vempala, S. S. & Zhang, E. (2025). "Why Language Models Hallucinate."** [arXiv:2509.04664](https://arxiv.org/abs/2509.04664). Argues that models guess because training and tests reward a confident guess over "I don't know". Read the introduction and the section on evaluations, then look at this script's table: it's a test that gives credit for saying "I don't know".
- **Zheng, L. et al. (2023). "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena." _NeurIPS 2023 Datasets and Benchmarks Track_.** [arXiv:2306.05685](https://arxiv.org/abs/2306.05685). How far a model's verdicts can be trusted. Look for the judge's known biases, such as preferring longer answers and the first answer it reads, before you rely on this script's judge.
