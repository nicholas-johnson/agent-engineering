# Clip 1 — The square root

> A promise to explain MCP in ninety seconds. Then an AI gives three different, confident, wrong answers to the same maths question, a tool call fixes it, and four extra lines turn that tool into an MCP server. We look at what the wrapper gives us and at the JSON the AI actually sees, then at Google's real servers for Gmail and Calendar. Then a sign-off.

- **Length:** about 230 spoken words to explain MCP and show the real servers, then about 25 for the sign-off. The check estimates about 92 seconds before the sign-off, against a hook that promises ninety, so time your first take: see the notes if it runs over.
- **Ending:** the sign-off, full-face: "Follow if you'd like to know more." Cut straight after it.
- **Recording:** [`index.html`](index.html) in this folder. It puts you, the animation and the captions on one stage. Run `pnpm social`, open <http://127.0.0.1:8765/01-square-root/> in Chrome and press R. Each press of space brings up the next caption: say it, then press again.

## The script

### 1. Hook

To camera, full-screen for the first two lines:

> "I'm going to explain MCP to you in ninety seconds."

The promise is the hook. It tells people what they get for staying, and the clip has to keep it.

> "I asked an AI the same maths question three times. I got three different answers. All completely confident. All wrong."

Pause. Let the screen do the work.

**Screen:** the three answers stacked, with the right one underneath:

```text
2,766.6443672823
2,766.6443839608
2,766.6442826149
2,766.6443573398   ← the right answer
```

### 2. The odd bit

> "They all start off right, then drift away. It isn't calculating. It's guessing what a square root *looks like*."

**Screen:** highlight the digits where each answer leaves the right one.

### 3. The fix

> "Python gets it right in one line."

**Screen:**

```python
def square_root(number: float) -> float:
    """Return the square root of a number, exactly, to full precision."""
    return math.sqrt(number)
```

> "But Python can't read a question. So we give this function to the AI as a tool. Now when I ask, it doesn't guess. It asks *me* to run `square_root` on 7,654,321. And this is a *tool call*. My code runs it and hands back the answer."

Put some warmth into "it asks *me*". The AI asking for help is the charming part. Then say "and this is a tool call" plainly, as the name for what just happened. The heading on screen changes from "It asks for help" to "A tool call" as you say it.

**Screen:** the transcript, with the `[tool]` line highlighted:

```text
You: What is the square root of 7,654,321, to 10 decimal places?
  [tool] square_root({"number":7654321}) -> 2766.644357339772
Agent: The square root of 7,654,321 to 10 decimal places is 2766.6443573398.
```

> "Right first time. Every time."

### 4. The reveal

> "And that tool? It's the same function… plus four lines."

**Screen:** the same function, with the four new lines (marked `+`) appearing around it in a highlight colour:

```python
from mcp.server.mcpserver import MCPServer    # +

server = MCPServer("maths")                   # +

@server.tool()                                # +
def square_root(number: float) -> float:
    """Return the square root of a number, exactly, to full precision."""
    return math.sqrt(number)

server.run()                                  # +
```

> "That's an MCP server."

Then say what the wrapper gives us:

> "So what does the wrapper give us? It's discoverable: any app can ask what tools it has. Each tool describes itself: its name, arguments and purpose. It's a standard, so there's no custom glue for each app. And it's separate: the AI never sees your code."

**Screen:** "What the wrapper gives us", with four cards, one per line: Discoverable, Described, Standard, Separate.

Then show what the AI is actually given:

> "And here is what the AI actually sees. Not your code. Just a name, a description and the arguments."

**Screen:** the tool as the model receives it:

```json
{
  "type": "function",
  "name": "square_root",
  "description": "Return the square root of
    a number, exactly, to full precision.",
  "parameters": {
    "type": "object",
    "properties": {
      "number": {"type": "number"}
    },
    "required": ["number"]
  }
}
```

> "Write it once, and Claude, Cursor and VS Code can all use it."

That last line keeps the promise: it says what MCP is for. Then make it real:

> "Google has one for Gmail: your AI can search your inbox and draft replies. And one for Calendar: it can find a free slot and book the meeting. And now there's yours."

**Screen:** three cards, one per line: Gmail, Calendar, and your `maths` server.

### 5. Sign-off

Full-face again:

> "I'm Nicholas Johnson. I'm a principal dev working with AI. I'm doing a series on AI fundamentals. Follow if you'd like to know more."

Cut. End the clip right there.

## Captions and presses

The captions are the `<p class="cue">` lines in `index.html`. They are your autocue and the viewer's subtitles, so if you change the words, change them there too. Words in italics show in yellow.

