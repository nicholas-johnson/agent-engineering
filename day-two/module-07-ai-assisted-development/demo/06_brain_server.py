# Run from the module folder: uv run python demo/06_brain_server.py
# You don't run it yourself: Claude Code, Cursor or the Claude app starts it. See demo/06_company_brain.md.

import json
from pathlib import Path

from mcp.server.mcpserver import MCPServer

DATA = Path(__file__).parent.parent / "data"
TOPICS = ["product", "customers", "voice", "glossary", "decisions", "design"]

# Log warnings only, so the tool that starts it doesn't fill up with messages.
server = MCPServer("dormouse-brain", log_level="WARNING")


@server.tool()
def read_brain(topic: str) -> str:
    """Read one part of Dormouse's company brain. `topic` is one of: product (every feature, and where each
    setting lives), customers (who they are, and what they care about), voice (how we write, and the words
    we don't use), glossary (our terms, and what customers call them), decisions (product decisions we've
    made, and why) or design (colours, type, and how a settings screen is laid out). Read decisions before
    making any product decision, and voice before writing anything a customer will read."""
    if topic not in TOPICS:
        return f"There is no {topic}. Choose one of: {', '.join(TOPICS)}"
    return (DATA / "brain" / f"{topic}.md").read_text()


@server.tool()
def get_ticket(ticket_id: str) -> str:
    """Read one ticket, such as DOR-231: the problem, what we're building, and its acceptance criteria."""
    path = DATA / "tickets" / f"{ticket_id.upper()}.md"
    if not path.is_file():
        tickets = sorted(ticket.stem for ticket in (DATA / "tickets").glob("*.md"))
        return f"There is no {ticket_id}. The tickets are: {', '.join(tickets)}"
    return path.read_text()


@server.tool()
def search_feedback(words: str) -> str:
    """Customer feedback from September and October 2026 that contains any of these words, as JSON: each
    piece with its id, channel, date and text. Use it to find what customers have said about a feature."""
    wanted = words.lower().split()
    feedback = json.loads((DATA / "feedback.json").read_text())
    return json.dumps([item for item in feedback if any(word in item["text"].lower() for word in wanted)], indent=2)


server.run()
