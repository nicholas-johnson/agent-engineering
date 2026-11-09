# Module 1 — Intro to Language Models

> A language model does one thing: given some text, it predicts what comes next. In this module we build one from nothing, in five steps. We start by counting which word follows which, and keep hitting the same wall — there are far too many possible contexts to count. Each step pushes the wall back a little, until finally we train a small neural network that gets around it. No libraries, no GPUs, just plain Python and *Alice's Adventures in Wonderland*.

## Learning goals

- Explain what a **language model** is: a function from *context* to a **probability for every possible next token**.
- Build a **bigram model** by counting word pairs, and use it to generate text.
- Explain the **context window**, and why longer windows make counting models **combinatorially explode**.
- Compare **words, letters and tokens** as the units a model predicts, and the trade-off between vocabulary size and sequence length.
- Build a token vocabulary with **byte-pair encoding (BPE)** and split text with it.
- Train a tiny **neural language model** with hand-written backpropagation, and see it make sensible predictions for contexts it has **never seen**.

---

## The idea: predict the next thing

Every language model, from the ones in this module to the largest frontier models, answers the same question:

> Given this context, how likely is each possible next token?

The answer is a **vector of probabilities** — one number for every word (or letter, or token) the model knows, all adding up to 1. To generate text, pick a next token according to those probabilities, add it to the context, and ask again.

The only thing that changes from step to step in this module is **how we get that vector**.

## The corpus

Everything runs on *Alice's Adventures in Wonderland* by Lewis Carroll, from [Project Gutenberg](https://www.gutenberg.org/ebooks/11) (public domain). Each demo runs on a small corpus first, then a large one:

| File | What | Size |
|------|------|------|
| `data/alice-chapter-1.txt` | Chapter 1, *Down the Rabbit-Hole* | ~2,200 words |
| `data/alice.txt` | The whole book | ~27,000 words |
| `data/tokens.json` | A 500-token vocabulary, built by `data/build_tokens.py` | 500 tokens |

The text has had the Project Gutenberg header and footer removed, and curly quotes and dashes replaced with plain ASCII.

## Running the demos

From this folder:

```bash
uv run python demo/01_word_pairs.py
```

Each demo does two things. It **writes the model to a file in `demo/output/`**, so you can open it, look through it and search it. Then it **completes the sentence** *"alice was beginning to get"* three times. Each completion runs until it reaches a full stop, question mark or exclamation mark. Demos 1–4 take a second or two. Demo 5 trains a neural network in plain Python and takes about two and a half minutes.

| Demo | Writes |
|------|--------|
| `01_word_pairs.py` | `01_word_pairs_<corpus>.json` |
| `02_context_window.py` | `02_context_window_<corpus>.json` |
| `03_letters.py` | `03_letters_<corpus>.json` |
| `04_tokens.py` | `04_tokens_<corpus>.json` |
| `05_neural_model.py` | `05_neural_model_embeddings.txt` |

Generated text is random, so your output will differ from the examples below.

---

## 1. Word pairs — the simplest language model

**Demo:** `demo/01_word_pairs.py`

Split the text into words. Then, for every word, count which words come straight after it:

```python
for word, next_word in zip(words, words[1:]):
    counts[word][next_word] += 1
```

Divide each count by the total for that word, and you have a probability for each next word. That is a language model. It is called a **bigram model** — it looks at pairs of words.

Open `01_word_pairs_alice.json` and look up `"the"`:

```json
"the": {
  "queen": 0.0396,
  "king": 0.0365,
  "mock": 0.0323,
  "gryphon": 0.0323,
  ...
}
```

This is the **vector of next-word probabilities** for "the". The full vector has an entry for all 2,676 words in the book, but almost all of them are zero, so we only store the ones we have seen.

To complete a sentence, look up the probabilities for the last word, pick a next word using them, and repeat until the sentence ends:

> alice was beginning to get into the people that very tired of tumbling down the second time , she could see , and there was now , now only knew how late !

Each pair of words makes sense. The sentence as a whole doesn't, because the model only ever sees **one word of context**. It has no idea what it said two words ago.

On chapter 1 the model mostly knows about rabbits and tables. On the whole book, "the" is most often followed by queen, king, mock (turtle) and gryphon. **The model is only as good as the text it has counted.**

## 2. The context window

**Demo:** `demo/02_context_window.py`

One word of context isn't enough, so use more. Slide a window of **five words** along the text, and for each five-word context, count the word that comes next:

```python
for i in range(len(words) - WINDOW):
    context = " ".join(words[i : i + WINDOW])
    counts[context][words[i + WINDOW]] += 1
```

