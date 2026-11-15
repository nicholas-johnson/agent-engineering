# Calculator MCP server — started automatically as a subprocess by play.py.
# Don't run this file directly; run `playground/calculator/play.py` instead.
#
# To play: delete `square_root` to see if the agent uses `power(x, 0.5)` instead,
# or make `power` return exact Python `int` values when both inputs are whole numbers.

import math

from mcp.server.mcpserver import MCPServer

server = MCPServer("calculator")


# Each @server.tool() exposes its function name, docstring, and type hints to the model.
@server.tool()
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b


@server.tool()
def subtract(a: float, b: float) -> float:
    """Subtract b from a."""
    return a - b


@server.tool()
def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b


@server.tool()
def divide(a: float, b: float) -> float:
    """Divide a by b."""
    return a / b


@server.tool()
def power(base: float, exponent: float) -> float:
    """Raise base to the power of exponent."""
    return base**exponent


@server.tool()
def square_root(number: float) -> float:
    """Return the square root of a number."""
    return math.sqrt(number)


server.run()
