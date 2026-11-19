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

Each sentence is turned into 1,536 numbers by `text-embedding-3-small`, as in demo 2, and each score is the **cosine similarity** of two of those vectors: near 1 when they point the same way, near 0 when they have nothing to do with each other. The list comes back closest first.

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

The API can return very slightly different vectors from one call to the next, so your scores may differ in the third decimal place. Two more from the same run, using the module's request and demo 3's error code:

```text
Sentence: Customers can't sign in after resetting their password

  0.867  Customers can sign in after resetting their password
  0.637  Log in with the new password after a password reset
  0.516  Password reset email arrives within two minutes
  0.444  Sign-in screen layout

Sentence: The display shows E-104

  0.838  The display shows E-401
  0.788  The display shows E-217
  0.520  The display shows a pairing error
  0.227  Pairing timed out
```

## Things to notice

- **Opposites score high.** "The heating works" scores 0.829 against "The heating doesn't work". That's higher than "The radiators are stone cold" (0.470) or "The boiler won't fire up" (0.523), which mean almost the same thing. An embedding records what a sentence is about (the heating, and whether it works) much more than what it says about it. In the second list, the opposite of the request (0.867) beats the script that answers it (0.637).
- **Other languages score well.** The German and French translations (0.766 and 0.759) score higher than the English sentences that say the same thing in other words. The Japanese one is lower, at 0.626.
- **Codes look alike.** E-104 means "pairing timed out" on a Dormouse. But "The display shows E-401" scores 0.838 and "Pairing timed out" only 0.227. The model has never seen Dormouse's error codes, so it sees "the display shows" plus a code. That's why demo 3 returned scripts for the wrong codes.
- **Unrelated isn't zero.** A cat and its sardines still score 0.127. The numbers live in a narrow band, so a score only means something next to other scores from the same model.

## Try this

1. **Your own pairs.** Try synonyms ("sign in" and "log in"), a typo, the same sentence in capitals, or an emoji. Which changes move the score most?
2. **Word order.** "The dog bit the man" and "The man bit the dog". Do embeddings notice who did what?
3. **Length.** Compare one word with a paragraph that contains it, then with a longer paragraph. Does extra text pull the score down?
4. **A list from the library.** Type a request, then paste the 20 titles from `data/test-scripts-small.json`, one per line. Do you agree with the order?
5. **The bigger model.** Set `EMBEDDING_MODEL = "text-embedding-3-large"` (3,072 numbers) and type the heating list again. Do opposites still score high? Are the numbers on the same scale?
6. **Records.** Find two sentences that mean opposite things and score above 0.95, and two that mean the same thing and score below 0.3.

## Questions

For discussion. There are no right answers.

- "The heating works" and "The heating doesn't work" scored 0.829. For a search engine, is that a bug? For which jobs would it not matter at all?
- A tester searches for "can't sign in" and gets the script for "can sign in" near the top. Whose job is it to notice: the search, the agent reading the results, or the tester?
- The German and French sentences scored higher than an English sentence with the same meaning. What does that suggest an embedding is recording?
- If scores don't sit on a fixed scale, how would you choose the score that counts as "similar enough"?
