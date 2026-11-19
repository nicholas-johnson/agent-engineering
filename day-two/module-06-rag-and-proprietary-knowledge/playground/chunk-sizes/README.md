# Chunk sizes

Demo 3 cut every document at its headings. The other common way is to ignore the headings and cut every so many words. You'll chunk the knowledge base four ways, run the 24 answerable questions against each, and see how often the top five holds the answer, and how many tokens each way sends the model.

From the module folder (`day-two/module-06-rag-and-proprietary-knowledge`):

```bash
uv run python playground/chunk-sizes/play.py
```

Or without `uv` (set up `.venv` once at the repo root with `python3 -m venv .venv && .venv/bin/pip install -e .`):

```bash
source ../../.venv/bin/activate
python playground/chunk-sizes/play.py
```

Needs `OPENAI_API_KEY` in `.env`. The first run embeds the knowledge base four times, about 6,500 chunks, and keeps each way in its own table in `playground/chunk-sizes/output/chunks.db`. That took a long time on the day I ran it (13 minutes, with the embeddings API slow), so start it and go and do something else. After that, a run only embeds the 24 questions and counts tokens. The top five for each question and each way are written to `playground/chunk-sizes/output/results.json`.

---

The four ways:

- **headings**: demo 3's chunks, one per section, each starting with its "Title > Heading" line
- **50 words**, **150 words**, **400 words**: **fixed windows**. Each document's words, cut every 50, 150 or 400 words, wherever the cut falls. A heading is just more words, and a window doesn't say which document it came from

```python
def split_into_windows(document, size):
    words = document["body"].split()
    step = size - OVERLAP
    return [
        {"id": f"{document['name']}#words-{start + 1}", "text": " ".join(words[start : start + size])}
        for start in range(0, max(len(words) - OVERLAP, 1), step)
    ]
```

A question counts as found if one of its top five chunks contains its facts, as in demo 3. "Tokens sent" is the whole prompt demo 3 would send for that question, averaged over the 24: the instructions, the five chunks and the question. The API counts them with `client.responses.input_tokens.count`, without running the model.

```text
  Chunking    Chunks  Words each  Tokens sent   Facts in the top 5, of 24
  headings     1,823          86          611    22
  50 words     3,108          48          439    19
  150 words    1,130         132          928    23
  400 words      507         293        1,694    22
```

The last window of each document is usually short, which is why "Words each" is under 50, 150 and 400.

## Things to notice

- **Small windows find the right document and cut off the answer.** For "My thermostat is showing E-305. What should I do?", the 50-word search's first result is the start of `thermostat-shows-e-305.md`. It ends "Check the boiler in this order: 1. Confirm that it is switched on. 2. Check that". The pressure, 1.5 bar, is in the next window, which didn't make the top five. E-217 and E-110 went the same way.
- **Big windows cost more for no more answers.** 400-word windows found 22, the same as the headings, and sent nearly three times as many tokens (1,694 against 611).
- **150 words won, by one question.** It found "The heating turns down every time I nip out to the shops", which needs a chunk that says "geofencing"; the headings and 400-word windows didn't. One question in 24 is a thin margin to change a design on, and it costs half as many tokens again as the headings.
- **One question beat every way.** "Why does my Dormouse turn the heating on before the time I set?" was missed four times out of four. Its nearest chunks are all about smart-home routines. When every chunk size fails the same question, the problem isn't the chunk size.
- **The ids tell you something, too.** A heading chunk's id, `user-guide.md#boost`, means something to a reader checking a citation. `user-guide.md#words-751` doesn't.

## Try this

1. **Overlap.** Set `OVERLAP = 25`, so each 50-word window repeats the last 25 words of the one before. Does E-305 come back? What does it do to the number of chunks and the tokens sent?
2. **More chunks.** Set `TOP = 10`. Do the 50-word windows catch up? At how many tokens?
3. **A title on every window.** Start each window with the document's title, as the heading chunks do. Does it help the small windows most, or the big ones? [chunk-headings](../chunk-headings/) measures the same idea for heading chunks.
4. **Cut at sentences.** Instead of cutting mid-sentence, add whole sentences to a window until it reaches about 150 words. Does finishing the sentence matter?
5. **Headings, but capped.** Keep the heading chunks, but split any section longer than 150 words into pieces, each starting with the same heading line. Can you beat 23?
6. **Facts, not windows.** Ask `gpt-6-luna` to rewrite each section as a list of short facts that each stand on their own ("Boost heats the home for one hour."). Embed the facts, but give the model the section each one came from. This is the idea behind Chen et al.'s **propositions**, below.

## Questions

For discussion. There are no right answers.

- 150-word windows beat the headings by one question and cost half as much again in tokens. Would you switch? What else would you want to know first?
- The 50-word search found the right document and missed the answer, and the model would have said the documentation doesn't say. Who would notice that in a real system, and how?
- Heading chunks only work when the documents have good headings. Whose job is that: the people who write the documents, or the people who build the search?
- The right size depends on how the documents are written. If your knowledge base mixed tidy guides with long email threads, would one size fit both?

## Further reading

- **Chen, T., Wang, H., Chen, S., Yu, W., Ma, K., Zhao, X., Zhang, H. & Yu, D. (2024). "Dense X Retrieval: What Retrieval Granularity Should We Use?" _EMNLP 2024_, 15159–15177.** [arXiv:2312.06648](https://arxiv.org/abs/2312.06648). Compares retrieving passages, sentences and **propositions**, short facts that each stand on their own. Look at the comparison tables: smaller, self-contained units retrieved better, and fitted more useful text into a fixed number of tokens. That's "Try this" 6, and the reason the 50-word windows failed: they were small, but not self-contained.
