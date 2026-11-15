import math

from mcp.server.mcpserver import MCPServer

server = MCPServer("maths")


@server.tool()
def square_root(number: float) -> float:
    """Return the square root of a number, exactly, to full precision."""
    return math.sqrt(number)


server.run()
