# Further reading and extensions

Why did demo 1 make up a fix for E-305? Why not just put every document in the prompt? Where did RAG come from, and how does a vector database find the nearest chunks without checking every one? Why does a list of made-up customer questions help search find the right chunk? How do you check a citation? And why is fine-tuning the wrong way to teach a model facts?

## The exercise

1. **Pick one paper** from the reading list. If you're not sure, start with one marked ⭐.
2. **Read the part that matters.** You don't need to read it all. Each description says what to look for.
3. **Connect it to a demo.** Write two or three sentences: what problem was the paper solving, and which of our demos does it relate to?
4. **Pick one extension** from the list at the end and start it. Most will take longer than a break, so take them home.

---

## Reading list

### Hallucination: where demo 1 comes from

**⭐ Kalai, A. T., Nachum, O., Vempala, S. S. & Zhang, E. (2025). "Why Language Models Hallucinate." [arXiv:2509.04664](https://arxiv.org/abs/2509.04664)**

Why demo 1 guessed instead of saying "I don't know". The paper makes two arguments. First, pre-training makes some mistakes unavoidable: a fact with no pattern to it, such as someone's birthday, that appears only once in the training data can't be learned reliably. If 20% of birthdays appear exactly once, a base model should get at least about 20% of birthdays wrong. Second, later training doesn't fix this, because most tests give a point for a right answer and nothing for "I don't know". Like a student in a multiple-choice exam, a model scores better by guessing. Read section 1, where DeepSeek-V3 gives three different wrong dates for the first author's birthday, and section 4.2, which suggests telling the model in every test question how much a wrong answer will cost. Dormouse is the extreme case: it appears nowhere in the training data, so gpt-6-luna knew nothing and guessed "early start". Demo 6's `answered` field is the "I don't know" the paper wants rewarded.

**Ji, Z. et al. (2023). "Survey of Hallucination in Natural Language Generation." *ACM Computing Surveys* 55(12):1–38. [arXiv:2202.03629](https://arxiv.org/abs/2202.03629)**

The survey that gave the field its words. Section 2.1 splits hallucinations in two. An **intrinsic** hallucination contradicts the source the model was given. An **extrinsic** one can't be checked against the source at all. Demo 1 gave the model no source, so its E-305 fix (cut the power at the breaker, when the real fix is to check the boiler pressure) is extrinsic: nothing in the prompt could confirm or contradict it. Once demos 2 to 6 hand the model documents, the worry becomes intrinsic: an answer that disagrees with the chunks in front of it. Read section 2, then section 9 on question answering. Use the rest as a reference.

**Mallen, A., Asai, A., Zhong, V., Das, R., Khashabi, D. & Hajishirzi, H. (2023). "When Not to Trust Language Models: Investigating Effectiveness of Parametric and Non-Parametric Memories." *ACL 2023*, 9802–9822. [arXiv:2212.10511](https://arxiv.org/abs/2212.10511)**

How much a model knows about something depends on how famous it is. They built PopQA, about 14,000 questions about people, places and works, and measured fame by Wikipedia page views. Models did well on popular subjects and badly on obscure ones, and bigger models mostly got better at the popular ones. Retrieval helped most in this **long tail** of obscure subjects, and could hurt on popular ones when it fetched a page about the wrong thing. Look at figure 1, then section 6, **adaptive retrieval**: search only when the question is about something obscure, which improved accuracy and cut the cost of answering. Dormouse is at the very end of the long tail, with no page views at all. That's why demo 1 had to guess, and why demo 3 always searches.

### Long context: where demo 2 comes from

**⭐ Liu, N. F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M., Petroni, F. & Liang, P. (2024). "Lost in the Middle: How Language Models Use Long Contexts." *Transactions of the Association for Computational Linguistics* 12:157–173. [arXiv:2307.03172](https://arxiv.org/abs/2307.03172)**

Fitting in the context window is not the same as being used. They gave models 10, 20 or 30 Wikipedia passages, one of which held the answer, and moved that passage from first to last. Accuracy made a U shape: best when the answer was at the start or the end, worst in the middle. With 20 or 30 passages and the answer in the middle, GPT-3.5-Turbo did worse than with no passages at all (56.1%). Look at figure 1. Then read section 5: when the passages came from a search, going beyond 20 of them added only 1 to 1.5 points, while the prompt, and the bill, kept growing. In demo 2 the Warm Wake section is buried somewhere in every document we have. In demo 3 it is one of five chunks.

**Hsieh, C.-P., Sun, S., Kriman, S., Acharya, S., Rekesh, D., Jia, F., Zhang, Y. & Ginsburg, B. (2024). "RULER: What's the Real Context Size of Your Long-Context Language Models?" *COLM 2024*. [arXiv:2404.06654](https://arxiv.org/abs/2404.06654)**

The advertised window is not the window that works. The usual test hides one fact (a **needle in a haystack**) in a long text, and most models pass it. RULER adds harder tasks: several needles, following a chain of variables, finding the most common words in a long list, and answering questions among distracting paragraphs. A model's **effective context length** is the longest input at which it still scores at least 85.6%, which is what Llama 2 7B scores at 4,000 tokens. Of the models that claimed 32,000 tokens or more, only half held up at 32,000. Look at table 3: GPT-4 claimed 128K and managed 64K. gpt-6-luna's 1,050,000 tokens is a claim worth testing the same way before you put a whole knowledge base in the prompt.

**Li, Z., Li, C., Zhang, M., Mei, Q. & Bendersky, M. (2024). "Retrieval Augmented Generation or Long-Context LLMs? A Comprehensive Study and Hybrid Approach." *EMNLP 2024 Industry Track*, 881–893. [arXiv:2407.16833](https://arxiv.org/abs/2407.16833)**

Demo 2 against demo 3, measured. Given enough budget, putting everything in the prompt beat RAG on average for Gemini-1.5-Pro, GPT-4o and GPT-3.5-Turbo. But the two gave exactly the same answer for 63% of questions. So they built **Self-Route**: try RAG first, telling the model it may reply "unanswerable" if the chunks don't contain the answer, and send only those questions on with the whole context. That stayed close to long-context accuracy and cut the cost by 65% for Gemini-1.5-Pro and 39% for GPT-4o. Look at figure 1, and at section 5.2's four reasons RAG fails, such as questions that need one search before you know what to search for next. Demo 6's `answered: false` is the same signal Self-Route uses to decide.

### Retrieval-augmented generation: where demo 3 comes from

**⭐ Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Küttler, H., Lewis, M., Yih, W., Rocktäschel, T., Riedel, S. & Kiela, D. (2020). "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks." *Advances in Neural Information Processing Systems 33 (NeurIPS 2020)*, 9459–9474. [arXiv:2005.11401](https://arxiv.org/abs/2005.11401)**

The paper that named **RAG**, promised at the end of Module 5's reading list. A retriever (DPR, also in Module 5's list) searches 21 million 100-word chunks of Wikipedia, and a generator (BART, a language model) writes the answer from what it finds. They call the model's weights its **parametric memory** and the searchable index its **non-parametric memory**. Look at figure 1, then section 4.5 on "index hot-swapping". They asked about 82 world leaders who changed between 2016 and 2018. With the index that matched the year, it answered 70% (2016) and 68% (2018) correctly; with the wrong year's index, 12% and 4%. Change the documents and the answers change, with no retraining. That is why demo 4's server checks the documents on every search: an edited document can be found straight away. One difference from demo 3: they trained the question encoder and the generator together, where we use two models off the shelf.

**Guu, K., Lee, K., Tung, Z., Pasupat, P. & Chang, M.-W. (2020). "Retrieval Augmented Language Model Pre-Training." *ICML 2020*, PMLR 119:3929–3938. [arXiv:2002.08909](https://arxiv.org/abs/2002.08909)**

REALM: the same idea in the same year, built in deeper. Instead of adding search to a finished model, REALM learns to search while it is being pre-trained. To fill in a blanked-out word, it first fetches passages from Wikipedia (about 13 million chunks), and the training signal flows back into the retriever, so it learns which passages help. Look at figure 1: to fill the gap in "the ___ at the top of the pyramid", the retriever is rewarded for finding a passage about the pyramidion. It beat earlier systems on three question-answering tests by 4 to 16 points. The cost is that search and model are tied together. Demo 3 keeps them apart, which is why we can swap the documents or the model (Module 4) without retraining anything.

**Gao, Y. et al. (2023). "Retrieval-Augmented Generation for Large Language Models: A Survey." [arXiv:2312.10997](https://arxiv.org/abs/2312.10997)**

A map of everything people have added to RAG since 2020. Don't read it through; use it as an index. Figure 3 puts three stages side by side. **Naive RAG** is index, retrieve, generate: demo 3 exactly. **Advanced RAG** adds steps before and after the search, and demo 5 is one of them. **Modular RAG** breaks the pipeline into parts you can rearrange. Section III-B1, "Chunking Strategy", covers the trade-off behind demo 3's chunks: bigger chunks carry more context and more noise. Section II-D and figure 4 compare RAG with fine-tuning (see "Why not fine-tune?" below).

**Chen, T., Wang, H., Chen, S., Yu, W., Ma, K., Zhao, X., Zhang, H. & Yu, D. (2024). "Dense X Retrieval: What Retrieval Granularity Should We Use?" *EMNLP 2024*, 15159–15177. [arXiv:2312.06648](https://arxiv.org/abs/2312.06648)**

How big should a chunk be? Demo 3 cuts at headings. This paper compares 100-word passages, single sentences and **propositions**: the smallest statements that each carry one fact and make sense on their own. Figure 1 shows why it matters. Asked how far the Leaning Tower of Pisa leans, a passage brings dates and other details, a sentence says "the tower" without saying which, and the proposition "The Leaning Tower of Pisa now leans at about 3.99 degrees" answers it alone. For embedding models trained without labelled examples, propositions raised top-20 recall by 10.1 points on average; for models trained with them, by 2.7. Look at figure 1 and table 3. "Make sense on their own" is the reason demo 3 puts "Document title > Heading" at the top of every chunk.

**⭐ Malkov, Y. A. & Yashunin, D. A. (2020). "Efficient and Robust Approximate Nearest Neighbor Search Using Hierarchical Navigable Small World Graphs." *IEEE Transactions on Pattern Analysis and Machine Intelligence* 42(4):824–836. [arXiv:1603.09320](https://arxiv.org/abs/1603.09320)**

How ChromaDB searches demo 3's chunks without comparing the question with every one. **HNSW** links each vector to a few of its neighbours, in layers. A search starts on a top layer with few vectors and long links, and zooms in layer by layer. It is **approximate**: it can miss the true nearest neighbour, in exchange for being much faster. Look at figure 1 and algorithm 2. In demo 3, `configuration={"hnsw": {"space": "cosine"}}` is the setting for this index, and Chroma's `max_neighbors` and `ef_search` settings are the paper's `M` and `ef`. On our 1,823 chunks it finds exactly what comparing every chunk finds; the speed only matters at millions.

### Turning documents into questions: where demo 5 comes from

**⭐ Nogueira, R., Yang, W., Lin, J. & Cho, K. (2019). "Document Expansion by Query Prediction." [arXiv:1904.08375](https://arxiv.org/abs/1904.08375)**

Demo 5's idea, five years earlier and for keyword search. Train a model on pairs of a search and the passage that answered it. Then, for every passage in the collection, have it write 10 searches the passage might answer, and paste them onto the end of the passage before indexing. They called it **doc2query**. The general idea is **document expansion**: change the documents, not the question. On the MS MARCO passage collection's test set it raised BM25's score (MRR@10, which rewards putting the right passage near the top) from 18.6 to 21.8. Look at figure 1, then at the analysis of the predicted words. 69% were copied from the passage, which tells the search which of its words matter; 31% were new, words a searcher might use that the passage never did. Each helped, and both together helped most. A search took 90 ms instead of 50. Its successor, docTTTTTquery ([Nogueira & Lin, 2019, PDF](https://cs.uwaterloo.ca/~jimmylin/publications/Nogueira_Lin_2019_docTTTTTquery-v2.pdf)), used the T5 model and reached 27.2 on the same test. Demo 5 stores its questions as vectors of their own that point back to their chunk, rather than pasting them on, but the deal is the same: the work happens once, when indexing, not on every question.

**Lewis, P., Wu, Y., Liu, L., Minervini, P., Küttler, H., Piktus, A., Stenetorp, P. & Riedel, S. (2021). "PAQ: 65 Million Probably-Asked Questions and What You Can Do With Them." *Transactions of the Association for Computational Linguistics* 9:1098–1115. [arXiv:2102.07033](https://arxiv.org/abs/2102.07033)**

Demo 5 taken all the way. They generated questions and answers for 10 million Wikipedia passages and kept a pair only if a separate question-answering system, not shown the passage, came up with the same answer. That left 65 million pairs. Their system, RePAQ, answers a new question by finding the nearest stored question and returning its answer: more than 1,000 questions a second, with no language model writing anything. It can also tell when it is unsure. When the nearest stored question isn't close enough, it can decline, or hand the question to a slower, better system; together the two were both faster and more accurate than the slow system alone. Look at figure 1 and section 5.2.4 on answering selectively. Demo 5 uses its questions only to find chunks, and still asks gpt-6-luna to write the answer. See the "An FAQ that answers itself" extension.

**Gao, L., Ma, X., Lin, J. & Callan, J. (2023). "Precise Zero-Shot Dense Retrieval without Relevance Labels." *ACL 2023*, 1762–1777. [arXiv:2212.10496](https://arxiv.org/abs/2212.10496)**

The mirror image of demo 5, and in Module 5's reading list too. Demo 5 makes the documents look more like questions. **HyDE** makes the question look more like a document: it asks a model to write a made-up answer, then searches with that. Look at figure 1. Then compare the bills: demo 5 pays for a model call per ten chunks, once; HyDE pays for one per question, every time, as demo 4's agent does. Which would you rather pay for at 30 questions a day? At 30,000?

### Citations: where demo 6 comes from

**⭐ Gao, T., Yen, H., Yu, J. & Chen, D. (2023). "Enabling Large Language Models to Generate Text with Citations." *EMNLP 2023*, 6465–6488. [arXiv:2305.14627](https://arxiv.org/abs/2305.14627)**

How to score citations without a person checking each one. Their benchmark, ALCE, gives models questions and a search over Wikipedia or the web, and asks for answers with numbered citations. Then a model trained for **natural language inference** (deciding whether one text follows from another) measures two things. **Citation recall**: is each statement fully supported by what it cites? **Citation precision**: is each citation needed? On ELI5, a set of open "why" and "how" questions, even the best models lacked full support for their statements half the time. Look at figure 1 and section 3.3. Demo 6's check is simpler and stricter: a quote must appear word for word in the chunk it cites. That catches an invented quote. It doesn't catch a real quote attached to a claim it doesn't support, which is what an inference model is for.

**Liu, N. F., Zhang, T. & Liang, P. (2023). "Evaluating Verifiability in Generative Search Engines." *Findings of EMNLP 2023*, 7001–7025. [arXiv:2304.09848](https://arxiv.org/abs/2304.09848)**

The same measures, on real products. In March 2023 they asked Bing Chat, NeevaAI, perplexity.ai and YouChat 1,450 questions, and had people check the sentences against the pages they cited. Only 51.5% of sentences were fully supported by their citations, and only 74.5% of citations supported the sentence they were attached to. Then read section 4.3: the engines whose answers people rated most useful had the least precise citations. An answer that looks well sourced is not the same as one that is, which is why demo 6 checks its quotes in code instead of trusting how the answer reads.

**Menick, J. et al. (2022). "Teaching language models to support answers with verified quotes." [arXiv:2203.11147](https://arxiv.org/abs/2203.11147)**

GopherCite, from DeepMind: demo 6's design, built into the model. Each answer comes with a claim and a quote, and the model's output is constrained so the quote can only be text that really is in the retrieved document: it cannot invent a quote at all. Raters judged its answers supported and plausible 80% of the time on a set of Natural Questions and 67% on ELI5. Letting it decline the third of questions it was least sure about raised that to 90% and 80%. Read section 2.9 on declining to answer. Then read section 3.7, "Misalignment between 'Supported' and 'True'": a quote can support a claim that is still false, because the source was fiction, a joke or a study nobody could repeat. Demo 6's quote check can't catch that either.

**Es, S., James, J., Espinosa-Anke, L. & Schockaert, S. (2024). "RAGAs: Automated Evaluation of Retrieval Augmented Generation." *EACL 2024 System Demonstrations*, 150–158. [arXiv:2309.15217](https://arxiv.org/abs/2309.15217)**

Scoring without an answer key. Demos 3 to 6 score answers against the facts in `data/questions.json`, which someone had to write. RAGAS uses a language model to score three things without them. **Faithfulness**: split the answer into short statements, ask whether the retrieved text supports each one, and report the share that it does. **Answer relevance**: does it answer the question that was asked? **Context relevance**: how much of the retrieved text was needed? On their small WikiEval test, its faithfulness judgements agreed with people's 95% of the time (table 1). Read section 3. It's also a Python library, and the starting point for the "A judge for every claim" extension.

### Why not fine-tune?

**⭐ Ovadia, O., Brief, M., Mishaeli, M. & Elisha, O. (2024). "Fine-Tuning or Retrieval? Comparing Knowledge Injection in LLMs." *EMNLP 2024*, 237–250. [arXiv:2312.05934](https://arxiv.org/abs/2312.05934)**

RAG against fine-tuning, tested. They tried to teach three 7-billion-parameter models new facts in two ways: **fine-tuning**, carrying on training the model on the documents, and RAG. The facts came from five MMLU subjects and from 910 questions about US events between August and November 2023, after the models' training data ended. RAG won throughout. On the current events, Mistral-7B went from 48.1% to 87.5% with RAG, and to 50.4% with fine-tuning. Fine-tuning did better (58.8%) when each fact was trained in several paraphrased versions, and figure 4 shows accuracy rising with every extra paraphrase. A model needs to see a fact many ways before it can recall it; a search only needs to find it once. Read table 2 and section 6, "The Importance of Repetition".

**Gekhman, Z., Yona, G., Aharoni, R., Eyal, M., Feder, A., Reichart, R. & Herzig, J. (2024). "Does Fine-Tuning LLMs on New Knowledge Encourage Hallucinations?" *EMNLP 2024*, 7765–7784. [arXiv:2405.05904](https://arxiv.org/abs/2405.05904)**

Worse than not working: fine-tuning on facts a model doesn't know can teach it to make things up. They sorted training questions by whether the model already knew the answer, then fine-tuned on different mixes. Examples with new facts were learned much more slowly, and as the model finally learned them, it hallucinated more on other questions, in proportion. Look at figure 1: accuracy on held-back questions peaks early, once the model has fitted the facts it already knew and before it has fitted many new ones. Their conclusion is that fine-tuning mostly teaches a model to use what it already knows. Fine-tuning gpt-6-luna on Dormouse's documentation would ask it to do the thing it is worst at.

**Berglund, L., Tong, M., Kaufmann, M., Balesni, M., Stickland, A. C., Korbak, T. & Evans, O. (2024). "The Reversal Curse: LLMs trained on 'A is B' fail to learn 'B is A'." *ICLR 2024*. [arXiv:2309.12288](https://arxiv.org/abs/2309.12288)**

A clear, strange example of how a fact in the weights differs from a fact in the prompt. Fine-tune a model on "Uriah Hawthorne is the composer of Abyssal Melodies" and ask "Who composed Abyssal Melodies?": it does no better than picking a random name. Training on many rewordings didn't help. Real facts show the same pattern: GPT-4 answered "Who is Tom Cruise's mother?" correctly 79% of the time, and "Who is Mary Lee Pfeiffer's son?" only 33%. But put "A is B" in the context window, and models work out "B is A" easily. Look at figure 1 and table 1. Customers come at Warm Wake from both ends: "What is Warm Wake?" and "Why does my heating come on early?" With RAG, the fact is in the prompt either way.

### Where it went next

**Trivedi, H., Balasubramanian, N., Khot, T. & Sabharwal, A. (2023). "Interleaving Retrieval with Chain-of-Thought Reasoning for Knowledge-Intensive Multi-Step Questions." *ACL 2023*, 10014–10037. [arXiv:2212.10509](https://arxiv.org/abs/2212.10509)**

Searching more than once. Demo 3 searches once, with the customer's own words. Some questions need a fact you only learn from the first search: their example, "In what country was Lost Gravity manufactured?", needs the manufacturer before you can search for the country. **IRCoT** takes turns: write one sentence of reasoning, use that sentence as the next search, and repeat. On four multi-step question sets it improved retrieval by up to 21 points and answers by up to 15. Look at figure 2. Give a model a search tool and let it decide when to search, as demo 4 does, and you get the same loop. People now call this **agentic RAG**.

**Asai, A., Wu, Z., Wang, Y., Sil, A. & Hajishirzi, H. (2024). "Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection." *ICLR 2024*. [arXiv:2310.11511](https://arxiv.org/abs/2310.11511)**

Demo 3 fetches five chunks for every question, needed or not. Self-RAG trains a model (Llama 2, 7B and 13B) to decide for itself, using special **reflection tokens** that it writes as it goes: should I search now? Is this passage relevant? Is my sentence fully, partly or not supported by it? How useful is my answer? Look at table 1, the four kinds of token, and figure 1. The third token is demo 6's quote check, done by the model instead of by code.

**Edge, D. et al. (2024). "From Local to Global: A Graph RAG Approach to Query-Focused Summarization." [arXiv:2404.16130](https://arxiv.org/abs/2404.16130)**

Questions no chunk answers. "What do customers complain about most?" isn't in any one chunk, so a top-5 search can't answer it. GraphRAG has a model read every chunk once and pull out the things it mentions and how they relate, building a **knowledge graph**. It groups related things into communities and writes a summary of each. A question is answered from the summaries, and the partial answers are combined. On two collections of about 1 and 1.7 million tokens, a language model acting as judge found its answers more comprehensive than plain RAG's between 72% and 83% of the time. Look at figure 1. Note the cost: a model call for every chunk before you can ask anything. Microsoft's version is open source at [github.com/microsoft/graphrag](https://github.com/microsoft/graphrag).

**Zou, W., Geng, R., Wang, B. & Jia, J. (2025). "PoisonedRAG: Knowledge Corruption Attacks to Retrieval-Augmented Generation of Large Language Models." *34th USENIX Security Symposium*, 3827–3844. [arXiv:2402.07867](https://arxiv.org/abs/2402.07867)**

Once the knowledge base decides the answers, whoever can write to it can change them. Five texts written for one target question, added to a knowledge base of millions, produced the attacker's chosen answer 90% of the time, and the defences they tried weren't enough. Read the introduction. Demo 4 showed the accidental version of the problem: its server handed the model internal sections for customer questions as readily as the user guide. Who may read, and who may write, which documents is Module 8.

---

## Books, videos and posts

- **Jurafsky, D. & Martin, J. H. *Speech and Language Processing* (3rd edition draft).** Free online at [web.stanford.edu/~jurafsky/slp3](https://web.stanford.edu/~jurafsky/slp3/). The chapter *Information Retrieval and RAG* (chapter 11 in the August 2026 draft) goes from search to RAG in one place.
- **Andrej Karpathy (2025), *Deep Dive into LLMs like ChatGPT*.** [Video](https://www.youtube.com/watch?v=7xTGNNLPyMI). The section "hallucinations, tool use, knowledge/working memory" (from 1:20:32) explains why models make things up, and the difference between what a model remembers from training and what it can read in its context window. That difference is the whole idea of RAG.
- **Lilian Weng (2024). "Extrinsic Hallucinations in LLMs."** [Blog post](https://lilianweng.github.io/posts/2024-07-07-hallucination/). Causes (including fine-tuning on new knowledge, as in Gekhman et al.), ways to detect hallucination, and fixes, including retrieval with citations, GopherCite and Self-RAG. Note that she uses *extrinsic* slightly differently from Ji et al.: for her it means not grounded in the training data or the world.
- **[Anthropic: Introducing Contextual Retrieval](https://www.anthropic.com/research/contextual-retrieval)** (2024). Demo 3 puts "Document title > Heading" at the top of each chunk so the chunk makes sense alone. Anthropic goes further: a model reads the whole document and writes 50 to 100 tokens of context for each chunk, such as "This chunk is from an SEC filing on ACME corp's performance in Q2 2023". It also says a knowledge base under 200,000 tokens (about 500 pages) can simply go in the prompt: demo 2's answer, for small collections.
- **[Anthropic: Citations](https://platform.claude.com/docs/en/build-with-claude/citations)**. Citations built into an API. You pass documents, and the reply comes back with the exact text it cites, which the API guarantees points into the documents you sent. It can't be combined with structured outputs, so you'd get citations or demo 6's JSON, not both.
- **[OpenAI: Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs)**. How demo 6 makes gpt-6-luna reply with exactly `answered`, `answer` and `citations`, and nothing else.
- **[OpenAI: Retrieval](https://developers.openai.com/api/docs/guides/retrieval)**. Demo 3 as a service. Upload files to a vector store and OpenAI chunks them (800 tokens with 400 tokens of overlap, by default), embeds them and searches them, with filters on metadata and a mix of keyword and vector ranking. Worth comparing with what we built by hand.
- **[Chroma documentation](https://docs.trychroma.com/)**: collections, metadata filters (`where`, and `where_document` for filtering on the text itself), and the HNSW settings behind demo 3.
- **Eugene Yan (2023). "Patterns for Building LLM-based Systems & Products."** [Blog post](https://eugeneyan.com/writing/llm-patterns/). Seven patterns, from evaluations to defensive user interfaces. The RAG section makes the point behind demo 3's checksums: keeping an index up to date is cheaper than training the model again.
- **Hamel Husain (2024). "Your AI Product Needs Evals."** [Blog post](https://hamel.dev/blog/posts/evals/). The case for a test set like our 30 questions. Start with cheap checks that run on every change (demo 3's `contains_facts` is one), add review by people and by models, and look at your data. It has a section on evaluating RAG.

---

## Extensions

Bigger projects than the playground. ★ is an afternoon, ★★★ is a weekend.

**★ Where the answer sits.** Build prompts of 20, 100 and 500 chunks from `demo/output/chunks.json`, leaving out every chunk that mentions Warm Wake. Then put the user guide's Warm Wake chunk first, in the middle or last, ask demo 1's question five times at each position, and count the answers that contain "Warm Wake" and "90" (demo 3's `contains_facts` does this). Do you get Liu et al.'s U shape with gpt-6-luna, or have newer models fixed it? Does it get worse as the prompt grows? Read Liu et al. first.

**★★ An FAQ that answers itself.** Change demo 5 so the model writes a short answer next to each question it generates. When a customer asks something, find the nearest stored question. If it is close enough, reply with its stored answer straight away, with no call to gpt-6-luna; if not, fall back to demo 3. Over the 30 questions, try several thresholds: how many are answered from the FAQ, how many of those are right, and how much faster and cheaper is it? Then change a fact in the user guide, such as how long a household invitation lasts. Which stored answers are now wrong, and how will you know to rewrite them? Read Lewis et al. 2021 (PAQ).

**★★ A judge for every claim.** Demo 6 checks that each quote is really in its chunk. Add a second check, in the style of RAGAS faithfulness: split each answer into short statements, and ask a model whether the chunks it cited support each one. Run it over the 30 answers demo 6 writes to `demo/output/06_citations.json`. Find an answer whose quotes all pass the word-for-word check but which still says something the quotes don't. Run the judge twice: does it always agree with itself? Read Es et al. and Gao et al. 2023 (ALCE).

**★★ Search until you're sure.** Demo 4's agent may search again, but rarely does: 1.2 searches a question. Write five new questions that need two documents, where what the first search finds tells you what to search for next. How often does the agent search twice when it needs to? Then change its instructions so it writes one sentence of reasoning before each search, as IRCoT does, and compare the searches, the answers and what each answer costs. Read Trivedi et al. first.

**★★★ Teach it by fine-tuning instead.** Fine-tune a small open model from Hugging Face, such as Qwen3-0.6B (with the `local` extra), on the user guide: once as it is, and once with ten reworded versions of every section written by a model. Ask the 30 questions with no documents in the prompt, and compare with demo 6's RAG results. Then change a fact in the user guide, such as how early Warm Wake can start. What does it take to make the fine-tuned model forget the old fact, and does it learn the new one? Ask about Warm Wake from both ends. Read Ovadia et al., Gekhman et al. and Berglund et al. first.

**★★★ Your own knowledge base, and a real exam.** Build demos 3 and 6 over your team's real documentation. First check that you're allowed to send it to an API; if not, use a local embedding model and a local language model through Ollama, as in Module 4. Leave internal documents out until you've done Module 8. Then build the exam from real support tickets instead of invented questions: the customer's first message as the question, and the facts in the reply that solved it as the answer. Keep half the exam hidden while you tune anything, and score on the hidden half only at the end. How many tickets could your documentation have answered at all? The ones it couldn't are a list of documentation to write.
