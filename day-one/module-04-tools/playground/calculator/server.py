import math

from mcp.server.mcpserver import MCPServer

server = MCPServer("calculator")


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
