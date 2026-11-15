# The protocol by hand

From the module folder (`day-one/module-04-tools`):

```bash
uv run python playground/raw-protocol/play.py
```

Or without `uv` (set up `.venv` once at the repo root with `python3 -m venv .venv && .venv/bin/pip install -e .`):

```bash
source ../../.venv/bin/activate
python playground/raw-protocol/play.py
```

No API key needed. Every message, sent and received, is written to `playground/raw-protocol/output/messages.json`.

---

The `mcp` package hides the protocol. This takes it away: it starts the maths server from demo 3 and talks to it by writing JSON to its standard input and reading JSON back from its standard output, one line per message. No API key, no model, no `mcp` client.

```text
>> {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-11-25", ...}}
<< {"jsonrpc": "2.0", "id": 1, "result": {"capabilities": {"prompts": ..., "resources": ..., "tools": ...}, "protocolVersion": "2025-11-25", "serverInfo": {"name": "maths", "version": ""}}}

>> {"jsonrpc": "2.0", "method": "notifications/initialized"}
>> {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}
<< {"jsonrpc": "2.0", "id": 2, "result": {"tools": [{"description": "Return the square root of a number, exactly, to full precision.", "inputSchema": {...}, "name": "square_root", "outputSchema": {...}}]}}

>> {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "square_root", "arguments": {"number": 7654321}}}
<< {"jsonrpc": "2.0", "id": 3, "result": {"content": [{"text": "2766.644357339772", "type": "text"}], "isError": false, "structuredContent": {"result": 2766.644357339772}}}
```

That's all MCP is: **JSON-RPC** messages (a request has a `method`, `params` and an `id`; the reply has the same `id`) over a pipe.

1. `initialize`: agree a protocol version, and say what each side can do.
2. `notifications/initialized`: "ready". A notification has no `id` and gets no reply.
3. `tools/list`: "what tools do you have?"
4. `tools/call`: "run this one, with these arguments".

## Things to notice

- **The server offers more than tools.** Its `capabilities` mention `prompts` and `resources` too. MCP servers can also offer ready-made prompts and data to read. We only used tools.
- **The tool has an output schema too.** Because `square_root` is declared to return a `float`, the server describes its output, and sends the answer twice: as text in `content`, and as data in `structuredContent`.

## Try this

1. **Another version.** Change `protocolVersion` to `"2026-07-28"`, a newer version the SDK knows about. What version does the server reply with? (Each side says which versions it supports, and they settle on one.)
2. **A mistake.** Call a tool that doesn't exist, or send `"number": "seven"`. What does an error look like?
3. **Skip the handshake.** Send `tools/list` without `initialize` first. Does the server still answer?
4. **Another server.** Point `SERVER` at `../../demo/04_cards_server.py` and call `find_card` by hand.
5. **Ping.** Send `{"jsonrpc": "2.0", "id": 4, "method": "ping"}`. What comes back, and what might it be for?

## Questions

For discussion. There are no right answers.

- MCP is just JSON messages over a pipe. Why does agreeing a standard matter more than any one tool?
- What should a server be allowed to know about the client that connects to it, and what should the client know about the server?
- MCP servers offer prompts and resources as well as tools. What might each be useful for?
