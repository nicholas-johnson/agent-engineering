---
title: Room Sensor Radio-Link Commissioning
product: room sensor
type: installation
audience: customer
firmware: 4.1
updated: 2026-06-17
---

# Room Sensor Radio-Link Commissioning

## Purpose and scope

This guide covers joining a Dormouse Room Sensor to a zone controlled by a Dormouse Thermostat, then checking that the sensor is communicating with that thermostat over the low-power 868 MHz radio link.

A Room Sensor measures temperature and humidity in another room in the zone. It does not connect to Wi-Fi: only the thermostat uses Wi-Fi. The sensor communicates with its zone thermostat over the radio link.

This guide covers sensor commissioning and basic checks. It does not provide wiring instructions. The thermostat must be wired to the boiler by a qualified installer.

## Equipment and system limits

Before commissioning, confirm that the home has a Dormouse Thermostat controlling the zone where the sensor will be used. A home can have up to four thermostats, each controlling its own zone and schedule. A sensor must join the thermostat for the zone where it is to measure temperature.

Each zone supports up to three Dormouse Room Sensors. A sensor measures temperature and humidity. Its power source is one CR2032 coin cell, which lasts about a year.

Valves and sensors communicate with their zone thermostat over a low-power 868 MHz radio link. Do not use the thermostat's Wi-Fi connection as a test of sensor communication: the sensor itself does not use Wi-Fi.

## Before commissioning

Check that the thermostat is powered and operating, and identify the thermostat that controls the intended zone. If the home has more than one thermostat, use the correct zone thermostat for the room where the sensor will be installed.

Have access to the Dormouse app or web dashboard. Most settings are available in either. The thermostat's menu can also be used for some functions, but adding a device is done through the app or web dashboard:

**Settings > Home > Add a device**

Check that the sensor has its CR2032 battery. If the thermostat displays an error code, consult the thermostat's error-code guidance before proceeding. In particular, E-217 means the thermostat's temperature sensor is disconnected; the thermostat turns the heating off to be safe, and Dormouse support should be contacted to arrange a replacement.

## Adding the sensor to its zone

1. Open the Dormouse app or web dashboard.
2. Go to **Settings > Home > Add a device**.
3. Follow the on-screen instructions to add the Dormouse Room Sensor.
4. Assign the sensor to the thermostat controlling the intended zone, following the device-setup prompts.
5. Confirm that the setup process reports completion.

Do not add the sensor to a different zone's thermostat simply because that thermostat is easier to reach. Each thermostat controls its own zone, and the sensor must be associated with the thermostat for the zone it is intended to measure.

Once added, the sensor measures temperature and humidity in another room of that zone. The zone can have up to three Room Sensors. If the limit has already been reached, another sensor cannot be added to that zone without first resolving the device allocation.

## Checking radio communication

After setup, check the sensor in the app or web dashboard and confirm that its temperature and humidity readings are available. The sensor's readings should be present for the zone to which it was added.

If the readings are missing or do not appear to update:

1. Confirm that the sensor is listed under the intended zone thermostat.
2. Check that the sensor's CR2032 battery is present and correctly fitted.
3. Allow the app or web dashboard to refresh, then check the readings again.
4. Check the thermostat display for an error code and consult the error-code table in the user guide.

The thermostat uses Wi-Fi to communicate with the Dormouse cloud, while the sensor uses the 868 MHz radio link to communicate with its thermostat. A thermostat that is offline from Wi-Fi may affect access to current information in the app or web dashboard, but Wi-Fi status alone does not establish whether the sensor's radio link is working.

## Interpreting readings and faults

The Room Sensor provides temperature and humidity readings. If humidity readings disappear while heating continues to work, check the thermostat display for E-221. This code indicates a humidity sensor fault. Contact Dormouse support if the code remains for more than a day.

E-217 is different: it indicates that the thermostat's temperature sensor is disconnected, not that a Room Sensor has lost its radio link. The thermostat turns heating off to be safe. Contact Dormouse support to arrange a replacement.

If the thermostat shows E-110, it cannot reach the Dormouse cloud. The thermostat keeps running its schedules, and changes made in the app wait until it reconnects. This code concerns the cloud connection; it is not identified as a Room Sensor radio-link error.

## Completion checks

Commissioning is complete when all of the following are true:

- The Room Sensor is listed under the thermostat for the intended zone.
- The app or web dashboard displays the sensor's temperature and humidity readings.
- The thermostat does not show an error that needs attention.

Record which thermostat and zone the sensor was assigned to, along with the date of commissioning, in the installation record. This helps identify the correct thermostat if the home has several zones or sensors.

## Support and care

If the sensor cannot be added, or its readings remain unavailable after the checks in this guide, contact Dormouse support in the app under **Help > Contact support**. Include the thermostat's displayed error code, if there is one, and identify the affected zone.

The Room Sensor's CR2032 coin cell lasts about a year. Check and replace the battery as needed. The thermostat backup-battery instructions do not apply to the Room Sensor: those instructions concern the thermostat's two AA batteries.
