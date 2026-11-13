# Clip 1 — The square root

> A promise to explain MCP in sixty seconds. Then an AI gives three different, confident, wrong answers to the same maths question, a tool call fixes it, and four extra lines turn that tool into an MCP server that any MCP app can use, alongside Google's real ones for Gmail and Calendar. Then a sign-off.

- **Promotes:** Module 4, Tools
- **Length:** about 155 spoken words to explain MCP and show the real servers, then about 25 for the sign-off. The hook promises sixty seconds, so time your first take: see the notes if it runs over.
- **Ending:** the sign-off, full-face: "Follow if you'd like to know more." Cut straight after it.
- **Recording:** [`index.html`](index.html) in this folder. It puts you, the animation and the captions on one stage. Run `pnpm social`, open <http://127.0.0.1:8765/01-square-root/> in Chrome and press R. Each press of space brings up the next caption: say it, then press again.

## The script

### 1. Hook

To camera, full-screen for the first two lines:

> "I'm going to explain MCP to you in sixty seconds."

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

> "But Python can't read a question. So we give this function to the AI as a tool. Now when I ask, it doesn't guess. It asks *me* to run `square_root` on 7,654,321. My code runs it and hands back the answer."

Put some warmth into "it asks *me*". The AI asking for help is the charming part.

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

> "That's an MCP server. Write it once, and Claude, Cursor and VS Code can all use it."

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
| — | I'm going to explain *MCP* to you in sixty seconds. | You, full-screen |
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
| 13 | My code runs it… | The result types out |
| 14 | …and hands back the answer. | The AI's reply streams in, word by word |
| 15 | Right first time. Every time. | — |
| 16 | And that tool? It's the same function… | The function on its own |
| 17 | …plus four lines. | The four lines open up around the function, and the heading becomes "An MCP server." |
| 18 | That's an *MCP server*. | — |
| 19 | Write it once, and Claude, Cursor and VS Code can all use it. | — |
| 20 | Google has one for Gmail: your AI can search your inbox and draft replies. | "Real MCP servers", with a Gmail card |
| 21 | And one for Calendar: it can find a free slot and book the meeting. | A Calendar card |
| 22 | And now there's yours. | Your `maths` server joins them |
| 23 | I'm Nicholas Johnson. I'm a principal dev working with AI. | You, full-screen again |
| 24 | I'm doing a series on *AI fundamentals*. | — |
| 25 | Follow if you'd like to know more. | — |

Then press R to stop.

## Post text

For the description under the video, not on it.

Repeat the promise, then the course plug:

> MCP in sixty seconds: a Python function, four more lines, and Claude, Cursor and VS Code can all use it.

## Notes

- **The code on screen is squeezed to fit a phone.** The docstring is wrapped onto two lines, there is one blank line where the real files have two, and `import math` is left off. Otherwise it is the real code.
- **Expect the comment "just use a reasoning model".** That's the follow-up clip. Module 4 found that with reasoning turned on, the model does get the right answer, but each answer took 9 to 57 seconds of thinking you pay for, against about a second for the tool. And nothing guarantees the reasoning model gets it right; the tool is right because it's arithmetic.
- **If the explanation runs over sixty seconds** (everything before the sign-off), drop "All completely confident." and "It isn't calculating." here and in `index.html`. If it's still over, drop the Calendar line and keep Gmail. Don't split it into two parts: the hook promises the whole thing in one.

## Where the material comes from

From Module 4, `day-one/module-04-tools/`, except the two real servers:

| On screen | Source |
|-----------|--------|
| The three wrong answers and the right one | README, section 1 (`demo/01_maths.py`) |
| The function | `demo/02_function.py` |
| The transcript with the tool call | README, section 3 (`demo/03_agent.py`) |
| The MCP server | `demo/03_maths_server.py` |
| Reasoning taking 9 to 57 seconds | README, section 1, "What about reasoning?" |
| Google's Gmail and Calendar MCP servers | Google's [Workspace MCP server announcement](https://workspaceupdates.googleblog.com/2026/05/agent-tools-and-security-updates-for-workspace-developers.html), May 2026: Gmail can search and draft, Calendar can find free times and manage events. Public developer preview. Checked 13 November 2026 |

The model's answers are random, so rerunning `demo/01_maths.py` gives different wrong answers. If you rerun it, update the numbers here.
