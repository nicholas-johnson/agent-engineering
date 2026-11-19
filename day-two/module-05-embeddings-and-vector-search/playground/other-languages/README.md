# Other languages

Not every tester or customer writes in English. You'll search the English library with the same four requests in six languages, once by keywords (BM25, as in demo 1) and once by vectors (as in demo 2), and see which search still finds the right script.

From the module folder (`day-two/module-05-embeddings-and-vector-search`):

```bash
uv run python playground/other-languages/play.py
```

Or without `uv` (set up `.venv` once at the repo root with `python3 -m venv .venv && .venv/bin/pip install -e .`):

```bash
source ../../.venv/bin/activate
python playground/other-languages/play.py
```

Needs `OPENAI_API_KEY` in `.env`. The first run embeds the library and keeps the vectors in `playground/other-languages/output/vectors.db`. Every search, with where the right script landed and the top three each method found instead, is written to `playground/other-languages/output/ranks.json`.

---

The four requests are written out in `REQUESTS`, in English, French, German, Spanish, Polish and Japanese. The library stays in English. Each request is searched on its own platform, as the module's search tool does, and the table shows where the right script lands (1 means first). A `-` means the right script shares no word with the request, so keyword search can't find it at all.

```text
Customers can't sign in after resetting their password (android)
              keyword  vector
  English          14       1
  French           21       2
  German            -       3
  Spanish          36       1
  Polish           57       1
  Japanese          -       6

The same thermostat shows up twice in the home after adding it again (ios)
              keyword  vector
  English           1       1
  French           91       1
  German            7       1
  Spanish         167       1
  Polish            -       1
  Japanese          -       2

The thermostat says 21 but the room feels colder. Is its reading accurate? (device)
              keyword  vector
  English          61       1
  French           87       1
  German          136       1
  Spanish          11       1
  Polish            -       5
  Japanese          -       7

E-104 came up while setting up a new thermostat (device)
              keyword  vector
  English           1       1
  French            1       1
  German            1       3
  Spanish           1       2
  Polish            1       2
  Japanese          1       1

A right script in the top 5, of 24 searches:
  keyword 7, vector 22
(- means the right script shares no word with the request.)
```

## Things to notice

- **Vectors barely notice the language.** The right script is in the top five in 22 of 24 searches, and first in most of them. Nobody wrote a word of French or Polish into the library. The embedding model learned from text in many languages, so a request and a script can land close together without sharing a single word.
- **Some languages are weaker.** Japanese is the weakest row in three of the four requests (6, 2 and 7), and Polish slips to fifth on the thermostat reading. A model is usually best at the languages it saw most of while training.
- **Keyword search's hits are almost all the error code.** Six of its seven top-five finds are the E-104 request, in every language, Japanese included. "E-104" is spelled the same everywhere, and BM25 only needs one rare word to match. Codes, product names and numbers survive translation, and that is where keywords still earn their place.
- **When keywords do match, look at why.** German found the duplicated thermostat at 7th because German spells "Thermostat" the English way. The Spanish and Polish matches are accidents. The word splitter from demo 1 only knows the letters a to z, so Spanish "añadirlo" becomes "a" and "adirlo", and Polish "hasła" (password) becomes "has" and "a". That's how Spanish gets the thermostat reading to 11th: on "a" and "s".

## Try this

1. **Your language.** Add a language you speak, and write the request as you'd really say it, not as a translation.
2. **Mixed languages.** Write a request half in one language and half in another ("Le thermostat affiche E-104 after the update"). Many people write like this at work.
3. **Translate first.** Ask `gpt-6-luna` to translate each request into English before the keyword search. How close does keyword search get to vectors?
4. **Messy English.** Add requests like "cant log in after pw reset" and "thermo stuck on E104". What does keyword search make of "E104" without the hyphen?
5. **The bigger model.** Switch to `text-embedding-3-large`. Do the Japanese rows improve?
6. **A better word splitter.** Change `words()` to split on `\w+`, which keeps "añadirlo" and "hasła" whole. Which matches survive? What would keyword search need to work across languages?

## Questions

For discussion. There are no right answers.

- Vector search found the right script from Japanese, though nobody wrote the scripts in Japanese. Does that mean a team no longer needs to translate its documentation?
- Japanese and Polish did worse than French and Spanish. Who is let down when a search works less well in some languages, and how would anyone find out?
- An error code was the one thing keyword search found in every language. What other words in your own work are the same in every language?
- Would you tell users which languages your search works well in? How would you know?
