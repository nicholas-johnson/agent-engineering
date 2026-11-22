# Similarity explorer

Type two sentences and see how similar their embeddings are. You'll find pairs that mean the same thing and score low, and pairs that mean the opposite and score high.

From the module folder (`day-two/module-05-embeddings-and-vector-search`):

```bash
uv run python playground/similarity-explorer/play.py
```

Or without `uv` (set up `.venv` once at the repo root with `python3 -m venv .venv && .venv/bin/pip install -e .`):

```bash
source ../../.venv/bin/activate
python playground/similarity-explorer/play.py
```

Needs `OPENAI_API_KEY` in `.env`. Type a sentence, then one or more sentences to compare it with, pressing Enter after each. An empty line ends the list and shows the scores. An empty line at `Sentence:` stops. Every comparison is saved to `playground/similarity-explorer/output/similarities.json`.

You can also pipe the lines in:

```bash
printf 'The heating works\nThe heating does not work\n\n\n' | uv run python playground/similarity-explorer/play.py
```

---

Each sentence is turned into 1,536 numbers by `text-embedding-3-small`, as in demo 4, and each score is the **cosine similarity** of two of those vectors, as in demo 5: near 1 when they point the same way, near 0 when they have nothing to do with each other. The list comes back closest first.

```text
Sentence: The heating doesn't work
  Compare with: The heating works
  Compare with: The heating isn't working
  Compare with: The radiators are stone cold
  Compare with: The boiler won't fire up
  Compare with: Le chauffage ne marche pas
  Compare with: Die Heizung funktioniert nicht
  Compare with: 暖房が動かない
  Compare with: My cat likes sardines
  Compare with:

  0.939  The heating isn't working
  0.829  The heating works
  0.766  Die Heizung funktioniert nicht
  0.759  Le chauffage ne marche pas
  0.626  暖房が動かない
  0.523  The boiler won't fire up
  0.470  The radiators are stone cold
  0.127  My cat likes sardines
```

The API can return very slightly different vectors from one call to the next, so your scores may differ in the third decimal place. Two more from the same run. The first compares the module's running question with titles from `data/docs/` and the first sentence of `understand-warm-wake`, the document that answers it. The second compares an error code with the titles of error-code documents:

```text
Sentence: Why is the heating already on before my alarm goes off?

  0.900  Why isn't the heating on before my alarm goes off?
  0.617  Warm Wake is a heating feature that starts the heating before a schedule period.
  0.542  Set a heating schedule
  0.381  Understand Warm Wake
  0.375  Thermostat Shows the Sunrise Symbol
  0.245  Enter your boiler size for energy reports

Sentence: The display shows E-104

  0.700  Thermostat Shows E-104
  0.583  Thermostat Shows E-401
  0.583  Thermostat Shows E-217
  0.436  Resolve error E-104: Pairing timed out
  0.227  Pairing timed out
```

## Things to notice

- **Opposites score high.** "The heating works" scores 0.829 against "The heating doesn't work". That's higher than "The radiators are stone cold" (0.470) or "The boiler won't fire up" (0.523), which mean almost the same thing. An embedding records what a sentence is about (the heating, and whether it works) much more than what it says about it. In the second list, the question that asks the opposite (0.900) beats the sentence that answers it (0.617).
- **Other languages score well.** The German and French translations (0.766 and 0.759) score higher than the English sentences that say the same thing in other words. The Japanese one is lower, at 0.626.
- **A name means nothing until it's explained.** "Understand Warm Wake" and "Thermostat Shows the Sunrise Symbol" are the titles of the two right documents, but they score 0.381 and 0.375, below "Set a heating schedule" (0.542). Warm Wake is a Dormouse name the model has never seen. The first sentence of Understand Warm Wake says what it does, and scores 0.617. That's one reason the module embeds each document whole, not just its title.
- **Codes look alike.** E-104 means "pairing timed out" on a Dormouse. "Thermostat Shows E-104" does come first, at 0.700, but the titles for two other codes score 0.583 each, well above the title of the page that resolves E-104 (0.436). "Pairing timed out" on its own scores only 0.227. The model has never seen Dormouse's error codes, so it mostly sees "the thermostat shows" plus a code. An exact code is a job for keyword search, as in demo 1.
- **Unrelated isn't zero.** A cat and its sardines still score 0.127. The numbers live in a narrow band, so a score only means something next to other scores from the same model.

## Try this

1. **Your own pairs.** Try synonyms ("sign in" and "log in"), a typo, the same sentence in capitals, or an emoji. Which changes move the score most?
2. **Word order.** "The dog bit the man" and "The man bit the dog". Do embeddings notice who did what?
3. **Length.** Compare one word with a paragraph that contains it, then with a longer paragraph. Does extra text pull the score down?
4. **A list from the documentation.** Type a question from `data/questions.json`, then paste a dozen document titles, one per line (`sed -n 's/^title: //p' data/docs/*.md` lists all 275). Do you agree with the order? Then try each document's first sentence instead of its title.
5. **The bigger model.** Set `EMBEDDING_MODEL = "text-embedding-3-large"` (3,072 numbers) and type the heating list again. Do opposites still score high? Are the numbers on the same scale?
6. **Records.** Find two sentences that mean opposite things and score above 0.95, and two that mean the same thing and score below 0.3.

## Questions

For discussion. There are no right answers.

- "The heating works" and "The heating doesn't work" scored 0.829. For a search engine, is that a bug? For which jobs would it not matter at all?
- "Understand Warm Wake" scored lower against the customer's question than "Set a heating schedule". Who is a document's title for: the customer, the support team or the search? Would you change it?
- The German and French sentences scored higher than an English sentence with the same meaning. What does that suggest an embedding is recording?
- If scores don't sit on a fixed scale, how would you choose the score that counts as "similar enough"?

## Further reading

- **Neelakantan, A. et al. (2022). "Text and Code Embeddings by Contrastive Pre-Training." [arXiv:2201.10005](https://arxiv.org/abs/2201.10005)** How OpenAI trained its earlier embedding models: pairs of texts that belong together are pulled close, and unrelated texts pushed apart. Look at how the training pairs are made (neighbouring pieces of text on the internet), and think about why a sentence and its opposite, which turn up in the same places, end up close.
- **Sciavolino, C., Zhong, Z., Lee, J. & Chen, D. (2021). "Simple Entity-Centric Questions Challenge Dense Retrievers." *EMNLP 2021*, 6138–6148. [arXiv:2109.08535](https://arxiv.org/abs/2109.08535)** Embedding search does badly on names it rarely saw in training, which is the Warm Wake and E-104 problem. Look at table 1, where BM25 beats a dense retriever on simple questions such as where a person was born.
