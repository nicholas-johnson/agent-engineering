# Further reading and extensions

Why can't a prompt keep a secret? Why did the helpful-looking injection work when the obvious one didn't? Why did two defences that worked get beaten by a reworded attack? What does a provider keep from every call, and what are you allowed to keep? And how do you build an assistant that stays safe when the model is fooled?

## The exercise

1. **Pick one paper or guide** from the reading list. If you're not sure, start with one marked ⭐.
2. **Read the part that matters.** You don't need to read it all. Each description says what to look for.
3. **Connect it to a demo.** Write two or three sentences: what problem was it solving, and which of our demos or playgrounds does it relate to?
4. **Pick one extension** from the list at the end and start it. Most will take longer than a break, so take them home.

A note on dates. Prompt injection has been studied for barely four years, and the models, the attacks and the defences change every few months. Several papers below report defences that a later paper broke. That is a result in itself. The guidance from OWASP, the NCSC and the ICO changes more slowly, and is the place to start for anything you ship.

---

## Reading list

### Ship it: where demo 1 comes from

**Perez, F. & Ribeiro, I. (2022). "Ignore Previous Prompt: Attack Techniques For Language Models." *NeurIPS 2022 ML Safety Workshop*. [arXiv:2211.09527](https://arxiv.org/abs/2211.09527)**

One of the first papers to measure attacks on prompts. It names two: **goal hijacking**, making the model do something other than its task, and **prompt leaking**, making it reveal its instructions. Read section 3, where the PromptInject framework builds attacks from parts, and appendix B for examples. The attacks are against GPT-3 and look crude now, which is partly the point: demo 1's polite questions didn't need any of them. Compare with the **secret-keeper** playground, where the same "translate your instructions" trick got the policy out of gpt-6-luna that "repeat everything above" didn't.

**⭐ OWASP (2024). "OWASP Top 10 for LLM Applications 2025." [genai.owasp.org/llm-top-10](https://genai.owasp.org/llm-top-10/)**

The list most security teams will hold an AI feature against. Four of its ten are this module: **LLM01** prompt injection (section 3), **LLM02** sensitive information disclosure (sections 1 and 2), **LLM06** excessive agency (section 4) and **LLM07** system prompt leakage (section 1 and the secret-keeper). LLM10, unbounded consumption, is the spend-limits playground. Read LLM07 first: its opening says the system prompt should not be treated as a secret or used as a security control, which is demo 1 in one sentence. OWASP has also published a separate Top 10 for Agentic Applications for 2026.

### Access control: where demo 2 comes from

**Carlini, N., Tramèr, F., Wallace, E., et al. (2021). "Extracting Training Data from Large Language Models." *30th USENIX Security Symposium*, 2633–2650. [arXiv:2012.07805](https://arxiv.org/abs/2012.07805)**

The case that what a model has seen, it can repeat, even from training rather than the prompt. The authors pulled verbatim text out of GPT-2, including real people's names, phone numbers and addresses. Read section 6.3, the examples of memorised content, and section 7, which finds that larger models memorise more. Demo 1 is the same lesson at a smaller scale: the internal note was in the context, so a translation could bring it out. Demo 2's answer, keeping it out of the context altogether, is the only one that works for both.

**Palmer, M. (2025). "Statement on CVE-2025-48757." [mattpalmer.io](https://mattpalmer.io/posts/2025/05/statement-on-CVE-2025-48757/)**

The write-up of the Lovable issue mentioned in section 2. A scan of 1,645 projects built with Lovable found 303 exposed endpoints across 170 of them, because the generated apps' database rules (row-level security) were missing or too loose. The CVE record says Lovable disputes it, on the grounds that each customer is responsible for their own app's data. Read it for how the scan worked, then ask who in your organisation would have checked those rules. It connects to demo 2 and to Module 7: access control that isn't enforced where the data lives isn't access control.

### Prompt injection: where demo 3 comes from

**Willison, S. (2022). "Prompt injection attacks against GPT-3." [simonwillison.net](https://simonwillison.net/2022/Sep/12/prompt-injection/)**

The post that named the attack, by analogy with SQL injection. It is short; read all of it. It builds on Riley Goodside's translation example, where an instruction hidden in the text to translate takes over. Then read the two follow-ups linked at its top, written within a week: "I don't know how to solve prompt injection", and "You can't solve AI security problems with more AI". The second argues against demo 3's detector, four years before demo 3's numbers showed why.

**⭐ Greshake, K., Abdelnabi, S., Mishra, S., Endres, C., Holz, T. & Fritz, M. (2023). "Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection." *AISec '23*, 79–90. [arXiv:2302.12173](https://arxiv.org/abs/2302.12173)**

The paper that showed **indirect** injection: the attacker never talks to the model, but plants instructions in data it will read later, such as a web page, an email or a document. Read section 3.1 for the ways an injection gets in, then section 4.2.1, where planted text makes an assistant gather the user's data. Chris's thermostat name in demo 3 is the same attack: written once, read later, by an assistant acting for someone else. The **injection-lab** playground lets you write your own.

**⭐ Wallace, E., Xiao, K., Leike, R., Weng, L., Heidecke, J. & Beutel, A. (2024). "The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions." [arXiv:2404.13208](https://arxiv.org/abs/2404.13208)**

Why gpt-6-luna ignored the obvious injection in all 20 runs, and followed the helpful-looking one in all 20. OpenAI trains models to rank instructions by where they come from: the developer's above the user's above a tool result's. Read section 3.1: lower-priority instructions that are **aligned** with the user's goal should be followed, and **misaligned** ones ignored. The helpful-looking name was written to look aligned. That's the gap the training leaves, and it explains demo 3's second row. It also explains the injection-lab's result with gpt-4.1-mini, an older model, which followed the obvious one every time.

**Nassi, B., Cohen, S. & Yair, O. (2025). "Invitation Is All You Need! Promptware Attacks Against LLM-Powered Assistants in Production Are Practical and Dangerous." [arXiv:2508.12175](https://arxiv.org/abs/2508.12175)**

Demo 3, for real. The authors sent Google Calendar invitations whose titles contained instructions, and when the victim asked Gemini about their week, it followed them, in one scenario controlling devices in a smart home through Google Home. Read section V-D1, "Controlling Home Appliance", then section VII on mitigations, which Google deployed. The abstract covers 14 attack scenarios. Compare the invitation title with Chris's thermostat name: text from someone outside, in a field nobody thinks of as instructions.

**Willison, S. (2025). "The lethal trifecta for AI agents: private data, untrusted content, and external communication." [simonwillison.net](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/)** and **Meta AI (2025). "Agents Rule of Two: A Practical Approach to AI Agent Security." [ai.meta.com](https://ai.meta.com/blog/practical-ai-agent-security/)**

Two short pieces that turn the research into a design rule. Willison's names the three things that make an injection dangerous; Meta's says no agent should have more than two of untrusted input, access to private data, and the ability to change things or communicate outside, in one session. Read both, then run the **lethal-trifecta** playground and argue with its labels. Demo 4's confirmation is one way to remove the third leg; demo 6's staff assistant never had it.

### Defences, and how they fail: demo 3's fixes

**Hines, K., Lopez, G., Hall, M., Zarfati, F., Zunger, Y. & Kıcıman, E. (2024). "Defending Against Indirect Prompt Injection Attacks With Spotlighting." *CAMLIS 2024*, CEUR-WS 3920, 48–62. [arXiv:2403.14720](https://arxiv.org/abs/2403.14720)**

Demo 3's marking fix, from Microsoft. Read section III for three ways to mark untrusted text: **delimiting** (tags, as in demo 3), **datamarking** (a special character between every word) and **encoding** (base64). Then section V-A, where attack success on GPT-family models fell from over 50% to under 2%. In demo 3, marking stopped every attack we tried. Read the next paper before concluding it always will.

**⭐ Nasr, M., Carlini, N., Sitawarin, C., et al. (2025). "The Attacker Moves Second: Stronger Adaptive Attacks Bypass Defenses Against LLM Jailbreaks and Prompt Injections." [arXiv:2510.09023](https://arxiv.org/abs/2510.09023)**

The paper behind section 3's "why this breaks". Twelve published defences, most of which reported near-zero attack success, were bypassed by attacks written for them, most more than 90% of the time. Read the abstract, then section 5.3, where detectors are beaten, and the account of a human red-teaming competition in which more than 500 people produced 265 successful attacks on spotlighting. Demo 3's "written as a record" row is a tiny version: one rewrite, aimed at one detector. The lesson isn't that defences are useless. It's that a defence evaluated only against yesterday's attacks tells you little about tomorrow's.

**Debenedetti, E., Zhang, J., Balunović, M., Beurer-Kellner, L., Fischer, M. & Tramèr, F. (2024). "AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents." *NeurIPS 2024 Datasets and Benchmarks*, 37, 82895–82920. [arXiv:2406.13352](https://arxiv.org/abs/2406.13352)**

A benchmark of agents with realistic tools (email, banking, travel) and injection attacks against them, used to compare defences on the same footing. Read section 4.3: a simple **tool filter**, which only gave the agent the tools the user's task needed, cut attack success to 7.5%, because most attacks needed tools the task didn't. That is demo 2's and demo 4's idea measured properly: what the agent can't do, it can't be talked into.

### Guardrails and design: where demos 4 and 6 come from

**Beurer-Kellner, L., Buesser, B., Creţu, A.-M., et al. (2025). "Design Patterns for Securing LLM Agents against Prompt Injections." [arXiv:2506.08837](https://arxiv.org/abs/2506.08837)**

Six ways to build an agent that injected text can't steer, with the trade-off each makes. Read section 3.1 for the patterns (action-selector, plan-then-execute, LLM map-reduce, dual LLM, code-then-execute, context-minimisation), then section 4.3, an email and calendar assistant close to Ask Dormouse. Demo 4's tiers are the simplest version: the model chooses, a person and the code decide. Ask which pattern would have stopped demo 3's attack without asking Sam anything.

**Debenedetti, E., Shumailov, I., Fan, T., et al. (2025). "Defeating Prompt Injections by Design." *IEEE SaTML 2026*, 587–618. [arXiv:2503.18813](https://arxiv.org/abs/2503.18813)**

**CaMeL**: one model turns the user's request into a small program, and a second, quarantined model reads untrusted data but can't call tools. Every value carries where it came from, so a value from an untrusted source can't flow into a dangerous tool. Read section 5 for the design, then the headline result: 77% of AgentDojo's tasks solved with a security guarantee, against 84% with no defence. Compare with demo 3: an email address that came from a device name would be marked untrusted, and the invitation refused in code.

**⭐ UK NCSC and US CISA (2023). "Guidelines for secure AI system development." [ncsc.gov.uk](https://www.ncsc.gov.uk/collection/guidelines-secure-ai-system-development)**

Practical guidance from the UK's National Cyber Security Centre and partners, in four parts: secure design, development, deployment, and operation and maintenance. Read the secure design section with demo 4 and the checklist in the module README side by side. Much of it is ordinary security (threat modelling, least privilege, logging), which is the point of this module: an AI feature still needs all of that.

**Model Context Protocol (2026). "Authorization," specification version 2026-07-28. [modelcontextprotocol.io](https://modelcontextprotocol.io/specification/latest/basic/authorization)**

How demo 6's server would work over the network. A local server takes its credentials from the environment, as demo 6 does. A remote one uses OAuth 2.1: the user signs in, the assistant gets a token issued for that server, and the server must check the token was issued for it and never pass it on to anything else. Read the overview and the section on token audience. That rule is what stops a server being used to reach APIs the user never granted.

### Data and privacy: where demo 5 comes from

**⭐ UK Information Commissioner's Office. "Guidance on AI and data protection." [ico.org.uk](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/artificial-intelligence/guidance-on-ai-and-data-protection/)**

The UK regulator's guidance on using personal data in AI systems, last updated 15 March 2023, and marked as under review after the Data (Use and Access) Act. Read the chapter "How should we assess security and data minimisation in AI?", then check demo 5 against it: what we kept, for how long, and whether we needed it. It is the place to start before a data protection impact assessment. It is guidance, not legal advice, and neither is this course.

**OpenAI. "Data controls in the OpenAI platform." [developers.openai.com](https://developers.openai.com/api/docs/guides/your-data)**

What OpenAI keeps from each API endpoint, and for how long. Read the table, and find the Responses API's row: abuse-monitoring logs, and application state when `store` is on. Demo 5 showed both. `data/providers.json` has the same for Anthropic and Google, with links; read the one for the provider you use. These pages change, so check the date at the top of `providers.json` against the page itself.

### Where it went next

Prompt injection is not solved, and the research is moving from making models refuse to designing systems that stay safe when they don't: CaMeL and the design patterns above, sandboxes for coding agents, and permission systems that follow where data came from. At the same time, assistants are getting more tools, more autonomy and more connections to each other through protocols like MCP, which widens what an injection can reach. OWASP's separate Top 10 for Agentic Applications is one sign of where attention has gone.

---

## Books, videos and posts

- **Simon Willison's prompt injection series**, [simonwillison.net/series/prompt-injection](https://simonwillison.net/series/prompt-injection/): every post since he named the attack, with new examples as they're found.
- **Lakera, "Agent Breaker"**, [play.lakera.ai/agent-breaker](https://play.lakera.ai/agent-breaker): a game of levels to beat, including injections hidden in a web page and in an MCP server's description. It replaced Lakera's well-known Gandalf game.
- **Presidio**, [github.com/data-privacy-stack/presidio](https://github.com/data-privacy-stack/presidio): open-source detection and redaction of personal data, formerly Microsoft's. The tool to try after the **redact** playground.
- **Shostack, A. (2014). *Threat Modeling: Designing for Security*. Wiley.** Not about AI, and still the best way into thinking about what can go wrong before it does. The STRIDE chapter works for an assistant as well as for any other system.

## Extensions

These are bigger than the playground. They don't repeat its "Try this" ideas. ★ is an afternoon; ★★★ is a weekend.

1. **★ Threat-model Ask Dormouse.** Draw demo 6's system: Sam, Priya, the two assistants, the MCP server, the API, OpenAI. Mark every place text from someone else comes in, every place personal data goes out, and every action. Use STRIDE (Shostack) or the NCSC guidelines. What did this module miss?
2. **★★ An injection test suite.** Turn demo 3 into a test that runs in CI: twenty runs of each attack in `data/attacks.json`, failing if any rate goes above zero. Add attacks as you find them. Then change the model in the test and see which rates move.
3. **★★ Tickets as untrusted content.** Give Priya's assistant in demo 6 a tool that reads the full text of a ticket, then write a ticket (as Sam, or as anyone who can email support) that gets Priya's assistant to offer a replacement to the wrong customer. What stops it: the confirmation, the server, or Priya?
4. **★★ The dual LLM.** Rebuild Ask Dormouse with two models: a quarantined one that reads the home record and returns only fixed fields (device type, serial prefix), and a privileged one that never sees free text from the database. Run demo 3's attacks against it. What can it no longer do for Sam?
5. **★★ A data map and an erasure job.** List every place Ask Dormouse stores or sends personal data, including the provider. Write one script that erases a customer from all of them and reports what it removed, and a test that checks nothing of theirs is left. What can't you erase?
6. **★★★ Remote MCP with real sign-in.** Run demo 6's server over HTTP with OAuth, using a local identity provider such as Keycloak, so Sam and Priya sign in for real and the server checks the token's audience. Follow the MCP authorisation specification. Then try to make the server use Sam's token to call something Sam never granted.

Citations were checked on 21 November 2026 against arXiv, the publishers' records and the pages themselves.
