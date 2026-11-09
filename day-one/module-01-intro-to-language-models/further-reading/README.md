# Further reading and extensions

Everything in this module was invented by someone first. This is where it came from, and where it went next.

## The exercise

1. **Pick one paper** from the reading list. If you're not sure, start with one marked ⭐.
2. **Read the part that matters.** You don't need to read it all. Each description says what to look for.
3. **Connect it to a demo.** Write two or three sentences: what problem was the paper solving, and which of our five demos does it relate to?
4. **Pick one extension** from the list at the end and start it. Most will take longer than a break, so take them home.

---

## Reading list

### Counting: where demos 1–3 come from

**⭐ Shannon, C. E. (1948). "A Mathematical Theory of Communication." *Bell System Technical Journal* 27(3):379–423.**

The paper that founded information theory. Look for the section on *"The series of approximations to English"*. Shannon generates text from letter counts, then from letter pairs and triples, then from word counts and word pairs, getting closer to English each time. That is demos 1 to 3, done in 1948, partly by opening a book at random and copying out what followed.

**Shannon, C. E. (1951). "Prediction and Entropy of Printed English." *Bell System Technical Journal* 30(1):50–64.**

Shannon asked people to guess the next letter of a passage, one letter at a time, and counted how many guesses they needed. From that he estimated how much information each letter of English really carries: around one bit, far less than the nearly five bits needed to pick one of 27 symbols at random. People are very good language models.

**Katz, S. M. (1987). "Estimation of probabilities from sparse data for the language model component of a speech recognizer." *IEEE Transactions on Acoustics, Speech, and Signal Processing* 35(3):400–401.**

Two pages that introduced **backoff**: if a long context has never been seen, fall back to a shorter one. This is what the `backoff` playground does, done carefully so the probabilities still add up to 1.

**Chen, S. F. & Goodman, J. (1999). "An empirical study of smoothing techniques for language modeling." *Computer Speech & Language* 13(4):359–394.**

What do you do about word pairs you have never seen? This paper compares every smoothing method of the time on the same data, and finds a clear winner: modified Kneser–Ney smoothing. Read it after the `score-a-sentence` playground, where adding one to every count went badly wrong.

**Brants, T., Popat, A. C., Xu, P., Och, F. J. & Dean, J. (2007). "Large Language Models in Machine Translation." *EMNLP-CoNLL 2007*.**

Google trained counting models on up to two trillion words of web text. At that scale a very simple method they called "stupid backoff" worked as well as the careful ones. Note the title: "large language models", in 2007, about counting.

### Tokens: where demo 4 comes from

**Gage, P. (1994). "A New Algorithm for Data Compression." *C Users Journal* 12(2):23–38.**

Byte-pair encoding was invented as a way to compress files: find the most common pair of bytes, replace it with a single unused byte, repeat. The algorithm in `data/build_tokens.py` is this one, used for a different job.

