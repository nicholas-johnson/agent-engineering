# Run sheet: the company brain

The live demo for section 6. `demo/06_brain_server.py` is an MCP server that offers Dormouse's company brain as three tools: `read_brain`, `get_ticket` and `search_feedback`. You attach it to Claude Code, Cursor and the Claude app, then ask each one something only the brain can answer.

You don't run the server yourself: each tool starts it. Every command below needs the full path to this module folder, so set it once. From the module folder:

```bash
MODULE="$PWD"
```

Set up the project as in the other run sheets, if you haven't:

```bash
cp -R data/project ~/dormouse-dashboard && cd ~/dormouse-dashboard && git init -q && git add . && git commit -qm "Start"
```

## 1. Claude Code

1. In `~/dormouse-dashboard`:

   ```bash
   claude mcp add --transport stdio dormouse-brain -- uv run --directory "$MODULE" python demo/06_brain_server.py
   ```

2. Start `claude` and type `/mcp`. `dormouse-brain` should be connected, with three tools.
3. Ask: "What have we decided about where settings go, and why?" It calls `read_brain("decisions")`, and asks before it does.
4. Then: "Build DOR-233." It fetches the ticket with `get_ticket`, and can read the voice before writing the labels.

Point out: the brain isn't in the project. Any project, and any session, can use it.

## 2. Cursor

1. In `~/dormouse-dashboard`, create `.cursor/mcp.json`, putting the module folder's full path in place of `MODULE`:

   ```json
   {
     "mcpServers": {
       "dormouse-brain": {
         "type": "stdio",
         "command": "uv",
         "args": ["run", "--directory", "MODULE", "python", "demo/06_brain_server.py"]
       }
     }
   }
   ```

2. Open Cursor's settings, find MCP, and check `dormouse-brain` is on, with three tools.
3. In Ask mode: "What did customers say about the heating coming on early?" It calls `search_feedback`.

Point out: the same server, unchanged, in a different tool.

## 3. The Claude app

1. In the Claude desktop app, open **Settings → Developer → Edit Config**, and add the same `dormouse-brain` entry under `mcpServers` in `claude_desktop_config.json`. Restart the app.
2. In a new chat: "Write a two-line reply to a customer who asks why their heating comes on at 5:40 for a 7:00 period." It can read the voice and the product before it writes.

Point out: no code at all. Support, product and marketing get the same brain as the developers.

## Where it stops

Lovable's connectors and the cloud agents run on someone else's computer, so they can't start a program on yours. They need the server running on the internet, at a URL, with sign-in in front of it. That is deployment, and Module 8.
