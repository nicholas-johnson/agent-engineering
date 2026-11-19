# Further reading and extensions

Where did keyword search come from? How do you turn a whole sentence into numbers? How do real vector databases avoid comparing the request with every vector? And why did hybrid search lose in demo 4?

## The exercise

1. **Pick one paper** from the reading list. If you're not sure, start with one marked ⭐.
2. **Read the part that matters.** You don't need to read it all. Each description says what to look for.
3. **Connect it to a demo.** Write two or three sentences: what problem was the paper solving, and which of our demos or playgrounds does it relate to?
4. **Pick one extension** from the list at the end and start it. Most will take longer than a break, so take them home.

---

## Reading list

### Keyword search: where demo 1 comes from

**⭐ Spärck Jones, K. (1972). "A statistical interpretation of term specificity and its application in retrieval." *Journal of Documentation* 28(1):11–21. [PDF](https://www.staff.city.ac.uk/~sbrp622/idfpapers/ksj_orig.pdf)**

Where the "rarity" line in demo 1 comes from. Spärck Jones argued that a match on a rare word should count for more than a match on a common one, and weighted each word by how few documents contain it. This is **inverse document frequency** (IDF), and it is inside nearly every keyword search engine today. Look for the section on weighting by specificity: in a collection of 200 documents, a word found in ninety of them gets a weight of 2, and a word found in three gets a weight of 7. It's why a common word adds so little to a script's score in demo 1.

**Salton, G., Wong, A. & Yang, C. S. (1975). "A vector space model for automatic indexing." *Communications of the ACM* 18(11):613–620. [doi:10.1145/361219.361220](https://doi.org/10.1145/361219.361220)**

Documents as vectors, fifty years before ours. Each document is a list of numbers with one place for every word in the vocabulary, weighted by how often the word appears and how rare it is (they cite Spärck Jones). Two documents are similar when the angle between their vectors is small, measured after scaling every vector to length one: that is cosine similarity, the same calculation as in demo 2. Look at figure 1, where three words are the three axes of the space. The difference from demo 2 is what the numbers mean. Here each number belongs to one word, so two texts with no words in common can never be similar. In an embedding, no number belongs to any one word.

**Robertson, S. & Zaragoza, H. (2009). "The Probabilistic Relevance Framework: BM25 and Beyond." *Foundations and Trends in Information Retrieval* 3(4):333–389. [PDF](https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf)**

BM25 explained by one of the people who created it. It's long, so read section 3.4, "The Eliteness Model and BM25". It explains the two settings at the top of demo 1. `K1` controls **saturation**: the tenth mention of *password* in a script adds much less than the first. `B` controls how much long scripts are held back. Equation 3.15 is, almost exactly, demo 1's `bm25` function. Section 3.6, on BM25F, scores fields such as the title separately, so a match in a script's title could count for more than one in its steps. SQLite's full-text search in demo 4 uses a version of the same formula, with `k1` fixed at 1.2 where demo 1 uses 1.5.

### Embeddings: where demo 2 comes from

**Mikolov, T., Chen, K., Corrado, G. & Dean, J. (2013). "Efficient Estimation of Word Representations in Vector Space." [arXiv:1301.3781](https://arxiv.org/abs/1301.3781)**

word2vec, previewed at the end of Module 1. Module 1's neural model learned 16 numbers for each token as a side effect of predicting the next one. word2vec keeps only that part and trains it fast, on more than a billion words, so words used in similar ways get similar vectors. Look at figure 1, the two small architectures, and table 8, the word relationships. It gives one vector per word. Demo 2 needs one vector for a whole sentence, which is the next paper.

**⭐ Reimers, N. & Gurevych, I. (2019). "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks." *EMNLP-IJCNLP 2019*, 3980–3990. [arXiv:1908.10084](https://arxiv.org/abs/1908.10084)**

How to get one vector for a whole sentence that you can compare with cosine similarity. The obvious way, averaging the vectors a language model gives each word, works badly: often worse than averaging old-fashioned word vectors. Their fix is to train the network on pairs of sentences, two copies with the same weights side by side (a **siamese network**), so that sentences with similar meanings end up with similar vectors. Finding the most similar pair among 10,000 sentences went from about 65 hours to about 5 seconds. Read the introduction and look at figure 1. Demo 2 is this idea, called through an API.

**Karpukhin, V., Oğuz, B., Min, S., Lewis, P., Wu, L., Edunov, S., Chen, D. & Yih, W. (2020). "Dense Passage Retrieval for Open-Domain Question Answering." *EMNLP 2020*, 6769–6781. [arXiv:2004.04906](https://arxiv.org/abs/2004.04906)**

Demo 1 against demo 2, on Wikipedia. Embeddings are **dense** vectors: every number carries some meaning. Keyword search uses **sparse** ones: one number per vocabulary word, nearly all zero. Their dense retriever found a passage containing the answer in its top 20 far more often than BM25, by 9 to 19 points. Look at table 2, and at the rows "BM25 + DPR", which add the two scores together. On some datasets that helps. On Natural Questions it does worse than vectors alone (76.6 against 78.4), just as hybrid search did worse than vectors in demo 4.

**Neelakantan, A. et al. (2022). "Text and Code Embeddings by Contrastive Pre-Training." [arXiv:2201.10005](https://arxiv.org/abs/2201.10005)**

OpenAI's paper on how it trained its earlier embedding models. It doesn't describe `text-embedding-3-small`, but it is the clearest account of the idea behind it: **contrastive** training. Take pairs of texts that belong together (here, neighbouring pieces of text on the internet) and train so that each pair's vectors are close and unrelated texts are far apart. Look at how the training pairs are made, and at figure 1: bigger models give better embeddings. Connects to demo 2 and the `similarity-explorer` playground.

**Muennighoff, N., Tazi, N., Magne, L. & Reimers, N. (2023). "MTEB: Massive Text Embedding Benchmark." *EACL 2023*, 2014–2037. [arXiv:2210.07316](https://arxiv.org/abs/2210.07316)**

We used `text-embedding-3-small` without comparing it with anything. MTEB tests embedding models on 8 kinds of task, 58 datasets and 112 languages, and finds that no model is best at everything. Look at how a model's place changes from one kind of task to another. Its public leaderboard (below) is where most people go to choose a model. Connects to the `other-languages` playground.

### Vector databases: where demo 3 comes from

**Malkov, Y. A. & Yashunin, D. A. (2020). "Efficient and Robust Approximate Nearest Neighbor Search Using Hierarchical Navigable Small World Graphs." *IEEE Transactions on Pattern Analysis and Machine Intelligence* 42(4):824–836. [arXiv:1603.09320](https://arxiv.org/abs/1603.09320)**

The version of sqlite-vec we use compares the request with every stored vector. That's fine for 1,000 scripts, and far too slow for 100 million. **HNSW** links each vector to a few of its neighbours, in layers. A search starts on a top layer with few vectors and long links, and zooms in layer by layer. It is **approximate**: it can miss the true nearest neighbour, in exchange for being much faster. Look at figure 1 and algorithm 2. Many vector databases use HNSW, and newer test releases of sqlite-vec are adding approximate indexes too.

**Johnson, J., Douze, M. & Jégou, H. (2021). "Billion-scale similarity search with GPUs." *IEEE Transactions on Big Data* 7(3):535–547. [arXiv:1702.08734](https://arxiv.org/abs/1702.08734)**

The paper behind FAISS, Facebook AI Research's library for searching vectors. Our 1,000 vectors of 1,536 numbers take about 6 MB; a billion would take 6 TB. So they **compress** the vectors (**product quantisation** stores each one as a few short codes) and use GPUs. They linked a billion vectors to their nearest neighbours in under 12 hours on four GPUs. Read the introduction and the section on product quantisation. It's another way of making vectors smaller; compare it with the `shrink-the-vectors` playground.

**Kusupati, A. et al. (2022). "Matryoshka Representation Learning." *NeurIPS 2022*. [arXiv:2205.13147](https://arxiv.org/abs/2205.13147)**

Why the `dimensions` parameter can work. Train an embedding so that its first few numbers already make a usable, smaller embedding, like nested Russian dolls. In their image tests, embeddings up to 14 times smaller kept the same accuracy. Look at figure 1, and at **adaptive retrieval**: search a short version of every vector, then reorder the best few using the full vectors. OpenAI's guide says its newer models can be shortened without losing their meaning; this paper is the best-known way to train a model like that. Connects to the `shrink-the-vectors` playground.

**⭐ Sciavolino, C., Zhong, Z., Lee, J. & Chen, D. (2021). "Simple Entity-Centric Questions Challenge Dense Retrievers." *EMNLP 2021*, 6138–6148. [arXiv:2109.08535](https://arxiv.org/abs/2109.08535)**

Demo 3's E-104 problem, in a paper. They asked simple questions about named things, such as where a little-known person was born. A dense retriever found the right passage in its top 20 for 49.7% of them; BM25 managed 72.0%. Look at table 1: for "Where was [E] born?" it is 25.4% against 75.3%. Dense retrievers only cope well with names that were common in their training data. An error code like E-104 is the same kind of thing, which is why demo 3 returned scripts for other errors, including E-217.

### Hybrid search: where demo 4 comes from

**⭐ Cormack, G. V., Clarke, C. L. A. & Büttcher, S. (2009). "Reciprocal rank fusion outperforms Condorcet and individual rank learning methods." *SIGIR 2009*, 758–759. [PDF](https://cormack.uwaterloo.ca/cormacksigir09-rrf.pdf)**

Two pages, and the formula in demo 4's `hybrid` function: each list gives a document 1 / (k + its rank), and the scores are added up. Look at where k = 60 comes from: they picked it in a small pilot experiment and never changed it. Our `RRF_K = 60` comes straight from here. On their data, rank fusion almost always beat the best of the systems it combined. It didn't for us: a right script was in the top 5 for 12 of our 20 requests with keywords, 18 with vectors and 15 with hybrid. The next paper explains why.

**⭐ Bruch, S., Gai, S. & Ingber, A. (2023). "An Analysis of Fusion Functions for Hybrid Retrieval." *ACM Transactions on Information Systems* 42(1):1–35. [arXiv:2210.11934](https://arxiv.org/abs/2210.11934)**

Why our hybrid search lost. Rank fusion only looks at positions, so it throws away how far apart the scores were: a script one search was sure of and a script both searches half-liked can end up level, or the wrong way round. They find rank fusion is sensitive to k, and that a **convex combination** does better: scale each search's scores to the same range, then take a weighted average. Its one weight can be chosen from a handful of examples. Read section 5, "Analysis of Reciprocal Rank Fusion". Then try both in the `fusion-knobs` playground.

**Thakur, N., Reimers, N., Rücklé, A., Srivastava, A. & Gurevych, I. (2021). "BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models." *NeurIPS 2021 Datasets and Benchmarks Track*. [arXiv:2104.08663](https://arxiv.org/abs/2104.08663)**

Eighteen datasets and ten search systems. Dense retrievers trained on one dataset often lost to plain BM25 on the others, which makes BM25 a strong **baseline**: the simple method anything new has to beat. The best results came from BM25 followed by a **reranker** that reads the question and each document together; it beat BM25 on 16 of the 18 datasets. Look at table 2. Our 20 test requests are one small, invented dataset; this paper shows how much the winner can change from one dataset to the next.

### Search as a tool: where demo 5 comes from

**⭐ Gao, L., Ma, X., Lin, J. & Callan, J. (2023). "Precise Zero-Shot Dense Retrieval without Relevance Labels." *ACL 2023*, 1762–1777. [arXiv:2212.10496](https://arxiv.org/abs/2212.10496)**

HyDE. A question doesn't look much like the document that answers it. So ask a language model to write a **hypothetical document**, a made-up answer, then embed that and search for real documents near it. Mistakes in the made-up answer matter less than you'd think, because the search can only return real documents. Look at figure 1. Demo 5's agent does a lighter version: the tool description asks for a search written like a test's title, so the agent turns a long bug report into something that looks like a script.

**Sun, W., Yan, L., Ma, X., Wang, S., Ren, P., Chen, Z., Yin, D. & Ren, Z. (2023). "Is ChatGPT Good at Search? Investigating Large Language Models as Re-Ranking Agents." *EMNLP 2023*. [arXiv:2304.09542](https://arxiv.org/abs/2304.09542)**

Give a language model a question and a numbered list of passages, and ask it to put them in order. With the right instructions, it matched or beat rerankers trained specially for the job. Look at figure 2, three ways of asking, and figure 3, a sliding window for lists too long for one prompt. Demo 5's agent does a small version of this: it reads the top five and picks one. When nothing fits, it searches again, which is the ReAct loop from Module 3's reading list.

### Where it went next

**Nogueira, R. & Cho, K. (2019). "Passage Re-ranking with BERT." [arXiv:1901.04085](https://arxiv.org/abs/1901.04085)**

An embedding model reads the request and the script separately, so it never compares them word by word. A **cross-encoder** reads both together and scores the pair: much better, and much too slow to run on a whole library. So BM25 finds a thousand candidates, and BERT reorders them. It beat the previous best on the MS MARCO leaderboard by 27%. The method section is short. It's the basis of the reranker extension below.

**Khattab, O. & Zaharia, M. (2020). "ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT." *SIGIR 2020*. [arXiv:2004.12832](https://arxiv.org/abs/2004.12832)**

A middle way between one vector per text and a cross-encoder: one vector per token. Each token of the request finds its best match among the document's tokens, and those matches are added up. Look at figure 2, which puts four designs side by side. Remember demo 2's side finding: squeezing the whole script into one vector pushed the right script down to 4th. Keeping many vectors per document keeps the detail. See the "One vector per step" extension.

**⭐ Weller, O., Boratko, M., Naim, I. & Lee, J. (2026). "On the Theoretical Limitations of Embedding-Based Retrieval." *ICLR 2026*. [arXiv:2508.21038](https://arxiv.org/abs/2508.21038)**

A single vector of a fixed size can only express so many different "top k" results, however good the model. They build a dataset called LIMIT to show it: short profiles listing what each person likes, and questions asking who likes a given thing. The best embedding models find fewer than 20% of the right answers in their top 100; BM25 finds 93.6%. Look at figure 3. It's the strongest argument for keeping keyword search around, and the E-104 lesson again.

**Lewis, P. et al. (2020). "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks." *NeurIPS 2020*. [arXiv:2005.11401](https://arxiv.org/abs/2005.11401)**

The paper that named **RAG**: a language model that searches a vector index of Wikipedia (using the DPR retriever, above) and writes its answer from what it finds. Look at figure 1. Our agent found a test script and recommended it; RAG uses the same kind of search to answer questions. It's coming up later in the course.

---

## Books, videos and posts

- **Manning, C. D., Raghavan, P. & Schütze, H. (2008). *Introduction to Information Retrieval*. Cambridge University Press.** Free online at [nlp.stanford.edu/IR-book](https://nlp.stanford.edu/IR-book/). The chapter *Scoring, term weighting and the vector space model* covers tf-idf and cosine similarity; *Probabilistic information retrieval* ends with BM25; *Evaluation in information retrieval* is how to test a search properly.
- **Jurafsky, D. & Martin, J. H. *Speech and Language Processing* (3rd edition draft).** Free online at [web.stanford.edu/~jurafsky/slp3](https://web.stanford.edu/~jurafsky/slp3/). The *Embeddings* chapter covers cosine similarity and word2vec. *Information Retrieval and Retrieval-Augmented Generation* covers tf-idf, BM25, dense retrieval and evaluation, and leads into RAG.
- **3Blue1Brown, *Transformers, the tech behind LLMs*.** Free video and text at [3blue1brown.com/lessons/gpt](https://www.3blue1brown.com/lessons/gpt/). The section on the embedding matrix shows how directions in an embedding space can carry meaning.
- **Simon Willison (2023). "Embeddings: What they are and why they matter."** [Blog post](https://simonwillison.net/2023/Oct/23/embeddings/). The best plain-language introduction: related articles, search by meaning, word2vec arithmetic, and images and text in the same space.
- **Jay Alammar, "The Illustrated Word2vec."** [Blog post](https://jalammar.github.io/illustrated-word2vec/). Pictures of how word2vec learns its vectors. Read it alongside Mikolov et al.
- **[sqlite-vec documentation](https://alexgarcia.xyz/sqlite-vec/)**: the page on [`vec0` tables](https://alexgarcia.xyz/sqlite-vec/features/vec0.html) explains the metadata columns we filtered on in demo 3, and the `+` auxiliary columns that carry the title along. Its author's post [Hybrid full-text search and vector search with SQLite](https://alexgarcia.xyz/blog/2024/sqlite-vec-hybrid-search/index.html) (2024) combines FTS5 and sqlite-vec in three ways, rank fusion among them.
- **[SQLite FTS5: the bm25() function](https://www.sqlite.org/fts5.html#the_bm25_function)**: the keyword search in demo 4. Its scores are negative, so better matches are smaller, which is why demo 4 sorts in ascending order.
- **[OpenAI embeddings guide](https://developers.openai.com/api/docs/guides/embeddings)**: the models, the `dimensions` parameter, and a useful detail: OpenAI's embeddings already have length 1, so a plain dot product gives the same ranking as demo 2's cosine similarity.
- **[MTEB leaderboard](https://huggingface.co/spaces/mteb/leaderboard)**: embedding models compared task by task. Sort by retrieval, then by your language.
- **[Anthropic: Introducing Contextual Retrieval](https://www.anthropic.com/research/contextual-retrieval)** (2024): a case where hybrid search did help. Their improved embeddings alone cut failed searches by 35%; adding BM25 took that to 49%, and a reranker on top to 67%.

---

## Extensions

Bigger projects than the playground. ★ is an afternoon, ★★★ is a weekend.

**★ A script that doesn't exist.** Before searching, ask the model to write the test script it would like to find for a request: a title, steps and an expected result. Embed that instead of the request, and search with it (Gao et al. 2023). Run all 20 requests in `data/requests.json` and count how often a right script is in the top five, as demo 4 does. Does it beat searching with the request itself? Is it worth an extra model call on every search?

**★★ Two tools.** Give the search server a second tool, `find_by_words`, that runs demo 4's FTS5 keyword search, and say in each tool's description when to use it. Then give the agent two bug reports: one about an E-104 error and one about passwords. Does it choose the right tool for each? What does it do when the two tools disagree?

**★★ A reranker.** Take the top 20 from hybrid search and reorder them with something that reads the request and each script together: a small cross-encoder model from Hugging Face, with the `local` extra (Nogueira & Cho 2019), or a language model asked to sort the list (Sun et al. 2023). Run the 20-request test again. Does reranking beat vectors' 18? What does it add to each search in time and money?

**★★ One vector per step.** Embed each script's title, each of its steps and its expected result separately, so a script has several vectors instead of one. In sqlite-vec, store one row per piece with the script's id, ask for more neighbours, and keep each script's best match. Demo 2 found that one vector for the whole script pushed the right script down to 4th. With one vector per piece, does it come back to the top? How much bigger is the database? Read Khattab & Zaharia first.

**★★★ HNSW by hand.** Write HNSW in plain Python from Malkov & Yashunin's algorithms 1 to 5. Fill it with 100,000 vectors (random ones are fine for timing; use 256 numbers each so plain Python copes), and put the same vectors in sqlite-vec. For a few hundred searches, measure the time per search and the **recall@10**: how many of the true ten nearest neighbours your index finds. How do the settings `M` and `ef` trade speed for recall? Then compare your numbers with real libraries on [ANN-Benchmarks](https://ann-benchmarks.com/).

**★★★ Your own library, and a fair exam.** Build the search over your team's real test cases. First check that you're allowed to send them to an embedding API; if not, use a local embedding model through Ollama, as in Module 4. Then build an exam from real history instead of invented requests: last quarter's bug reports with the test that should have caught each one, or your search box's logs (what people typed, and what they opened next). Keep half the exam hidden while you tune anything, and score on the hidden half only at the end. Which wins on your data: keywords, vectors or hybrid? Read the evaluation chapter of Manning et al. first.