**⭐ Sennrich, R., Haddow, B. & Birch, A. (2016). "Neural Machine Translation of Rare Words with Subword Units." *ACL 2016*. [arXiv:1508.07909](https://arxiv.org/abs/1508.07909)**

The paper that brought byte-pair encoding to language. Translation models had a fixed vocabulary and could not handle rare words or names. Splitting words into learned pieces fixed that. The core algorithm is printed in the paper as a short Python listing: compare it with `data/build_tokens.py`.

**Kudo, T. & Richardson, J. (2018). "SentencePiece: A simple and language independent subword tokenizer and detokenizer for Neural Text Processing." *EMNLP 2018*. [arXiv:1808.06226](https://arxiv.org/abs/1808.06226)**

Our tokenizer splits on spaces first, which assumes the language uses spaces. SentencePiece treats text as a raw stream and makes the space part of the token, so the same method works for Japanese or Chinese. Many open models use it.

**Radford, A., Wu, J., Child, R., Luan, D., Amodei, D. & Sutskever, I. (2019). "Language Models are Unsupervised Multitask Learners." OpenAI. [PDF](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf)**

The GPT-2 paper. For tokens, look at section 2.2 on byte-level BPE: start from all 256 possible bytes instead of the characters in the training text, so nothing is ever unknown. That fixes the `1234` problem in the `tokenizer-lab` playground. The rest of the paper shows a language model doing tasks it was never trained for.

### Neural language models: where demo 5 comes from

**Rumelhart, D. E., Hinton, G. E. & Williams, R. J. (1986). "Learning representations by back-propagating errors." *Nature* 323:533–536.**

The four-page paper that made backpropagation the standard way to train neural networks. Compare their description of the backward pass with the `train` function in demo 5.

**⭐ Bengio, Y., Ducharme, R., Vincent, P. & Jauvin, C. (2003). "A Neural Probabilistic Language Model." *Journal of Machine Learning Research* 3:1137–1155. [PDF](https://www.jmlr.org/papers/volume3/bengio03a/bengio03a.pdf)**

Demo 5, at full size. Read the introduction: it describes the combinatorial problem exactly as we met it, and proposes the fix, learning a vector for each word so the model can generalise to sentences it has never seen. Their model beat the best counting models of the time.

**Mikolov, T., Karafiát, M., Burget, L., Černocký, J. & Khudanpur, S. (2010). "Recurrent neural network based language model." *Interspeech 2010*.**

Our model looks at a fixed three tokens. A recurrent network carries a hidden state forward from one token to the next, so in principle it can remember the whole text so far. This paper showed it beat counting models by a wide margin.

**Hochreiter, S. & Schmidhuber, J. (1997). "Long Short-Term Memory." *Neural Computation* 9(8):1735–1780.**

In practice, plain recurrent networks forget quickly. The LSTM adds gates that decide what to keep and what to forget. LSTMs were the standard language model until transformers arrived.

### Where it went next

**Mikolov, T., Chen, K., Corrado, G. & Dean, J. (2013). "Efficient Estimation of Word Representations in Vector Space." [arXiv:1301.3781](https://arxiv.org/abs/1301.3781)**

word2vec. It throws away most of the language model and keeps only the embeddings, trained fast on billions of words. Famous for showing that the vector for *king*, minus *man*, plus *woman*, lands near *queen*. Embeddings are coming up later in the course; this is a good preview.

**⭐ Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł. & Polosukhin, I. (2017). "Attention Is All You Need." *NeurIPS 2017*. [arXiv:1706.03762](https://arxiv.org/abs/1706.03762)**

The transformer, the architecture behind every modern LLM. Instead of joining the context vectors together and passing them through one layer, each token looks at every other token in the context window and decides which ones matter (**attention**). Look at figure 1 and compare it with our model diagram.

**Holtzman, A., Buys, J., Du, L., Forbes, M. & Choi, Y. (2020). "The Curious Case of Neural Text Degeneration." *ICLR 2020*. [arXiv:1904.09751](https://arxiv.org/abs/1904.09751)**

Why does always picking the most likely word produce repetitive text, as we saw at low temperature in the `temperature` playground? This paper shows it happens to big neural models too, and proposes **nucleus (top-p) sampling**, now a standard setting in LLM APIs.

**Kaplan, J., McCandlish, S., Henighan, T., Brown, T. B., Chess, B., Child, R., Gray, S., Radford, A., Wu, J. & Amodei, D. (2020). "Scaling Laws for Neural Language Models." [arXiv:2001.08361](https://arxiv.org/abs/2001.08361)**

What happens to the loss as you make the model bigger, the data bigger, and the training longer? It falls, smoothly and predictably, as a power law. This paper is why everyone started building enormous models.

**Brown, T. B. et al. (2020). "Language Models are Few-Shot Learners." *NeurIPS 2020*. [arXiv:2005.14165](https://arxiv.org/abs/2005.14165)**

GPT-3: our model, scaled up to 175 billion parameters. Its surprise was that a big enough next-token predictor can do a new task from a few examples in the prompt, with no further training.

**Hoffmann, J. et al. (2022). "Training Compute-Optimal Large Language Models." [arXiv:2203.15556](https://arxiv.org/abs/2203.15556)**

"Chinchilla." For a fixed amount of computing power, how big should the model be and how much text should it see? The answer is to grow both together, about 20 training tokens for every parameter. Most earlier models were too big and undertrained.

---

## Books, videos and posts

- **Jurafsky, D. & Martin, J. H. *Speech and Language Processing* (3rd edition draft).** Free online at [web.stanford.edu/~jurafsky/slp3](https://web.stanford.edu/~jurafsky/slp3/). The chapter on n-gram language models covers everything in demos 1–2 plus smoothing, backoff and perplexity, properly. Later chapters cover neural language models and transformers.
- **Andrej Karpathy, *Neural Networks: Zero to Hero*.** Free videos at [karpathy.ai/zero-to-hero.html](https://karpathy.ai/zero-to-hero.html). The "makemore" lectures start with a counting model and then build the Bengio model, very close to this module. Later lectures build a GPT from scratch, and *Let's build the GPT Tokenizer* goes deep on byte-pair encoding.
- **Andrej Karpathy (2015). "The Unreasonable Effectiveness of Recurrent Neural Networks."** [Blog post](https://karpathy.github.io/2015/05/21/rnn-effectiveness/). A letter-level neural model trained on Shakespeare, Wikipedia, LaTeX and the Linux source code. Compare with the `other-books` playground.
- **3Blue1Brown, *Neural Networks*.** Free videos at [3blue1brown.com/topics/neural-networks](https://www.3blue1brown.com/topics/neural-networks). The best visual explanation of backpropagation there is, and later videos on transformers and attention.

---

## Extensions

Bigger projects than the playground. ★ is an afternoon, ★★★ is a weekend.

**★ Shannon's approximations to English.** Write a script that prints Shannon's series: random letters, letters weighted by how common they are, then letter pairs, letter triples, single words and word pairs, all trained on *Alice*. Put your output next to his from the 1948 paper.

**★ The guessing game.** Recreate Shannon's 1951 experiment. Show a sentence from *Alice* one letter at a time and make the player guess the next letter, counting guesses. Then let the eight-letter model play the same game, guessing letters in order of probability. Who needs fewer guesses?

**★★ A fair scoreboard.** Train all five models on chapters 1–11 only. Then measure each model's perplexity on chapter 12, which none of them has seen. The counting models will need smoothing or backoff so an unseen context doesn't score zero. Which model wins on text it hasn't memorised? (Chen & Goodman, and the Jurafsky & Martin chapter, show how.)

**★★ Kneser–Ney smoothing.** Implement interpolated Kneser–Ney for the word-pair model and compare its perplexity with add-k smoothing from the `score-a-sentence` playground. The Jurafsky & Martin chapter explains the idea; the core insight is that "Francisco" is common but only ever follows "San".

**★★ A real tokenizer.** Make our tokenizer work like GPT-2's: start from the 256 possible bytes, learn merges, and split new text by replaying the merges in order. Check that any text at all, including emoji, can be tokenized and turned back into exactly the same text.

**★★ Automatic gradients.** Demo 5 works out every gradient by hand. Write a tiny `Value` class that records each calculation and can run the chain rule backwards by itself (Karpathy's *micrograd* lecture shows how). Rebuild demo 5 on it. How much slower is it, and why?

**★★★ Remember everything.** Replace the fixed three-token context with a recurrent hidden state (Mikolov 2010), in plain Python. The model now reads the whole sentence so far. Does it beat the three-token model? How long does it take to train?

**★★★ One attention head.** Replace the step that joins the three context vectors together with a single self-attention head (Vaswani 2017, section 3.2): each token scores every other token, and the scores decide how much of each one to mix in. This is the heart of a transformer, in a few dozen lines.
