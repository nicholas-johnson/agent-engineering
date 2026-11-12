import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
OUTPUT = HERE / "output"
OUTPUT.mkdir(exist_ok=True)

SERVER = HERE.parent.parent / "demo" / "03_maths_server.py"

# Start the maths server, exactly as the agent does, and talk to it ourselves.
server = subprocess.Popen(
    [sys.executable, str(SERVER)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True
)
log = []


def send(message):
    server.stdin.write(json.dumps(message) + "\n")
    server.stdin.flush()
    print(f">> {json.dumps(message)}")
    log.append({"sent": message})
    if "id" in message:
        reply = json.loads(server.stdout.readline())
        print(f"<< {json.dumps(reply)}\n")
        log.append({"received": reply})


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
