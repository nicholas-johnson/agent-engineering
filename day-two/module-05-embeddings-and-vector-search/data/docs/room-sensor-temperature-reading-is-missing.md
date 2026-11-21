---
title: Room Sensor Temperature Reading Is Missing
product: room sensor
type: troubleshooting
audience: customer
firmware: 4.1
updated: 2025-04-01
---

# Room Sensor Temperature Reading Is Missing

Use this guide to check whether your Dormouse Room Sensor has joined the intended zone and whether its readings are available in the Dormouse app.

## How the Room Sensor works

A Dormouse Room Sensor measures temperature and humidity in another room in its zone. It communicates with that zone's thermostat over a low-power 868 MHz radio link. The thermostat uses Wi-Fi to connect to the app; the Room Sensor does not use Wi-Fi.

A home can have up to four zones, and each zone can have up to three Room Sensors. Check that you are looking at the zone the sensor is meant to measure.

## Check the sensor and zone

In the app, open **Settings > Home** and review the devices in your home. Confirm that the Room Sensor is listed and that it is associated with the intended zone.

If the sensor is missing from the home, or is listed under a different zone, it may not have joined the zone you expect. To add a sensor to a zone, go to **Settings > Home > Add a device** and follow the app's steps. Select the intended zone when prompted.

A Room Sensor can join only one zone at a time. If the intended zone already has three Room Sensors, it has reached its limit.

## Check the app reading

Open the zone's view in the app and look for the Room Sensor's temperature reading. Check that you have selected the zone to which the sensor belongs, rather than another zone in the home.

The sensor measures both temperature and humidity. If the temperature is missing, check whether the humidity reading is also missing. This can help establish whether the app is showing readings from that sensor, but it does not by itself identify the cause.

## Check the thermostat connection

The Room Sensor communicates with its zone's thermostat over the 868 MHz radio link. Confirm that the thermostat assigned to the intended zone is present in the app and that you are checking the sensor reading under that zone.

Only the thermostat connects to Wi-Fi. If the thermostat is not connected to Wi-Fi, its display shows a Wi-Fi symbol with a cross. A thermostat that cannot reach the Dormouse cloud may show E-110. In that case, it continues running its schedules, but changes made in the app wait until it reconnects.

## Check for an error

If the thermostat displays an error code, the app shows the same code and can notify you about it. Check the code in the thermostat's error-code list. For example, E-217 means the thermostat's temperature sensor is disconnected; the thermostat turns the heating off to be safe. Contact Dormouse support to arrange a replacement.

A missing Room Sensor reading does not, by itself, identify an error code. Do not treat a thermostat error as proof that the Room Sensor has failed.

## Check the sensor battery

The Room Sensor uses one CR2032 coin cell, which lasts about a year. If the reading is still missing after you have checked the zone and app view, check the sensor's battery and replace it if needed. Take care to use a CR2032 coin cell.

After checking the battery, return to the intended zone in the app and see whether the sensor reading is available.

## When the reading is still missing

If the sensor is listed in the intended zone, the thermostat is connected, and the reading is still unavailable, contact Dormouse support in the app under **Help > Contact support**. Include the zone you checked and whether the temperature, humidity, or both readings are missing.
