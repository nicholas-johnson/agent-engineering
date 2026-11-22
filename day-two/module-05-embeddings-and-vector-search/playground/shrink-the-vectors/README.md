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

Needs `OPENAI_API_KEY` in `.env`. The first run embeds the library once for each size, which takes about ten seconds, and keeps the vectors in `playground/shrink-the-vectors/output/vectors.db`. The counts, and the rank of the right document for each question at each size, are written to `playground/shrink-the-vectors/output/results.json`.

---

The embeddings API takes a `dimensions` argument:

```python
client.embeddings.create(model=EMBEDDING_MODEL, input=batch, dimensions=256)
```

`text-embedding-3-small` is made so that a vector can be cut short and still work: the first numbers carry the most meaning, and later ones add detail. So the API can keep the first 256, rescale them so the vector has length 1 again, and hand those back. For each size, the script embeds all 275 documents whole, as demos 5 and 6 do, and searches the whole library for each of the 20 questions in `data/questions.json`. It counts how often a right document comes first and how often one is in the top five. Storage assumes 4 bytes per number, the 32-bit floats that ChromaDB stores.

```text
The 20 questions, searched at each size:

  Dimensions  Bytes per vector  A million vectors  Right document first  In the top 5
       1,536             6,144           6,144 MB                    15            19
         512             2,048           2,048 MB                    15            19
         256             1,024           1,024 MB                    12            18
          64               256             256 MB                    12            15
```

## Things to notice

- **A third of the size, the same search.** At 512 numbers the counts don't change at all: 15 first and 19 in the top five, as at full length. The full-length row is demo 5's search over all the documentation, run for twenty questions instead of one.
- **Even 64 numbers do better than you might expect.** A right document is still in the top five for 15 of 20 questions. The documents are about quite different things (boost, returns, Wi-Fi, warranties), so even a rough vector can probably tell many of them apart.
- **Shrinking reshuffles; it doesn't only lose.** In `output/results.json`, the module's question goes 1st, 2nd, 3rd and back to 1st at 64 numbers. "Can I ask Alexa to turn the heating up?" goes 8th, 3rd, 4th, then 1st: better at 64 numbers than at full length. Meanwhile "It thinks we're out when we're sitting at home" falls from 1st to 46th, and the new broadband router question from 1st to 20th. Twenty questions is a small test, and a single question moving is as much luck as signal.
- **Size only matters at scale.** For this library the full vectors take under 2 MB (275 × 6,144 bytes). A million would take 6 GB, and ChromaDB needs its whole index in memory. That's when 1 GB starts to look attractive.

## Try this

1. **Smaller still.** Add 128, 32 and 16 to `DIMENSIONS`. Where does search fall apart completely?
2. **Cut them yourself.** Check the claim above. Take the first 256 numbers of a 1,536-number vector, divide by their length so the vector has length 1, and compare the result with what `dimensions=256` returns. Are they the same?
3. **Fewer bits per number.** Keep all 1,536 numbers, but store only whether each one is positive or negative: 1 bit each, 192 bytes per vector, smaller than 64 full numbers. Compare vectors by counting the bits that differ. Which is better, 1,536 signs or 64 numbers?
4. **Time it.** Use `time.perf_counter()` to time the 20 searches at each size. Does halving the vector halve the time?
5. **Search short, then check long.** Use 64 numbers to pick the 20 closest documents, then re-rank just those 20 with the full 1,536. How close do you get to the full search, and how much work did you save?
6. **The bigger model.** `text-embedding-3-large` returns 3,072 numbers. Ask it for 512. Does a cut-down large model beat the full small one?

## Questions

For discussion. There are no right answers.

- At 512 numbers nothing changed on these twenty questions. Is that enough to make the switch? What would you want to test first?
- At 64 numbers the Alexa question came first, and at full length it came eighth. Does that make 64 better? What does it say about judging a change on twenty questions?
- Storage is cheap. Apart from size, why might you still want shorter vectors?
- If you shrank the vectors and nobody noticed for a month, was it the right decision?

## Further reading

- **Kusupati, A., Bhatt, G., Rege, A., Wallingford, M., Sinha, A., Ramanujan, V., Howard-Snyder, W., Chen, K., Kakade, S., Jain, P. & Farhadi, A. (2022). "Matryoshka Representation Learning." _Advances in Neural Information Processing Systems 35 (NeurIPS 2022)_.** [arXiv:2205.13147](https://arxiv.org/abs/2205.13147). How to train embeddings so that the first numbers can stand on their own, like nested dolls. Figure 1 shows the idea; the adaptive retrieval experiments do Try this 5 (search short, then re-rank long) at scale.
- **OpenAI, [Vector embeddings](https://developers.openai.com/api/docs/guides/embeddings).** The section on reducing embedding dimensions: the `dimensions` argument, and why a vector you shorten yourself has to be rescaled to length 1.

## Rabbit holes

Optional extensions and interesting things to look at.

1. **How much memory a vector database wants.** ChromaDB's [Single-Node Performance](https://docs.trychroma.com/guides/deploy/performance) guide says the index must sit in RAM, and gives a rule of thumb for how many 1,024-number vectors fit in a given amount of memory. Work out what it means for 1,536 numbers and for 256. Then build demo 6's database a second time with `dimensions=256` vectors, and see which of the files in its folder shrink.
2. **Eight bits instead of thirty-two.** Hugging Face's post [Binary and Scalar Embedding Quantization for Significantly Faster & Cheaper Retrieval](https://huggingface.co/blog/embedding-quantization) (Shakir, Aarsen and Lee, 2024) turns each number into a whole number from -128 to 127, using that number's smallest and largest values in a sample of vectors. That is a quarter of the size, without cutting any numbers off. Try it on the 275 documents, with the post's trick of fetching a few more results than you need and re-scoring them with the full-precision question vector, and compare it with 512 numbers at full precision.
