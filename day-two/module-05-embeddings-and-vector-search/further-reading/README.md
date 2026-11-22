# Further reading and extensions

Where did keyword search come from? Why should words used in the same places mean similar things, how do you draw words on a map and group them, and why did counting and training find such similar neighbours? Why is adding up word vectors such a weak way to make a sentence vector?

## The exercise

1. **Pick one paper** from the reading list. If you're not sure, start with one marked ⭐.
2. **Read the part that matters.** You don't need to read it all. Each description says what to look for.
3. **Connect it to a demo.** Write two or three sentences: what problem was the paper solving, and which of our demos or playgrounds does it relate to?
4. **Pick one extension** from the list at the end and start it. Most will take longer than a break, so take them home.

---

## Reading list

### Keyword search: where demo 1 comes from

**⭐ Spärck Jones, K. (1972). "A statistical interpretation of term specificity and its application in retrieval." *Journal of Documentation* 28(1):11–21. [PDF](https://www.staff.city.ac.uk/~sbrp622/idfpapers/ksj_orig.pdf)**

Where the "rarity" line in demo 1 comes from. Spärck Jones argued that a match on a rare word should count for more than a match on a common one, and weighted each word by how few documents contain it. This is **inverse document frequency** (IDF), and it is inside nearly every keyword search engine today. Look for the section on weighting by specificity: in a collection of 200 documents, a word found in ninety of them gets a weight of 2, and a word found in three gets a weight of 7. It's why "why", in 7 of our 275 documents, outweighed "heating", in 177, and put a document about boiler sizes first.

**Robertson, S. & Zaragoza, H. (2009). "The Probabilistic Relevance Framework: BM25 and Beyond." *Foundations and Trends in Information Retrieval* 3(4):333–389. [PDF](https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf)**

BM25 explained by one of the people who created it. It's long, so read section 3.4, "The Eliteness Model and BM25". It explains the two settings at the top of demo 1. `K1` controls **saturation**: the tenth "heating" in a document adds much less than the first. `B` controls how much long documents are held back. Equation 3.15 is, almost exactly, demo 1's `bm25` function. Section 3.6, on BM25F, scores fields such as the title separately, so a match in a document's title could count for more than one in its text.

### Counting: where demo 2 comes from

**Harris, Z. S. (1954). "Distributional Structure." *Word* 10(2–3):146–162. [doi:10.1080/00437956.1954.11659520](https://doi.org/10.1080/00437956.1954.11659520)**

The idea demos 2 and 5 are built on, sixty years before word2vec: if two words keep turning up in the same surroundings, they are probably similar in meaning. This is the **distributional hypothesis**. Harris was a linguist with no computer, and the paper has no equations. Look for his argument that difference in meaning goes with difference in distribution. Demo 2 is that argument done with arithmetic: a word's surroundings, counted, are its vector. That's why *warm* ended up next to *wake* and *sunrise*.

**Church, K. W. & Hanks, P. (1990). "Word Association Norms, Mutual Information, and Lexicography." *Computational Linguistics* 16(1):22–29. [ACL Anthology](https://aclanthology.org/J90-1003/)**

The fix for demo 2's common words. A raw count rewards words that are near everything, like *is* and *and*. Church and Hanks compared how often two words appear near each other with how often chance alone would put them there, using **mutual information**. A pair that meets far more often than chance is a real association; *the* next to anything isn't. Read the section that defines their "association ratio". Weighting demo 2's counts this way is called **PMI** (pointwise mutual information).

**⭐ Levy, O. & Goldberg, Y. (2014). "Neural Word Embedding as Implicit Matrix Factorization." *NeurIPS 2014*. [Proceedings](https://papers.nips.cc/paper_files/paper/2014/hash/b78666971ceae55a8e87efb7cbfd9ad4-Abstract.html)**

Why demos 2 and 5 found such similar neighbours. They showed that word2vec's skip-gram with negative sampling is, in effect, working on demo 2's table: it counts neighbours, weights the counts by PMI, then squeezes the table into short vectors. Look for where the shift of log *k* comes from: *k* is the number of random words, demo 5's `NEGATIVES`. It means the choice between counting and training is less about what the vectors know and more about how long they are.

### Maps of words: where demo 3 comes from

**⭐ von Luxburg, U. (2007). "A Tutorial on Spectral Clustering." *Statistics and Computing* 17(4). [arXiv:0711.0189](https://arxiv.org/abs/0711.0189)**

The clearest account of what demo 3 does. Start with how alike every pair of points is (a **similarity graph**), find the few directions that keep alike points together, give each point its numbers along them, then group the points with k-means. Read section 4, "Spectral Clustering Algorithms": demo 3 follows the box headed "Normalized spectral clustering according to Ng et al.", which scales every point to length 1 before grouping, just as the demo pushes every word out to the circle. Section 6 explains the same idea as a random walk, which is our "move each word halfway towards the words it is most like".

**Ng, A. Y., Jordan, M. I. & Weiss, Y. (2001). "On Spectral Clustering: Analysis and an algorithm." *Advances in Neural Information Processing Systems 14 (NIPS 2001)*, 849–856. [Proceedings](https://papers.nips.cc/paper_files/paper/2001/hash/801272ee79cfde7fa5960571fee36b9b-Abstract.html)**

The algorithm demo 3 is built on. Look for the step that rescales each point to length 1 before running k-means, and their argument for it: when the groups are well apart, each group's points end up pointing in its own direction. Compare that with the three spokes on the map in the slides.

### Word vectors: where demo 5 comes from

**⭐ Mikolov, T., Chen, K., Corrado, G. & Dean, J. (2013). "Efficient Estimation of Word Representations in Vector Space." [arXiv:1301.3781](https://arxiv.org/abs/1301.3781)**

word2vec. Module 1's neural model learned 16 numbers for each token as a side effect of predicting the next one. word2vec keeps only that part and trains it fast, on more than a billion words, so words used in similar ways get similar vectors. Look at figure 1: the right-hand architecture, **skip-gram**, is demo 5's model. Then look at table 8, the word relationships, such as *Paris* is to *France* as *Rome* is to *Italy*. Our 1,794 words are far too few for that, which is the point of demo 5's "Why this breaks".

**Mikolov, T., Sutskever, I., Chen, K., Corrado, G. & Dean, J. (2013). "Distributed Representations of Words and Phrases and their Compositionality." *NeurIPS 2013*, 3111–3119. [arXiv:1310.4546](https://arxiv.org/abs/1310.4546)**

The follow-up that made word2vec quick, and the source of demo 5's training loop. Instead of asking "which of all the words comes next?", **negative sampling** asks "is this a real neighbour?" for one real word and a few random ones. Read section 2.2. The random words are drawn in proportion to each word's count raised to the power 3/4, which is the `counts[w] ** 0.75` in demo 5's `noise` list. They found 5 to 20 random words works for small data. Demo 5 uses 5.

**Pennington, J., Socher, R. & Manning, C. D. (2014). "GloVe: Global Vectors for Word Representation." *EMNLP 2014*, 1532–1543. [ACL Anthology](https://aclanthology.org/D14-1162/)**

Demos 2 and 5 joined up. word2vec learns from one window at a time. GloVe first counts, over the whole text, how often each word appears near each other word, exactly as demo 2 does, then fits short vectors to those counts. Look at table 1, which shows how the *ratio* of two counts separates *ice* from *steam*. It connects to the `word-vectors` playground: try more text and see how the neighbours change.

### Sentence vectors: where demos 4, 5 and 6 come from

**Arora, S., Liang, Y. & Ma, T. (2017). "A Simple but Tough-to-Beat Baseline for Sentence Embeddings." *ICLR 2017*. [OpenReview](https://openreview.net/forum?id=SyK00v5xx)**

The sums in demos 4 and 5, done better. A plain sum gives common words like "the" and "is" as much say as "heating", and they were two of the six words our question kept. Their fix: weight each word by how rare it is, then remove the one direction that every sentence shares. That improved on plain averages by 10% to 30% on tests of how similar two sentences are, and beat much bigger neural networks. Read Algorithm 1, which is only a few lines. It's an extension below.

**⭐ Reimers, N. & Gurevych, I. (2019). "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks." *EMNLP-IJCNLP 2019*, 3980–3990. [arXiv:1908.10084](https://arxiv.org/abs/1908.10084)**

How to get one vector for a whole sentence that you can compare with cosine similarity. The obvious way, averaging the vectors a language model gives each word, works badly: often worse than averaging old-fashioned word vectors (demo 5's sums, in effect). Their fix is to train the network on pairs of sentences, two copies with the same weights side by side (a **siamese network**), so that sentences with similar meanings end up with similar vectors. Finding the most similar pair among 10,000 sentences went from about 65 hours to about 5 seconds. Read the introduction and look at figure 1. Demo 6's `text-embedding-3-small` is this idea, called through an API.

**Neelakantan, A. et al. (2022). "Text and Code Embeddings by Contrastive Pre-Training." [arXiv:2201.10005](https://arxiv.org/abs/2201.10005)**

OpenAI's paper on how it trained its earlier embedding models. It doesn't describe `text-embedding-3-small`, but it is the clearest account of the idea behind it: **contrastive** training. Take pairs of texts that belong together (here, neighbouring pieces of text on the internet) and train so that each pair's vectors are close and unrelated texts are far apart. It's demo 5's "pull neighbours closer, push random words away", for whole passages. Look at how the training pairs are made, and at figure 1: bigger models give better embeddings.

### Similarity: where demo 6 comes from

**Salton, G., Wong, A. & Yang, C. S. (1975). "A vector space model for automatic indexing." *Communications of the ACM* 18(11):613–620. [doi:10.1145/361219.361220](https://doi.org/10.1145/361219.361220)**

Documents as vectors, fifty years before ours. Each document is a list of numbers with one place for every word in the vocabulary, weighted by how often the word appears and how rare it is (they cite Spärck Jones). Two documents are similar when the angle between their vectors is small: that is cosine similarity, the same calculation as in demo 6. Look at figure 1, where three words are the three axes of the space. The difference from demo 6 is what the numbers mean. Here each number belongs to one word, so two texts with no words in common can never be similar. In an embedding, no number belongs to any one word. The `distance-measures` playground builds both kinds.

**Karpukhin, V., Oğuz, B., Min, S., Lewis, P., Wu, L., Edunov, S., Chen, D. & Yih, W. (2020). "Dense Passage Retrieval for Open-Domain Question Answering." *EMNLP 2020*, 6769–6781. [arXiv:2004.04906](https://arxiv.org/abs/2004.04906)**

Demo 1 against demo 6, on Wikipedia. Embeddings are **dense** vectors: every number carries some meaning. Keyword search uses **sparse** ones: one number per vocabulary word, nearly all zero. Their dense retriever found a passage containing the answer in its top 20 far more often than BM25, by 9 to 19 points. Look at table 2, and at the rows "BM25 + DPR", which add the two scores together. On some datasets that helps; on Natural Questions it does worse than vectors alone (76.6 against 78.4).

**Muennighoff, N., Tazi, N., Magne, L. & Reimers, N. (2023). "MTEB: Massive Text Embedding Benchmark." *EACL 2023*, 2014–2037. [arXiv:2210.07316](https://arxiv.org/abs/2210.07316)**

We used `text-embedding-3-small` without comparing it with anything. MTEB tests embedding models on 8 kinds of task, 58 datasets and 112 languages, and finds that no model is best at everything. Look at how a model's place changes from one kind of task to another. Its public leaderboard (below) is where most people go to choose a model. Connects to the `other-languages` playground.

### Where it went next

**Johnson, J., Douze, M. & Jégou, H. (2021). "Billion-scale similarity search with GPUs." *IEEE Transactions on Big Data* 7(3):535–547. [arXiv:1702.08734](https://arxiv.org/abs/1702.08734)**

The paper behind FAISS, Facebook AI Research's library for searching vectors. Each of our vectors is 1,536 numbers, about 6 KB; a billion of them would take 6 TB. So they **compress** the vectors (**product quantisation** stores each one as a few short codes) and use GPUs. They linked a billion vectors to their nearest neighbours in under 12 hours on four GPUs. Read the introduction and the section on product quantisation. It's another way of making vectors smaller; compare it with the `shrink-the-vectors` playground.

**Kusupati, A. et al. (2022). "Matryoshka Representation Learning." *NeurIPS 2022*. [arXiv:2205.13147](https://arxiv.org/abs/2205.13147)**

Why the `dimensions` parameter can work. Train an embedding so that its first few numbers already make a usable, smaller embedding, like nested Russian dolls. In their image tests, embeddings up to 14 times smaller kept the same accuracy. Look at figure 1, and at **adaptive retrieval**: search a short version of every vector, then reorder the best few using the full vectors. OpenAI's guide says its newer models can be shortened without losing their meaning; this paper is the best-known way to train a model like that. Connects to the `shrink-the-vectors` playground.

**⭐ Gao, L., Ma, X., Lin, J. & Callan, J. (2023). "Precise Zero-Shot Dense Retrieval without Relevance Labels." *ACL 2023*, 1762–1777. [arXiv:2212.10496](https://arxiv.org/abs/2212.10496)**

HyDE. A question doesn't look much like the document that answers it: "before my alarm goes off" against "starts the heating before a schedule period". So ask a language model to write a **hypothetical document**, a made-up answer, then embed that and search for real documents near it. Mistakes in the made-up answer matter less than you'd think, because the search can only return real documents. Look at figure 1. It's the first extension below.

**Sciavolino, C., Zhong, Z., Lee, J. & Chen, D. (2021). "Simple Entity-Centric Questions Challenge Dense Retrievers." *EMNLP 2021*, 6138–6148. [arXiv:2109.08535](https://arxiv.org/abs/2109.08535)**

Where embeddings lose to keywords. They asked simple questions about named things, such as where a little-known person was born. A dense retriever found the right passage in its top 20 for 49.7% of them; BM25 managed 72.0%. Look at table 1: for "Where was [E] born?" it is 25.4% against 75.3%. Dense retrievers only cope well with names that were common in their training data. Dormouse's error codes, like E-104, are the same kind of thing: try them in the `similarity-explorer` playground.

**Cormack, G. V., Clarke, C. L. A. & Büttcher, S. (2009). "Reciprocal rank fusion outperforms Condorcet and individual rank learning methods." *SIGIR 2009*, 758–759. [PDF](https://cormack.uwaterloo.ca/cormacksigir09-rrf.pdf)**

**Hybrid search**: run keyword search and vector search, and merge the two lists. Each list gives a document 1 / (k + its rank), and the scores are added up. Two pages. Look at where k = 60 comes from: they picked it in a small pilot experiment and never changed it. Whether it helps depends on your data, so measure it. That's an extension below.

**Thakur, N., Reimers, N., Rücklé, A., Srivastava, A. & Gurevych, I. (2021). "BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models." *NeurIPS 2021 Datasets and Benchmarks Track*. [arXiv:2104.08663](https://arxiv.org/abs/2104.08663)**

Eighteen datasets and ten search systems. Dense retrievers trained on one dataset often lost to plain BM25 on the others, which makes BM25 a strong **baseline**: the simple method anything new has to beat. The best results came from BM25 followed by a **reranker** that reads the question and each document together; it beat BM25 on 16 of the 18 datasets. Look at table 2. Our 20 questions are one small, invented dataset; this paper shows how much the winner can change from one dataset to the next.

**Nogueira, R. & Cho, K. (2019). "Passage Re-ranking with BERT." [arXiv:1901.04085](https://arxiv.org/abs/1901.04085)**

An embedding model reads the question and the document separately, so it never compares them word by word. A **cross-encoder** reads both together and scores the pair: much better, and much too slow to run on a whole library. So a fast search finds a thousand candidates, and BERT reorders them. It beat the previous best on the MS MARCO leaderboard by 27%. The method section is short. It's the basis of the reranker extension below.

**⭐ Weller, O., Boratko, M., Naim, I. & Lee, J. (2026). "On the Theoretical Limitations of Embedding-Based Retrieval." *ICLR 2026*. [arXiv:2508.21038](https://arxiv.org/abs/2508.21038)**

A single vector of a fixed size can only express so many different "top k" results, however good the model. They build a dataset called LIMIT to show it: short profiles listing what each person likes, and questions asking who likes a given thing. The best embedding models find fewer than 20% of the right answers in their top 100; BM25 finds 93.6%. Look at figure 3. It's the strongest argument for keeping keyword search around.

**Lewis, P. et al. (2020). "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks." *NeurIPS 2020*. [arXiv:2005.11401](https://arxiv.org/abs/2005.11401)**

The paper that named **RAG**: a language model that searches a vector index of Wikipedia (using the DPR retriever, above) and writes its answer from what it finds. Look at figure 1. Demo 6 found the right document and stopped; RAG answers from it. That's Module 6.

---

## Books, videos and posts

- **Manning, C. D., Raghavan, P. & Schütze, H. (2008). *Introduction to Information Retrieval*. Cambridge University Press.** Free online at [nlp.stanford.edu/IR-book](https://nlp.stanford.edu/IR-book/). The chapter *Scoring, term weighting and the vector space model* covers tf-idf and cosine similarity; *Probabilistic information retrieval* ends with BM25; *Evaluation in information retrieval* is how to test a search properly.
- **Jurafsky, D. & Martin, J. H. *Speech and Language Processing* (3rd edition draft).** Free online at [web.stanford.edu/~jurafsky/slp3](https://web.stanford.edu/~jurafsky/slp3/). The *Embeddings* chapter covers cosine similarity and word2vec, with skip-gram and negative sampling worked through step by step. *Information Retrieval and Retrieval-Augmented Generation* covers tf-idf, BM25, dense retrieval and evaluation, and leads into RAG.
- **Jay Alammar, "The Illustrated Word2vec."** [Blog post](https://jalammar.github.io/illustrated-word2vec/). Pictures of how word2vec learns its vectors, including negative sampling. Read it alongside demo 5.
- **3Blue1Brown, *Transformers, the tech behind LLMs*.** Free video and text at [3blue1brown.com/lessons/gpt](https://www.3blue1brown.com/lessons/gpt/). The section on the embedding matrix shows how directions in an embedding space can carry meaning.
- **Simon Willison (2023). "Embeddings: What they are and why they matter."** [Blog post](https://simonwillison.net/2023/Oct/23/embeddings/). The best plain-language introduction: related articles, search by meaning, word2vec arithmetic, and images and text in the same space.
- **[OpenAI embeddings guide](https://developers.openai.com/api/docs/guides/embeddings)**: the models, the `dimensions` parameter, and a useful detail: OpenAI's embeddings already have length 1, so a plain dot product gives the same ranking as cosine similarity. The `distance-measures` playground checks that claim, and finds it holds at the top but not quite all the way down.
- **[MTEB leaderboard](https://huggingface.co/spaces/mteb/leaderboard)**: embedding models compared task by task. Sort by retrieval, then by your language.
- **[Anthropic: Introducing Contextual Retrieval](https://www.anthropic.com/research/contextual-retrieval)** (2024): search over chunks of documents, which is where Module 6 goes. Their improved embeddings alone cut failed searches by 35%; adding BM25 took that to 49%, and a reranker on top to 67%.

---

## Extensions

Bigger projects than the playground. ★ is an afternoon, ★★★ is a weekend.

**★ A document that doesn't exist.** Before searching, ask a model to write the help article it would like to find for a question. Embed that instead of the question, and search with it (Gao et al. 2023). Run all 20 questions in `data/questions.json` and count how often a right document is in the top five. Does it beat searching with the question itself? Is it worth an extra model call on every search?

**★★ Better sums.** Make demo 5's sums stronger with Arora et al.'s recipe: weight each word by how rare it is, then remove the shared direction. Train the word vectors on more of the documentation first (plain Python is slow, so start with a few dozen documents and time it). Measure on the 20 questions: how close can a model you trained yourself get to `text-embedding-3-small`?

**★★ Hybrid search.** Run demo 1's BM25 and demo 6's cosine similarity over all 275 documents, and merge the two lists with reciprocal rank fusion (Cormack et al. 2009). Measure on the 20 questions, then write a few questions that quote an error code ("E-104 came up during setup"). Does hybrid search beat vectors alone? On which kind of question?

**★★ A reranker.** Take Chroma's top 20 and reorder them with something that reads the question and each document together: a small cross-encoder model from Hugging Face, with the `local` extra (Nogueira & Cho 2019), or a language model asked to sort the list. Run the 20 questions again. Does reranking move more right documents into first place? What does it add to each search in time and money?

**★★★ HNSW by hand.** Write HNSW in plain Python from Malkov & Yashunin's algorithms 1 to 5. Fill it with 100,000 vectors (random ones are fine for timing; use 256 numbers each so plain Python copes), and put the same vectors in Chroma. For a few hundred searches, measure the time per search and the **recall@10**: how many of the true ten nearest neighbours your index finds. How do the settings `M` and `ef` trade speed for recall? Then compare your numbers with real libraries on [ANN-Benchmarks](https://ann-benchmarks.com/).

**★★★ Your own documentation, and a fair exam.** Build the search over your team's real documentation. First check that you're allowed to send it to an embedding API; if not, use a local embedding model through Ollama, as in Module 4. Then build an exam from real history instead of invented questions: last quarter's support tickets with the article that answered each one, or your search box's logs (what people typed, and what they opened next). Keep half the exam hidden while you tune anything, and score on the hidden half only at the end. Which wins on your data: keywords or vectors? Read the evaluation chapter of Manning et al. first.
