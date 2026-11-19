# Chunk headings

Every chunk in demo 3 starts with a line like `Dormouse Thermostat User Guide > Heating > Boost`: the document's title and the headings above the section. A section cut out of its document loses its context, and this line puts some back. You'll embed every chunk with that line and without it, and see where the right chunk lands for each of the 24 answerable questions.

From the module folder (`day-two/module-06-rag-and-proprietary-knowledge`):

```bash
uv run python playground/chunk-headings/play.py
```

Or without `uv` (set up `.venv` once at the repo root with `python3 -m venv .venv && .venv/bin/pip install -e .`):

```bash
source ../../.venv/bin/activate
python playground/chunk-headings/play.py
```

Needs `OPENAI_API_KEY` in `.env`. The first run embeds all 1,823 chunks twice and keeps each way in its own table in `playground/chunk-headings/output/chunks.db`. That took 17 minutes when I ran it, with the embeddings API slow and other scripts embedding at the same time; on a quiet day it's a few minutes. After that a run only embeds the 24 questions. Where the right chunk landed, and the top five each way, are written to `playground/chunk-headings/output/results.json`.

---

Only what gets embedded changes:

```python
WAYS = {
    "without": lambda chunk: chunk["content"],
    "with": lambda chunk: chunk["text"],  # "Title > Heading", a blank line, then the section: demo 3
}
```

Either way, the database stores the whole chunk, heading line included, because that's what the model would be given. So the facts are checked against the same text both ways, and any difference comes from the search alone. For each question, the table shows where the first chunk holding its facts lands among all 1,823 (1 = first).

```text
Where the first chunk with the facts lands (1 = first), searching 1,823 chunks:

  Question                                                    without      with
  Why does my Dormouse turn the heating on before the ...          90         6
  We switched the heating off before going away in Jan...           1         1
  How do I warm the house up quickly for a little while?            1         1
  Boost isn't warm enough for me. Can I make it hotter?             1         1
  I clicked the link to reset my password but it says ...           1         1
  How many people in my family can control the heating?             2         3
  My partner didn't accept the invite in time and now ...           1         1
  Can I have a separate thermostat for upstairs?                    3         1
  We had a power cut. Will I lose my heating times?                 1         1
  Is the heating off while the thermostat updates itse...           2         4
  The heating turns down every time I nip out to the s...           6         9
  Where can I see how much gas I've been using?                     1         2
  How do I wipe the thermostat before I sell the house?             3         1
  There's a little sun coming up on the screen. What d...           1         1
  What's the coldest I can set the thermostat to?                   2         1
  Will it work with my new 5 GHz router?                            1         1
  Someone keeps trying to get into my account. How do ...           1         1
  I don't want a message every time the heating is lef...           1         2
  My thermostat is showing E-305. What should I do?                 4         1
  E-104 came up while I was setting up the thermostat.              1         1
  The display says E-217.                                           9         3
  What does E-401 mean?                                             2         1
  My thermostat showed E-510 this morning.                          2         1
  E-110 keeps appearing on the display.                             1         3

  Facts in the top 5, of 24                                        21        22
```

The API can return very slightly different vectors from one call to the next, so a rank may move by one between runs, or between this and the other playgrounds.

## Things to notice

- **One more question in the top five.** 22 against 21. The one that crossed the line is E-217, from 9th to 3rd.
- **The ranks move far more than the count.** The Warm Wake question jumps from 90th to 6th. The section itself never says "Dormouse"; with its heading line, it starts `Dormouse Thermostat User Guide > Schedules > Warm Wake`, and the question asks about "my Dormouse" and "the time I set". It still misses the top five.
- **The heading helps when it names what the question asks about.** E-305 goes from 4th to 1st, and "How do I wipe the thermostat" from 3rd to 1st.
- **And hurts in the same way.** For "E-110 keeps appearing on the display", the first chunk without headings was a section of the known-issues document that says to check the router. With headings, the first two are chunks headed "What E-110 means". Their headings match the question perfectly, and neither mentions the router; the first chunk that does comes third.
- **Eight questions better, six worse, ten the same.** The heading line moves chunks towards questions about their topic, which is usually, but not always, where the answer is.

## Try this

1. **The title alone.** Add a way that starts each chunk with the document's title but not its headings: `lambda chunk: chunk["heading"].split(" > ")[0] + "\n\n" + chunk["content"]`. Which part of the line does the work?
2. **The heading alone.** Add a way that embeds only `chunk["heading"]`. How many questions does a list of headings answer?
3. **More context from the front matter.** Add the document's type and audience: "Troubleshooting, for customers: Boost does not start > Check the button". You'll need to keep them in each chunk in `split_into_chunks`.
4. **Ask a model for the context.** For each chunk, give `gpt-6-luna` the whole document and the chunk, and ask for one or two sentences on where the chunk fits. Embed those sentences plus the chunk. This is Anthropic's **contextual retrieval**, below. Batch 20 chunks to a call, as demo 4 does with its questions.
5. **Deeper.** Set `TOP = 10`. Does the heading line still make a difference at ten?
6. **Headings that answer.** "What E-110 means" won the search and lost the answer. Rewrite the headings of the three E-110 documents so each says what its section tells you to do, and run again.

## Questions

For discussion. There are no right answers.

- The heading line costs a few tokens per chunk and gained one question in 24. Would you keep it? What would change your mind?
- Headings are written for people skimming a page. Should writers now write them for a search engine too? What might that do to the documents?
- Contextual retrieval spends a model call on every chunk to write its context. When would that be worth it over a heading line that costs nothing?
- The heading pulled "What E-110 means" above the chunk with the fix. Is a customer better served by the meaning or by the fix? Who decides what a right chunk is?

## Further reading

- **[Anthropic: Introducing Contextual Retrieval](https://www.anthropic.com/research/contextual-retrieval)** (2024). This playground's idea with a model doing the writing: before embedding, each chunk gets 50 to 100 tokens of context written by a model that has read the whole document. Look for the table of results: the context alone cut failed retrievals in the top 20 by 35%, and adding keyword search and a reranker took that to 67%. Their test passed 20 chunks to the model, not 5.
