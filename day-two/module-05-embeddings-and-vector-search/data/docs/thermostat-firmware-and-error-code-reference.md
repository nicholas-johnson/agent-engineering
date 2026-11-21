---
title: Thermostat Firmware and Error Code Reference
product: thermostat
type: specification
audience: customer
firmware: 4.1
updated: 2026-07-10
---

# Thermostat Firmware and Error Code Reference

## Scope

This reference covers the Dormouse Thermostat with firmware 4.1. To check the installed firmware, press the dial to open the menu and choose Menu > About.

The thermostat shows an error code on its display when something is wrong. The app shows the same code and can notify you about it. The action needed depends on the code; use the tables below to identify its meaning and response.

## Firmware 4.1

Firmware 4.1 is the current firmware covered by this reference. It includes the following changes:

- The boost temperature can be changed in Settings > Heating > Boost temperature. The default is 21 degrees.
- Password reset links work for 30 minutes and can only be used once.

Firmware 4.1 was released on 17 August 2026.

## Automatic updates

The thermostat installs firmware updates automatically between 02:00 and 04:00 local time. Updates cannot be postponed.

While an update installs, the display shows UPDATING and the thermostat restarts. Installation takes about two minutes. Heating pauses until the update has finished.

## Update failure

If an update fails, the display shows E-510. The thermostat keeps its current firmware and tries the update again the next night. No action is needed.

## Error codes: connectivity and pairing

| Code | Meaning | What to do |
|---|---|---|
| E-101 | Wi-Fi network not found | Check that the router is on and offers a 2.4 GHz network. If the network name or password has changed, pair the thermostat again. |
| E-104 | Pairing timed out | Pairing must finish within 3 minutes of the display showing PAIR. Hold the dial down for 5 seconds to start again. Keep the phone within 5 metres of the thermostat until pairing finishes. |
| E-110 | Cannot reach the Dormouse cloud | Check that the router is connected to the internet. The thermostat continues running its schedules. Changes made in the app wait until the thermostat reconnects. |

## Error codes: sensors and boiler

| Code | Meaning | What to do |
|---|---|---|
| E-217 | Temperature sensor disconnected | The thermostat turns the heating off to be safe. Contact Dormouse support to arrange a replacement. In the app, go to Help > Contact support. |
| E-221 | Humidity sensor fault | The heating continues working, but humidity readings disappear from the app. Contact Dormouse support if the code remains for more than a day. In the app, go to Help > Contact support. |
| E-305 | Boiler not responding | Check that the boiler is switched on and its pressure is between 1 and 1.5 bar. Then check the boiler's own display for a fault. |
| E-312 | Boiler reports a fault | The boiler has found a fault of its own. Look up the fault in the boiler manual, or call a registered gas engineer. |

## Error codes: power and batteries

| Code | Meaning | What to do |
|---|---|---|
| E-401 | Backup batteries low | Replace the two AA batteries behind the front cover within a month. |
| E-402 | Mains power interrupted | The thermostat is running on backup batteries. It keeps the clock and schedules for up to 48 hours, but cannot switch the heating on while mains power is off. |

To reach the backup batteries, pull the bottom of the front cover gently towards you. Replace the batteries once a year, or when E-401 appears.

## Error code: firmware update

| Code | Meaning | What to do |
|---|---|---|
| E-510 | Firmware update failed | No action is needed. The thermostat keeps its current firmware and tries the update again the next night. |

## Support and reference

The app shows the same error code as the thermostat and can notify you about it. To contact Dormouse support, use Help > Contact support in the app.

For firmware details, open the thermostat menu and choose Menu > About. For battery replacement, pairing and heating operation, follow the relevant instructions in the Dormouse Thermostat User Guide.
