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
      subtitle: 'The tools teams build software with, one at a time',
      icon: 'bot',
    },
  },
  {
    type: 'description',
    content: {
      title: 'The question',
      icon: 'question',
      description:
        'There is a new AI tool for building software every week, and the ones you know change every month. **What is each of the main ones good at, how do you use it, and what should you watch out for?**',
    },
  },
  {
    type: 'code',
    content: {
      title: 'The data',
      code: `project/                   the Dormouse web dashboard
  dormouse/settings.py     every setting, and what it allows
  dormouse/warm_wake.py    when Warm Wake switches the heating on
  dormouse/pages.py        the settings page
  homes/flat-3b.json       a saved home: python -m dormouse
  tests/                   16 tests
  AGENTS.md  CLAUDE.md     how agents should work here

tickets/  DOR-231  choose how early Warm Wake starts
          DOR-232  let the week start on Saturday
          DOR-233  choose how long Boost lasts
          DOR-234  bug: 90 minutes early in small homes`,
      highlights: [
        'A small stand-in for real code, with **real tests**',
        'Four tickets, a stand-in for **Jira**',
        'One **real bug** the tests miss',
      ],
    },
  },

  // ---- Section 1: Just build it ----
  {
    type: 'title',
    content: {
      title: '1. Just build it',
      subtitle: 'A prompt, a few lines of Python, a page',
      icon: 'zap',
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
        'Underneath every app builder: **a request** for a whole app',
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
    type: 'comparison',
    content: {
      title: 'A prompt in Python',
      left: {
        label: 'Known for',
        items: [
          'A clickable page in **30 seconds**',
          'Cheap, and entirely yours: any model, a few lines',
        ],
      },
      right: {
        label: 'Watch out for',
        items: [
          'One page: no database, no sign-in, no hosting',
          'Everything on it **invented**: a slider to 2 hours, *6:30 AM*',
          'Polished guesses get treated as decisions',
        ],
      },
    },
  },

  // ---- Section 2: Lovable ----
  {
    type: 'title',
    content: {
      title: '2. Lovable',
      subtitle: 'From a paragraph to a hosted app',
      icon: 'sparkles',
    },
  },
  {
    type: 'standard',
    content: {
      title: 'App builders',
      icon: 'blocks',
      points: [
        'Describe an app in a chat; it **writes, runs and hosts** it',
        'A live preview next to the chat',
        '**Lovable**, v0, Bolt.new, Replit Agent, Figma Make, Google AI Studio',
        'For people who want something clickable, not code',
      ],
    },
  },
  {
    type: 'rules',
    content: {
      title: 'Three modes',
      rules: [
        {
          rule: 'Plan',
          example: 'Asks questions, writes a plan you edit and approve',
          icon: 'map',
        },
        {
          rule: 'Build',
          example: 'The default: builds, fixes, reads the logs',
          icon: 'wrench',
        },
        {
          rule: 'Chat',
          example: 'Answers questions; never changes the code',
          icon: 'message-square',
        },
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'Around the chat',
      icon: 'layers',
      points: [
        '**Built-in backend**: database, sign-in, storage, on by default',
        '**Instructions**: what it reads before every message',
        '**Preview toolbar**: point at an element, edit text in place',
        '**Security scan**: quick on every publish, deep when asked',
        '**Publish** to a URL; **GitHub sync** both ways',
      ],
      credit: 'Free: 5 credits a day. Pro: from $25 a month. Checked 23 November 2026',
    },
  },
  {
    type: 'title',
    content: {
      title: 'Demo — Lovable',
      subtitle: 'Switch to Lovable: demo/02_lovable.md',
      icon: 'rocket',
    },
  },
  {
    type: 'comparison',
    content: {
      title: 'Lovable',
      left: {
        label: 'Known for',
        items: [
          'A hosted app with a **database and sign-in**, from a paragraph',
          'Plan first, then build, without writing code',
          'A real React app you can take to GitHub',
        ],
      },
      right: {
        label: 'Watch out for',
        items: [
          "Lovable's stack, not your product's code",
          'Credits run out on a big build',
          'Publishing is one click, **safe or not**: Module 8',
        ],
      },
    },
  },

  // ---- Section 3: Claude Code ----
  {
    type: 'title',
    content: {
      title: '3. Claude Code',
      subtitle: 'A coding agent in your terminal',
      icon: 'terminal',
    },
  },
  {
    type: 'code',
    content: {
      title: 'The tool loop, again',
      code: `TOOLS = [read_file, edit_file, search, run_command]

while True:
    response = model(instructions, conversation, tools=TOOLS)
    calls = [item for item in response.output
             if item.type == "function_call"]
    if not calls:
        break                            # the job is done
    for call in calls:
        conversation.append(run(call))   # read, edit, test...`,
      highlights: [
        "Module 3's loop, with tools for **code**",
        'Reads `CLAUDE.md` first. Ours imports `AGENTS.md`',
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'Using it',
      icon: 'terminal',
      points: [
        '`claude` in a project folder, then say what you want',
        '**Shift+Tab**: manual, accept edits, **plan**, auto',
        '`/` for commands: `/clear`, `/mcp`, `/permissions`, skills',
        '`claude -p "..."`: the same agent with **no person**',
        'Also in VS Code, JetBrains, the Claude app, and the cloud',
      ],
    },
  },
  {
    type: 'code',
    content: {
      title: 'An agent file',
      code: `---
name: ticket-checker
description: Checks a change against its ticket's acceptance
  criteria, one by one. Use after a change is made, before
  it is committed.
tools: Read, Grep, Glob, Bash
model: sonnet
---

You check a change against the ticket it is for.
1. Read the change: run git diff and git status...
2. Go through the acceptance criteria one at a time...`,
      highlights: [
        'In `.claude/agents/`: the team shares it',
        'A **subagent** gets its own context, and reports back a summary',
        'Several run **at once**, in the background',
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'Skills and connectors',
      icon: 'puzzle',
      points: [
        '**Skill**: a folder with a `SKILL.md`, in `.claude/skills/`',
        'Used when the description matches the job, or as `/release-notes`',
        'An open format: Cursor, Codex and Copilot read it too',
        '**Connector**: an MCP server (Module 3) for another service',
        'GitHub, Linear, Google Drive... listed in `/mcp`',
      ],
      credit:
        'Claude Pro and above: from $17 a month, billed annually. Checked 23 November 2026',
    },
  },
  {
    type: 'title',
    content: {
      title: 'Demo — Claude Code',
      subtitle: 'Switch to terminal: demo/03_claude_code.md',
      icon: 'rocket',
    },
  },
  {
    type: 'comparison',
    content: {
      title: 'Claude Code',
      left: {
        label: 'Known for',
        items: [
          'A strong agent anywhere a terminal runs',
          'The most ways to shape it: **agent files**, skills, hooks, connectors',
          '`claude -p` for scripts and CI',
        ],
      },
      right: {
        label: 'Watch out for',
        items: [
          'It acts on **real files** and runs real commands',
          'No editor: read its changes with `git diff`',
          'Long sessions use a lot of your allowance',
        ],
      },
    },
  },

  // ---- Section 4: Cursor ----
  {
    type: 'title',
    content: {
      title: '4. Cursor',
      subtitle: 'An editor with a mode for each job',
      icon: 'code',
    },
  },
  {
    type: 'rules',
    content: {
      title: 'Four modes',
      rules: [
        {
          rule: 'Ask',
          example: 'How does this work? Reads, never edits',
          icon: 'question',
        },
        {
          rule: 'Agent',
          example: 'The default: build, fix, refactor',
          icon: 'robot',
        },
        {
          rule: 'Plan',
          example: 'Questions, an editable plan, then build',
          icon: 'map',
        },
        {
          rule: 'Debug',
          example: 'Hypotheses and logs, then a small fix',
          icon: 'search',
        },
      ],
    },
  },
  {
    type: 'code',
    content: {
      title: 'A real bug: DOR-234',
      code: `$ python -m dormouse homes/flat-3b.json
Flat 3B: the room is at 18 degrees. The next period starts
at 07:00, at 20 degrees.
Warm Wake switches the heating on at 05:30, 90 minutes early.

def learned_rate(heat_ups):
    """How fast the home warms, in degrees an hour..."""
    ...
    return degrees / minutes`,
      highlights: [
        'Flat 3B needs **24 minutes**: it should be 06:36',
        'Degrees a **minute**, 60 times too small',
        'All **16 tests pass**: none check it',
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'Debug mode',
      icon: 'search',
      points: [
        'Lists a few **hypotheses** for the cause',
        'Adds **logging** to the code',
        'Asks you to **reproduce** the bug',
        'Reads what the logs caught, then makes a **small fix**',
        'You check it; it takes the logging out again',
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'Several at once',
      icon: 'layers',
      points: [
        '`/multitask`: two tickets, **two agents**, in parallel',
        '**Build in Parallel**: a plan’s independent steps at once',
        'Reads `AGENTS.md`, its own **rules** in `.cursor/rules/`, and skills',
        'MCP servers in `.cursor/mcp.json`',
      ],
      credit: 'Free: limited. Plus $8, Premium $30 a month. Checked 23 November 2026',
    },
  },
  {
    type: 'title',
    content: {
      title: 'Demo — Cursor',
      subtitle: 'Switch to Cursor: demo/04_cursor.md',
      icon: 'rocket',
    },
  },
  {
    type: 'comparison',
    content: {
      title: 'Cursor',
      left: {
        label: 'Known for',
        items: [
          'An agent **next to the code** you are reading',
          'A mode for each job: Ask, Agent, Plan, **Debug**',
          '`/multitask` for parallel work',
        ],
      },
      right: {
        label: 'Watch out for',
        items: [
          'Changes arrive fast: **read them** before you keep them',
          'Parallel agents can change the same files',
          'Owner, prices and model supply all changed this year',
        ],
      },
    },
  },

  // ---- Section 5: Cloud agents ----
  {
    type: 'title',
    content: {
      title: '5. Cloud agents',
      subtitle: 'Hand over a ticket, get back a pull request',
      icon: 'globe',
    },
  },
  {
    type: 'standard',
    content: {
      title: 'A cloud agent',
      icon: 'server',
      points: [
        'The same loop, on **someone else’s computer**',
        'A fresh copy of your repository: it needs **GitHub** (or similar)',
        'Close the tab; come back to a **pull request**',
        'Reads the same files: `AGENTS.md`, `CLAUDE.md`',
      ],
    },
  },
  {
    type: 'cards',
    content: {
      title: 'Four of them',
      cards: [
        {
          heading: 'Claude Code on the web',
          points: [
            'claude.ai/code, `claude --cloud`',
            'A branch, then a pull request',
            'Claude Pro and above',
          ],
        },
        {
          heading: 'Copilot in the cloud',
          points: [
            'Assign an issue to Copilot',
            'One pull request per task',
            'Paid Copilot plans, from $10',
          ],
        },
        {
          heading: 'Codex cloud',
          points: [
            'The Codex app: Work in → Cloud',
            'A diff, to open as a pull request',
            'ChatGPT Plus and above',
          ],
        },
        {
          heading: 'Cursor Cloud Agents',
          points: [
            'cursor.com/agents, `@cursor`',
            'A pull request, with screenshots',
            'Cursor Premium and above',
          ],
        },
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'A review nobody has to start',
      icon: 'git-branch',
      points: [
        '`/install-github-app` in Claude Code adds a **GitHub Action**',
        'Comment `@claude` on any pull request',
        'One agent wrote it, another reviews it',
        'A person still decides whether to **merge**',
      ],
      credit:
        'Also Devin. Google is closing Jules on 31 December 2026. Checked 23 November 2026',
    },
  },
  {
    type: 'title',
    content: {
      title: 'Demo — Cloud agents',
      subtitle: 'Switch to GitHub: demo/05_cloud_agents.md',
      icon: 'rocket',
    },
  },
  {
    type: 'comparison',
    content: {
      title: 'Cloud agents',
      left: {
        label: 'Known for',
        items: [
          'Work that happens **while you do something else**',
          'Several tasks at once',
          'Results arrive where you **already review** code',
        ],
      },
      right: {
        label: 'Watch out for',
        items: [
          'Nobody is watching: the pull request is the only check',
          '**Review** becomes the bottleneck',
          'What the cloud machine can reach: secrets, internet (Module 8)',
        ],
      },
    },
  },

  // ---- Section 6: The company brain ----
  {
    type: 'title',
    content: {
      title: '6. The company brain',
      subtitle: 'One MCP server, every tool',
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
## 2026-02: Give customers a choice of three, not a number`,
      highlights: [
        'What the company knows, **written down once**',
        'Asked cold, every tool writes the most likely answer for **a company like yours**',
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'Five tools, five copies',
      icon: 'refresh-cw',
      points: [
        'Lovable **Instructions**',
        '`CLAUDE.md`, `AGENTS.md`, Cursor **rules**',
        'Claude and ChatGPT **Projects**',
        'Each pasted in by someone, once: they **drift apart**',
        "Tickets and feedback change daily: they don't belong in a file",
      ],
    },
  },
  {
    type: 'code',
    content: {
      title: 'The brain as an MCP server',
      code: `server = MCPServer("dormouse-brain")

@server.tool()
def read_brain(topic: str) -> str:
    """Read one part of Dormouse's company brain. ...
    Read decisions before making any product decision,
    and voice before writing anything a customer will read."""

@server.tool()
def get_ticket(ticket_id: str) -> str: ...

@server.tool()
def search_feedback(words: str) -> str: ...`,
      highlights: [
        'Three tools, under **50 lines**',
        'The docstring says **when** to use it',
      ],
    },
  },
  {
    type: 'code',
    content: {
      title: 'Attach it',
      code: `# Claude Code
claude mcp add --transport stdio dormouse-brain -- \\
  uv run --directory <module> python demo/06_brain_server.py

# Cursor: .cursor/mcp.json
{ "mcpServers": { "dormouse-brain": {
    "type": "stdio", "command": "uv",
    "args": ["run", "--directory", "<module>",
             "python", "demo/06_brain_server.py"] } } }

# The Claude app: the same entry in claude_desktop_config.json`,
      highlights: [
        'Each tool **starts** the server itself',
        'The same brain for developers, support and marketing',
      ],
    },
  },
  {
    type: 'title',
    content: {
      title: 'Demo — The company brain',
      subtitle: 'Switch to terminal: demo/06_company_brain.md',
      icon: 'rocket',
    },
  },
  {
    type: 'comparison',
    content: {
      title: 'The company brain',
      left: {
        label: 'Known for',
        items: [
          '**One source of truth** that every tool reads',
          'Kept up to date in one place',
          'For people who never open a code editor, too',
        ],
      },
      right: {
        label: 'Watch out for',
        items: [
          'Local only: Lovable and cloud agents need it **deployed** (Module 8)',
          'Tool descriptions need writing as carefully as the brain',
          'A mistake in it spreads to **every tool** at once',
        ],
      },
    },
  },

  // ---- Wrap-up ----
  {
    type: 'title',
    content: {
      title: 'Wrap-up',
      subtitle: 'Choosing tools',
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
            'Copilot in the cloud, Devin',
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
          rule: 'Instruction files',
          example: '`AGENTS.md`, `CLAUDE.md`, rules',
          icon: 'file-text',
        },
        {
          rule: 'Plan first',
          example: 'Plan mode in Claude Code, Cursor, Codex, Copilot and Lovable',
          icon: 'map',
        },
        {
          rule: 'Skills and MCP',
          example: 'The same `SKILL.md` and the same server, in every tool',
          icon: 'puzzle',
        },
        {
          rule: 'No person needed',
          example: '`claude -p`, `codex exec`, cloud agents, GitHub Actions',
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
        'Google replaced Gemini CLI with **Antigravity CLI**, and is closing **Jules**',
        'Windsurf became **Devin Desktop** (June)',
        'Copilot moved to **usage-based** billing; its cloud agent became **Copilot in the cloud**',
        'Security incidents in apps built with Lovable: more in **Module 8**',
      ],
      credit: 'Checked on 23 November 2026. Sources in data/tools.json and the README',
    },
  },
  {
    type: 'standard',
    content: {
      title: 'How this course was built',
      icon: 'book',
      points: [
        "`CLAUDE.md` imports `MODULE_GUIDE.md`: the course's **brain**",
        "Every module's outline agreed **before** anything was built: plan first",
        'A **skill** makes the promotional clips',
        'A **test** checks every module against the guide',
        'Agents working in their own **git worktrees**, side by side',
      ],
    },
  },
  {
    type: 'rules',
    content: {
      title: 'Summary',
      rules: [
        {
          rule: '1. A prompt in Python',
          example: 'A page in 30 seconds; everything on it invented',
          icon: 'zap',
        },
        {
          rule: '2. Lovable',
          example: 'A hosted app from a paragraph; its stack, not your code',
          icon: 'sparkles',
        },
        {
          rule: '3. Claude Code',
          example: 'A terminal agent you can shape; it acts on real files',
          icon: 'terminal',
        },
        {
          rule: '4. Cursor',
          example: 'A mode for each job; changes need reading',
          icon: 'code',
        },
        {
          rule: '5. Cloud agents',
          example: 'Done while you are away; review is the bottleneck',
          icon: 'globe',
        },
        {
          rule: '6. The company brain',
          example: 'One source of truth; local until deployed',
          icon: 'brain',
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
        'Every coding tool here is the **tool loop**, run in a different place',
        'App builders get you a **hosted app**; coding agents work in **your code**',
        'Agent files, skills and hooks **shape** an agent; plan mode checks it first',
        'Cloud agents hand back **pull requests**: reviewing them is the job',
        'A **company brain** behind MCP gives every tool the same context',
        'The tools change monthly. **Recheck** before you rely on any of it',
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
