# Word vectors

Demo 2 trained a small word2vec model on the user guide, with its settings fixed. Here they're all yours. You'll change what it reads, how many numbers each word gets and how wide its window is, retrain, and see which words end up next to which. Then you can type any word and see its closest words.

From the module folder (`day-two/module-05-embeddings-and-vector-search`):

```bash
uv run python playground/word-vectors/play.py
```

Or without `uv` (set up `.venv` once at the repo root with `python3 -m venv .venv && .venv/bin/pip install -e .`):

```bash
source ../../.venv/bin/activate
python playground/word-vectors/play.py
```

No API key needed: everything runs on your own computer, in plain Python. With the settings as they are, training takes about ten seconds. Then type a word and press Enter to see its closest words; an empty line stops. You can also pipe the words in:

```bash
printf 'boost\nsunrise\n\n' | uv run python playground/word-vectors/play.py
```

The vectors are written to `playground/word-vectors/output/vectors.txt`, one word per line followed by its numbers. The closest words for every word shown or typed, with their similarities and the settings that produced them, go in `playground/word-vectors/output/closest.json`.

---

The model is **skip-gram with negative sampling**, the same as demo 2. Every word starts with `SIZE` random numbers. Training reads the text one word at a time. For each word near it (up to `WINDOW` words either side), it nudges the two words' vectors closer together, and pushes the word away from `NEGATIVES` words picked at random. Words that keep turning up beside the same neighbours end up pointing the same way. This is the step that does it:

```python
for other, is_neighbour in [(tokens[j], 1)] + [(random.choice(noise), 0) for _ in range(NEGATIVES)]:
    neighbour = neighbours[other]
    step = rate * (is_neighbour - sigmoid(math.sumprod(vector, neighbour)))
    change = [c + step * n for c, n in zip(change, neighbour)]
    neighbours[other] = [n + step * v for n, v in zip(neighbour, vector)]
```

The settings are at the top of `play.py`. They start at demo 2's values:

| Setting | Starts at | What it does |
|---------|-----------|--------------|
| `DOCUMENTS` | `["user-guide"]` | Which documents to read: file names from `data/docs`, without `.md` |
| `SIZE` | 20 | How many numbers each word gets |
| `WINDOW` | 3 | How many words either side count as neighbours |
| `NEGATIVES` | 5 | How many random words are pushed away for each real neighbour |
| `MIN_COUNT` | 2 | Words seen fewer times than this get no vector |
| `EPOCHS` | 30 | How many times training reads the whole text |
| `LEARNING_RATE` | 0.05 | How big each nudge is at the start. It shrinks to nothing by the last epoch |
| `SEED` | 1 | Picks the random starting numbers and the random words, so a rerun gives the same result |

The arithmetic is written a little differently from demo 2's so that it runs faster, but with these settings it finds the same closest words. Here is a run, typing `boost` and `sunrise`:

```text
=== Trained on 1 document in 6 seconds: 1,794 words, 235 different words ===
  warm       wake, sunrise, heat, early, power
  boost      see, running, starts, button, press
  schedule   period, open, starts, temperature, four
  password   sign, network, link, account, cleaning
  heating    hours, switch, early, protection, for
  alarm      never seen

Word: boost
  see, running, starts, button, press
Word: sunrise
  wake, early, symbol, warm, snowflake
Word:
```

## What more text costs

Every word is compared with `2 × WINDOW` neighbours, each with `1 + NEGATIVES` updates of `SIZE` numbers, on every epoch. With the settings above that is about 1.9 million updates for the user guide's 1,794 words. Time grows with each of these: double the text, the window or the epochs and training takes about twice as long. Plain Python is slow at this. Measured on a Mac:

| Trained on | Words | Different words | Training time |
|------------|------:|----------------:|---------------|
| The user guide, as it starts | 1,794 | 235 | 6 to 9 seconds |
| The user guide and twelve Warm Wake, boost and schedule documents (Try this 3) | 6,361 | 473 | 25 to 28 seconds |
| All 275 documents | 147,382 | 1,899 | 694 seconds, about 11½ minutes |

That's about 250 words a second, or four seconds for every thousand words of text. The Mac was busy with other work during the long run, so yours may be a little quicker. To train on everything, set `DOCUMENTS = [p.stem for p in sorted(DOCS.glob("*.md"))]`. This is what it found, typing `boost`, `sunrise`, `wake` and `morning`:

```text
=== Trained on 275 documents in 694 seconds: 147,382 words, 1,899 different words ===
  warm       wake, sunrise, active, interacts, symbol
  boost      button, hour, configured, pressing, cancel
  schedule   edit, period, starts, tab, periods
  password   reset, forgot, forgotten, passwords, sign
  heating    activates, hours, off, while, protection
  alarm      never seen

Word: boost
  button, hour, configured, pressing, cancel
Word: sunrise
  symbol, warm, flame, unexpected, wake
Word: wake
  warm, sunrise, active, interacts, arrow
Word: morning
  half, degree, later, reflects, conflict
Word:
```

A real word2vec library does the same sums in compiled code, far faster (see Rabbit holes).

## Things to notice

