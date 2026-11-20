# Clip 3 — Search by meaning

> A promise to explain embeddings in sixty seconds. Search *Alice in Wonderland* for "the angry queen", and keyword search finds a cat talking about a dog: "angry" is in the book five times, never about the Queen. Cut the book into passages and turn each into 1,536 numbers, and passages that mean similar things land close together. The question lands among the Queen's passages, next to "The Queen turned crimson with fury". Keywords match words; embeddings match meaning. That's how an AI finds the right page of your documents.

- **Promotes:** Module 5, Embeddings and Vector Search
- **Length:** about 140 spoken words to explain it, then about 25 for the sign-off. `pnpm social:check` estimates about 65 seconds in all, so time your first take.
- **Ending:** the sign-off, full-face: "Follow if you'd like to know more." Cut straight after it.
- **Recording:** [`index.html`](index.html), with the map drawn by `clip-deck`'s `space.js` from [`scene.js`](scene.js) and [`map.js`](map.js). Run `pnpm social`, open <http://127.0.0.1:8765/03-search-by-meaning/> in Chrome and press R.

## The script

### 1. The promise

To camera, full-screen:

> "I'm going to explain embeddings to you in sixty seconds."

### 2. The odd thing

> "I searched Alice in Wonderland for 'the angry queen'. 'Angry' is in there five times. Never about the Queen. So the best keyword match is a cat, talking about a dog."

**Screen:** a search box types *the angry queen*. Then the five places Ctrl+F finds "angry": Alice to the Mouse, the White Rabbit twice and the Cheshire Cat twice. They give way to keyword search's best passage, with *angry* highlighted: the Cheshire Cat's "a dog growls when it's angry, and wags its tail when it's pleased."

### 3. The reveal

> "Now cut the book into passages, and turn each one into numbers. Passages that mean similar things get similar numbers. Turn the question into numbers too, and find the closest passage. 'The Queen turned crimson with fury.' She's never called angry."

**Screen:** 178 dots scatter onto a map, one per passage, with one passage's first numbers below: `[0.024, -0.008, 0.027, 0.027, …]`. The dots take the colour of who they're about: the Queen and King, the tea party, the Caterpillar, the Mock Turtle. The question drops onto the map among the Queen's passages, a line joins it to the closest one, and the passage appears with *fury* highlighted.

> "Try 'the creature with a pipe'. There's no 'pipe' in the book. Keywords find a baby that turns into a pig. Meaning finds the Caterpillar, smoking its hookah."

**Screen:** a new search, and "pipe": 0 matches. Two cards side by side: keyword search's passage, with *creature* highlighted ("What am I to do with this creature when I get it home?" It's a pig.), and the closest by meaning (the Caterpillar "put the hookah into its mouth and began smoking again").

### 4. The payoff

> "That list of numbers is called an embedding. Keywords match words. Embeddings match meaning. It's how an AI finds the right page in your documents before it answers."

**Screen:** the heading *Embeddings*, with the numbers again, then "Keywords match words. Embeddings match meaning." Then a question, "Can I bring my dog to work?", and the closest page of a staff handbook: "Pets aren't allowed in the office". The handbook is illustrative: see the notes.

### 5. Sign-off

Full-face again:

> "I'm Nicholas Johnson. I'm a principal dev working with AI. I'm doing a series on AI fundamentals. Follow if you'd like to know more."

## Captions and presses

The captions are the `<p class="cue">` lines in `index.html`, and the map's changes are in `scene.js`, keyed by the same steps. Words in italics show in yellow.

| Press | Caption: what you say | What else happens |
|-------|-----------------------|-------------------|
| — | I'm going to explain *embeddings* to you in sixty seconds. | You, full-screen |
| 1 | I searched *Alice in Wonderland* for "the angry queen". | You shrink into the box. A search box types "the angry queen". |
| 2 | "Angry" is in there five times. Never about the Queen. | The five matches, with *angry* highlighted and who each is about |
| 3 | So the best keyword match is a cat, talking about a dog. | The matches give way to the best keyword match: the Cheshire Cat's dog |
| 4 | Now cut the book into passages, and turn each one into numbers. | 178 dots scatter onto a map; one passage's first four numbers below |
| 5 | Passages that mean similar things get similar numbers. | The dots take their group's colour, and the groups are named |
| 6 | Turn the question into numbers too, and find the closest passage. | "the angry queen" drops onto the map, among the Queen's passages |
| 7 | "The Queen turned crimson with fury." She's never called angry. | A line joins it to the closest passage, which appears below with *fury* highlighted |
| 8 | Try "the creature with a pipe". There's no "pipe" in the book. | A new search types out, then "pipe": 0 matches |
| 9 | Keywords find a baby that turns into a pig. | The keywords card, with *creature* highlighted |
| 10 | Meaning finds the Caterpillar, smoking its hookah. | The meaning card |
| 11 | That list of numbers is called an *embedding*. | The heading "Embeddings", with the numbers |
| 12 | Keywords match words. Embeddings match *meaning*. | "Remember: Keywords match words. Embeddings match meaning." |
| 13 | It's how an AI finds the right page in your documents before it answers. | "Can I bring my dog to work?" and the handbook's page about pets |
| 14 | I'm Nicholas Johnson. I'm a principal dev working with AI. | You, full-screen again |
| 15 | I'm doing a series on *AI fundamentals*. | — |
| 16 | Follow if you'd like to know more. | — |

