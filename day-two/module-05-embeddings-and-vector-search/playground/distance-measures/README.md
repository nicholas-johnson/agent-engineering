# Distance measures

There's more than one way to say how close two vectors are. You'll rank all 275 Dormouse documents against the module's question in three ways, with **cosine similarity**, the **dot product** and straight-line **distance**, on two kinds of vector, and see when the choice matters and when it makes no difference.

From the module folder (`day-two/module-05-embeddings-and-vector-search`):

```bash
uv run python playground/distance-measures/play.py
```

Or without `uv` (set up `.venv` once at the repo root with `python3 -m venv .venv && .venv/bin/pip install -e .`):

```bash
source ../../.venv/bin/activate
python playground/distance-measures/play.py
```

Needs `OPENAI_API_KEY` in `.env`. The first run embeds the question and the 275 documents with `text-embedding-3-small`, which took about four seconds, and keeps the vectors in `playground/distance-measures/output/vectors.db`. Later runs take a second or two and don't call the API for them again. Every document's score and rank under each measure, for both kinds of vector, is written to `playground/distance-measures/output/results.json`.

---

The script turns the question and every document into two kinds of vector:

- **Word-count vectors**: one number for each of 2,493 different words (the 2,491 that the documentation uses, plus "my" and "alarm" from the question), saying how many times the text uses that word. It's one of the oldest ways of turning a text into a vector for search (see Further reading).
- **Embeddings** from `text-embedding-3-small`, as in demos 4 and 5: 1,536 numbers each.

A vector's **length** is the square root of the sum of its numbers squared: how far its point is from zero. A word-count vector gets longer as its document does. The user guide's has length 224.7; a 49-word release note's, 8.7. An embedding has length 1 (very nearly: see Things to notice), however long the text. Then the script ranks the documents three ways:

```python
def cosine_similarity(a, b):
    # The angle between the vectors, ignoring their lengths. Higher is closer.
    return math.sumprod(a, b) / (length(a) * length(b))


def dot_product(a, b):
    # Like cosine similarity, but multiplied by both lengths. Higher is closer.
    return math.sumprod(a, b)


def distance(a, b):
    # Straight-line (Euclidean) distance between the two points. Lower is closer.
    return math.dist(a, b)
```

Cosine similarity divides the dot product by both lengths, so length cancels out and only the direction counts. The dot product keeps the lengths, so a long vector scores high. Distance treats each vector as a point and measures the gap between the points, so a long vector is a long way from a short one even when they point the same way. When every vector has length 1, the three should agree: the dot product _is_ the cosine similarity, and distance squared is 2 − 2 × cosine similarity, so the order is the same (lowest first for distance). In the output, `words` is the document's length in words, and `length` is its vector's length.

```text
=== Word counts: one number for each of 2,493 words ===
Q: Why is the heating already on before my alarm goes off?

  Cosine similarity (higher is closer)
        score  words   length
        0.452    445   66.068  Heating Starts Below Five Degrees
        0.422    120   20.000  Understand frost protection
        0.416    804   99.940  Frost Protection Safety Behaviour QA Report

  Dot product (higher is closer)
        score  words   length
      257.000   1794  224.704  Dormouse Thermostat User Guide
      197.000   1394  186.601  Boost Temperature Configuration Support Playbook
      187.000   1579  166.472  Thermostat Firmware 4.1 Baseline

  Distance (lower is closer)
        score  words   length
        9.055     49    8.660  Firmware 3.3 release notes
        9.381     45    9.110  Firmware 4.1 release notes
       11.619     72   11.916  Firmware 3.5 release notes

=== text-embedding-3-small: 1,536 numbers, length 1 ===
Q: Why is the heating already on before my alarm goes off?

  Cosine similarity (higher is closer)
        score  words   length
        0.488     99    1.000  Understand Warm Wake
        0.455    445    1.000  Heating Starts Below Five Degrees
        0.427    299    1.000  Set a heating schedule

  Dot product (higher is closer)
        score  words   length
        0.488     99    1.000  Understand Warm Wake
        0.455    445    1.000  Heating Starts Below Five Degrees
        0.427    299    1.000  Set a heating schedule

  Distance (lower is closer)
        score  words   length
        1.012     99    1.000  Understand Warm Wake
        1.044    445    1.000  Heating Starts Below Five Degrees
        1.070    299    1.000  Set a heating schedule
```

The word counts come out the same every time. The API can return very slightly different embeddings from one call to the next, so if you delete the cache your scores may differ in the third decimal place.

