# Score a sentence

A language model doesn't only generate text. Run it the other way round and it tells you **how likely a piece of text is**.

Take a sentence, and for each word ask the model: how likely was this word, given the one before it? Multiply those probabilities together and you have the probability of the whole sentence.

```bash
uv run python play.py
```

This builds its own word-pair counts from `data/alice.txt`, so no demos need to be run first.

```text
      55  Alice was beginning to get very tired of sitting by her sister on the bank.
      61  The Queen was beginning to get very cross with the Hatter.
    4051  Bank the on sister her by sitting of tired very get to beginning was Alice.
    3818  The server returned an error because the database was down.
```

The number is the **perplexity**: roughly, how many words the model was choosing between at each step. **Lower means the model is less surprised.** The real sentence from the book scores best. The Carroll-style sentence that isn't in the book comes close. The same words backwards, and a sentence from the wrong century, are a long way behind.

`output/scores.txt` shows the probability of every step, so you can see exactly where the model was surprised:

```text
Bank the on sister her by sitting of tired very get to beginning was Alice.
Perplexity: 4051
            bank -> the            0.033927
             the -> on             0.000006
```

## Smoothing

A word pair the model has never seen would get a probability of zero, and one zero makes the whole sentence impossible. So the script adds a little (`SMOOTHING = 0.01`) to every count, giving every pair a small chance.

## Try this

1. **Add-one smoothing.** Set `SMOOTHING = 1`, the textbook version. The real sentence now loses to the invented one. Why? (Hint: there are 2,677 words in the vocabulary, and "beginning" only appears a handful of times.)
2. **Your own sentences.** Write a sentence Carroll might have written, and one he never would. Can you get a made-up sentence to score better than a real one?
3. **Spot the fake.** Take five real sentences from the book and five you wrote. Can the model tell them apart?
4. **Who wrote it?** Train a second model on the other book in `../other-books/looking-glass.txt`. Score sentences from each book with both models. Does each model prefer its own book?
5. **Chapter 1 only.** Count only `data/alice-chapter-1.txt`. Score a sentence from chapter 12. What happens to the perplexity, and why?
