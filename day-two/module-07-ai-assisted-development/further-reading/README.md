# Further reading and extensions

Why was the first prototype so generic? Why did the coding agent make product decisions nobody asked it to make? Why plan before you build? How do you review code you didn't write, and who should do it? And do these tools actually make people faster, or does it only feel that way?

## The exercise

1. **Pick one paper** from the reading list. If you're not sure, start with one marked ⭐.
2. **Read the part that matters.** You don't need to read it all. Each description says what to look for.
3. **Connect it to a demo.** Write two or three sentences: what problem was the paper solving, and which of our demos does it relate to?
4. **Pick one extension** from the list at the end and start it. Most will take longer than a break, so take them home.

A note on dates. This is a fast-moving field, and the tools in this module change every few months. The papers below are the ones that explain *why* the tools work as they do. The evidence section is the one to treat with most care: several studies there measured tools that are already out of date. That is a result in itself.

---

## Reading list

### The coding agent: where demo 3 comes from

**Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K. & Cao, Y. (2023). "ReAct: Synergizing Reasoning and Acting in Language Models." *ICLR 2023*. [arXiv:2210.03629](https://arxiv.org/abs/2210.03629)**

The loop at the heart of demo 3's 80 lines. A **ReAct** agent alternates between *thinking* (writing down what it plans to do), *acting* (calling a tool) and *observing* (reading what came back), and repeats until it is done. Before this, models either reasoned without touching the world or acted without explaining themselves. Read section 2 for the loop, and the example traces in the figures, where the model's thoughts change course after a tool result surprises it. Then open `demo/03_coding_agent.py` and find the same three steps: the model's reply, the tool call, and the tool result appended to the conversation. Claude Code, Cursor and Codex are far bigger, but this is still the loop inside them.

**Jimenez, C. E., Yang, J., Wettig, A., Yao, S., Pei, K., Press, O. & Narasimhan, K. (2024). "SWE-bench: Can Language Models Resolve Real-World GitHub Issues?" *ICLR 2024*. [arXiv:2310.06770](https://arxiv.org/abs/2310.06770)**

The test that turned "can a model write code?" into "can it fix a real bug in a real project?" SWE-bench has 2,294 problems taken from real GitHub issues in 12 popular Python repositories. The model gets the codebase and the issue text, and must change the code so the project's own tests pass. When it came out in 2023 the best model, Claude 2, solved 1.96%. Look at section 2, which explains how each problem is built and checked, and ask what a passing test can and cannot tell you. In demo 3 the tests pass, and the agent still made product decisions on its own. A benchmark that only counts passing tests would score that as a success. Today's coding agents are measured on descendants of this benchmark, so read this one to understand what the numbers on their launch pages mean.

**⭐ Yang, J., Jimenez, C. E., Wettig, A., Lieret, K., Yao, S., Narasimhan, K. & Press, O. (2024). "SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering." *NeurIPS 2024*. [arXiv:2405.15793](https://arxiv.org/abs/2405.15793)**

Why demo 3 has the four tools it has, and not forty. The authors argue that an agent is a new kind of user, and needs an interface built for it, the way people need an IDE. They tested this by changing only the tools and watching the score. Look at section 3, the design principles: tools should be simple, give compact feedback, and guard against common mistakes. Then look at their editing tool, which checks the code before it saves, and at the ablation table, where taking features away makes the agent worse. Compare it with `write_file` in demo 3, which will happily save broken code, and think about what feedback the agent would need to notice. This is also the case for the **permissions** playground: the interface is where you decide what the agent may do.

**Xia, C. S., Deng, Y., Dunn, S. & Zhang, L. (2024). "Agentless: Demystifying LLM-based Software Engineering Agents." [arXiv:2407.01489](https://arxiv.org/abs/2407.01489)**

The paper that asks whether you need an agent at all. **Agentless** has no loop and no tool choice. It runs a fixed three-step process: find the faulty code, write a fix, check it against tests. On SWE-bench Lite (a 300-problem subset), it fixed 32.00% of problems at an average cost of $0.70 each, which beat every open-source agent they compared against at the time. Read the introduction and section 3 to see how little machinery it takes. It is a useful counterweight to demo 3: a loop that lets the model decide what to do next is powerful, and also where the surprises come from. Ask yourself the question from the other direction: how much freedom should the agent have, and when?

### Plan, review, then implement: where demo 4 comes from

**Wang, L., Xu, W., Lan, Y., Hu, Z., Lan, Y., Lee, R. K.-W. & Lim, E.-P. (2023). "Plan-and-Solve Prompting: Improving Zero-Shot Chain-of-Thought Reasoning by Large Language Models." *ACL 2023*. [arXiv:2305.04091](https://arxiv.org/abs/2305.04091)**

The small, research version of plan mode. Plain "let's think step by step" prompts often skip steps. Plan-and-Solve asks the model first to devise a plan, then to carry it out. Read the introduction, which names the three kinds of mistake that the plan is meant to prevent, and the prompt in the early figures. Note what this paper does *not* have: a person in the middle. In demo 4 the plan is not just there to help the model reason. It is a document a human reads and approves before any file is written. That is the extra step that stops the agent deciding for itself how early "Warm Wake" should start.

**GitHub. "Spec Kit: toolkit for spec-driven development." [github.com/github/spec-kit](https://github.com/github/spec-kit)**

A worked example of **spec-driven development**, the idea behind demo 4. It is open source, and breaks work into stages you run in your agent's chat: write down the project's principles once, specify what to build and why, make a technical plan, break it into tasks, then implement. Read the README's walkthrough, and compare its stages with the files that demo 4 writes. Note where a person is expected to read and correct something before the next stage starts. Spec Kit is also a good example of how a method turns into a template, which is the point of the **test-first** playground: write down what "done" means before the agent starts.

### The company brain: where demo 2 comes from

**⭐ Denisov-Blanch, Y., Agarwal, S., Azaletskiy, P., He, H., Schaeffer, R., Miranda, B., Vasilescu, B. & Koyejo, S. (2026). "A Few Pages of Markdown: Committed AI Configuration and Lower Quality Cost after Coding-Agent Adoption." [arXiv:2608.25241](https://arxiv.org/abs/2608.25241)**

A 2026 study of something close to demo 2's idea, applied to code. The authors looked at 441 open-source repositories and sorted them by how much AI configuration the team had committed: behavioural rules and coding standards, then named agent definitions, then several agents working together. Agents sped up work in every group, with 28 to 38% more commits. But among projects where agents came first, those with no committed configuration saw roughly twice the rise in cognitive complexity (+53% against +27%). Read the abstract and the section on RAMP, their maturity scale. Be careful: the study is observational, and the authors say themselves that teams who write such files may simply be more disciplined. It is a hint and not proof, but it points the same way as demo 2. Another finding fits this module's `AGENTS.md` slide: 73.8% of these files were written once and never changed. A company brain that nobody maintains goes stale. See the **brain-pieces** playground.

**Anthropic (2025). "Effective context engineering for AI agents." *Anthropic Engineering*, 29 September 2025. [anthropic.com/engineering/effective-context-engineering-for-ai-agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)**

Why you can't just paste everything into the prompt. The post explains **context rot**: the more tokens in the window, the less accurately the model recalls any of them, so context is a limited resource and each piece should earn its place. Read the sections on the anatomy of effective context, and on loading data "just in time" (the agent holds a file path and reads the file only when it needs it). This is the argument for several small files in demo 2 instead of one huge one, and for `AGENTS.md` pointing to the product, customer and voice files instead of containing them. Module 6's reading list has the research behind the same idea (Liu et al., "Lost in the Middle").

**AGENTS.md. "A README for agents." [agents.md](https://agents.md)**

The shared file format for instructions to coding agents, backed by several tools (Codex, Cursor and others), and now looked after by the Agentic AI Foundation. It is plain Markdown with no required fields. Read the page's example and the part on nested files, where the file nearest to the code being changed takes precedence. Claude Code reads `CLAUDE.md` in the same way. Then look at the `AGENTS.md` in demo 2 and ask what you would add, and what you would move out into its own file.

### Review and automate: where demo 5 comes from

**⭐ Perry, N., Srivastava, M., Kumar, D. & Boneh, D. (2023). "Do Users Write More Insecure Code with AI Assistants?" *Proceedings of the 2023 ACM SIGSAC Conference on Computer and Communications Security (CCS '23)*, 2785–2799. [arXiv:2211.03622](https://arxiv.org/abs/2211.03622)**

The reason demo 5 is about reviewing. Researchers gave people security-related coding tasks, some with an AI assistant and some without. Those with the assistant wrote significantly less secure code, and were more likely to believe their code was secure. The people who trusted the assistant less, and who rewrote and adjusted their prompts, did better. Look at the results sections on both findings. The model used (codex-davinci-002) is long retired, so don't read the numbers as a measure of today's tools. Read it for the pattern: *confidence went up as quality went down.* It connects to the **permissions** playground, and to why demo 5 asks what a reviewer should look at, and not simply whether the tests pass.

**Pearce, H., Ahmad, B., Tan, B., Dolan-Gavitt, B. & Karri, R. (2022). "Asleep at the Keyboard? Assessing the Security of GitHub Copilot's Code Contributions." *2022 IEEE Symposium on Security and Privacy (SP)*, 754–768. [arXiv:2108.09293](https://arxiv.org/abs/2108.09293)**

The first careful test of an AI coding assistant's security. They built 89 scenarios based on well-known weaknesses (the "CWE Top 25"), asked Copilot for code, and got 1,689 programs. About 40% were vulnerable. Read section 3 on how they built the scenarios, and the results by weakness type. As with Perry et al., the tool tested is long gone, and what lasts is the method: take a list of known mistakes, make the tool face each, count. That is what a review skill, like the one in demo 5, does on every pull request.

**⭐ Zheng, L., Chiang, W.-L., Sheng, Y., Zhuang, S., Wu, Z., Zhuang, Y., Lin, Z., Li, Z., Li, D., Xing, E. P., Zhang, H., Gonzalez, J. E. & Stoica, I. (2023). "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena." *NeurIPS 2023 Datasets and Benchmarks Track*. [arXiv:2306.05685](https://arxiv.org/abs/2306.05685)**

The paper behind "use a second model as the reviewer", and behind the automatic voice check in demo 6. A strong model such as GPT-4 agreed with human judges more than 80% of the time, which is as often as humans agree with each other. But the paper also lists the judge's faults: it prefers the answer in the first position, prefers longer answers, and prefers answers that sound like its own. Read section 4, "Limitations of LLM-as-a-judge" and the fixes they try (swapping the order, giving a reference answer). Then run the **second-opinion** playground with the same model as the author, and again with a different one, and see whether self-preference shows up. In the **voice-check** playground the judge's verdict is only as good as the voice guide you give it.

**Anthropic. "Agent Skills" and the open specification. [agentskills.io](https://agentskills.io) · [specification](https://agentskills.io/specification.md) · example skills at [github.com/anthropics/skills](https://github.com/anthropics/skills)**

The format used in demo 5. A skill is a folder with a `SKILL.md` file: a name, a description, and instructions, plus optional scripts and reference files. Agents load skills in three stages (**progressive disclosure**): at the start only the names and descriptions, then the full instructions when a task matches, then any extra files when they are needed. Read the overview page for the three stages, and the specification for the rules on fields. Skim a few of the example skills for how good ones are written: the description is a trigger ("use when..."), not a summary. See the **write-a-skill** playground. The format was started by Anthropic and has been taken up by other tools, so a skill you write for one should work in another.

### Evidence: do the tools make people faster?

This is the section to read most critically. Most of these studies measure one task, one group of people and one generation of tools.

**Peng, S., Kalliamvakou, E., Cihon, P. & Demirer, M. (2023). "The Impact of AI on Developer Productivity: Evidence from GitHub Copilot." [arXiv:2302.06590](https://arxiv.org/abs/2302.06590)**

The headline study of the first wave. Developers were asked to write an HTTP server in JavaScript as fast as they could, and those with Copilot finished 55.8% faster. Read the description of the task: a small, well-defined problem that is in many training sets, the kind of job an assistant is best at. Compare it with the next entry, which uses the same measure (time to finish) and gets a very different answer. Both can be right. The task is the difference.

**⭐ Becker, J., Rush, N., Barnes, E. & Rein, D. (2025). "Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity." *METR*. [arXiv:2507.09089](https://arxiv.org/abs/2507.09089)**

The surprising one. Sixteen experienced developers worked on 246 real tasks in projects they had known for about five years. Each task was randomly assigned to allow AI tools (mostly Cursor Pro with Claude 3.5 and 3.7 Sonnet) or to forbid them. Before starting, developers predicted AI would cut their time by 24%. Afterwards they believed it had cut it by 20%. In fact it took 19% *longer* with AI. Read the design section, and the list of factors that might explain the result, such as the size of the projects and the time spent waiting for and checking the AI's output. Treat it as a careful result about one setting and not a verdict: 16 people, early 2025 tools, and projects they knew very well. Read it for the gap between feeling fast and being fast, and think about how you would know in your own team (see the extension "Measure your own team").

**METR (2026). "We are changing our developer productivity experiment design." *METR blog*, 24 February 2026. [metr.org/blog/2026-02-24-uplift-update](https://metr.org/blog/2026-02-24-uplift-update/)**

The follow-up, and an honest account of why it is hard. With 57 developers (10 returning, 47 new) and over 800 tasks in late 2025, they estimated that the returning developers took 18% *less* time with AI (confidence interval from 38% less to 9% more), and the new ones 4% less (15% less to 9% more). Both ranges include "no effect". The authors call the data an unreliable signal, because developers increasingly refused to take part if it meant working without AI, and many held back tasks they didn't want to do without it. Read the section on selection effects. It is a good example of a measurement getting harder as the thing measured becomes normal, and of the people running the study saying so.

**Brynjolfsson, E., Li, D. & Raymond, L. R. (2025). "Generative AI at Work." *The Quarterly Journal of Economics* 140(2):889–942. [arXiv:2304.11771](https://arxiv.org/abs/2304.11771)**

Evidence from a real workplace, and not an experiment set up for the study. A company introduced an AI assistant for its customer support agents at different times, which let the authors compare 5,172 agents. Resolved issues per hour went up by 15% on average. The gain was largest for the least experienced workers, and the most experienced saw small gains in speed and small drops in quality. Read the sections on who gained most. This is the pattern to look for in demos 2 and 6: does the company brain lift the beginner more than the expert? It is also the closest match to customer feedback work in the **feedback-themes** playground.

**Noy, S. & Zhang, W. (2023). "Experimental evidence on the productivity effects of generative artificial intelligence." *Science* 381(6654):187–192. [doi:10.1126/science.adh2586](https://www.science.org/doi/10.1126/science.adh2586)**

The writing version of the same question, and relevant to demo 6. 453 college-educated professionals did occupation-specific writing tasks, such as press releases and short reports, and half were given ChatGPT. Average time fell by 40%, and quality, as rated by other professionals, rose by 18%. Read the results on the spread: the weakest writers gained most, so the gap between people narrowed. The authors warn that the real-world gains may be smaller, because someone has to check the facts and write the prompts. That someone is your voice check. (The page needs a Science login for the full text, but the abstract is free.)

**Dell'Acqua, F., McFowland, E., Mollick, E. R., Lifshitz-Assaf, H., Kellogg, K., Rajendran, S., Krayer, L., Candelon, F. & Lakhani, K. R. (2023). "Navigating the Jagged Technological Frontier: Field Experimental Evidence of the Effects of AI on Knowledge Worker Productivity and Quality." *Harvard Business School Working Paper* 24-013. [SSRN 4573321](https://papers.ssrn.com/abs/4573321)**

Why the same tool can help on one task and hurt on the next. 758 consultants at BCG were given tasks either inside or outside what the model could do well. Inside, those with AI finished 12% more work, about 25% faster, with 40% higher quality. Outside, on a task chosen so that it looked ordinary but needed information the model lacked, those with AI were 19 percentage points less likely to get the right answer. Read the introduction and the part on **centaur** and **cyborg** working styles: splitting tasks between you and the AI, or mixing them at every step. Demo 3 is the outside-the-frontier case: the work looked fine, and the product decisions were wrong. (Published later in a journal; this is the working paper version.)

**Agarwal, S., He, H. & Vasilescu, B. (2026). "AI IDEs or Autonomous Agents? Measuring the Impact of Coding Agents on Software Development." [arXiv:2601.13597](https://arxiv.org/abs/2601.13597)**

A study of what happens to real open-source projects after they start using coding agents, using a method that compares them with similar projects that didn't (difference-in-differences). Projects that began with an agent saw large early gains in speed. Projects that already used AI in their editor saw small or short-lived gains. In both cases quality fell: static-analysis warnings rose by about 18% and cognitive complexity by about 39%. Read the abstract and the results on quality, which the authors read as technical debt. It is the most direct evidence for the "Review and automate" section: more code, faster, with more to review. Like the other 2026 papers here it has been out only a short time and should be read as a first result.

**Balepur, N., Baumler, C., Chen, V., Choi, E., Rudinger, R. & Boyd-Graber, J. L. (2026). "(Im)Paired Programming: Coding Agents Improve Productivity but Harm Understanding." [arXiv:2607.26375](https://arxiv.org/abs/2607.26375)**

A small study with a point that matters for review. 54 students built a website with an agent that edits their code, or with a chatbot. The agent helped them finish, but they understood their own code less, and they were worse at extending it afterwards without the agent. The people who copied prompts in and accepted edits automatically understood least. Yet they preferred the agent, because it was quick and easy. Read the findings on the "low-effort" ways of using it. It fits the **permissions** playground and the plan step in demo 4: reading and approving the plan is how you stay in charge of code you will have to maintain. It is a study of students and a short task, so don't stretch it to experienced teams.

**DORA (Google Cloud) (2025). *State of AI-assisted Software Development 2025*. [dora.dev/dora-report-2025](https://dora.dev/dora-report-2025/)**

The yearly industry survey of how software teams work, this time on AI. Its main message, as the page puts it, is that AI is an **amplifier**: it magnifies the strengths and weaknesses an organisation already has, and the biggest returns come from fixing the surrounding system and not from the tools. The full report needs a form to download. Read the summary and the companion "AI Capabilities Model". It is a survey, so it shows what teams report and not what a controlled test would find. Use it for the question in the extension "Measure your own team".

### Where it went next

**Anthropic (2024). "Building effective agents." *Anthropic*, 19 December 2024. [anthropic.com/research/building-effective-agents](https://www.anthropic.com/research/building-effective-agents)**

The simplest guide to what to build, from people who have built it many times. It tells you to use the simplest approach that works and add complexity only when it earns its place. It names five workflow patterns: prompt chaining, routing, parallelisation, orchestrator-workers and evaluator-optimiser. Demo 5's author-then-reviewer pair is the last of those. Read the whole post. It is short. Then compare its advice with Agentless, above.

**Ben Sghaier, O., Li, H., Adams, B. & Hassan, A. E. (2026). "Don't Blame the Large Language Model: How Agent Harness Evolution Shapes Coding Agent Quality." [arXiv:2607.03691](https://arxiv.org/abs/2607.03691)**

Where the field is heading: the part around the model matters as much as the model. The **harness** is everything that sits between the developer and the model (system prompts, tools, context management and the loop), and demo 3's 80 lines are a very small one. The authors fixed the model, tracked 35 releases of one coding agent's harness, and measured how well it did on 50 SWE-bench Verified tasks. They report that harnesses are released very fast (over two releases a day across five popular open-source ones) and that quality moves from release to release. Read the abstract and introduction. It's a good reason to keep your own small test set, like the one in the **test-first** playground, and rerun it when your tools update.

---

## Books, videos and posts

- **Simon Willison (2025). "Not all AI-assisted programming is vibe coding (but vibe coding rocks)."** [simonwillison.net/2025/Mar/19/vibe-coding](https://simonwillison.net/2025/Mar/19/vibe-coding/). The short post that separates two things people call by one name. **Vibe coding** means building with a model without ever checking the code. Professional AI-assisted work means you review it, test it and could explain it. Demo 1 is the first kind, demos 3 to 5 are the second.
- **Simon Willison (2025). "Here's how I use LLMs to help me write code."** [simonwillison.net/2025/Mar/11/using-llms-for-code](https://simonwillison.net/2025/Mar/11/using-llms-for-code/). A working programmer's habits in practice.
- **Claude Code documentation.** [Best practices](https://code.claude.com/docs/en/best-practices) and [Skills](https://code.claude.com/docs/en/skills). The tool's own advice on planning first, giving it a `CLAUDE.md`, and writing skills. Documentation like this changes often; check the date. The same ideas appear in Cursor and Codex, whose docs ([Codex](https://developers.openai.com/codex/)) are worth comparing.
- **Model Context Protocol.** [modelcontextprotocol.io](https://modelcontextprotocol.io). The standard way for an agent to reach tools and data. You need it for the extension that serves the company brain to every tool.

---

## Extensions

These are bigger than the playground. They don't repeat its "Try this" ideas. ★ is an afternoon; ★★★ is a weekend.

1. **★★ Review as a real GitHub Action.** Fork a small repository you don't mind breaking. Take the review skill from demo 5 and run it headless in a GitHub Action, so that every pull request gets a review comment, a test plan and a change summary. Then open a pull request with a deliberate bug and one with a clean change. What does the reviewer catch? What does it invent? Read the permissions it needs and give it no more than it needs. (Perry et al. is the reason to keep a human as the final approver.)
2. **★★ A company brain as an MCP server.** Serve the product, customer, voice and decisions files from demo 2 through an MCP server, so that any MCP-capable tool can ask for the piece it needs, when it needs it, and not carry everything in `AGENTS.md`. Compare the answers to DOR-231 with the brain in the prompt and the brain behind tools. Read Anthropic's context engineering post first. Modules 3 and 5 show how to build a server.
3. **★★ Measure your own team.** Pick a small task your team does regularly (a bug fix, a help article, a release note). Have people do five of them with the tools and five without, in random order, and record the time and a quality score from someone who doesn't know which was which. Then ask everyone to guess the result beforehand, and compare. METR's developers were wrong by about 40 percentage points. What are you going to get wrong?
4. **★★ Spec Kit on the next ticket.** Run GitHub's Spec Kit on a follow-up ticket, such as "let customers set a different wake time for each weekday". Compare its spec, plan and task list with what demo 4 produced. Which stage needed a human to step in? Which part of the company brain would have saved you the most editing?
5. **★★★ Persistence and a migration for Dormouse.** The demo codebase keeps the setting in memory. Add a database to it, and a migration that gives every existing customer a sensible default for the new setting. Use the plan-first workflow from demo 4 and have the agent do the work, with your review. This is where product decisions get expensive: what is the default for 40,000 customers who never chose, and who do you tell? Keep a log of every decision the agent made without asking.
6. **★★★ Agent against pipeline.** Rebuild demo 3's task as a fixed pipeline in the style of Agentless: one step to find the files, one to propose the change, one to run the tests, with no loop. Compare the two on five small changes to the Dormouse code, in cost, number of tool calls, and how many product decisions each made unprompted. Which would you let run in CI unattended?
