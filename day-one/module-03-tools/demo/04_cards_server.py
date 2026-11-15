# Run from the module folder: uv run python demo/04_cards_server.py

import json
import time
import urllib.error
import urllib.parse
import urllib.request

from mcp.server.mcpserver import MCPServer

server = MCPServer("cards")

# Scryfall asks every program to say who it is, and to make at most two requests a second.
HEADERS = {"User-Agent": "AgentEngineeringCourse/1.0", "Accept": "application/json"}


def scryfall(path, **params):
    time.sleep(0.5)
    url = f"https://api.scryfall.com/{path}?{urllib.parse.urlencode(params)}"
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS)) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        return json.load(error)


@server.tool()
def search_cards(query: str) -> str:
    """Search Magic: The Gathering cards using Scryfall search syntax, for example
    'name:rabbit t:creature' or 'o:"draw a card" c:blue'. Returns up to 10 card names
    with their current US dollar prices, most expensive first."""
    found = scryfall("cards/search", q=query, order="usd", dir="desc")
    if found["object"] == "error":
        return found["details"]
    return json.dumps([{"name": card["name"], "usd": card["prices"]["usd"]} for card in found["data"][:10]])


@server.tool()
def find_card(name: str) -> str:
    """Look up one Magic: The Gathering card by name (spelling can be approximate).
    Returns its cost, type, rules text, set and current prices."""
    card = scryfall("cards/named", fuzzy=name)
    if card["object"] == "error":
        return card["details"]
    fields = ["name", "mana_cost", "type_line", "oracle_text", "set_name", "released_at", "prices"]
    return json.dumps({field: card.get(field) for field in fields})


server.run()
