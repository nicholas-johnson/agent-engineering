export const slides = [
  {
    type: 'title',
    content: {
      title: 'Agent Engineering',
      subtitle: 'Nicholas Johnson',
      icon: 'sparkles',
    },
  },
  {
    type: 'title',
    content: {
      title: 'Module 7 — AI-Assisted Development',
      subtitle: 'One feature, from customer feedback to launch',
      icon: 'bot',
    },
  },
  {
    type: 'description',
    content: {
      title: 'The question',
      icon: 'question',
      description:
        'Dormouse customers keep asking why their heating comes on early. Product wants to let them choose how early Warm Wake starts. Every step of shipping that now has an AI tool: working out what to build, prototyping, coding, reviewing, testing, telling customers. **Which tools help, and how do you use them so the result is something you would ship?**',
    },
  },
  {
    type: 'code',
    content: {
      title: 'The data',
      code: `F01  app review    Heating comes on at 5:40 when my schedule says 7.
                   Have checked the schedule three times.
F02  support chat  My boiler fires up over an hour before the time
                   I set. Is the clock on the thermostat wrong?
F16  support chat  Where is the setting that stops the heating coming
                   on before my schedule? I looked under Schedule ...
F22  email         Can I choose how early it warms the house? 90 minutes
                   is far too long for a small flat like mine ...`,
      highlights: [
        '**30 pieces of feedback** from September and October: **14** about the heating coming on early',
        "Most customers don't know it's a feature: **Warm Wake**",
        "A small stand-in for the dashboard's code, with **16 tests**",
        'One feature, **DOR-231**, followed all the way to launch',
      ],
    },
  },

  // ---- Section 1: Just build it ----
  {
    type: 'title',
    content: {
      title: '1. Just build it',
      subtitle: 'From a sentence to something you can click',
      icon: 'zap',
    },
  },
  {
    type: 'standard',
    content: {
      title: 'App builders',
      icon: 'sparkles',
      points: [
        'Describe an app in a sentence; get a working one in minutes',
        '**Lovable**, v0, Bolt, Replit, Figma Make, Google AI Studio',
        'Good for: testing an idea with customers before anyone builds it properly',
        'Underneath: a request to a model, asking for a whole app',
      ],
    },
  },
  {
    type: 'code',
    content: {
      title: 'One request',
      code: `INSTRUCTIONS = "You build prototypes. Reply with one complete,
                self-contained HTML file and nothing else."
REQUEST = "Build the settings screen for the Dormouse thermostat app,
           where customers choose how early Warm Wake starts the heating."

with client.responses.stream(model=MODEL, instructions=INSTRUCTIONS,
                             input=REQUEST) as stream:
    for event in stream:
        if event.type == "response.output_text.delta":
            written += len(event.delta)
            print(f"Building... {written:,} characters", end="\\r")`,
      highlights: [
        "The same request in every section's demo",
        'Streamed, so a long file shows progress as it arrives',
      ],
    },
  },
  {
    type: 'title',
    content: {
      title: 'Demo — Just build it',
      subtitle: 'Switch to terminal: python demo/01_just_build_it.py',
      icon: 'rocket',
    },
  },
  {
    type: 'image',
    content: {
      title: 'What we got',
      src: '/prototype-01.png',
      alt: 'A generic Warm Wake screen with a slider, a Save button and 6:30 AM',
      credit: 'demo/output/01_prototype.html, one run: 14,237 characters in 30 seconds',
    },
  },
  {
    type: 'description',
    content: {
      title: 'Why this breaks',
      icon: 'warning',
      description:
        "Nothing on it is ours. A slider to **2 hours early**, where Warm Wake has never gone past 90 minutes. A screen of its own, *A softer start*. A **Save changes** button, where our app saves as you go. **6:30 AM**, where we use the 24-hour clock. Copy like an advert: *Wake up to a home that's already just right.* We told it none of that. And a prototype this polished gets treated as if its details were decisions.",
    },
  },

  // ---- Section 2: The company brain ----
  {
    type: 'title',
    content: {
      title: '2. The company brain',
      subtitle: 'Write down what the company knows, once',
      icon: 'brain',
    },
  },
  {
    type: 'code',
    content: {
      title: 'The company brain',
      code: `brain/
  product.md     every feature, and where each setting lives
  customers.md   who they are, and what they care about
  voice.md       how we write, and the words we don't use
  glossary.md    our terms, and what customers call them
  decisions.md   what we've decided, and why
  design.md      colours, type, how a settings screen looks

# decisions.md
## 2026-05: Settings about when the heating runs live under Schedule
## 2026-02: Give customers a choice of three, not a number
## 2025-11: Defaults should use less gas, not more`,
      highlights: [
        '**1,287 words**: short enough to read, and to keep up to date',
        'Decisions with their **reasons**, so a model can apply them to new cases',
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'Where each tool reads it',
      icon: 'layers',
      points: [
        '**AGENTS.md** in the code: Codex, Cursor, Copilot, Devin, Jules and more',
        '**CLAUDE.md** for Claude Code. Ours is one line: `@AGENTS.md`',
        'Lovable **Instructions**, Cursor **rules**, Claude and ChatGPT **Projects**',
        'Things that change every day, like tickets: connect them with **MCP** (Module 3)',
        'At scale, this is **RAG** (Module 6)',
      ],
    },
  },
  {
    type: 'code',
    content: {
      title: 'The same request, with the brain',
      code: `brain = "\\n\\n".join(path.read_text()
                     for path in sorted((DATA / "brain").glob("*.md")))

spec = ask(f"{SPEC_INSTRUCTIONS}\\n\\n{brain}\\n\\n{feedback}",
           f"The request: {REQUEST}")
html = ask(f"{PROTOTYPE_INSTRUCTIONS}\\n\\n{brain}\\n\\n{spec}",
           REQUEST)`,
      highlights: [
        "First a product manager's **spec**, from the brain and the feedback",
        'Then the **prototype**, from the brain and the spec',
      ],
    },
  },
  {
    type: 'title',
    content: {
      title: 'Demo — The company brain',
      subtitle: 'Switch to terminal: python demo/02_company_brain.py',
      icon: 'rocket',
    },
  },
  {
    type: 'image',
    content: {
      title: 'With the brain',
      src: '/prototype-02.png',
      alt: 'A Dormouse settings screen under Schedule with Up to 30, 60 or 90 minutes',
      credit: 'demo/output/02_prototype.html, one run: spec and prototype in 23 seconds',
    },
  },
  {
    type: 'comparison',
    content: {
      title: 'Results',
      left: {
        label: 'The request alone',
        items: [
          'A screen of its own, *A softer start*',
          'A slider, *At wake-up* to *2 hours early*',
          'A Save button, and *6:30 AM*',
          'Dark green',
        ],
      },
      right: {
        label: 'With the brain',
        items: [
          'Settings > Schedule',
          'Up to **30, 60 or 90** minutes, 60 chosen',
          'Saved automatically',
          'Dormouse cream, night blue and ember orange',
        ],
      },
    },
  },
  {
    type: 'description',
    content: {
      title: 'Why this breaks',
      icon: 'warning',
      description:
        "The spec quotes the feedback by id and picks three choices with 60 as the default: the answer product agreed, from the decisions alone. But the prototype is still a guess: it dropped the switch that turns Warm Wake off, which its own spec says must stay. And it isn't the product. The real settings live in **code**, with its own structure and tests. Changing that means read, decide, edit, test and fix: **many steps**.",
    },
  },

  // ---- Section 3: The coding agent ----
  {
    type: 'title',
    content: {
      title: '3. The coding agent',
      subtitle: "Day One's tool loop, pointed at code",
      icon: 'robot',
    },
  },
  {
    type: 'code',
    content: {
      title: 'Four tools and a loop',
      code: `TOOLS = [
    tool("list_files", "List every file in the project."),
    tool("read_file", "Read a file.", path=...),
    tool("write_file", "Replace a file with new content.", path=..., content=...),
    tool("run_tests", "Run the project's tests."),
]

for step in range(MAX_STEPS):
    response = client.responses.create(model=MODEL, instructions=instructions,
                                       input=conversation, tools=TOOLS)
    conversation += response.output
    calls = [item for item in response.output if item.type == "function_call"]
    if not calls:
        return response.output_text
    ...`,
      highlights: [
        '**Read**, **write**, **run the tests**: that is a coding agent',
        "Reads the project's `AGENTS.md` first, like the real tools",
        'Works on a copy of the project, so every run starts clean',
      ],
    },
  },
  {
    type: 'tool-loop',
    content: {
      title: 'The coding agent, a step at a time',
      steps: [
        {
          caption: 'One line, as a developer would type it',
          at: 'ask',
          message: {
            kind: 'you',
            text: 'Let customers choose how early Warm Wake starts the heating.',
          },
        },
        {
          caption: 'First it **reads** the code: `read_file("dormouse/settings.py")`',
          at: 'call',
        },
        {
          caption: 'Our code reads the file, and it goes back to the model',
          at: 'back',
        },
        {
          caption: 'Eight files read, six written, then it **runs the tests**',
          at: 'call',
          message: { kind: 'call', label: 'The model: please run', text: 'run_tests()' },
        },
        {
          caption: 'One of its new tests fails',
          at: 'run',
          message: {
            kind: 'result',
            label: 'Our code runs it',
            text: '→ FAILED (failures=1)',
          },
        },
        {
          caption: 'It rewrites **the test**, and runs them again',
          at: 'back',
        },
        {
          caption: '18 tool calls, 56 seconds: **done**',
          at: 'answer',
          message: {
            kind: 'answer',
            text: 'Added a Warm Wake lead-time setting ... All 19 tests pass.',
          },
        },
      ],
    },
  },
  {
    type: 'code',
    content: {
      title: 'All 18 tool calls',
      code: `list_files
read_file   dormouse/settings.py      write_file  dormouse/settings.py
read_file   dormouse/warm_wake.py     write_file  dormouse/warm_wake.py
read_file   dormouse/pages.py         write_file  dormouse/pages.py
read_file   tests/test_settings.py    write_file  tests/test_settings.py
read_file   tests/test_warm_wake.py   write_file  tests/test_warm_wake.py
read_file   tests/test_pages.py       write_file  tests/test_pages.py
read_file   README.md                 run_tests   → FAILED (failures=1)
read_file   AGENTS.md                 write_file  tests/test_pages.py
                                      run_tests   → OK`,
      highlights: [
        'Reads everything first, including `AGENTS.md`',
        'When a test fails, it changes **the test**',
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'Where the loop runs',
      icon: 'terminal',
      points: [
        '**AI editors**, next to your code: Cursor, Copilot in VS Code, Devin Desktop, Kiro, Antigravity',
        '**Terminal agents**, in your project: Claude Code, Codex, Antigravity CLI',
        '**Cloud agents**: give it a ticket, get a pull request. Copilot cloud agent, Codex, Devin, Jules',
        '**Open source**, with any model: Aider, Cline, OpenCode',
      ],
    },
  },
  {
    type: 'title',
    content: {
      title: 'Demo — The coding agent',
      subtitle: 'Switch to terminal: python demo/03_coding_agent.py',
      icon: 'rocket',
    },
  },
  {
    type: 'comparison',
    content: {
      title: 'Why this breaks',
      left: {
        label: 'What the agent decided',
        items: [
          'Six choices, **15 to 90** minutes',
          'Default: **90** minutes',
          'Under **Heating**',
          'Called *Warm Wake lead time*',
          'Shown when Warm Wake is off',
        ],
      },
      right: {
        label: "What we'd already decided",
        items: [
          'Three choices (decisions.md)',
          'Default: 60 minutes (DOR-231)',
          'Under Schedule (decisions.md)',
          'Plain words (voice.md)',
          'Hidden when Warm Wake is off (design.md)',
        ],
      },
    },
  },
  {
    type: 'description',
    content: {
      title: 'All 19 tests pass',
      icon: 'warning',
      description:
        'The agent wrote the tests to match its own decisions, so passing tests say the code does what **the agent** meant, not what **we** meant. The detail was in the ticket and the brain. It got one line, and a person who knew that little would have asked. Nothing asked it to.',
    },
  },

  // ---- Section 4: Plan, review, then implement ----
  {
    type: 'title',
    content: {
      title: '4. Plan, review, then implement',
      subtitle: 'Agree the plan before the code',
      icon: 'clipboard-list',
    },
  },
  {
    type: 'standard',
    content: {
      title: 'Plan mode',
      icon: 'map',
      points: [
        'Give it the **agreed ticket**, with acceptance criteria, not one line',
        'First a **plan**, with tools that can only look',
        'A person reads it, and pushes back: the **cheapest** moment to fix anything',
        'Then it builds exactly that',
        'Claude Code, Cursor, Codex, Copilot: **plan mode**, usually Shift+Tab',
        'Kiro, GitHub Spec Kit: **spec-driven**, requirements, then design, then tasks',
      ],
    },
  },
  {
    type: 'code',
    content: {
      title: 'Plan first, in code',
      code: `plan, _ = run_agent(f"{ticket}\\n\\n{PLAN}", instructions,
                    TOOLS[:2])   # list_files and read_file only
print(plan)

if input("Go ahead with this plan? (y/n) ").strip().lower() != "y":
    sys.exit()

summary, conversation = run_agent(
    f"{ticket}\\n\\n# Your plan\\n\\n{plan}\\n\\n{BUILD}", instructions, TOOLS)`,
      highlights: [
        "Planning **can't change anything**: it has no write tool",
        'Nothing is written until a person types **y**',
      ],
    },
  },
  {
    type: 'title',
    content: {
      title: 'Demo — Plan first',
      subtitle: 'Switch to terminal: python demo/04_plan_first.py',
      icon: 'rocket',
    },
  },
  {
    type: 'code',
    content: {
      title: 'The plan',
      code: `1. dormouse/settings.py — Add a how_early setting with a default of 60
   and allow only 30, 60 or 90.
   Tests: ... the default and allowed values, and rejection of others.

2. dormouse/warm_wake.py — Use how_early as the maximum number of minutes
   Warm Wake can start before a schedule period ...
   Tests: Update the existing 90-minute cap test ... to reflect the new
   default of 60, and add coverage for all three choices.

3. dormouse/pages.py — Move the Warm Wake row from Heating to Schedule,
   add How early there, and show How early only when Warm Wake is on.

Uncertainties: The ticket doesn't specify the exact customer-facing label ...`,
      highlights: [
        'Every file, every test it will change, and **why**',
        "And what it isn't sure about",
      ],
    },
  },
  {
    type: 'comparison',
    content: {
      title: 'Results',
      left: {
        label: 'One line',
        items: [
          '15 to 90 minutes, default 90',
          'Under Heating',
          'Shown when Warm Wake is off',
          '31 lines added, 3 removed',
          '19 tests pass, 56 seconds',
        ],
      },
      right: {
        label: 'The ticket, and a plan',
        items: [
          '**30, 60 or 90** minutes, default **60**',
          'Under **Schedule**',
          '**Hidden** when Warm Wake is off',
          '51 lines added, 10 removed',
          '21 tests pass, 53 seconds',
        ],
      },
    },
  },
  {
    type: 'code',
    content: {
      title: 'Why this breaks',
      code: `# A home's settings, saved before firmware 4.2
saved_before_4_2 = {"boost_temperature": 21.0, "warm_wake": True,
                    "week_starts_on": "Monday", "away_temperature": 16.0,
                    "geofencing": False}

heating_start(datetime(2026, 11, 20, 7, 0), 10, 21, 2, saved_before_4_2)
# KeyError: 'how_early'`,
      highlights: [
        'You approved a plan. Have you read the **61 changed lines**?',
        "Every existing customer's saved settings have no `how_early`",
        "The agent's tests only use the new defaults, so they all pass",
        "Merging code you haven't read because it passes: **vibe coding**",
      ],
    },
  },

  // ---- Section 5: Review and automate ----
  {
    type: 'title',
    content: {
      title: '5. Review and automate',
      subtitle: 'A second opinion, and the jobs you repeat',
      icon: 'check-square',
    },
  },
  {
    type: 'standard',
    content: {
      title: 'Reviewing AI-written code',
      icon: 'eye',
      points: [
        "The same job as reviewing anyone's, done more often",
        'Check it against the **ticket**, not against itself',
        'Look hard at any **test that changed**',
        "Ask what the tests **don't** cover",
        'Some of this can be automated, and the steps you repeat are worth writing down',
      ],
    },
  },
  {
    type: 'code',
    content: {
      title: 'A skill',
      code: `---
name: review
description: Review a code change against its ticket and the
  project's rules. Use when asked to review a diff or a pull request.
---

# Review a change

Check, in this order:

1. Does the change do everything the ticket's acceptance criteria ask?
2. Does it do anything the ticket didn't ask for?
3. Were any existing tests changed or deleted? ...`,
      highlights: [
        'A folder with a **SKILL.md**: a name, a description, instructions',
        'The agent loads it when the **description** matches the job',
        'Claude Code, Codex, Copilot, Cursor and others read the same format',
        'Ours: review, test plan, change summary',
      ],
    },
  },
  {
    type: 'title',
    content: {
      title: 'Demo — Skills',
      subtitle: 'Switch to terminal: python demo/05_skills.py',
      icon: 'rocket',
    },
  },
  {
    type: 'code',
    content: {
      title: 'The review',
      code: `Verdict: Request changes.

Must fix:
- dormouse/settings.py: check accepts values such as 60.0 for how_early.
- dormouse/pages.py: The new "How early" setting has no row in the page
  when Warm Wake is off. This conflicts with AGENTS.md ...

Acceptance criteria:
- Any other value for How early is rejected. — Not met (60.0 is accepted).
- A new customer, and an existing customer who has never changed it,
  gets 60 minutes. — Met (default is 60).`,
      highlights: [
        '**Caught**: `60.0` gets through',
        '**False alarm**: hiding How early is what the ticket asked for',
        '**Missed**: existing customers marked *Met*. They crash',
        "The test plan's test 3 would catch it: *an existing customer who has never changed it*",
      ],
    },
  },
  {
    type: 'description',
    content: {
      title: 'A second opinion, not a sign-off',
      icon: 'eye',
      description:
        "Three skills, 7 seconds. An AI review is quick, tireless and good at anything you can list. It shares the author's blind spots, especially when the same model wrote the code: both reasoned from the new defaults. A different model, or a reviewer told to look for one kind of problem, helps. The person who knows that saved settings exist still catches this one.",
    },
  },
  {
    type: 'code',
    content: {
      title: 'Without a person',
      code: `# From a script, or a step in the build pipeline
claude -p "Review the change in git diff against DOR-231"
codex exec "Write a test plan for DOR-231"

# On every pull request, in GitHub Actions
- uses: anthropics/claude-code-action@v1
- uses: openai/codex-action@v1`,
      highlights: [
        'Review every pull request',
        'Explain why a build failed',
        'Write test plans and plain-English change summaries',
        'Update the ticket',
      ],
    },
  },
  {
    type: 'description',
    content: {
      title: 'Why this breaks',
      icon: 'warning',
      description:
        "This is where the code is done. But a feature isn't shipped when it's merged. Customers need telling, the help centre is now wrong, support need to know what changed, and sales will be asked about it. That is a lot of writing, by people who weren't in the room.",
    },
  },

  // ---- Section 6: Out the door ----
  {
    type: 'title',
    content: {
      title: '6. Out the door',
      subtitle: 'The same brain, for marketing and sales',
      icon: 'mail',
    },
  },
  {
    type: 'standard',
    content: {
      title: 'The launch kit',
      icon: 'package',
      points: [
        'Five more skills: **release notes**, **help article**, **launch email**, **social posts**, **sales sheet**',
        'The same ticket, the same change, the same brain',
        'Then a **check** on everything that goes out, from rules in the brain',
      ],
    },
  },
  {
    type: 'code',
    content: {
      title: 'The check',
      code: `def check(text):
    """Problems a person would otherwise have to spot."""
    problems = [f'"{word}"' for word in banned_words()
                if re.search(rf"\\b{re.escape(word)}\\b", text, re.IGNORECASE)]
    problems += [f'a savings figure, "{m}"'
                 for m in re.findall(r"\\d+ ?%|\\d+ per ?cent", text)]
    return problems`,
      highlights: [
        "`banned_words()` reads the list under *Words we don't use* in voice.md",
        'Savings figures, because of the decision *No savings figures in marketing*',
      ],
    },
  },
  {
    type: 'title',
    content: {
      title: 'Demo — Out the door',
      subtitle: 'Switch to terminal: python demo/06_out_the_door.py',
      icon: 'rocket',
    },
  },
  {
    type: 'code',
    content: {
      title: 'Results',
      code: `  release-notes.md     voice check passed
  help-article.md      voice check passed
  launch-email.md      voice check passed
  social-post.md       voice check passed
  sales-sheet.md       voice check passed

Short
Warm Wake now starts the heating no more than 30, 60 or 90 minutes
before a schedule period. The default is 60 minutes. Choose how early
it starts in Settings > Schedule.`,
      highlights: [
        'All five in about **10 seconds**',
        'Email subject: *Choose how early Warm Wake starts*',
        "The sales sheet's *What not to say* comes straight from decisions.md",
      ],
    },
  },
  {
    type: 'description',
    content: {
      title: 'Where this stops',
      icon: 'warning',
      description:
        "The check only catches what somebody wrote down as a rule. The sales sheet said *shorter lead time*, the agent's jargon, and passed. On one run the social post came back twice, run together, and passed too. And it all describes the change as written, crash included. A person still reads it before it goes out, but they are **editing**, not starting from a blank page.",
    },
  },

  // ---- Wrap-up ----
  {
    type: 'title',
    content: {
      title: 'Wrap-up',
      subtitle: 'Choosing tools, and what lasts',
      icon: 'star',
    },
  },
  {
    type: 'cards',
    content: {
      title: 'Four kinds of tool',
      cards: [
        {
          heading: 'Build from a prompt',
          points: [
            'Lovable, v0, Bolt.new',
            'Replit, Figma Make, AI Studio',
            'For trying an idea',
          ],
        },
        {
          heading: 'AI editors',
          points: [
            'Cursor, Copilot in VS Code',
            'Devin Desktop, Kiro, Antigravity',
            'For developers, in their editor',
          ],
        },
        {
          heading: 'Coding agents',
          points: [
            'Claude Code, Codex, Antigravity CLI',
            'Copilot cloud agent, Devin, Jules',
            'Aider, Cline, OpenCode',
          ],
        },
        {
          heading: 'Everyone else',
          points: [
            'Claude, ChatGPT, Gemini, NotebookLM',
            'Microsoft 365 Copilot, Notion AI',
            'Glean, Granola',
          ],
        },
      ],
    },
  },
  {
    type: 'rules',
    content: {
      title: 'What they share',
      rules: [
        {
          rule: 'A brain file',
          example: '`AGENTS.md`, `CLAUDE.md`, rules, Projects',
          icon: 'brain',
        },
        {
          rule: 'Plan first',
          example: 'Plan mode in Claude Code, Cursor, Codex and Copilot',
          icon: 'map',
        },
        {
          rule: 'Skills',
          example: '`SKILL.md`, read by Claude Code, Codex, Copilot and Cursor',
          icon: 'puzzle',
        },
        {
          rule: 'No person needed',
          example: '`claude -p`, `codex exec`, GitHub Actions, cloud agents',
          icon: 'robot',
        },
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'What changed this year',
      icon: 'calendar',
      points: [
        'SpaceX bought **Cursor** (August). OpenAI said it would stop supplying it models',
        'Google replaced Gemini CLI with **Antigravity CLI** (June)',
        'Windsurf became **Devin Desktop** (June)',
        'GitHub Copilot moved to **usage-based** billing (June)',
        'Security incidents in apps built with Lovable: more in **Module 8**',
      ],
      credit: 'Checked on 20 November 2026. Sources in data/tools.json and the README',
    },
  },
  {
    type: 'standard',
    content: {
      title: 'How this course was built',
      icon: 'book',
      points: [
        "`CLAUDE.md`, 24 lines, imports `MODULE_GUIDE.md`, 185 lines: the course's **brain**",
        "Every module's outline agreed **before** anything was built: plan first",
        'A **skill** makes the promotional clips',
        'A **test** checks every module against the guide',
      ],
    },
  },
  {
    type: 'rules',
    content: {
      title: 'Summary',
      rules: [
        {
          rule: '1. Just build it',
          example: 'Polished in 30 seconds, and all invented',
          icon: 'zap',
        },
        {
          rule: '2. The company brain',
          example: 'Ours, but still a guess at a screen',
          icon: 'brain',
        },
        {
          rule: '3. The coding agent',
          example: 'Tests pass; it made the decisions itself',
          icon: 'robot',
        },
        {
          rule: '4. Plan first',
          example: 'The right feature; 61 unread lines, with a bug',
          icon: 'clipboard-list',
        },
        {
          rule: '5. Review and automate',
          example: 'Quick second opinion; it missed the bug',
          icon: 'check-square',
        },
        {
          rule: '6. Out the door',
          example: "Five pieces in 10 seconds; checks catch only what's written down",
          icon: 'mail',
        },
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'What we learned',
      icon: 'lightbulb',
      points: [
        'Asked cold, every tool writes the **most likely** answer for a company like yours',
        "A **company brain**, written once, makes every tool's output yours",
        'A coding agent is a **tool loop**: read, write, run the tests',
        'Agree a **plan** against the ticket before any code',
        "**Read** what it wrote. Passing tests aren't a review, and nor is an AI reviewer alone",
        'Turn repeated work into **skills**, and run them without a person',
        'The tools change monthly. The **context** and the **checks** are yours to keep',
      ],
    },
  },
  {
    type: 'title',
    content: {
      title: 'Final exercise: further reading',
      subtitle: 'further-reading/README.md',
      icon: 'book-open',
    },
  },
];
