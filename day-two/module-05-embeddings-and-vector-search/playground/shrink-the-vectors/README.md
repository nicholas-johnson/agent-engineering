# Shrink the vectors

Every vector in the module is 1,536 numbers long. You'll ask the API for shorter ones (512, 256 and 64 numbers) and see how much storage that saves and how much search gets worse.

From the module folder (`day-two/module-05-embeddings-and-vector-search`):

```bash
uv run python playground/shrink-the-vectors/play.py
```

Or without `uv` (set up `.venv` once at the repo root with `python3 -m venv .venv && .venv/bin/pip install -e .`):

```bash
source ../../.venv/bin/activate
python playground/shrink-the-vectors/play.py
```

Needs `OPENAI_API_KEY` in `.env`. The first run embeds the library once for each size and keeps the vectors in `playground/shrink-the-vectors/output/vectors.db`. The counts, and the rank of the right script for each request at each size, are written to `playground/shrink-the-vectors/output/results.json`.

---

The embeddings API takes a `dimensions` argument:

```python
client.embeddings.create(model=EMBEDDING_MODEL, input=batch, dimensions=256)
```

`text-embedding-3-small` is made so that a vector can be cut short and still work: the first numbers carry the most meaning, and later ones add detail. So the API can keep the first 256, rescale them so the vector has length 1 again, and hand those back. For each size, the script embeds the library (title + expected result, as in the demos), searches each of the 20 requests in `data/requests.json` on its own platform, as demo 4 does, and counts how often the right script comes first and how often it's in the top five. Storage assumes 4 bytes per number, the 32-bit floats that sqlite-vec stores.

```text
The 20 requests, searched at each size:

  Dimensions  Bytes per vector  A million vectors  Right script first  In the top 5
       1,536             6,144           6,144 MB                  11            18
         512             2,048           2,048 MB                   9            17
         256             1,024           1,024 MB                   7            17
          64               256             256 MB                   3             6
```

## Things to notice

- **A sixth of the size, nearly the same search.** At 256 numbers the top five still holds a right script for 17 of 20 requests, against 18 at full length. That 18 is the same as demo 4's vector search, because it is the same search.
- **First place suffers sooner than the top five.** Right first falls from 11 to 9 to 7 as the vectors shrink. The right script is still close, but something else is often closer.
- **64 is too few.** Six of 20. Somewhere between 256 and 64 the vectors stop holding enough to tell the scripts apart.
- **Size only matters at scale.** For this library the full vectors take 6 MB. A million scripts would take 6 GB, and a vector database wants to keep its vectors in memory to search fast. That's when 1 GB starts to look attractive.

## Try this

1. **Smaller still.** Add 128, 32 and 16 to `DIMENSIONS`. Where does search fall apart completely?
2. **Cut them yourself.** Check the claim above. Take the first 256 numbers of a 1,536-number vector, divide by their length so the vector has length 1, and compare the result with what `dimensions=256` returns. Are they the same?
3. **Fewer bits per number.** Keep all 1,536 numbers, but store only whether each one is positive or negative: 1 bit each, 192 bytes per vector, smaller than 64 full numbers. Compare vectors by counting the bits that differ. Which is better, 1,536 signs or 64 numbers?
4. **Time it.** Use `time.perf_counter()` to time the 20 searches at each size. Does halving the vector halve the time?
5. **Search short, then check long.** Use 64 numbers to pick the 50 closest scripts, then re-rank just those 50 with the full 1,536. How close do you get to the full search, and how much work did you save?
6. **The bigger model.** `text-embedding-3-large` returns 3,072 numbers. Ask it for 256. Does a cut-down large model beat the full small one?

## Questions

For discussion. There are no right answers.

- At 256 numbers the top five lost one request in twenty, but first place lost four. The agent in demo 5 reads the top five. Which number matters for it?
- Storage is cheap. Apart from size, why might you still want shorter vectors?
- Is it surprising that the first 256 numbers carry most of the meaning? What does it tell you about how the numbers are arranged?
- If you shrank the vectors and nobody noticed for a month, was it the right decision?

## Further reading

- **Kusupati, A., Bhatt, G., Rege, A., Wallingford, M., Sinha, A., Ramanujan, V., Howard-Snyder, W., Chen, K., Kakade, S., Jain, P. & Farhadi, A. (2022). "Matryoshka Representation Learning." _Advances in Neural Information Processing Systems 35 (NeurIPS 2022)_.** [arXiv:2205.13147](https://arxiv.org/abs/2205.13147). How to train embeddings so that the first numbers can stand on their own, like nested dolls. Figure 1 shows the idea; the retrieval experiments do Try this 5 (search short, then re-rank long) at scale.
- **OpenAI, [Vector embeddings](https://developers.openai.com/api/docs/guides/embeddings).** The section on reducing dimensions: the `dimensions` argument, and why a vector you shorten yourself has to be rescaled to length 1.

## Rabbit holes

Optional extensions and interesting things to look at.

1. **Shorter vectors inside the database.** sqlite-vec's [Matryoshka guide](https://alexgarcia.xyz/sqlite-vec/guides/matryoshka.html) uses `vec_slice()` and `vec_normalize()` to cut the full vectors down inside SQL. Store the 1,536 numbers once in demo 3's database, and search them at any length you like without calling the API again.
2. **Binary quantisation.** sqlite-vec's [binary quantisation guide](https://alexgarcia.xyz/sqlite-vec/guides/binary-quant.html) turns each number into one bit with `vec_quantize_binary()`, searches the bits, then re-scores the best candidates with the full vectors. Build it beside demo 3's table and compare its top five with the full search on the 20 requests.
