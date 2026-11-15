# Score a sentence

Point a word-pair model at a finished sentence and it says how likely that sentence is. You'll score a few sentences and see where the model was surprised.

From the module folder (`day-one/module-01-intro-to-language-models`):

```bash
uv run python playground/score-a-sentence/play.py
```

Or without `uv` (standard library only, no packages needed):

```bash
python3 playground/score-a-sentence/play.py
```

Builds word-pair counts from `data/alice.txt` and writes step-by-step probabilities to `playground/score-a-sentence/output/scores.txt`.

---

Take a sentence, and for each word ask the model: how likely was this word, given the one before it? Multiply those probabilities together and you have the probability of the whole sentence.

```text
      55  Alice was beginning to get very tired of sitting by her sister on the bank.
      61  The Queen was beginning to get very cross with the Hatter.
    4051  Bank the on sister her by sitting of tired very get to beginning was Alice.
    3818  The server returned an error because the database was down.
```

The number is the **perplexity**: roughly, how many words the model was choosing between at each step. **Lower means the model is less surprised.** The real sentence from the book scores best. The Carroll-style sentence that isn't in the book comes close. The same words backwards, and a sentence from the wrong century, are a long way behind.

`playground/score-a-sentence/output/scores.txt` shows the probability of every step, so you can see exactly where the model was surprised:

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

## Questions

For discussion. There are no right answers.

- The made-up Carroll-style sentence scored almost as well as the real one. What does that say about tools that claim to detect AI-written text?
- Low perplexity means unsurprising. Is good writing unsurprising?
- Smoothing decides how much chance to give things never seen before. Where else do people have to make that decision?

## Further reading

- **Chen, S. F. & Goodman, J. (1999). "An empirical study of smoothing techniques for language modeling." *Computer Speech & Language* 13(4):359–394.** What to do about word pairs the model has never seen. They compare the methods of the time on the same data. Read it after trying `SMOOTHING = 1`.
- **Shannon, C. E. (1951). "Prediction and Entropy of Printed English." *Bell System Technical Journal* 30(1):50–64.** How surprised a reader is by the next letter of English. Perplexity, the number this playground prints, is that surprise measured on words.

## Rabbit holes

Optional. These leave the script.

1. **GLTR.** **Gehrmann, S., Strobelt, H. & Rush, A. M. (2019). "GLTR: Statistical Detection and Visualization of Generated Text." *ACL System Demonstrations*, 111–116.** [Paper](https://aclanthology.org/P19-3019.pdf), and the tool at [gltr.io](http://gltr.io/). `scores.txt` is already most of what they built: colour each word by its probability.
2. **Their demo.** Paste the real sentence and the backwards one into the tool, and compare its colours with `scores.txt`. Their model was trained on different text, so the colours will not match. Where do the two still agree?
