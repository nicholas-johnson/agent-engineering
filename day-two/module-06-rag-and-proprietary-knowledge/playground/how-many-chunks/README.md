# How many chunks

Demo 3 gives the model the five nearest chunks. Why five? Here you'll try every number from 1 to 20 on the 24 answerable questions, and set what each extra chunk finds against the tokens, and dollars, it adds to every question.

From the module folder (`day-two/module-06-rag-and-proprietary-knowledge`):

```bash
uv run python playground/how-many-chunks/play.py
```

Or without `uv` (set up `.venv` once at the repo root with `python3 -m venv .venv && .venv/bin/pip install -e .`):

```bash
source ../../.venv/bin/activate
python playground/how-many-chunks/play.py
```

Needs `OPENAI_API_KEY` in `.env`. The first run embeds all 1,823 chunks and keeps them in a ChromaDB store in `playground/how-many-chunks/output/chroma`. That took 13 minutes when I ran it, with the embeddings API slow and other scripts embedding at the same time; on a quiet day it's a couple of minutes. After that, a run embeds the 24 questions and counts tokens. Each row of the table, and the rank of each question's first right chunk, are written to `playground/how-many-chunks/output/results.json`.

---

Each question's 20 nearest chunks are found once. `TOP` then runs from 1 to 20: a question counts as found if one of its first `TOP` chunks contains its facts, as in demo 3. "Tokens in" is the whole prompt demo 3 would send, averaged over the 24 questions, counted by the API without running the model. The dollars are those tokens at `gpt-6-luna`'s $0.10 per million input tokens, from Module 4's price list (checked 10 November 2026).

To save 480 calls, the script counts the instructions and questions once, then all 24 first chunks together, then all 24 second chunks, and adds them up. When I counted the 24 prompts for `TOP = 5` one at a time instead, they averaged 620 tokens, against the script's 612: close enough.

```text
   TOP  Facts in the top TOP, of 24  Tokens in   Per question
     1   16  ################               156      $0.000016
     2   18  ##################             272      $0.000027
     3   21  #####################          388      $0.000039
     4   22  ######################         496      $0.000050
     5   22  ######################         612      $0.000061
     6   23  #######################        729      $0.000073
     7   23  #######################        844      $0.000084
     8   23  #######################        943      $0.000094
     9   23  #######################      1,066      $0.000107
    10   24  ########################     1,182      $0.000118
    11   24  ########################     1,303      $0.000130
    12   24  ########################     1,415      $0.000142
    13   24  ########################     1,539      $0.000154
    14   24  ########################     1,655      $0.000165
    15   24  ########################     1,765      $0.000177
    16   24  ########################     1,883      $0.000188
    17   24  ########################     2,003      $0.000200
    18   24  ########################     2,114      $0.000211
    19   24  ########################     2,233      $0.000223
    20   24  ########################     2,359      $0.000236

  Embedding each question costs $0.00000026, whatever TOP is.
```

## Things to notice

- **The first chunk is right two times in three.** 16 of 24. Three chunks get 21; after that, each extra one finds less.
- **The cost grows in a straight line; the answers don't.** Every chunk adds about 115 tokens. Going from 5 to 10 doubles the tokens and finds two more questions. Going from 10 to 20 doubles them again and finds nothing.
- **The two late arrivals.** The Warm Wake question, demo 3's own, has its first right chunk 6th, behind five chunks about smart-home routines, so it's missed at `TOP = 5`. The geofencing question ("The heating turns down every time I nip out to the shops") comes 10th. Both are in `output/results.json`.
- **Retrieval is nearly free.** Embedding a question costs $0.00000026. Even at `TOP = 20`, the model's input is the bill, and at $0.000236 a question that's still about 80 times cheaper than putting the whole knowledge base in the prompt (see [long-context-or-rag](../long-context-or-rag/)).
- **Found isn't answered.** This counts whether the facts were in the chunks the model was given, not whether its answer used them. Twenty chunks of mostly irrelevant text give the model more to get confused by, as Liu et al. found (below). Measuring that needs the answers, as [grounding-rules](../grounding-rules/) does.

## Try this

1. **Answers, not chunks.** For `TOP` = 3, 5, 10 and 20, ask `gpt-6-luna` each question with that many chunks and check its answer with `contains_facts`, as demo 6 does. Does the right-answer count follow the found count, or fall off at 20?
2. **Order matters?** At `TOP = 10`, put the nearest chunk last instead of first. Do the answers change?
3. **A similarity cut-off.** Instead of a fixed `TOP`, keep every chunk within 0.05 of the best one's similarity. How many chunks does each question get, and how many are found?
4. **A pricier model.** Set `INPUT_PRICE` to a frontier model's price from Module 4's `data/prices.json`. At what price does `TOP = 10` stop being an easy choice?
5. **Better chunks, not more.** Use [chunk-headings](../chunk-headings/) or [chunk-sizes](../chunk-sizes/) to change the chunks, then come back. Does the curve rise faster?
6. **Rerank.** Take the top 20 and ask `gpt-6-luna` to pick the five most useful for the question, then send only those. Does a **reranker** reach 24 for the price of five chunks plus one extra call?

## Questions

For discussion. There are no right answers.

- Ten chunks found all 24; five found 22, for half the tokens. Which would you choose, and would your answer change at a million questions a day?
- At these prices, `TOP = 20` costs a fraction of a cent a question. When is the cost of extra chunks money, and when is it something else: time, or a model distracted by text it doesn't need?
- The Warm Wake question was 6th. Is that a problem to fix with a bigger `TOP`, or a sign that the chunks or the documents need fixing?
- These 24 questions were written for this course. How would you find out what `TOP` your real customers' questions need?

## Further reading

- **Liu, N. F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M., Petroni, F. & Liang, P. (2024). "Lost in the Middle: How Language Models Use Long Contexts." _Transactions of the Association for Computational Linguistics_ 12:157–173.** [arXiv:2307.03172](https://arxiv.org/abs/2307.03172). Gives models 10, 20 or 30 documents with the answer in one of them, and moves that document around. Look at the U-shaped curves in the multi-document question answering section: models did best when the answer came first or last and worst when it was in the middle, and more documents didn't always help. That's what "Found isn't answered" means, and "Try this" 2 tests it here.
