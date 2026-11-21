---
title: Room Sensor Zone Measurement QA Report
product: room sensor
type: internal
audience: internal
firmware: 4.1
updated: 2025-04-14
---

# Room Sensor Zone Measurement QA Report

## Scope

This report covers verification that a Dormouse Room Sensor joins a zone and supplies temperature and humidity measurements for that zone.

The Room Sensor measures temperature and humidity. It joins a zone that is controlled by a Dormouse Thermostat. Each zone can contain up to three Room Sensors. Sensors communicate with their zone's thermostat over a low-power 868 MHz radio link; only the thermostat uses Wi-Fi.

This report is for internal engineering and quality assurance use. It records the expected product behaviour and checks needed to verify device setup, zone association and measurement availability. It does not define measurement accuracy or reporting intervals for the Room Sensor.

## Product and system context

A home can contain up to four Dormouse Thermostats. Each thermostat controls its own zone and schedule. A Room Sensor joins one zone to measure temperature and humidity in another room in that zone.

The thermostat and Room Sensor have distinct roles:

| Device | Role |
|---|---|
| Dormouse Thermostat | Controls its zone and connects to Wi-Fi. |
| Dormouse Room Sensor | Measures temperature and humidity and communicates with its zone's thermostat over 868 MHz radio. |

The Room Sensor uses one CR2032 coin cell, which lasts about a year. The sensor does not use Wi-Fi to communicate. Tests of sensor-to-zone measurement delivery should therefore verify the radio link to the zone's thermostat, rather than expecting the sensor to join the household Wi-Fi network.

## Firmware and test baseline

Use a Dormouse Thermostat running firmware 4.1 as the baseline for this report. The thermostat's firmware version is available from the thermostat menu under Menu > About.

Firmware 4.0 introduced support for the Dormouse Room Sensor. Firmware 4.1 is the current firmware baseline specified for the user guide.

Before testing, record the thermostat firmware, the thermostat's zone identity, the Room Sensor identity, and the test date. Confirm that the sensor is intended to join the selected zone and that the zone is controlled by the thermostat under test. Do not treat a sensor's presence elsewhere in the home as evidence that it is associated with the correct zone.

## Test setup

Prepare a working Dormouse home with at least one thermostat and one Room Sensor. For zone-association coverage across multiple zones, use a home with more than one thermostat; each thermostat controls its own zone.

Check the following before starting:

1. The thermostat is powered and running firmware 4.1.
2. The intended zone is identifiable in the app or web dashboard.
3. The Room Sensor has its CR2032 battery installed and is available for setup.
4. The app or web dashboard is signed in to the relevant Dormouse account.
5. The test record identifies the sensor and the target zone.

A zone can have up to three Room Sensors. Include boundary coverage for the supported limit where the test environment allows it. Do not infer that the sensor has joined a zone merely because it is powered or physically near a thermostat.

## Join and zone-association checks

Use Settings > Home > Add a device to add the Room Sensor. Verify that setup completes and that the device is associated with the intended zone.

Check the resulting configuration in the app or web dashboard. Confirm that:

- the Room Sensor appears as a device in the home;
- its association is with the intended zone, not another thermostat's zone;
- the zone remains associated with its controlling thermostat; and
- the zone does not exceed three Room Sensors.

Repeat the association check when the home contains multiple thermostats. A successful device addition alone is not a pass: the test passes only when the sensor is shown in the intended zone and measurement data is attributed to that zone.

Record any mismatch between the selected zone during setup and the resulting zone association. Do not silently correct the configuration before recording the observed result.

## Measurement verification

Verify that the Room Sensor supplies both temperature and humidity measurements for its associated zone. Check the zone's data in the app or web dashboard and record whether both measurement types are available and attributed to the expected zone.

Where practical, use a controlled change in the sensor's surroundings to check that the displayed readings correspond to the Room Sensor rather than a different room or device. Record the conditions and observations. This report does not specify a numeric accuracy tolerance, an update cadence, or a required delay before readings appear; do not create pass thresholds for those items from this report.

Run the check with one sensor in a zone, then repeat with more than one sensor where supported. Confirm that the zone's sensor count remains within the limit of three and that the tested sensor's readings are not attributed to a different zone.

A pass requires evidence that both temperature and humidity are available for the intended zone. If either measurement is absent, stale, or associated with the wrong zone, record the exact observation and the test configuration.

## Communications and fault isolation

Room Sensors use a low-power 868 MHz radio link to communicate with their zone's thermostat. Wi-Fi connection status applies to the thermostat, not the Room Sensor.

For a missing measurement, first confirm the sensor's zone association, the selected thermostat and the sensor count for that zone. Then check whether the thermostat is operating and whether the measurement is being viewed in the correct zone in the app or web dashboard.

Do not diagnose a Room Sensor by asking it to join Wi-Fi. The thermostat is the device that uses Wi-Fi. If the thermostat cannot reach the Dormouse cloud, its E-110 behaviour and schedule operation are covered by the thermostat guide; that code is not, by itself, proof of a Room Sensor radio fault.

If measurements remain unavailable after configuration and zone checks, preserve the observed state and escalate through the internal support process. The customer-facing contact route is Help > Contact support.

## Regression and release coverage

Room Sensor support was introduced in firmware 4.0. Include a regression check on firmware 4.1 to verify that the sensor continues to join a zone and provide temperature and humidity measurements.

For each relevant release candidate, run at least one end-to-end check that covers device addition, correct zone association and visibility of both measurement types. Include a multi-zone check where the home has multiple thermostats, and a capacity check for the maximum of three Room Sensors in one zone when available.

Every firmware release is tested against the manual test-script library before rollout. Firmware rollout is staged to 1%, then 10%, then every thermostat over a week. QA records should identify the firmware build and the stage at which any issue was observed.

## Results and issue recording

For each run, record the firmware version, number of thermostats and zones, sensor count in the target zone, setup outcome, zone association, and whether temperature and humidity were available. Include reproduction steps and the observed app or web dashboard state for failures.

Classify outcomes clearly:

- **Pass:** Sensor is associated with the intended zone and supplies both temperature and humidity measurements for that zone.
- **Fail:** Association is wrong, either measurement is unavailable, or data is attributed to another zone.
- **Blocked:** The test cannot be completed because its setup or required device configuration is unavailable.

Do not assign an accuracy, latency or battery-life failure based on thresholds not specified here. The Room Sensor battery life is about a year; this is product context, not a per-test pass threshold. Preserve enough detail for engineering to reproduce the issue without changing the original configuration.