Then press R to stop.

## Post text

For the description under the video, not on it. Repeat the promise, then the course plug:

> Embeddings in sixty seconds: search Alice in Wonderland for "the angry queen", and keyword search finds a cat talking about a dog. Search by meaning finds the Queen, crimson with fury.

## Notes

- **"Keyword search" is BM25,** as in Module 5's first demo: passages score for the question's words, rare words counting for more. Its best passage for "the angry queen" is the Cheshire Cat's, which says "angry" twice. Ctrl+F's five matches are a plain search for "angry" in the whole book.
- **The passages** are the book's paragraphs, joined until each has at least 120 words: 178 of them. The search is over passages, so the clip quotes the line in each passage that matters.
- **Quotes are trimmed to fit.** The Queen's passage says "The Queen turned crimson with fury, and, after glaring at her for a moment like a wild beast, screamed 'Off with her head! Off - '". The clip shows "The Queen turned crimson with fury, and… screamed 'Off with her head!'".
- **The similarities are low,** about 0.45 for the Queen and 0.39 for the Caterpillar, because a four-word question and a 120-word passage are never very alike. What matters is which passage comes first, so the clip says "closest" and shows no scores.
- **The two questions were chosen.** Twelve were tried, and these show the difference most clearly. Some were muddier: "Where does Alice get huge?" found the cake that makes her *shrink*, the right topic but the opposite meaning. Embeddings are known for that, and it could be a clip of its own.
- **The map is real, but flattened.** Each dot is a real passage's embedding, squashed from 1,536 numbers to 2 with PCA (the two directions in which the passages differ most). Squashing loses detail: on the flat map, the Queen's passage is only the 12th nearest dot to the question, although the three nearest dots are also from the Queen's croquet game. The line goes to the real closest passage, worked out from all 1,536 numbers.
- **The colours are by character:** each passage is coloured by whichever group it names most, if it names it at least twice (the Queen or King; the Hatter, March Hare or Dormouse; the Mock Turtle or Gryphon; the Caterpillar). The rest are grey.
- **The numbers** `[0.024, -0.008, 0.027, 0.027, …]` are the first four of the Queen passage's real embedding. The API can return very slightly different numbers each time, so a rerun may differ in the third decimal place, and the map may shift a little.
- **The staff handbook is illustrative.** It's a made-up example of the same idea at work, not a real search. Its point is the same as the clip's: the question says "dog", and the right page says "pets".
- **If the explanation runs over sixty seconds,** cut the pipe frame (presses 8 to 10). The Queen already makes the point.

## Where the material comes from

| On screen | Source |
|-----------|--------|
| The book | *Alice's Adventures in Wonderland* by Lewis Carroll, from [Project Gutenberg](https://www.gutenberg.org/ebooks/11), public domain: Module 1's `day-one/module-01-intro-to-language-models/data/alice.txt` |
| Ctrl+F's five matches for "angry", and none for "pipe" | [`search.py`](search.py), run 19 November 2026: `uv run python social-scripts/03-search-by-meaning/search.py` |
| The best keyword matches: the Cheshire Cat's dog, and the baby that turns into a pig | `search.py`: BM25 over the 178 passages |
| The closest passages by meaning: the Queen's fury, and the Caterpillar's hookah | `search.py`: `text-embedding-3-small` and cosine similarity |
| The map, its colours, and where the question lands | `search.py`, which writes [`map.js`](map.js) |
| One passage as numbers: `[0.024, -0.008, 0.027, 0.027, …]` | `search.py`: the first four numbers of the Queen passage's embedding |
| "Can I bring my dog to work?" and the staff handbook | Made up, to show the idea at work. See the notes. |
