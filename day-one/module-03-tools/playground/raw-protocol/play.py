# The protocol by hand — talk raw JSON-RPC over stdin/stdout to an MCP server, no SDK client.
# Run from the module folder: uv run python playground/raw-protocol/play.py
#                         or: source ../../.venv/bin/activate && python playground/raw-protocol/play.py
#
# To play: send a bad tool name or wrong argument type to see MCP error responses,
# send a "ping" request, or point SERVER at demo/04_cards_server.py (see README.md).

import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
OUTPUT = HERE / "output"
OUTPUT.mkdir(exist_ok=True)

SERVER = HERE.parent.parent / "demo" / "03_maths_server.py"

# Launch the MCP server as a child process with pipes attached to stdin and stdout.
server = subprocess.Popen(
    [sys.executable, str(SERVER)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True
)
log = []


def send(message):
    # MCP stdio transport is one JSON-RPC object per line; notifications have no "id" and no reply.
    server.stdin.write(json.dumps(message) + "\n")
    server.stdin.flush()
    print(f">> {json.dumps(message)}")
    log.append({"sent": message})
    if "id" in message:
        reply = json.loads(server.stdout.readline())
        print(f"<< {json.dumps(reply)}\n")
        log.append({"received": reply})


# 1. Handshake: agree protocol version and capabilities.
send(
    {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2025-11-25",
            "capabilities": {},
            "clientInfo": {"name": "by-hand", "version": "1.0"},
        },
    }
)
send({"jsonrpc": "2.0", "method": "notifications/initialized"})

# 2. Discover tools, then call one.
send({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
send(
    {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {"name": "square_root", "arguments": {"number": 7654321}},
    }
)

server.terminate()
(OUTPUT / "messages.json").write_text(json.dumps(log, indent=2))
