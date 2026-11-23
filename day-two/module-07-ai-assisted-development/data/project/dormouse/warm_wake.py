"""When Warm Wake switches the heating on, so the home is warm when a schedule period starts."""

import math
from datetime import timedelta

MAX_MINUTES_EARLY = 90
DEFAULT_DEGREES_PER_HOUR = 3  # for a new home, until it has heated up a few times


def learned_rate(heat_ups):
    """How fast the home warms, in degrees an hour, from its recent heat-ups: (degrees gained, minutes taken) pairs."""
    if not heat_ups:
        return DEFAULT_DEGREES_PER_HOUR
    degrees = sum(gained for gained, _ in heat_ups)
    minutes = sum(taken for _, taken in heat_ups)
    return degrees / minutes


def minutes_to_heat(room, target, degrees_per_hour):
    """How many minutes the home takes to warm from room to target, at its learned heat-up rate."""
    if room >= target:
        return 0
    return math.ceil((target - room) / degrees_per_hour * 60)


def heating_start(period_start, room, target, degrees_per_hour, settings):
    """The time to switch the heating on for a schedule period that starts at period_start."""
    if not settings["warm_wake"]:
        return period_start
    minutes = min(minutes_to_heat(room, target, degrees_per_hour), MAX_MINUTES_EARLY)
    return period_start - timedelta(minutes=minutes)
