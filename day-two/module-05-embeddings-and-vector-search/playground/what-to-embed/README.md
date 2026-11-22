# What to embed

Before you can search by meaning, you have to decide what text stands for each document. You'll embed the Dormouse documentation four ways and see where the right document lands for twenty customer questions.

From the module folder (`day-two/module-05-embeddings-and-vector-search`):

```bash
uv run python playground/what-to-embed/play.py
```

Or without `uv` (set up `.venv` once at the repo root with `python3 -m venv .venv && .venv/bin/pip install -e .`):

```bash
source ../../.venv/bin/activate
python playground/what-to-embed/play.py
```

Needs `OPENAI_API_KEY` in `.env`. The first run embeds the library four ways (about 1,100 texts) and takes about ten seconds. It keeps the vectors in `playground/what-to-embed/output/vectors.db`, so later runs take a couple of seconds. The rank of the right document, and the top five for each way, are written to `playground/what-to-embed/output/ranks.json`.

---

Demos 5 and 6 embed each document whole: all of its Markdown after the front matter. That is about 149,000 words for 275 documents. This playground tests that choice. Each document is turned into text four ways:

```python
WAYS = {
    "whole document": whole_document,
    "title": title,
    "title + headings": title_and_headings,
    "title + opening": title_and_opening,
}
```

- **whole document**: what the demos embed
- **title**: the `title` from the front matter, such as "Understand Warm Wake"
- **title + headings**: the title, then every `##` and `###` heading, one per line. An outline of the document.
- **title + opening**: the title, then the first paragraph of text that isn't a heading

Then every question in `data/questions.json` is compared with all 275 documents, and the table shows where the best right document lands: 1 means first. A question counts as a hit if a right document is in the top five. The module's own question comes first, on its own.

```text
Where the right document lands (1 = first), searching all 275 documents:

  Question                                                whole document             title  title + headings   title + opening
  Why is the heating already on before my alarm g...                   1                18                11                 1

  The heating came on while we were away in winte...                   1                 6                 2                 3
  I got a new broadband router and now the thermo...                   1                 1                 2                 1
  There's a little sun on the screen                                   1                 1                 1                 1
  The radiator in the spare room stays cold                            1                 1                 2                 1
  Can my partner control the heating from their p...                   2                10                17                 8
  I forgot my password and can't get into the app                      1                 1                 1                 1
  The screen on the thermostat is completely blank                     1                 1                 1                 1
  What happens to my heating if there's a power cut?                   1                 1                 1                 1
  I pressed the button for an hour of extra heat ...                   1                62                 1                 1
  The extra hour of heat stopped after twenty min...                   1                 1                 2                 1
  I turned it up to 22 but later it went back dow...                   5                 6                 8                 2
  It thinks we're out when we're sitting at home                       1                 4                 3                 1
  How do I make it heat less while we're on holiday?                   2                 2                 1                 3
  Can I send it back if I don't like it?                               1                 1                 1                 1
  How long is it guaranteed for?                                       1                 1                 1                 1
  It says 21 degrees but the room feels freezing                       1                 1                 1                 1
  Can I ask Alexa to turn the heating up?                              8                20                 1                 2
  The thermostat restarted itself in the middle o...                   1                 1                 1                 1
  How do I wipe it before I sell the house?                            2                 2                 2                 2

  A right document in the top 5, of 20                                19                14                17                19
  Words embedded                                                 148,705             1,508             8,201             9,849
```

The progress line says 274 titles, not 275: two documents are both called "Understand heating history retention", and the cache only embeds the same text once. If you delete `output/` and run again, a rank may move by one place. The API doesn't always return exactly the same numbers for the same text, and on one fresh run the partner question's title rank was 11, not 10.

## Things to notice

- **On the module's question, the title fails.** "Understand Warm Wake" lands 18th. The name of a feature says nothing about heating that comes on before an alarm. The headings ("What Warm Wake does", "The sunrise symbol", "When it is not active") only lift it to 11th. The opening paragraph says what the feature does, that it "starts the heating before a schedule period", and that's enough for first place.
- **Title + opening ties the whole document.** Both put a right document in the top five for 19 of 20 questions, and both put one first for about three-quarters of them (15 for the whole document, 14 for title + opening). Title + opening does it with 9,849 words against 148,705, about a fifteenth.
- **Titles use Dormouse's words; customers use their own.** "I pressed the button for an hour of extra heat but nothing happened" is answered by "Boost Does Not Start", which lands 62nd on its title. The customer never says "boost". Every other way finds it first, because the document goes on to say "Check use of the boost button" and "pressing the boost button does not appear to start heating".
- **A long document can drown its own point.** The voice assistant guide never mentions Alexa, and many of its 691 words go on accounts, Wi-Fi and what to do when the thermostat is offline. Whole, it lands eighth for "Can I ask Alexa to turn the heating up?", behind pages about boost and schedules. Its outline ("Connect the voice assistant", "Change the target temperature by voice") puts it first. Splitting long documents into pieces is Module 6's job.
- **The partner question is the hardest.** "Can my partner control the heating from their phone too?" lands 2nd, 10th, 17th and 8th. The short ways bring up the app's heating-settings screens first, because the question says "phone" and "heating". The household documents that answer it talk about invitations and members instead.
- **The customer filter changes almost nothing.** With `CUSTOMERS_ONLY = True` the hits stay 19, 14, 17 and 19, and only three ranks move up one place. The documents that get in the way are other customer documents, not internal ones.

## Try this

1. **The opening alone.** Add a fifth way that embeds only the opening paragraph, with no title. How much was the title adding?
2. **Different cut-offs.** Set `TOP = 1`, then `TOP = 10`. Which way is best at putting the right document first?
3. **Say what kind of document it is.** Every document's front matter has a `type`, such as `troubleshooting` or `policy`. Add a way that puts it in front: `f"{document['type']}: {document['title']}\n{opening_paragraph(document)}"`. Does it help the questions that describe something going wrong?
4. **Your own questions.** Add five questions to the list after it is loaded, with the ids (file names without `.md`) of the documents that answer them. Use words the documentation doesn't use, as the boost and Alexa questions do. Does the order of the four ways hold?
5. **Two vectors per document.** Embed title + opening and the whole document separately, and score each document by the better of its two similarities. Does it beat both?
6. **Write what people will ask.** Ask `gpt-6-luna` to write, for each document, three questions a customer might type to find it, and embed those with the title. This is called **document expansion**. It costs 275 model calls once, and none per search.

## Questions

For discussion. There are no right answers.

- Title + opening matched the whole document with a fifteenth of the words. When two ways tie like this, which would you choose, and what would change your mind?
- The voice assistant guide never says "Alexa", and the boost guide's title never says "button". Whose job is it to close that gap: the people who write the documentation, or the people who build the search?
- A title like "Understand Warm Wake" is what people read in a list of results, yet it was the worst thing to search. Should documentation be written for people, for search, or both?
- One or two questions separate these four ways. How many questions would you want to see before trusting a choice like this, and where would you get them?
