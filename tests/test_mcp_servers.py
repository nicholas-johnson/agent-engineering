"""Tests every MCP server directly over stdio using mcp.Client."""

from __future__ import annotations

import asyncio
import json
import math
import sys

import pytest
from mcp import Client
from mcp.client.stdio import StdioServerParameters

from tests.conftest import REPO_ROOT, check_requirements, find_module

TOOLS = find_module("tools")
RAG = find_module("rag-and-proprietary-knowledge")
SECURITY = find_module("security-and-deployment")
DORMOUSE_SERVER = f"{SECURITY}/demo/06_dormouse_server.py"

SERVER_TOOLS: dict[str, set[str]] = {
    f"{TOOLS}/demo/03_maths_server.py": {"square_root"},
    f"{TOOLS}/demo/04_cards_server.py": {"search_cards", "find_card"},
    f"{TOOLS}/playground/calculator/server.py": {
        "add",
        "subtract",
        "multiply",
        "divide",
        "power",
        "square_root",
    },
    f"{TOOLS}/playground/weather-server/server.py": {"find_place", "get_weather"},
    f"{RAG}/demo/07_docs_server.py": {"search_docs"},
}

# Module 8's server needs the signed-in person's token, so it has its own test below.
COVERED_SERVERS: frozenset[str] = frozenset(SERVER_TOOLS) | {DORMOUSE_SERVER}


def _server_params(rel_path: str) -> StdioServerParameters:
    return StdioServerParameters(command=sys.executable, args=[str(REPO_ROOT / rel_path)])


@pytest.mark.offline
@pytest.mark.parametrize("rel_path,expected_tools", SERVER_TOOLS.items(), ids=SERVER_TOOLS.keys())
def test_mcp_server_lists_tools(rel_path: str, expected_tools: set[str]) -> None:
    async def check() -> None:
        async with Client(_server_params(rel_path)) as client:
            tools = (await client.list_tools()).tools
            names = {tool.name for tool in tools}
            assert names == expected_tools
            for tool in tools:
                assert tool.description, f"Tool {tool.name} in {rel_path} has no description"
                assert tool.input_schema.get("type") == "object"

    asyncio.run(check())


@pytest.mark.offline
def test_maths_server_square_root() -> None:
    async def check() -> None:
        async with Client(_server_params(f"{TOOLS}/demo/03_maths_server.py")) as client:
            result = await client.call_tool("square_root", {"number": 7654321})
            value = float(result.content[0].text)
            assert math.isclose(value, math.sqrt(7654321), rel_tol=1e-12)

    asyncio.run(check())


@pytest.mark.offline
def test_calculator_server_operations() -> None:
    async def check() -> None:
        async with Client(_server_params(f"{TOOLS}/playground/calculator/server.py")) as client:
            cases = [
                ("add", {"a": 12.5, "b": 7.5}, 20.0),
                ("subtract", {"a": 20.0, "b": 8.5}, 11.5),
                ("multiply", {"a": 6.0, "b": 7.0}, 42.0),
                ("divide", {"a": 45.0, "b": 9.0}, 5.0),
                ("power", {"base": 2.0, "exponent": 10.0}, 1024.0),
                ("square_root", {"number": 81.0}, 9.0),
            ]
            for name, arguments, expected in cases:
                result = await client.call_tool(name, arguments)
                assert math.isclose(float(result.content[0].text), expected, rel_tol=1e-12)

    asyncio.run(check())


@pytest.mark.network
def test_cards_server_live_lookup(pytestconfig: pytest.Config) -> None:
    check_requirements(pytestconfig, needs_internet=True)

    async def check() -> None:
        async with Client(_server_params(f"{TOOLS}/demo/04_cards_server.py")) as client:
            card_result = await client.call_tool("find_card", {"name": "Sol Ring"})
            card = json.loads(card_result.content[0].text)
            assert card["name"] == "Sol Ring"

    asyncio.run(check())


@pytest.mark.network
def test_weather_server_live_lookup(pytestconfig: pytest.Config) -> None:
    check_requirements(pytestconfig, needs_internet=True)

    async def check() -> None:
        async with Client(_server_params(f"{TOOLS}/playground/weather-server/server.py")) as client:
            place_result = await client.call_tool("find_place", {"name": "Oxford"})
            place = json.loads(place_result.content[0].text)
            assert place["name"] == "Oxford"

            weather_result = await client.call_tool(
                "get_weather",
                {"latitude": place["latitude"], "longitude": place["longitude"]},
            )
            weather = json.loads(weather_result.content[0].text)
            assert "current" in weather and "daily" in weather

    asyncio.run(check())


@pytest.mark.offline
def test_dormouse_server_gives_each_role_its_own_tools() -> None:
    """Sam's token gets the customer's tools and only Sam's home; Priya's gets the staff tools."""

    def params(token: str) -> StdioServerParameters:
        return StdioServerParameters(
            command=sys.executable, args=[str(REPO_ROOT / DORMOUSE_SERVER)], env={"DORMOUSE_TOKEN": token}
        )

    async def check() -> None:
        async with Client(params("sam-7f3a")) as sam:
            names = {tool.name for tool in (await sam.list_tools()).tools}
            assert names == {"search_docs", "get_my_home", "contact_support"}
            home = json.loads((await sam.call_tool("get_my_home", {})).content[0].text)
            assert home["id"] == "H-1042"
        async with Client(params("priya-91c2")) as priya:
            names = {tool.name for tool in (await priya.list_tools()).tools}
            assert names == {"search_docs", "get_customer", "offer_replacement"}
            customer = json.loads((await priya.call_tool("get_customer", {"customer_id": "C-1001"})).content[0].text)
            assert customer["home"]["id"] == "H-1042"

    asyncio.run(check())
