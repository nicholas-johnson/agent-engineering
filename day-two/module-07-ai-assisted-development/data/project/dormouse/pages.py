"""The settings page of the web dashboard, as HTML."""

from html import escape

# Each section of the page, and the settings in it: (setting, label, explanation).
SECTIONS = {
    "Heating": [
        ("boost_temperature", "Boost temperature", "The temperature a boost heats to, for one hour."),
        ("warm_wake", "Warm Wake", "Starts the heating up to 90 minutes early, so the home is warm when each period starts."),
    ],
    "Schedule": [
        ("week_starts_on", "Week starts on", "The first day shown in the Schedule tab."),
    ],
    "Away": [
        ("away_temperature", "Away temperature", "The temperature while away mode is on."),
        ("geofencing", "Geofencing", "Turns away mode on when everyone is more than 1 km from home."),
    ],
}


def control(name, value):
    """The form control for one setting."""
    if isinstance(value, bool):
        checked = " checked" if value else ""
        return f'<input type="checkbox" role="switch" name="{name}"{checked}>'
    if name == "week_starts_on":
        options = "".join(
            f'<option{" selected" if day == value else ""}>{day}</option>' for day in ("Monday", "Sunday")
        )
        return f'<select name="{name}">{options}</select>'
    return f'<input type="number" name="{name}" value="{value}" step="0.5"> degrees'


def settings_page(settings):
    """The whole settings page for one home's settings."""
    html = ["<h1>Settings</h1>"]
    for section, rows in SECTIONS.items():
        html.append(f"<h2>{section}</h2>")
        for name, label, explanation in rows:
            html.append(
                f'<div class="setting"><label>{escape(label)}</label>'
                f"<p>{escape(explanation)}</p>{control(name, settings[name])}</div>"
            )
    return "\n".join(html)
