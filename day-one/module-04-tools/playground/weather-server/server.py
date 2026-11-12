import json
import urllib.parse
import urllib.request

from mcp.server.mcpserver import MCPServer

server = MCPServer("weather")


def open_meteo(url, **params):
    with urllib.request.urlopen(f"{url}?{urllib.parse.urlencode(params)}") as response:
        return json.load(response)


@server.tool()
def find_place(name: str) -> str:
    """Find a town or city by name. Returns its country, latitude and longitude."""
    found = open_meteo("https://geocoding-api.open-meteo.com/v1/search", name=name, count=1)
    if not found.get("results"):
        return f"No place called {name} found."
    place = found["results"][0]
    return json.dumps({key: place[key] for key in ["name", "country", "latitude", "longitude"]})


@server.tool()
def get_weather(latitude: float, longitude: float) -> str:
    """Get the current weather and a three-day forecast for a latitude and longitude.
    Temperatures are in Celsius, wind in km/h, rain in mm."""
    weather = open_meteo(
        "https://api.open-meteo.com/v1/forecast",
        latitude=latitude,
        longitude=longitude,
        current="temperature_2m,precipitation,wind_speed_10m",
        daily="temperature_2m_max,temperature_2m_min,precipitation_probability_max",
        timezone="auto",
        forecast_days=3,
    )
    return json.dumps({"current": weather["current"], "daily": weather["daily"]})


server.run()
