# Fusion knobs

Demo 4's hybrid search lost to vector search on its own: 15 against 18. You'll turn the knobs on the merge (rank fusion's `k`, how many candidates each search hands over, how much the keywords count, and a different way of merging) and see whether any setting rescues it.

From the module folder (`day-two/module-05-embeddings-and-vector-search`):

```bash
uv run python playground/fusion-knobs/play.py
```

Or without `uv` (set up `.venv` once at the repo root with `python3 -m venv .venv && .venv/bin/pip install -e .`):

```bash
source ../../.venv/bin/activate
python playground/fusion-knobs/play.py
```

Needs `OPENAI_API_KEY` in `.env`. The first run builds its own database, `playground/fusion-knobs/output/test-scripts.db`, the same way demo 4 does. After that each run only embeds the 20 requests, so trying a setting takes a few seconds. The top five from each search, for every request, are written to `playground/fusion-knobs/output/results.json`.

---

This is demo 4: SQLite's full-text search (BM25) and sqlite-vec, each returning its best `CANDIDATES` scripts on the request's platform, merged into one list. The settings sit at the top of the file:

| Setting | Demo 4 | What it does |
|---------|--------|--------------|
| `FUSION` | `"rank"` | `"rank"` is **reciprocal rank fusion**: only each script's place in each list counts. `"score"` uses the scores: each list is rescaled so its best is 1 and its worst is 0 (**min-max normalisation**), and the two are added |
| `RRF_K` | `60` | Rank fusion gives a script `weight / (k + rank)` from each list. A small `k` makes first place worth far more than tenth; a big one makes them nearly equal |
| `CANDIDATES` | `20` | How many results each search hands to the merge |
| `KEYWORD_WEIGHT` | `1.0` | How much the keyword list counts, against 1.0 for the vector list |

With demo 4's settings it gives demo 4's numbers:

```text
rank fusion, k = 60, 20 candidates each, keyword weight 1.0
A right script in the top 5, for 20 requests:
  keyword 12, vector 18, hybrid 15
```

The keyword and vector counts stay at 12 and 18, because the knobs don't change either search's top five. Here is the hybrid count for some other settings, each from a real run:

| `FUSION` | `RRF_K` | `CANDIDATES` | `KEYWORD_WEIGHT` | Hybrid |
|----------|---------|--------------|------------------|--------|
| rank | 60 | 20 | 1.0 | 15 (demo 4) |
| rank | 1 | 20 | 1.0 | 15 |
| rank | 1,000 | 20 | 1.0 | 15 |
| rank | 60 | 5 | 1.0 | 14 |
| rank | 60 | 50 | 1.0 | 16 |
| rank | 60 | 20 | 2.0 | 14 |
| rank | 60 | 20 | 0.5 | 16 |
| rank | 60 | 20 | 0.1 | 16 |
| rank | 1 | 20 | 0.5 | 17 |
| rank | 60 | 20 | 0.0 | 18 |
| score | | 20 | 1.0 | 15 |
| score | | 20 | 0.5 | 17 |

## Things to notice

- **`k` changed nothing.** 1, 60 and 1,000 all gave 15. It changes how much first place beats tenth, but on these requests the same scripts made the top five either way.
- **Trusting keywords less helps, and not trusting them at all helps most.** A keyword weight of 0.5 gives 16, or 17 with score fusion. A weight of 0 is just the vector search, and gets 18. Even 0.1 costs two requests.
- **Why it loses.** In `output/results.json`, look at "The thermostat says 21 but the room feels colder. Is its reading accurate?" Vector search puts the right script, TS-1465, first. Keyword search ranks it 62nd, outside its 20 candidates. Rank fusion gives TS-1465 just 1/61 from the vector list, and any script in both lists beats that. The hybrid's top five are all scripts the keyword search found, and TS-1465 isn't among them.
- **Nothing beat vector search alone.** The best merge found was 17. And if a setting had scored 19, see the first question below before believing it.

## Try this

1. **Fresh requests.** Write ten new requests with the IDs of the scripts that answer them. Find the best settings on `data/requests.json`, then run them on your ten. Do they still win?
2. **Leave one out.** Choose `KEYWORD_WEIGHT` using 19 of the requests, then test it on the 20th. Do that for each of the 20 in turn. How many does a search tuned this way get right on requests it was never tuned on?
3. **Raw scores.** Add a third `FUSION` that adds `-bm25` and the similarity without rescaling them. Print a few of each first. Why does it go wrong?
4. **Z-scores.** Instead of min-max, rescale each list by subtracting its mean score and dividing by its standard deviation. Does it change the count?
5. **Route by request.** Use a high keyword weight when the request contains an error code (`E-` followed by digits) and a low one otherwise. Is that cheating, or design?
6. **Other cut-offs.** Set `TOP = 1`, then `TOP = 10`. Is hybrid search better at one than the other?

## Questions

For discussion. There are no right answers.

- If you keep turning the knobs until hybrid scores 18 or 19, you've chosen the settings with the same 20 requests you're measuring them on. How much of that score would carry over to the next 20 requests? (Fitting your choices to the test is called **overfitting**, and it's how teams fool themselves.)
- One request is 5% of twenty. How big a difference would you need to see before changing a setting in a real system?
- Six of the twenty requests are error codes. Is that the mix your testers would really send? Who decides what goes in the test set?
- Keyword search never helped here. Is there still a reason to keep it?

## Further reading

- **Bruch, S., Gai, S. & Ingber, A. (2023). "An Analysis of Fusion Functions for Hybrid Retrieval." _ACM Transactions on Information Systems_.** [arXiv:2210.11934](https://arxiv.org/abs/2210.11934). Compares reciprocal rank fusion with a weighted sum of normalised scores (what this script calls `FUSION = "score"`) across several datasets. Look for two findings: the weighted sum did better, and rank fusion was sensitive to its parameters. They also find the weight can be tuned on a small set of examples, which is worth setting beside the first question above.