The number of words the model looks at is its **context window**. Real models have context windows of hundreds of thousands of tokens.

The completion is now perfect English:

> alice was beginning to get very tired of sitting by her sister on the bank , and of having nothing to do : once or twice she had peeped into the book her sister was reading , but it had no pictures or conversations in it , and what is the use of a book , thought alice without pictures or conversations ?

...because it is the first sentence of the book, word for word. On the whole book it occasionally switches track at *"what is the use of"*, which appears twice, and finishes with the Mock Turtle's line instead.

Open `02_context_window_alice.json` and you can see why. Almost every context has exactly one next word, with a probability of 1.0:

| | Chapter 1 | Whole book |
|-|-----------|------------|
| Different words | 619 | 2,676 |
| Five-word contexts seen | 2,447 | 30,350 |
| Contexts with only one possible next word | 99% | 99% |
| Possible five-word contexts | 90,876,845,839,099 | 137,224,148,781,413,376 |

Almost every five-word sequence appears **exactly once**, so the model has only one choice for what comes next. It isn't predicting, it is **reciting**.

The flip side: try a sentence that isn't in the book. Of the seven five-word contexts in *"The Queen was beginning to get very cross with the Hatter"*, search the file and you will find only one, `"was beginning to get very"`. For the rest, the model has nothing to say at all.

This is the **combinatorial problem**. With a vocabulary of *V* words and a window of *n*, there are *V*ⁿ possible contexts. Even the whole book only covers a vanishingly small fraction of them. More text helps a little, but the number of possible contexts grows far faster than any amount of text we could collect.

## 3. Letters

**Demo:** `demo/03_letters.py`

The problem is the size of the vocabulary — thousands of words. What if we predict **letters** instead? There are only around 40 different characters in the book (letters, space and punctuation), so we can afford a longer window. Use **eight letters**:

```python
for i in range(len(text) - WINDOW):
    counts[text[i : i + WINDOW]][text[i + WINDOW]] += 1
```

| | Chapter 1 | Whole book |
|-|-----------|------------|
| Different characters | 38 | 41 |
| Eight-letter contexts seen | 9,454 | 84,162 |
| Contexts with only one possible next letter | 96% | 91% |
| Possible eight-letter contexts | 4,347,792,138,496 | 7,984,925,229,121 |

The completions on the whole book are surprisingly good:

> alice was beginning to get us dry would be of very like having found out a new kind of rule, "and i'll tell you just now.

It invents new sentences, and occasionally new words. But look closely: it rambles. Eight letters is only about **one and a half words**. The vocabulary got smaller, but each step now carries much less meaning, so the window has to be much longer to see the same amount of text — and 41⁸ is still about 8 trillion contexts.

Letters are too small. Words are too many. We want something in between.

## 4. Tokens

**Demo:** `demo/04_tokens.py` (vocabulary built by `data/build_tokens.py`)

A **token** is a common chunk of text: a whole word like `" the"` or `" caterpillar"`, a piece of a word like `"ing"`, or a single letter. Every modern language model works in tokens.

`data/tokens.json` holds our vocabulary of 500 tokens. It was built with **byte-pair encoding (BPE)**, the same idea used by GPT and Claude tokenizers:

1. Start with every single character as a token.
2. Count every pair of neighbouring tokens in the text.
3. Merge the most common pair into a new token.
4. Repeat until you have as many tokens as you want.

The first merges are `" t"`, `"he"`, `" a"`, `" s"` and then `" the"`. By the end it has learned whole words like `" caterpillar"` and `" replied"`.

To split text into tokens, the demo takes the **longest token that matches** at each position:

```text
alice was beginning to get very tired of sitting by her sister
['al', 'ice', ' was', ' begin', 'ning', ' to', ' get', ' very', ' ti', 'red', ' of', ' s', 'it', 'ting', ' by', ' her', ' s', 'ist', 'er']
```

Common words get one token. Rarer words get split into pieces. Any text can be written with this vocabulary, even words it has never seen, because single letters are tokens too.

Real tokenizers replay the merges in order rather than taking the longest match, and have 100,000–200,000 tokens rather than 500, but the idea is the same.

Now count four-token contexts:

| | Chapter 1 | Whole book |
|-|-----------|------------|
| Tokens | 4,060 | 52,729 |
| Four-token contexts seen | 3,818 | 41,689 |
| Contexts with only one possible next token | 97% | 92% |
| Possible four-token contexts | 62,500,000,000 | 62,500,000,000 |

The completions read well:

> alice was beginning to get very tired of swimming away from her as hard as she could, "if you can't think!

...but mostly because they are stitched together from long runs of the book. On chapter 1 they are almost all the opening sentence again.

