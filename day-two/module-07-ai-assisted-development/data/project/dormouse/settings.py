"""Every setting a customer can change, with its default and the values it allows."""

DEFAULTS = {
    "boost_temperature": 21.0,
    "warm_wake": True,
    "week_starts_on": "Monday",
    "away_temperature": 16.0,
    "geofencing": False,
}

TEMPERATURE_RANGES = {
    "boost_temperature": (15, 25),
    "away_temperature": (5, 20),
}


def check(name, value):
    """Raise ValueError if value isn't allowed for the setting called name."""
    if name not in DEFAULTS:
        raise ValueError(f"Unknown setting: {name}")
    if name in TEMPERATURE_RANGES:
        low, high = TEMPERATURE_RANGES[name]
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{name} must be a number")
        if not low <= value <= high or value * 2 != round(value * 2):
            raise ValueError(f"{name} must be from {low} to {high} degrees, in half-degree steps")
    elif name in ("warm_wake", "geofencing"):
        if not isinstance(value, bool):
            raise ValueError(f"{name} must be on or off")
    elif name == "week_starts_on":
        if value not in ("Monday", "Sunday"):
            raise ValueError("week_starts_on must be Monday or Sunday")


def update(settings, changes):
    """Return a copy of settings with the changes applied, after checking every change."""
    for name, value in changes.items():
        check(name, value)
    return {**settings, **changes}