| Press | Caption: what you say | What else happens |
|-------|-----------------------|-------------------|
| — | I'm going to explain *MCP* to you in ninety seconds. | You, full-screen |
| 1 | I asked an AI the same maths question three times. | — |
| 2 | I got three different answers. | You shrink into the box at the bottom, the question appears, and three answers type themselves out |
| 3 | All completely confident. | — |
| 4 | All wrong. | The right answer, in green |
| 5 | They all start off right, then drift away. | The wrong digits turn red, and the heading becomes "Right at first. Then guessing." |
| 6 | It isn't calculating. | — |
| 7 | It's guessing what a square root *looks like*. | — |
| 8 | Python gets it right in one line. | The function, then its output types out |
| 9 | But Python can't read a question. | The AI and Python side by side |
| 10 | So we give this function to the AI as a *tool*. | "So we give the function to the AI as a **tool**." |
| 11 | Now when I ask, it doesn't guess. | The question again |
| 12 | It asks *me* to run square_root on 7,654,321. | The AI's request types out |
| 13 | And this is a *tool call*. | The heading becomes "A tool call" |
| 14 | My code runs it… | The result types out |
| 15 | …and hands back the answer. | The AI's reply streams in, word by word |
| 16 | Right first time. Every time. | — |
| 17 | And that tool? It's the same function… | The function on its own |
| 18 | …plus four lines. | The four lines open up around the function, and the heading becomes "An MCP server." |
| 19 | That's an *MCP server*. | — |
| 20 | So what does the wrapper give us? | "What the wrapper gives us" |
| 21 | It's *discoverable*: any app can ask what tools it has. | The Discoverable card |
| 22 | Each tool *describes itself*: its name, arguments and purpose. | The Described card |
| 23 | It's a *standard*, so there's no custom glue for each app. | The Standard card |
| 24 | And it's *separate*: the AI never sees your code. | The Separate card |
| 25 | And here is what the AI *actually* sees. | "What the AI sees", with the tool's JSON |
| 26 | Not your code. Just a name, a description and the arguments. | — |
| 27 | Write it once, and Claude, Cursor and VS Code can all use it. | — |
| 28 | Google has one for Gmail: your AI can search your inbox and draft replies. | "Real MCP servers", with a Gmail card |
| 29 | And one for Calendar: it can find a free slot and book the meeting. | A Calendar card |
| 30 | And now there's yours. | Your `maths` server joins them |
| 31 | I'm Nicholas Johnson. I'm a principal dev working with AI. | You, full-screen again |
| 32 | I'm doing a series on *AI fundamentals*. | — |
| 33 | Follow if you'd like to know more. | — |

Then press R to stop.

## Post text

For the description under the video, not on it.

Repeat the promise, then the course plug:

> MCP in ninety seconds: a Python function, four more lines, and Claude, Cursor and VS Code can all use it.

## Notes

- **The code on screen is squeezed to fit a phone.** The docstring is wrapped onto two lines, there is one blank line where the real files have two, and `import math` is left off. Otherwise it is the real code.
- **Expect the comment "just use a reasoning model".** That's the follow-up clip. Module 4 found that with reasoning turned on, the model does get the right answer, but each answer took 9 to 57 seconds of thinking you pay for, against about a second for the tool. And nothing guarantees the reasoning model gets it right; the tool is right because it's arithmetic.
- **The JSON on screen is the real tool, trimmed to fit.** It comes from the same code `demo/03_agent.py` uses to build its `tools` list, run against `demo/03_maths_server.py`. The description string is broken onto two lines to fit the stage (the real one is a single line). Two `"title"` fields are left out: `"title": "Number"` inside `number`, and `"title": "square_rootArguments"` at the end of `parameters`. Everything else is as sent to the model.
- **The four cards on "What the wrapper gives us" only claim what the demos show:** the client asks the server for its tools (`list_tools`), each tool's name, description and arguments are read from the function, the same server works with any MCP client, and the server runs as its own program. Don't add claims about security, validation or sign-in without checking the `mcp` package first.
- **If the explanation runs over ninety seconds** (everything before the sign-off), drop "All completely confident." and "It isn't calculating." here and in `index.html`. If it's still over, drop the "Standard" card and its caption, then the Calendar line, keeping Gmail. Don't split it into two parts: the hook promises the whole thing in one.

## Where the material comes from

From Module 4, `day-one/module-04-tools/`, except the two real servers:

| On screen | Source |
|-----------|--------|
| The three wrong answers and the right one | README, section 1 (`demo/01_maths.py`) |
| The function | `demo/02_function.py` |
| The transcript with the tool call | README, section 3 (`demo/03_agent.py`) |
| The MCP server | `demo/03_maths_server.py` |
| The four things the wrapper gives us | README, section 3: the server lists its tools, the name, description and arguments come from the function, any MCP client can use it, and the agent starts it as a separate program (`demo/03_agent.py`) |
| The JSON the AI sees | The `tools` list built in `demo/03_agent.py` from the server's `list_tools()`, printed from a real run on 15 November 2026. Trimmed as described in the notes |
| Reasoning taking 9 to 57 seconds | README, section 1, "What about reasoning?" |
| Google's Gmail and Calendar MCP servers | Google's [Workspace MCP server announcement](https://workspaceupdates.googleblog.com/2026/05/agent-tools-and-security-updates-for-workspace-developers.html), May 2026: Gmail can search and draft, Calendar can find free times and manage events. Public developer preview. Checked 13 November 2026 |

The model's answers are random, so rerunning `demo/01_maths.py` gives different wrong answers. If you rerun it, update the numbers here.