## Things to notice

- **The dot product picks the longest documents.** Its top three on word counts are the three longest in the library. The user guide scores 257, and 171 of that is the word "the". The ten documents it ranks highest have a median of 1,188 words, against 493 for the whole library. Understand Warm Wake, the right answer, comes 247th of 275.
- **Distance picks the shortest.** Its top three are three of the four shortest documents. Firmware 3.3 release notes has only one word in common with the question, "the", used twice, but at 49 words its point sits close to the question's short vector. Distance's top ten have a median of 86.5 words. The right document happens to be short too (99 words), so distance ranks it 18th: better than cosine similarity does, by luck.
- **Cosine similarity ignores length, but not "the".** Its top three run from 120 words to 804. They're all about frost protection, heating that comes on when you'd turned it off, and they share "is", "the", "heating", "on" and "off" with the question. Every word counts the same, so "the" is worth as much as "heating". No document contains "my" or "alarm" at all. Understand Warm Wake comes 64th. Fixing length didn't fix meaning.
- **With embeddings, the three agree.** Same top three, in the same order, with Understand Warm Wake first. All three put the same seven documents at the top.
- **But not all the way down.** OpenAI's embeddings guide says "Cosine similarity and Euclidean distance will result in the identical rankings", because its vectors have length 1. Here the lengths run from 0.9993 to 1.0006. That's enough to swap documents whose scores differ only in the fourth decimal place. Cosine similarity puts Thermostat Shows the Sunrise Symbol 8th and Understand heating history retention 9th (both 0.4008); the dot product puts them the other way round. Distance first disagrees with cosine similarity at 12th. No document moves more than two places.

## Try this

1. **Another question.** Set `QUESTION` to "There's a little sun on the screen", or another question from `data/questions.json`. Does the dot product still pick the longest documents, and distance the shortest?
2. **Leave out the small words.** Skip common words such as "the", "is", "on" and "my" when counting (a **stop-word** list). Which measure changes most?
3. **Make the counts length 1.** Divide every word-count vector by its length before comparing. Do the three measures now agree, as they do for embeddings?
4. **Weight by rarity.** Multiply each count by demo 1's `rarity`, so that "the" is worth almost nothing and "wake" a lot. Does cosine similarity find Understand Warm Wake now?
5. **Exactly length 1.** Divide each embedding by its own length too. Do the three orders now match all the way down the 275?
6. **All 20 questions.** For each kind of vector and each measure, count how often a document from `expected` in `data/questions.json` makes the top three. Is any measure good on word counts?

## Questions

For discussion. There are no right answers.

- The dot product put the 1,794-word user guide first, mostly because it says "the" 171 times. Is a long document more likely to be useful, or only more likely to match?
- Cosine similarity fixed the length problem and still put the right document 64th. What was really wrong: the measure, or the vectors?
- With embeddings, the measures only disagreed about documents whose scores differed in the fourth decimal place. Could that ever matter to a customer?
- A vector database asks you to choose a measure when you create a collection. Who should choose, and how would you find out it was the wrong one?

## Further reading

- **Salton, G., Wong, A. & Yang, C. S. (1975). "A vector space model for automatic indexing." _Communications of the ACM_ 18(11):613–620.** [doi:10.1145/361219.361220](https://doi.org/10.1145/361219.361220). Documents as word-count vectors, compared by the angle between them. Look at figure 1, where three words are the three axes of the space. They weight each count by how rare the word is, which is Try this 4.
- **OpenAI, [Vector embeddings](https://developers.openai.com/api/docs/guides/embeddings).** The FAQ "Which distance function should I use?": why it recommends cosine similarity, and why it says that for its embeddings the choice makes little difference.

## Rabbit holes

Optional extensions and interesting things to look at.

1. **The measure inside ChromaDB.** Demo 6 creates its collection with `configuration={"hnsw": {"space": "cosine"}}`. ChromaDB's other choices are `"l2"`, distance squared, which is its default, and `"ip"` (inner product), which is one minus the dot product. Build demo 6's collection once with each and compare the top three for the running question. Then store the word-count vectors from this script instead, and watch the three come apart.
2. **pgvector's operators.** [pgvector](https://github.com/pgvector/pgvector) adds vectors to PostgreSQL and gives each measure its own operator: `<->` for distance, `<#>` for the dot product and `<=>` for cosine distance. Its README says that for vectors of length 1, like OpenAI's, you should use the dot product because it's fastest. Read its Querying section, then find out from the README why `<#>` returns the dot product with its sign flipped.
