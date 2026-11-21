---
title: Room Sensor Power and Measurement Notes
product: room sensor
type: internal
audience: internal
firmware: 4.1
updated: 2026-02-17
---

# Room Sensor Power and Measurement Notes

## Purpose and scope

These notes cover the Dormouse Room Sensor's measurements, power source, expected battery life and zone limit. They are intended for internal engineering, support and quality work.

The Room Sensor measures temperature and humidity in another room of a zone. It joins a zone controlled by a Dormouse Thermostat; it does not operate as a separate heating controller. The thermostat controls the zone, while the sensor provides readings from its location.

## Product and zone limits

A home can have up to four Dormouse Thermostats. Each thermostat controls its own zone, with its own schedule. A Dormouse Room Sensor can join a zone to measure conditions in another room of that zone.

The limit is **up to three Room Sensors per zone**. Treat this as a per-zone limit, not a per-home limit. For example, a home with multiple thermostat-controlled zones can have sensors assigned to those zones, subject to the limit in each one.

To add a sensor, use Settings > Home > Add a device. Ensure it is added to the intended zone.

## Measurements

The Room Sensor measures **temperature and humidity**. Its role is to measure conditions in another room of the zone it has joined.

The product information specifies the measurement types but does not specify a temperature or humidity accuracy, measurement range, sampling interval, or reporting interval. Do not provide numerical claims for these characteristics unless confirmed by an approved technical specification.

The Room Sensor's measurements are distinct from the thermostat's room-temperature display. The thermostat display shows room temperature and target temperature; use the app to view humidity readings. If the humidity sensor develops a fault, the thermostat can show E-221. Heating continues to work, but humidity readings disappear from the app. If E-221 remains for more than a day, contact Dormouse support through Help > Contact support in the app.

## Power source and expected battery life

The Room Sensor is powered by **one CR2032 coin cell**. Expected battery life is **about one year**.

This is an expected duration, not a guaranteed service interval. The available product information does not specify usage conditions or a low-battery warning threshold for the Room Sensor. Do not apply the thermostat's backup-battery instructions or E-401 guidance to the sensor: those instructions concern the thermostat's two AA backup batteries.

When supporting a battery-life concern, identify the device as a Room Sensor and confirm that the reported battery is its CR2032 cell. Avoid promising a precise replacement date based solely on the expected one-year life.

## Zone communication

Room Sensors communicate with the thermostat assigned to their zone over a **low-power 868 MHz radio link**. The Room Sensor does not use Wi-Fi. Only the thermostat uses Wi-Fi.

When checking a reported connection or measurement issue, first confirm that the sensor belongs to the intended zone. Do not direct users to pair the sensor to a Wi-Fi network. The product information does not specify radio range, link-quality indicators, or procedures for diagnosing radio interference; do not invent these details in support guidance.

## Support handling

Use these checks to keep support advice within the documented product behavior:

1. Confirm that the device is a Dormouse Room Sensor and identify its assigned zone.
2. Check that the zone has no more than three Room Sensors.
3. Confirm that the reported reading concerns temperature or humidity measured by the sensor.
4. If the issue is a missing humidity reading and E-221 is shown, explain that heating continues while humidity readings are unavailable. If the code stays for more than a day, contact support in the app under Help > Contact support.
5. For a battery concern, explain that the sensor uses one CR2032 cell and has an expected battery life of about one year.

Do not describe thermostat error codes E-401 or E-402 as Room Sensor battery codes. Those codes refer to the thermostat's backup batteries and mains power.

## Quality and documentation boundaries

Keep internal and user-facing descriptions consistent: the sensor measures temperature and humidity, uses one CR2032 cell, has an expected battery life of about one year, and is limited to three sensors per zone. It communicates with its zone's thermostat over low-power 868 MHz radio; Wi-Fi applies only to the thermostat.

The currently available product information does not define sensor measurement accuracy, operating-temperature range, battery replacement steps, radio range, or sampling behavior. Do not infer these specifications from the thermostat or publish unverified values.
