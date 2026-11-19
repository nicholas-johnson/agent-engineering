---
title: Away Temperature and Manual Override Support Playbook
product: thermostat
type: internal
audience: internal
firmware: 4.1
updated: 2026-09-09
---

# Away Temperature and Manual Override Support Playbook

## Purpose and scope

Use this playbook to explain away temperature, turning away mode on, and what happens when someone changes the target temperature by hand. It applies to Dormouse Thermostat firmware 4.1.

The thermostat's away temperature is 16 degrees by default. A user can change it in Settings > Away > Away temperature. Away mode keeps the home at that temperature until away mode is turned off.

A manual temperature change is different: it lasts until the next schedule period starts. Explain which control the user has changed before describing how long the setting will apply.

## Explain away temperature

Away temperature is the target temperature used while away mode is on. It is not the same as the target temperature in the home's schedule.

- The default away temperature is 16 degrees.
- Users can change it in Settings > Away > Away temperature.
- Away mode remains on until the user turns it off, or geofencing turns it off when applicable.
- Frost protection remains active while away mode is on. If the room falls below 5 degrees, the thermostat turns on the heating to protect the pipes.

Do not describe 16 degrees as a minimum or maximum. The guide identifies it as the default and confirms that it can be changed, but does not specify an allowed range for the away temperature.

## Enable and disable away mode

Users can turn away mode on in either of these ways:

1. In the app, tap Away.
2. On the thermostat, press the dial to open the menu, then choose Menu > Away.

Away mode keeps the home at the away temperature until it is turned off. When away mode is on, the display shows a house with an arrow.

The guide specifies how to turn away mode on, but does not give a manual off menu path. If a user needs help turning it off, direct them to the Away control in the app or the Away item in the thermostat menu, and have them follow the displayed control state. Do not promise that turning away mode off will restore a particular target temperature; the guide does not specify the exact temperature shown after it is turned off.

## Geofencing behaviour

Geofencing can turn away mode on and off using the location of household members' phones, provided each member chooses to share their location in the app.

- Away mode turns on when every member who shares their location is more than 1 km from home.
- It turns off when the first of those members comes back within 1 km.
- To stop geofencing for the whole home, go to Settings > Away > Geofencing.

Clarify that geofencing is based on the members who share their location, not necessarily every member of the household. Phone locations are never stored; the system stores only whether each member is home or away.

## Manual temperature changes and schedules

A user can turn the dial to change the target temperature, or make the change in the app. A manual change lasts until the next schedule period starts.

Explain this separately from away mode:

| Control or state | What it does | How long it applies |
|---|---|---|
| Manual target temperature change | Changes the target temperature by hand | Until the next schedule period starts |
| Away mode | Keeps the home at the configured away temperature | Until away mode is turned off |
| Frost protection | Heats if the room falls below 5 degrees | Always on, including when heating is off or away mode is on |

Do not tell users that a manual temperature change permanently edits their schedule. To change schedule periods, use the Schedule tab in the app or web dashboard. On the thermostat, Menu > Schedule shows today's periods, but they can only be changed in the app or web dashboard.

## Support handling

When a user reports that the home is not at the temperature they expected, establish the active control before suggesting a change:

1. Check whether away mode is on. The house-with-arrow symbol indicates that it is.
2. If away mode is on, confirm the configured away temperature in Settings > Away > Away temperature.
3. If away mode is off, ask whether the target was changed by hand and whether a schedule period has since started.
4. If geofencing is enabled, check whether household members' location-sharing choices and home/away status explain the change.
5. If the room is below 5 degrees, explain that frost protection can heat even while away mode is on.

Support is available in the app under Help > Contact support. Do not infer a fault from a difference between the schedule target and the away temperature: these are separate controls.

## Troubleshooting notes

If away mode turns on or off unexpectedly, check whether geofencing is enabled in Settings > Away > Geofencing. Explain its distance rules and confirm which household members share their location.

If the displayed target does not match the user's expected away temperature, confirm that away mode is active and check the configured value. If away mode is not active, a hand-set target lasts only until the next schedule period starts.

Frost protection is always on and cannot be turned off. If the room falls below 5 degrees, the thermostat may turn on the heating despite away mode or the heating being off. The snowflake symbol appears while frost protection is heating.

Do not promise a particular transition target when away mode is turned off; the guide does not define that behaviour.

## Known information limits

The user guide does not specify:

- an allowed range or step size for away temperature
- the exact target temperature selected when away mode is turned off
- how a manual temperature change interacts with away mode if both are active
- a thermostat-only menu path for changing the away temperature

Keep explanations within these limits. Do not invent timing, priority rules, or additional controls. If the observed behaviour appears inconsistent with the documented rules, record the user's settings and observed display state, then contact support through Help > Contact support.

## Internal QA and escalation notes

Use the documented behaviours as the basis for support guidance and QA checks: default away temperature of 16 degrees; configurable away temperature; manual changes lasting until the next schedule period; geofencing distance rules; and frost protection below 5 degrees.

Escalate cases where observed behaviour conflicts with these documented behaviours. Do not present internal escalation levels or rollout procedures as user-facing product behaviour.
