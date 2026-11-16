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
      title: 'Module 3 — Tools',
      subtitle: 'Giving the agent hands and feet',
      icon: 'wrench',
    },
  },
  {
    type: 'comparison',
    content: {
      title: 'Two kinds of clever',
      right: {
        label: 'A language model',
        items: ['Unpredictable', 'Flexible', 'Inefficient', 'Understands what you mean'],
      },
      left: {
        label: 'A computer program',
        items: ['Exact, every time.', 'Idempotent.', 'Fast', 'Only does what it is told'],
      },
    },
  },

  // ---- Section 1: Maths with a language model ----
  {
    type: 'title',
    content: {
      title: '1. Maths with a language model',
      subtitle: 'Ask it for a square root',
      icon: 'calculator',
    },
  },
  {
    type: 'code',
    content: {
      title: 'A simple question',
      code: `QUESTION = "What is the square root of 7,654,321, to 10 decimal places?"

response = client.responses.create(
    model="gpt-6-luna",
    reasoning={"effort": "none"},
    input=QUESTION,
)`,
      highlights: ['2766.6443573398'],
    },
  },
  {
    type: 'title',
    content: {
      title: 'Demo — Maths with a language model',
      subtitle: 'Switch to terminal: python demo/01_maths.py',
      icon: 'rocket',
    },
  },
  {
    type: 'code',
    content: {
      title: 'Why this breaks',
      code: `Model: ... is 2,766.6443672823.
Model: ... is 2,766.6443839608.
Model: ... is 2,766.6442826149.

The right answer: 2766.6443573398`,
      highlights: [
        'Three answers, all confidently wrong',
        'It is **predicting** digits, not calculating them',
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'What about reasoning?',
      icon: 'brain',
      points: [
        'Turn reasoning effort up, and it works it through step by step',
        'But **9 to 57 seconds**, and 668 to 4,543 tokens each',
        "There's still no guarantee",
      ],
    },
  },

  // ---- Section 2: A function ----
  {
    type: 'title',
    content: {
      title: '2. A function',
      subtitle: 'Exact, instantly',
      icon: 'code',
    },
  },
  {
    type: 'code',
    content: {
      title: 'Python can do this',
      code: `def square_root(number: float) -> float:
    """Return the square root of a number, exactly, to full precision."""
    return math.sqrt(number)


print(f"square_root(7654321) = {square_root(7654321):.10f}")`,
      highlights: ['One line of real work', 'Notice the docstring'],
    },
  },
  {
    type: 'title',
    content: {
      title: 'Demo — A function',
      subtitle: 'Switch to terminal: python demo/02_function.py',
      icon: 'rocket',
    },
  },
  {
    type: 'description',
    content: {
      title: 'Why this breaks',
      icon: 'warning',
      description:
        "`square_root(7654321) = 2766.6443573398` — exact. But someone had to know to call `square_root`, with `7654321`. The function can't read a question, and the model can't run code. **Two halves that can't talk to each other.**",
    },
  },

  // ---- Section 3: A tool ----
  {
    type: 'title',
    content: {
      title: '3. A tool',
      subtitle: 'The model asks, Python answers',
      icon: 'plug',
    },
  },
  {
    type: 'standard',
    content: {
      title: 'The Model Context Protocol',
      icon: 'link',
      points: [
        'An open standard for giving tools to AI applications (Anthropic, 2024)',
        'An **MCP server** offers tools and runs them on request',
        'An **MCP client** connects to servers and uses their tools',
        'Write a server once: Claude, ChatGPT, Cursor, VS Code and our agent can all use it',
      ],
    },
  },
  {
    type: 'code',
    content: {
      title: 'A whole MCP server',
      code: `from mcp.server.mcpserver import MCPServer

server = MCPServer("maths")


@server.tool()
def square_root(number: float) -> float:
    """Return the square root of a number, exactly, to full precision."""
    return math.sqrt(number)


server.run()`,
      highlights: [
        'Name from the function, description from the docstring',
        'Arguments from the type hints',
        'The description is all the model will ever know — write it for the model',
      ],
    },
  },
  {
    type: 'comparison',
    content: {
      title: 'A subprocess, not a server',
      left: {
        label: 'What we use: stdio',
        items: [
          'The agent starts the server as a child process',
          'JSON messages over stdin and stdout',
          'Lives as long as `async with Client(...)`',
          'One agent, one machine',
        ],
      },
      right: {
        label: 'A persistent server: HTTP',
        items: [
          'Started once, and left running',
          'Agents connect to its URL',
          'Can live on another machine',
          'Many agents can share it',
        ],
      },
    },
  },
  {
    type: 'code',
    content: {
      title: 'Giving the tools to the model',
      code: `from mcp import Client
from mcp.client.stdio import StdioServerParameters

MATHS_SERVER = StdioServerParameters(
    command=sys.executable, args=["03_maths_server.py"]
)

async with Client(MATHS_SERVER) as maths:
    tools = [
        {"type": "function", "name": tool.name,
         "description": tool.description, "parameters": tool.input_schema}
        for tool in (await maths.list_tools()).tools
    ]`,
      highlights: [
        '`Client` starts the server; `maths` is our connection to it',
        'Ask the server for its tools; describe them to OpenAI',
      ],
    },
  },
  {
    type: 'code',
    content: {
      title: 'What the model sees',
      code: `tools = [
  {
    "type": "function",
    "name": "square_root",
    "description": "Return the square root of a number, exactly, to full precision.",
    "parameters": {
      "type": "object",
      "properties": {
        "number": {"title": "Number", "type": "number"}
      },
      "required": ["number"],
      "title": "square_rootArguments"
    }
  }
]`,
      highlights: [
        'The function name, its docstring, and its type hints, as JSON',
        '`parameters` is a JSON Schema: one number, and it is required',
      ],
    },
  },
  {
    type: 'code',
    content: {
      title: 'Passing the tools to the model',
      code: `conversation = [{"role": "user", "content": QUESTION}]

response = openai.responses.create(
    model="gpt-6-luna",
    reasoning={"effort": "none"},
    instructions=INSTRUCTIONS,
    input=conversation,
    tools=tools,
)`,
      highlights: [
        'The same call as Module 2, plus `tools=tools`',
        'The model can now answer, **or** ask us to run one of these tools',
      ],
    },
  },
  {
    type: 'tool-loop',
    content: {
      title: 'The tool loop',
      steps: [
        {
          caption: 'The question goes to the model, with the tools',
          at: 'ask',
          message: {
            kind: 'you',
            text: 'What is the square root of 7,654,321, to 10 decimal places?',
          },
        },
        {
          caption: "The model doesn't answer: it **asks for a tool**",
          at: 'call',
          message: {
            kind: 'call',
            label: 'The model: please run',
            text: 'square_root({"number":7654321})',
          },
        },
        {
          caption: 'Our code runs it on the MCP server',
          at: 'run',
          message: {
            kind: 'result',
            label: 'Our code runs it',
            text: '→ 2766.644357339772',
          },
        },
        {
          caption: 'The result joins the conversation, and goes back to the model',
          at: 'back',
        },
        {
          caption: 'No tool call this time: **that is the answer**',
          at: 'answer',
          message: {
            kind: 'answer',
            text: 'The square root of 7,654,321 to 10 decimal places is 2766.6443573398.',
          },
        },
      ],
    },
  },
  {
    type: 'code',
    content: {
      title: 'The tool loop in code',
      code: `while True:
    response = openai.responses.create(..., input=conversation, tools=tools)
    conversation += response.output

    calls = [item for item in response.output if item.type == "function_call"]
    if not calls:
        break

    for call in calls:
        result = await maths.call_tool(call.name, json.loads(call.arguments))
        conversation.append({"type": "function_call_output",
                             "call_id": call.call_id,
                             "output": result.content[0].text})`,
      highlights: [
        "Module 2's conversation memory, with two new kinds of message",
        "No function calls in the response? Then it's the answer",
      ],
    },
  },
  {
    type: 'title',
    content: {
      title: 'Demo — A tool',
      subtitle: 'Switch to terminal: python demo/03_agent.py',
      icon: 'rocket',
    },
  },
  {
    type: 'code',
    content: {
      title: 'Right first time',
      code: `You: What is the square root of 7,654,321, to 10 decimal places?
  [tool] square_root({"number":7654321}) -> 2766.644357339772
Agent: The square root of 7,654,321 to 10 decimal places is 2766.6443573398.`,
      highlights: [
        'Every time',
        'See the whole conversation in `demo/output/03_agent.json`',
      ],
    },
  },
  {
    type: 'comparison',
    content: {
      title: 'Both worlds',
      left: {
        label: 'The model',
        items: [
          'Understood the question',
          'Decided it needed a square root',
          'Pulled 7654321 out of "7,654,321"',
          'Rounded and explained the answer',
        ],
      },
      right: {
        label: 'Python',
        items: ['Did the exact calculation', '...and nothing else'],
      },
    },
  },

  // ---- Section 4: The wider world ----
  {
    type: 'title',
    content: {
      title: '4. The wider world',
      subtitle: 'A tool that calls an API',
      icon: 'globe',
    },
  },
  {
    type: 'code',
    content: {
      title: 'A server that reaches the internet',
      code: `@server.tool()
def search_cards(query: str) -> str:
    """Search Magic: The Gathering cards using Scryfall search syntax, for example
    'name:rabbit t:creature' or 'o:"draw a card" c:blue'. Returns up to 10 card names
    with their current US dollar prices, most expensive first."""
    found = scryfall("cards/search", q=query, order="usd", dir="desc")
    ...


@server.tool()
def find_card(name: str) -> str:
    """Look up one Magic: The Gathering card by name..."""`,
      highlights: [
        "Scryfall: a free API for every *Magic* card, with today's prices",
        'Scryfall asks programs to name themselves, and send at most two requests a second',
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'Two servers, one loop',
      icon: 'layers',
      points: [
        'Connect to the maths server **and** the cards server',
        'Collect every tool from both',
        'Remember which server owns which tool',
        "The tool loop doesn't change at all",
      ],
    },
  },
  {
    type: 'title',
    content: {
      title: 'Demo — The wider world',
      subtitle: 'Switch to terminal: python demo/04_agent.py',
      icon: 'rocket',
    },
  },
  {
    type: 'code',
    content: {
      title: 'Three tools, two servers',
      code: `You: Which Magic: The Gathering rabbit creature is worth the most right now,
     what does it do, and what is the square root of its price?
  [tool] search_cards({"query":"t:creature t:rabbit"})
         -> [{"name": "Preston, the Vanisher", "usd": "62.89"}, ...
  [tool] find_card({"name":"Preston, the Vanisher"})
         -> {"name": "Preston, the Vanisher", "mana_cost": "{3}{W}", ...
  [tool] square_root({"number":62.89}) -> 7.930321557162736
Agent: Preston, the Vanisher is the most valuable rabbit creature
       I found, at $62.89 USD. ...
       The square root of $62.89 is approximately 7.93.`,
      highlights: ['Live data no model could know from its training'],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'It planned the steps',
      icon: 'route',
      points: [
        "Wrote its own search, in Scryfall's language: `t:rabbit`, the creature **type**",
        'Took the top result and looked it up',
        'Passed the price to a tool on a **different server**',
        'Wrote the answer from all three',
        'Nobody told it the steps',
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'Watch out for',
      icon: 'warning',
      points: [
        '**Services fail**: down, slow, rate-limited',
        '**Results can be wrong**, and the agent trusts them',
        "**Text from outside isn't instructions** — but the model may obey it: prompt injection",
        '**Tools act**: sending, paying, deleting needs much more care',
      ],
    },
  },

  // ---- Wrap-up ----
  {
    type: 'title',
    content: {
      title: 'Wrap-up',
      subtitle: 'A model that can act',
      icon: 'check',
    },
  },
  {
    type: 'standard',
    content: {
      title: 'What we built',
      icon: 'blocks',
      points: [
        '**Maths with a model** — confident, and wrong',
        "**A function** — exact, but it can't read",
        '**A tool** — an MCP server and a tool loop',
        '**The wider world** — a second server, calling a live API',
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'What we learned',
      icon: 'award',
      points: [
        'Models predict; programs calculate. **Tools join them**',
        'A tool is a function, a name and a description',
        'MCP: write a tool once, use it from any MCP application',
        'The **tool loop**: ask, run, add the result, repeat',
        'An **agent** decides which actions to take, until the job is done',
      ],
    },
  },
  {
    type: 'standard',
    content: {
      title: 'Final exercise: further reading',
      icon: 'book',
      points: [
        '**Schick et al. (2023)** — a model that taught itself to use tools',
        '**Yao et al. (2023)** — ReAct: reason, act, look, repeat',
        "**Greshake et al. (2023)** — when a tool's result attacks the agent",
        'Pick a paper, connect it to a demo, then start an extension',
        'Everything is in `further-reading/`',
      ],
    },
  },
];
