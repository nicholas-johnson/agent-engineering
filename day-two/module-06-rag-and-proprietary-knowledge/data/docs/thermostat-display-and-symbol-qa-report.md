---
title: Thermostat Display and Symbol QA Report
product: thermostat
type: internal
audience: internal
firmware: 4.1
updated: 2026-09-15
---

# Thermostat Display and Symbol QA Report

## Scope

This report covers display checks for the Dormouse Thermostat running firmware 4.1: room and target temperature presentation, target adjustment, dimming after inactivity, and the documented display symbols.

Use this report to verify visible behaviour against the user guide. Do not infer additional display states or meanings beyond those listed here. The thermostat's firmware version can be checked by pressing the dial to open the menu and choosing Menu > About.

## Room and target temperature presentation

When the display is showing the room temperature, verify that:

- The room temperature appears in large numbers.
- The target temperature appears underneath it.

The display is a 2.4-inch round colour screen. Its dimensions and colour capabilities do not change the expected placement or relative size of the two temperature readings.

Check that the displayed values are legible and that the room temperature is visually distinguished from the target temperature by its larger presentation. This report does not specify a tolerance for displayed temperature values, rounding behaviour, or display refresh timing.

## Target temperature adjustment

Turn the dial to change the target temperature. While the user is changing it, verify that the target temperature becomes larger on the display. Press the dial to confirm the change.

The target temperature can be set from 5 to 30 degrees in half-degree steps. A manual change lasts until the next schedule period starts. These limits and step sizes are useful context for display testing, but this report does not define a separate acceptance tolerance for the temperature measurement itself.

The display dims after 20 seconds without a touch. Confirm that interaction with the dial brings the target temperature into the larger adjustment presentation as expected. Do not treat dimming as an error state.

## Dimming after inactivity

With the display active, leave the thermostat untouched for 20 seconds. Verify that the display dims. The guide specifies the inactivity interval and dimmed state, but does not specify brightness levels, transition duration, or whether the display turns fully off.

Record any case in which the display does not dim after the stated interval, dims before the interval has elapsed, or becomes unreadable during normal interaction. Distinguish display dimming from a symbol indicating an operating condition or fault.

## Documented display symbols

Verify the symbol-to-meaning mapping below. The symbol indicates the described condition; do not assign it a different meaning based on appearance alone.

| Display symbol | Documented meaning |
|---|---|
| Flame | The thermostat is asking the boiler for heat. |
| Sunrise | Warm Wake is heating ahead of the next schedule period. |
| Snowflake | Frost protection is heating the home. |
| House with an arrow | Away mode is on. |
| Upward arrow | A boost is running. |
| Wi-Fi symbol with a cross | The thermostat is not connected to Wi-Fi. |
| Battery | The backup batteries are low. |

## Symbol checks in context

Check symbols against their documented operating conditions:

- **Flame:** confirm that it represents the thermostat asking the boiler for heat. It does not, by itself, indicate a boiler fault.
- **Sunrise:** confirm that it represents Warm Wake heating ahead of the next schedule period. This report does not specify how Warm Wake determines its timing.
- **Snowflake:** confirm that it appears while frost protection is heating. Frost protection operates if the room falls below 5 degrees, including when heating is off or away mode is on. It is always on and cannot be turned off.
- **House with an arrow:** confirm that it indicates away mode is on.
- **Upward arrow:** confirm that it indicates a boost is running. A boost lasts one hour unless cancelled by pressing the boost button again.
- **Wi-Fi symbol with a cross:** confirm that it indicates the thermostat is not connected to Wi-Fi. Do not use this symbol as the documented indication that the Dormouse cloud cannot be reached; that condition has error code E-110.
- **Battery:** confirm that it indicates low backup batteries. Error code E-401 also identifies low backup batteries.

## Fault and status separation

Display symbols and error codes have distinct documented roles. Check that a symbol is not reported as an error code and that an error code is not mistaken for one of the listed symbols.

For example, E-401 means backup batteries are low; replace the two AA batteries behind the front cover within a month. E-402 means mains power is interrupted: the thermostat runs on backup batteries, keeps the clock and schedules for up to 48 hours, but cannot switch the heating on. The low-battery symbol alone does not convey the full E-402 condition.

When the thermostat shows an error code, the app shows the same code. The display may also show the documented operating symbols described in this report; record what is visible without inferring undocumented combinations or priority rules.

## QA recording and escalation

For each check, record the firmware version, the observed display state, the interaction or condition that produced it, and whether the result matches the documented behaviour. Include the time allowed for inactivity checks and the symbol's relevant operating context.

Do not mark a behaviour as a defect solely because this report does not define its exact visual styling, brightness, animation, or timing beyond the stated 20-second dimming interval. Escalate a mismatch against documented behaviour through the established support route: in the app, choose Help > Contact support.
