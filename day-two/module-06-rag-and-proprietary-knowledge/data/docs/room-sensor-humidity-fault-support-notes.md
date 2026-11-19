---
title: Room Sensor Humidity Fault Support Notes
product: room sensor
type: internal
audience: internal
firmware: 4.1
updated: 2026-09-06
---

# Room Sensor Humidity Fault Support Notes

## Purpose and scope

This internal support note covers the user-visible effects of error code E-221, a humidity sensor fault, and when to contact Dormouse support.

The Dormouse Room Sensor measures temperature and humidity in another room in a zone. It communicates with that zone's thermostat over a low-power 868 MHz radio link. The thermostat display and the app report the E-221 code.

## User-visible effects

When E-221 appears:

- Humidity readings disappear from the app.
- The heating continues to work.

The code indicates a humidity sensor fault. Do not tell users that heating has stopped or that E-221 is the same as a temperature sensor fault. The guide does not specify that E-221 affects temperature readings.

## When to contact support

If E-221 remains displayed for more than a day, advise the user to contact Dormouse support. They can do this in the app under Help > Contact support.

If the code has been present for a day or less, explain that the stated contact threshold has not yet been reached. Do not promise that the code will clear or that humidity readings will return by a particular time.

## Support handling

1. Confirm the displayed code is E-221.
2. Explain that humidity readings disappear from the app while the fault is present, but the heating keeps working.
3. Establish whether the code has remained for more than a day.
4. If it has, direct the user to Help > Contact support in the app.
5. If it has not, advise them to contact support if the code stays for more than a day.

Do not apply E-217 guidance to E-221. E-217 is a temperature sensor disconnection; for that error, the thermostat turns the heating off to be safe and the user should contact support to arrange a replacement.

## Product context

A Dormouse Room Sensor measures temperature and humidity and uses one CR2032 coin cell, which lasts about a year. Up to three Room Sensors can join a zone. Room Sensors communicate with the zone's thermostat over a low-power 868 MHz radio link; only the thermostat uses Wi-Fi.

These product details may help explain the sensor's role, but they do not establish a user troubleshooting procedure for E-221. Do not recommend battery replacement, re-pairing, or other corrective action for this code unless separate approved guidance is available.

## Known issue boundaries

The user guide identifies E-221 as a humidity sensor fault and specifies its visible effects and contact threshold. It does not provide a cause, a recovery procedure, or a diagnostic test for the fault.

Keep explanations within those limits. In particular, do not claim that:

- The Room Sensor must be replaced.
- The user can resolve the fault by changing batteries or reconnecting the sensor.
- Temperature readings are affected.
- The heating will stop if the fault continues.

## Internal escalation context

Dormouse support has three levels:

1. Level 1: app chat agents.
2. Level 2: product specialists.
3. Level 3: engineering.

Use the normal support process to route a case if further investigation is needed. The E-221 guidance does not define a specific escalation level or additional diagnostic steps.
