---
title: Troubleshoot Dormouse Automation Connections
product: all
type: integration
audience: customer
firmware: 4.1
updated: 2025-10-07
---

# Troubleshoot Dormouse Automation Connections

## Identify the connection involved

Dormouse devices use different connections for different purposes:

| Connection | What it connects | What it affects |
|---|---|---|
| Thermostat Wi-Fi | The thermostat and your 2.4 GHz Wi-Fi network | Communication with the Dormouse app, web dashboard and Dormouse cloud |
| Zone radio link | A Room Sensor or Radiator Valve and the thermostat for its zone | Temperature readings from sensors and operation of valves |
| External automation setup | Dormouse and a separate home automation system, voice assistant or smart plug | Any connection or control provided by that external setup |

Only the thermostat uses Wi-Fi. Dormouse Room Sensors and Radiator Valves communicate with their zone's thermostat over a low-power 868 MHz radio link.

This guide helps you identify which connection may be involved. The thermostat's display symbols, error codes and the behaviour of devices in the affected zone can help narrow it down.

## Check the thermostat's Wi-Fi connection

Look at the thermostat display. A Wi-Fi symbol with a cross means the thermostat is not connected to Wi-Fi. Error codes can give more detail:

- **E-101: Wi-Fi network not found.** Check that your router is on and offers a 2.4 GHz network. The thermostat cannot join a 5 GHz network. If the network name or password has changed, pair the thermostat again.
- **E-110: Cannot reach the Dormouse cloud.** Check that your router is connected to the internet. The thermostat keeps running its schedules, but changes made in the app wait until it reconnects.

If there is no Wi-Fi symbol with a cross or relevant error code, that does not by itself confirm that an external automation connection is working. Check the external system separately.

When the thermostat is offline, changes made in the app may not reach it until it reconnects. Check the thermostat's display and whether its schedules continue to run before investigating other connections.

## Check a device's zone link

If the issue concerns a Room Sensor or Radiator Valve, first identify the zone it belongs to. Each thermostat controls its own zone, with its own schedule. A Room Sensor measures temperature and humidity in its zone. A Radiator Valve heats to its own temperature within that zone.

The thermostat does not show a dedicated symbol for a Room Sensor or Radiator Valve radio link in the display-symbol list. Instead, check what is missing or not working:

- If humidity readings have disappeared and the thermostat shows **E-221**, the thermostat has a humidity sensor fault. Heating keeps working; contact Dormouse support if the code remains for more than a day.
- If the thermostat shows **E-217**, its temperature sensor is disconnected. The thermostat turns the heating off to be safe. Contact Dormouse support to arrange a replacement.

These codes describe thermostat sensor faults; they do not establish that a Room Sensor or Radiator Valve has lost its zone radio link. If an added device is not behaving as expected, confirm which zone it has joined and whether the thermostat for that zone is operating normally.

## Check the heating and thermostat state

A heating issue can look like a connection issue. Check the thermostat's display and the current target temperature before changing settings elsewhere.

- The flame symbol means the thermostat is asking the boiler for heat.
- The upward arrow means a boost is running. Press the boost button again to cancel it.
- The snowflake means frost protection is heating. Frost protection always operates if the room falls below 5 degrees, even when heating is off or away mode is on.
- The house-with-an-arrow symbol means away mode is on.

If the boiler is not responding, the thermostat may show **E-305**. Check that the boiler is switched on, its pressure is between 1 and 1.5 bar, and its own display does not show a fault. **E-312** means the boiler reports a fault; check its manual or contact a registered gas engineer.

## Check the external automation setup

If the thermostat is connected to Wi-Fi and its normal Dormouse functions are available, but a separate automation, voice-control or smart-plug setup is not working, investigate that external setup separately. Dormouse's thermostat, app and web dashboard do not provide a diagnosis of an external system's connection or configuration.

Check the external system's own status and setup instructions. Confirm that the specific control or connection you expect is supported and configured there. Do not treat a Wi-Fi error, zone radio issue or boiler fault as proof that an external automation connection is at fault.

If the external setup appears to have changed a target temperature, remember that a manual temperature change lasts until the next schedule period starts. Check the thermostat's target and schedule as well as the external system's status.

## Use the app and dashboard to compare

The Dormouse app and web dashboard provide access to most thermostat settings. Menu paths in the app and dashboard use the same names. The thermostat can show today's schedule periods in Menu > Schedule, but schedule changes must be made in the app or web dashboard.

Compare what the thermostat displays with what appears in the app or dashboard:

1. Check whether the app or dashboard reflects the thermostat's current state.
2. If the thermostat is offline, use its display and schedules to assess local operation; app changes wait until it reconnects.
3. If the thermostat is online but only an external control is affected, check that external system rather than changing unrelated Dormouse settings.
4. If a Room Sensor or Radiator Valve is affected, verify its zone and the thermostat serving that zone.

Avoid factory resetting the thermostat as an initial troubleshooting step. A factory reset removes Wi-Fi details, schedules and the link to your account.

## When to contact support

Contact Dormouse support in the app under Help > Contact support if a thermostat error code remains unresolved or a sensor fault requires attention. Include the error code and describe which connection appears affected: thermostat Wi-Fi, a device's zone link, or an external automation setup.

For **E-217**, contact support to arrange a replacement. For **E-221**, contact support if the code stays for more than a day. For **E-110**, check the router's internet connection first; the thermostat continues running schedules while disconnected from the Dormouse cloud.

When reporting an issue with an external system, provide the relevant status shown by the thermostat and Dormouse app or dashboard, along with the behaviour seen in the external system. The Dormouse thermostat can confirm its own connection and operating state, but it cannot diagnose the external system's internal setup.
