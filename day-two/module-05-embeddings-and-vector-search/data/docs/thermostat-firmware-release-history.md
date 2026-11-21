---
title: Thermostat Firmware Release History
product: thermostat
type: internal
audience: internal
firmware: 4.1
updated: 2026-04-08
---

# Thermostat Firmware Release History

## Scope

This internal release history covers Dormouse Thermostat firmware releases 3.0 through 4.1 and the documented changes to account security, zones, reports, devices and updates. The current firmware is 4.1.

The release dates below use the format YYYY-MM-DD. User-facing menu paths are written as they appear in the app and web dashboard.

## Release 3.0 - 2025-01-20

- Added two-step verification for accounts. When enabled, signing in on a new phone or browser requires a 6-digit code as well as the password. The code can come by email or from an authenticator app.
- Increased the maximum number of thermostats in a home from two to four. Each thermostat controls its own zone and schedule.

Two-step verification is managed at Settings > Account > Two-step verification.

## Release 3.1 - 2025-03-17

- Added geofencing for Away mode. It uses the location-sharing choice of each household member's phone. Away mode turns on when all members who share their location are more than 1 km from home, and turns off when the first of them returns within 1 km.
- Made the away temperature adjustable at Settings > Away > Away temperature. The default is 16 degrees.

Each member chooses whether to share their location in the app. Geofencing for the whole home can be stopped at Settings > Away > Geofencing. Phone locations are never stored; the system stores only whether each member is home or away.

## Release 3.2 - 2025-05-26

- Added monthly energy reports in the app's Energy tab. Reports arrive on the 1st of each month and show daily heating hours compared with the previous month, plus an estimate of gas used in kWh.
- Changed cloud connectivity reporting. E-110 now appears when the Dormouse cloud cannot be reached; previously, the Wi-Fi symbol flashed.

The thermostat continues to run schedules when it cannot reach the cloud. Changes made in the app wait until the connection returns. The gas estimate depends on boiler size, which is entered at Settings > Home > Boiler size.

## Release 3.3 - 2025-08-11

- Increased the household sharing limit from five members to eight, in addition to the home owner.
- Changed invitations to expire after 7 days.

Only the owner can invite or remove members. Members can change the temperature, schedules and Away mode.

## Release 3.4 - 2025-10-06

- Added support for the Dormouse Radiator Valve.
- Changed the firmware update installation window from 01:00-05:00 to 02:00-04:00 local time.

A home can have up to four thermostats. Each thermostat controls its own zone; up to ten Radiator Valves can join a zone, with each valve heating its radiator to its own temperature. Valves communicate with their zone's thermostat over a low-power 868 MHz radio link. Only the thermostat uses Wi-Fi.

## Release 3.5 - 2025-12-01

- Added an automatic retry the night after a firmware update fails. The display shows E-510; the thermostat keeps its current firmware and tries again the next night.
- Changed the low backup-battery alert timing. E-401 now appears a month before the backup batteries run out.

E-401 means the two AA backup batteries need replacing within a month. They maintain the clock and schedules during a power cut for up to 48 hours; the thermostat cannot switch the heating on while mains power is off.

## Release 4.0 - 2026-03-09

- Added Warm Wake.
- Added display symbols, including the sunrise symbol for Warm Wake.
- Added support for the Dormouse Room Sensor, which measures temperature and humidity.

A Room Sensor joins a zone and communicates with that zone's thermostat over a low-power 868 MHz radio link. Up to three Room Sensors can join a zone. The thermostat remains the only device in the zone that uses Wi-Fi.

## Release 4.1 - 2026-08-17

- Made the boost temperature adjustable at Settings > Heating > Boost temperature. The default is 21 degrees; previously, it was fixed at 21 degrees.
- Changed password reset link validity from 24 hours to 30 minutes. Each link can be used once. If it expires, request a new one from the sign-in screen.

A boost heats at the configured boost temperature for one hour. Pressing the boost button again cancels it.

## Update behaviour and support notes

Firmware updates install automatically between 02:00 and 04:00 local time and cannot be postponed. During installation, the display shows UPDATING and the thermostat restarts. Installation takes about two minutes, and heating pauses until it finishes. If an update fails, the thermostat shows E-510, keeps its current firmware and retries the next night.

For E-510, no action is required. For E-110, check that the router is connected to the internet; schedules continue to run while the cloud is unreachable, and app changes wait until reconnection. For account or product support, use Help > Contact support in the app.
