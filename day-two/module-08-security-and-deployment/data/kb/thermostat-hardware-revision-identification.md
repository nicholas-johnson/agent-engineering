---
title: Thermostat Hardware Revision Identification
product: thermostat
type: internal
audience: internal
firmware: 4.1
updated: 2026-01-30
---

# Thermostat Hardware Revision Identification

## Purpose and scope

This internal reference explains how to identify Dormouse Thermostat hardware revisions A, B and C from the serial number prefix. Use it when recording a device's hardware revision for support, engineering, quality assurance or firmware work.

This document covers identification only. A serial number beginning with a recognised prefix identifies the thermostat's hardware revision; it does not identify its firmware version.

## Revision and prefix reference

| Hardware revision | Serial number prefix | Revision year |
|---|---|---|
| A | DMA | 2024 |
| B | DMB | 2025 |
| C | DMC | 2026 |

Use the prefix at the start of the serial number. The remaining characters do not change the revision mapping.

## Identification procedure

1. Locate the thermostat's serial number.
2. Read the first three characters.
3. Match those characters against the prefix reference:
   - `DMA` identifies revision A.
   - `DMB` identifies revision B.
   - `DMC` identifies revision C.
4. Record the revision alongside the serial number when documenting the device.

Do not infer the revision from the firmware version. The current firmware is 4.1, and firmware version and hardware revision are separate identifiers.

## Recording and reporting

When entering a device in an internal record, include the serial number and the identified revision. Preserve the prefix exactly as shown; do not replace it with the revision letter alone if the record also needs to identify the device.

For example, a serial number beginning `DMB` should be recorded as hardware revision B. The example prefix is illustrative; it is not a complete serial number.

If a serial number is available but its prefix is not `DMA`, `DMB` or `DMC`, do not assign A, B or C using this mapping. Record the observed prefix and escalate for verification through the appropriate internal process.

## Distinguishing hardware revision from firmware

Hardware revision describes the thermostat hardware. Firmware describes the software currently installed on it.

To check firmware on the thermostat, press the dial to open the menu and choose Menu > About. Do not use that firmware reading to determine the hardware revision: use the serial number prefix.

Keep both values distinct in engineering notes, support records and QA reports. For example, a record may contain hardware revision B and firmware 4.1; these are separate fields, not alternative ways of expressing the same version.

## Product context

The Dormouse Thermostat is powered by mains through its wall plate. Its display is 2.4 inches, round and colour. The thermostat measures 84 mm across and 24 mm deep, and is intended for indoor use between 0 and 40 degrees.

These product details provide general context but do not distinguish revisions A, B and C. Use the serial number prefix for revision identification.

## Related devices

A home can have up to four Dormouse Thermostats, each controlling its own zone. Identify each thermostat separately from its own serial number; do not assume that thermostats in one home have the same hardware revision.

A Dormouse Room Sensor or Dormouse Radiator Valve is not a thermostat hardware revision. Sensors and valves join a zone controlled by a thermostat. Record their device type separately rather than applying the thermostat's DMA, DMB or DMC revision mapping to them.

## Firmware and QA notes

The current thermostat firmware is 4.1. Firmware updates install automatically between 02:00 and 04:00 local time and cannot be postponed. Hardware revision identification does not change these firmware behaviours.

For internal QA records, capture the serial number prefix and firmware version as separate details when both are relevant. The prefix establishes the hardware revision; the firmware version establishes the installed software version. Do not treat a firmware release number as evidence of a particular hardware revision.

## Quick reference

- `DMA` -> hardware revision A (2024)
- `DMB` -> hardware revision B (2025)
- `DMC` -> hardware revision C (2026)
- Read the first three serial number characters.
- Do not infer hardware revision from firmware.
- For an unlisted prefix, record what is shown and seek verification rather than assigning a revision.
