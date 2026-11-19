# Your own server: the weather

A second MCP server, for the weather, to copy when you write your own. You'll ask a question in plain English and watch the agent chain its tools to answer.

From the module folder (`day-one/module-03-tools`):

```bash
uv run python playground/weather-server/play.py
```

Or without `uv` (set up `.venv` once at the repo root with `python3 -m venv .venv && .venv/bin/pip install -e .`):

```bash
source ../../.venv/bin/activate
python playground/weather-server/play.py
```

Needs `OPENAI_API_KEY` in `.env` and an internet connection. `play.py` starts `server.py` itself. The conversation is written to `playground/weather-server/output/conversation.json`.

---

It uses [Open-Meteo](https://open-meteo.com), which needs no key, and offers two tools:

- `find_place(name)`: a town's latitude and longitude
- `get_weather(latitude, longitude)`: the weather now, and a three-day forecast

```text
You: Is tomorrow a good day for a picnic by the river in Oxford, where Lewis Carroll first told the story of Alice?
  [tool] find_place({"name":"Oxford"}) -> {"name": "Oxford", "country": "United Kingdom", "latitude": 51.75222, "longitude": -1.25596}
  [tool] get_weather({"latitude":51.75222,"longitude":-1.25596}) -> {"current": {"time": "2026-11-12T14:30", "interval": 900, "temperature_2m": 6.8, "precipitation": 0.
Agent: Tomorrow, Friday 13 November, looks dry in Oxford, with little chance of rain. But it'll be cold: around 6°C at most, dipping below freezing overnight. So it's fine weather-wise if you bundle up, but probably not ideal for a leisurely riverside picnic.
```

The model chained the tools: a name became coordinates, and the coordinates became a forecast. Then it turned a page of numbers into advice.

## Things to notice

- **It knew what "tomorrow" meant.** The forecast comes back with dates in it, and the model matched them up.
- **Two small tools beat one big one.** `find_place` is useful on its own, and so is `get_weather`. The model composes them.

## Try this

1. **Ask something else.** "Where will it be warmest this weekend: Edinburgh, Cardiff or Belfast?" How many calls does it make?
2. **Add a tool.** Open-Meteo also has an [air quality API](https://open-meteo.com/en/docs/air-quality-api). Add `get_air_quality(latitude, longitude)`.
3. **Use it with the cards.** Connect this server and the cards server from demo 4 to the same agent, as `04_agent.py` does. Ask something that needs both.
4. **A different API.** Pick another free API that needs no key, such as [Gutendex](https://gutendex.com) (Project Gutenberg's books) or [REST Countries](https://restcountries.com), and write a server for it by copying this one.
5. **Use it from an app.** Many desktop AI apps, such as Claude Desktop, can run local MCP servers. Look up how to add one to an app you use, and give it this server. The app becomes the agent and does the tool loop for you.

## Questions

For discussion. There are no right answers.

- The agent turned a page of numbers into advice: not ideal for a picnic. When should an agent give opinions, and when should it stick to the facts?
- What public data would you most like an agent to have access to? What data should it never have?
- If an API changes the shape of its data overnight, the agent may quietly start giving wrong answers. How would you notice?

## Further reading

- **[Model Context Protocol](https://modelcontextprotocol.io).** The guides to writing a server. Copy this playground first, then use the spec when the next server needs something it does not have.
- **[Open-Meteo](https://open-meteo.com).** The weather API behind the two tools, including the air-quality API in the exercises. No key.