Tokens give us a fixed, small vocabulary that can spell anything, and each token carries more meaning than a letter. But **the problem is still combinatorial**. 62.5 billion possible contexts against 50,000 tokens of text: 92% of the contexts we have seen still have only one possible next token, and almost any new phrase is unseen.

Counting can't get us any further. We need a model that can make a sensible guess about a context it has **never seen**.

## 5. A neural language model

**Demo:** `demo/05_neural_model.py`

Instead of storing a count for every context, we **learn a function** that takes any context and produces the vector of next-token probabilities. The model is a tiny version of the one in Bengio et al. (2003), *A Neural Probabilistic Language Model*:

```text
last 3 tokens
   │
   ▼
look up a vector of 16 numbers for each token      ← the embeddings
   │  (3 × 16 = 48 numbers)
   ▼
hidden layer: 32 neurons, tanh
   │
   ▼
output layer: one score for each of the 500 tokens
   │
   ▼
softmax: turn the scores into probabilities
```

That is 26,068 numbers (the **parameters**), all starting random.

**Training** repeats one step 30,000 times:

1. Pick a random three-token context from the book, and the token that really came next.
2. Run the context forward through the model to get probabilities.
3. Measure how wrong it was: the **loss** is `-log(probability of the right token)`. Certain and right is 0; the less likely it thought the right answer, the bigger the loss.
4. Work backwards through the model, calculating how each parameter affected the loss. This is **backpropagation**.
5. Nudge every parameter a little in the direction that reduces the loss. This is **gradient descent**.

The demo does all of this with plain Python lists, so you can read every multiplication. The key line is where backpropagation starts:

```python
score_grads = probabilities[:]
score_grads[target] -= 1
```

For softmax with this loss, the gradient of each output score is simply *predicted probability minus actual*. Everything after that is the chain rule.

The loss starts at 6.21 — the loss of picking uniformly at random from 500 tokens — and falls to around 4.5.

### The result

The completions are rough:

> alice was beginning to getve had would meill it.

That's expected. It is a 26,000-parameter model trained for two minutes on one short book. The counting models looked better because they were copying the book.

The real result shows up when you ask the trained model for its next-token probabilities on two contexts, one from the book and one that isn't:

```text
' the queen said to' (seen in the book)
  ' the' 16%, ' alice' 13%, ' "' 8%, ' herself' 5%, ' this' 3%
' the mouse said to' (never seen in the book)
  ' the' 15%, ' alice' 12%, ' "' 7%, ' herself' 5%, ' a' 3%
```

The book never contains "the mouse said to". A counting model would have nothing. The neural model gives almost the same answer as for "the queen said to", because during training it learned to give `" mouse"` and `" queen"` similar vectors — both are characters who say things.

That is how a neural network breaks the combinatorial problem. It doesn't need to have seen a context, only contexts **like** it.

### Embeddings

Those per-token vectors are called **embeddings**. Open `demo/output/05_neural_model_embeddings.txt` to see all 500 of them. Nobody told the model what any token means; it arranged them so that tokens used in similar ways end up with similar vectors. We come back to embeddings later in the course.

### From here to a real language model

A modern language model is the same idea with everything made bigger:

| | Our model | A modern LLM |
|-|-----------|--------------|
| Vocabulary | 500 tokens | 100,000–200,000 tokens |
| Context window | 3 tokens | hundreds of thousands of tokens |
| Parameters | 26,068 | billions to trillions |
| Training text | one book | trillions of tokens |
| Architecture | one hidden layer | a deep **transformer** |
| Training time | two minutes, one CPU core | months, thousands of GPUs |

But it still does exactly what ours does: takes a context and produces a vector of probabilities for the next token.

---

## Summary

| Step | Predicts from | Problem |
|------|---------------|---------|
| 1. Word pairs | 1 word | Too little context — no memory beyond the last word |
| 2. Context window | 5 words | Combinatorial explosion — recites the book, knows nothing about new text |
| 3. Letters | 8 letters | Small vocabulary, but 8 letters is barely a word and a half |
| 4. Tokens | 4 tokens | Better trade-off, but still too many contexts to count |
| 5. Neural model | 3 tokens | Learns a function, so it can predict for contexts it has never seen |

## Playground

[`playground/`](playground/) has seven small scripts to play with between exercises: temperature, backoff, scoring sentences, other books, tokenizer experiments and more. Each comes with ideas for taking it further.

## Further reading and extensions

The final exercise is in [`further-reading/`](further-reading/): research papers, from Shannon in 1948 to Chinchilla in 2022, with a note on what to look for in each and which demo it relates to, plus extension projects to take home.

## Slides

```bash
pnpm slides:01
```