- **Some neighbours make sense at once.** "warm" comes out next to wake, sunrise, heat and early. Warm Wake heats the home early and shows a sunrise symbol, and the model worked that out from 1,794 words and no dictionary.
- **Others are chance.** "password" comes out next to sign, network, link, account and cleaning. Set `SEED = 2` and "warm" keeps wake, heat, early and sunrise, but "password" gets a completely new list: android, ios, email, later and address. Both words appear about as often in the user guide (8 times and 7), but "warm" is almost always followed by "Wake", while "password" turns up in a different sentence every time.
- **More text fixes some words.** Trained on all 275 documents, where it appears 238 times, "password" sits next to reset, forgot, forgotten and passwords. Nobody told the model that "passwords" is the plural; it noticed they are used the same way. "boost" moves from see and running to button, hour and cancel.
- **But a word needs more than two sightings.** "morning" appears twice in all 275 documents. That passes `MIN_COUNT = 2`, so it gets a vector, but its neighbours are half, degree, later, reflects and conflict: noise.
- **"alarm" is never seen.** Not in the user guide, and not in any of the 275 documents, so no setting can give it a vector. It's the customer's word, not the documentation's. `text-embedding-3-small` in demo 3 has no such gap: it can turn any text into numbers.
- **Neighbours are used alike, not mean alike.** "boost" ends up next to button and pressing, because they appear in the same sentences ("press the boost button"). A neighbour is a word that turns up in the same places, which is often, but not always, a word that means something similar.

## Try this

1. **A wider window.** Set `WINDOW = 8`. Do the closest words become more about the topic and less about the words right next door?
2. **More numbers, or fewer.** Try `SIZE = 5`, then `SIZE = 100`. With only 1,794 words to learn from, do more numbers help?
3. **A dozen more documents.** Add twelve documents about the features in `WORDS` to `DOCUMENTS`: `understand-warm-wake`, `warm-wake-known-issue-register`, `thermostat-shows-the-sunrise-symbol`, `start-or-cancel-a-boost`, `boost-does-not-start`, `boost-stops-before-the-hour-ends`, `boost-uses-an-unexpected-temperature`, `change-the-boost-temperature`, `set-a-heating-schedule`, `understand-how-schedule-periods-work`, `copy-schedule-periods-to-another-day` and `schedule-periods-are-missing`. It takes about half a minute. How do "warm", "boost" and "schedule" change? What happens to "password", which none of them mention?
4. **Skip some of the "the"s.** "the" is nearly one word in ten, and teaches the model very little. Section 2.3 of the second paper below drops each appearance of a common word with a chance that grows with how common it is. Add that before training. Is it faster, and are the neighbours better?
5. **Word sums.** word2vec became famous for sums like king − man + woman ≈ queen. Add a few lines that work out a sum such as `warm − wake + boost` and find the closest word to the result. Do any sums work on 1,794 words? On all 275 documents?
6. **Document vectors.** Average each document's word vectors, as demo 3 does, and rank all 275 documents against the running question with cosine similarity. Where does Understand Warm Wake come? Which words of the question have no vector to add?

## Questions

For discussion. There are no right answers.

- With one seed, "password" sat next to "cleaning"; with another, next to "android". If a different random start gives different neighbours, what has the model learned about "password"?
- "alarm" is in none of the 275 documents, but it's the word the customer used. Should a search system learn its words from your documents, your customers' questions, or everybody's text?
- Training on all of the documentation took over eleven minutes here, and the closest words still weren't all good. When would you train your own vectors, and when would you pay for an embeddings API?
- "boost" ended up next to "button" and "pressing". Is that a good neighbour or a bad one? Who decides, and how would you test it?

## Further reading

- **Mikolov, T., Chen, K., Corrado, G. & Dean, J. (2013). "Efficient Estimation of Word Representations in Vector Space." [arXiv:1301.3781](https://arxiv.org/abs/1301.3781)**. The paper that introduced word2vec. Look at figure 1, the two small architectures (skip-gram is the one on the right), and at table 8, the word relationships. They trained on billions of words where this script reads under two thousand.
- **Mikolov, T., Sutskever, I., Chen, K., Corrado, G. & Dean, J. (2013). "Distributed Representations of Words and Phrases and their Compositionality." _Advances in Neural Information Processing Systems 26 (NIPS 2013)_, 3111–3119. [arXiv:1310.4546](https://arxiv.org/abs/1310.4546)**. Where negative sampling comes from. Read section 2.2: the random words are picked in proportion to how often they appear, raised to the power 3/4. That is the `counts[w] ** 0.75` line in the script. Section 2.3 drops very common words such as "the" some of the time, which is Try this 4.

## Rabbit holes

Optional extensions and interesting things to look at.

1. **The same model, fast.** [gensim's `Word2Vec`](https://radimrehurek.com/gensim/models/word2vec.html) trains this model in compiled code. With `sg=1` it is skip-gram, and its `vector_size`, `window`, `negative`, `min_count`, `epochs`, `alpha` and `seed` are this script's settings under other names. It isn't one of the course's packages, so run your script with `uv run --with gensim python ...`. Train it on all 275 documents, and compare its closest words and its time with this script's.
2. **Someone else's vectors.** gensim can also download vectors that other people trained. `word2vec-google-news-300` has 3,000,000 words and phrases with 300 numbers each, trained on about 100 billion words of Google News (a 1.6 GB download); `glove-wiki-gigaword-50` is a smaller set, trained on Wikipedia and news text (65 MB). Look up "alarm", "thermostat" and "boost". What do they know that the Dormouse documents don't, and what have they never heard of?
