# Other languages

Not every customer writes in English. You'll ask the same four questions in six languages and search the English documentation, once by keywords (BM25, as in demo 1) and once by vectors (as in demo 4), and see which search still finds the right document.

From the module folder (`day-two/module-05-embeddings-and-vector-search`):

```bash
uv run python playground/other-languages/play.py
```

Or without `uv` (set up `.venv` once at the repo root with `python3 -m venv .venv && .venv/bin/pip install -e .`):

```bash
source ../../.venv/bin/activate
python playground/other-languages/play.py
```

Needs `OPENAI_API_KEY` in `.env`. The first run embeds all 275 documents, which took about five seconds, and keeps the vectors in `playground/other-languages/output/vectors.db`. After that it runs in a second or two. Every search, with where the right document landed and the top three each method found, is written to `playground/other-languages/output/ranks.json`.

---

The four questions come from `data/questions.json`, starting with the module's running question, and are written out in `QUESTIONS` in English, French, German, Spanish, Polish and Japanese. The documentation stays in English. Each question has one or more right documents (the password question has six), and the table shows where the best-placed one lands among all 275 documents (1 means first). A `-` means no right document shares a word with the question, so keyword search can't find it at all.

```text
Why is the heating already on before my alarm goes off?
              keyword  vector
  English         121       1
  French            -       1
  German           14       1
  Spanish           -       1
  Polish            -       1
  Japanese          -       2

I forgot my password and can't get into the app
              keyword  vector
  English           1       1
  French            -       1
  German            3       1
  Spanish          70       1
  Polish          115       1
  Japanese          -       1

It says 21 degrees but the room feels freezing
              keyword  vector
  English          11       1
  French           15       2
  German           18       1
  Spanish          18       1
  Polish           18       1
  Japanese         18       1

Can I ask Alexa to turn the heating up?
              keyword  vector
  English          13       8
  French            -       2
  German            -       8
  Spanish         131       7
  Polish          131      27
  Japanese          -       5

A right document in the top 5, of 24 searches:
  keyword 2, vector 20
(- means no right document shares a word with the question.)
```

The API can return very slightly different vectors from one call to the next, so on your first run a rank or two may differ.

## Things to notice

- **Vectors barely notice the language.** For the first three questions, the right document is first in 16 of 18 searches and second in the other two. Nobody wrote a word of French or Japanese into the documentation. The embedding model learned from text in many languages, so a question and a document can land close together without sharing a single word.
- **The weak question isn't a language.** All four of the vectors' misses are the Alexa question, and English does no better than the others: it comes 8th, behind French (2nd), Japanese (5th) and Spanish (7th). The documentation never says "Alexa". It says "voice assistant". In five of the six languages, the first result was "Change the boost temperature" instead: "turn the heating up" pulled harder than "Alexa".
- **Keyword search mostly finds nothing.** It got a right document into the top five twice, both for the password question: English (1st) and German (3rd). German got there on "app" and "in", two words that German and English happen to share. On the running question, even English only reaches 121st: no document contains "alarm" or "my", and Warm Wake talks about a "schedule period" instead.
- **Numbers survive translation, but don't decide.** In German, Spanish, Polish and Japanese, the right document came 18th every time, on "21" (and, in Polish, "a"). It can't do more, because 27 documents contain 21.
- **When keywords do match, look at why.** The word splitter from demo 1 only knows the letters a to z. Polish "hasła" (password) becomes "has" and "a", and Spanish "contraseña" becomes "contrase" and "a". Both "has" and "a" are English words, so they match most documents, which is mostly how Polish gets the password question to 115th. German reaches 14th on the running question with "an" alone. And Polish "Alexę" (Alexa, as the object of a sentence) becomes "alex", which wouldn't have matched "alexa" even if the documentation used it.

## Try this

1. **Your language.** Add a language you speak, and write the question as you'd really say it, not as a translation.
2. **Mixed languages.** Write a question half in one language and half in another ("Pourquoi le heating is on before my alarm?"). Many people write like this.
3. **Messy English.** Add questions like "heatings on b4 my alarm??" and "cant log in forgot pw". Which search copes better with typos and shorthand?
4. **The documentation's words.** Change the Alexa question to "Can I use a voice assistant to turn the heating up?" in every language. Do both searches improve? What does that say about writing documentation in your customers' words?
5. **A better word splitter.** Change `words()` to split on `\w+`, which keeps "contraseña" and "hasła" whole. Which matches survive? What would keyword search need to work across languages?
6. **Translate first.** Ask `gpt-6-luna` to translate each question into English before the keyword search. How close does keyword search get to vectors?

## Questions

For discussion. There are no right answers.

- Vector search found Warm Wake from a Japanese question, but the page it found is in English. Is finding it enough? What would a customer who doesn't read English need next?
- Four of the six languages missed the Alexa question, because the documentation says "voice assistant" and never "Alexa". Should the writers change the documentation, or should the search cope? Who would notice the problem first?
- The number 21 was the only word keyword search could match in four languages. What other words in your own work are the same in every language?
- Would you tell customers which languages your search works well in? How would you find out?

## Further reading

- **Muennighoff, N., Tazi, N., Magne, L. & Reimers, N. (2023). "MTEB: Massive Text Embedding Benchmark." *EACL 2023*, 2014–2037. [arXiv:2210.07316](https://arxiv.org/abs/2210.07316)** Tests embedding models on 58 datasets in 112 languages. Look at the bitext mining tasks, which match sentences with their translations, and at how a model's place changes from one kind of task to another.
