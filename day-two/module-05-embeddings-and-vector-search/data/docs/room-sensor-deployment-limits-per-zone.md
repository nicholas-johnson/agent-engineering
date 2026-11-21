---
title: Room Sensor Deployment Limits per Zone
product: room sensor
type: installation
audience: customer
firmware: 4.1
updated: 2026-05-19
---

# Room Sensor Deployment Limits per Zone

## Purpose

A Dormouse Room Sensor measures temperature and humidity in another room within a thermostat's zone. You can add up to three Dormouse Room Sensors to each zone.

Use this guide to plan sensor deployment when a zone needs temperature measurements from more than one room. A sensor measures the conditions where it is placed; it does not extend the zone or create a separate heating schedule. Each zone is controlled by its own Dormouse Thermostat and has its own schedule.

The limit is three Room Sensors per zone. Plan the locations before adding devices so that the available sensors measure the rooms that best represent the zone's heating needs.

## System layout

A home can have up to four Dormouse Thermostats. Each thermostat controls its own zone. A Dormouse Room Sensor can join a zone and measure temperature and humidity in another room in that zone.

Sensors communicate with the thermostat for their zone over a low-power 868 MHz radio link. Only the thermostat uses Wi-Fi. A sensor does not join Wi-Fi directly.

Dormouse Radiator Valves can also join a zone, up to ten per zone. Each valve heats its own radiator to its own temperature. Valves do not increase the Room Sensor limit: a zone can have up to ten valves and up to three Room Sensors.

| Device | Maximum per zone | Role |
|---|---:|---|
| Dormouse Room Sensor | 3 | Measures temperature and humidity in another room |
| Dormouse Radiator Valve | 10 | Controls heating at its own radiator |
| Dormouse Thermostat | 1 per zone | Controls the zone |

## Plan the sensor locations

Choose locations based on the rooms whose temperatures you need to measure. A sensor measures conditions at its own location, so place it in the room you want to monitor rather than assuming it represents the whole zone.

If you have several candidate rooms but fewer than three sensors, prioritise the rooms that are most important to include in your temperature measurements. Consider which rooms are served by the zone and where a separate reading will be useful when reviewing conditions.

Keep the zone boundary in mind. A sensor must be added to the zone it is intended to measure. Each thermostat controls its own zone and schedule; a sensor in one zone does not become a sensor for another zone.

## Understand the three-sensor limit

The limit applies separately to each zone: up to three Dormouse Room Sensors can join a zone. It is not a limit of three sensors for the whole home. For example, a home with two zones can have up to three sensors in each, provided each sensor is added to the intended zone.

If a zone already has three Room Sensors, you cannot add a fourth to that zone. Check the devices already assigned to the zone before planning an installation. If you need measurements in a different room, review whether one of the existing sensors should instead be placed there.

Adding another thermostat creates another zone, with its own schedule and device assignments. Do not treat a second thermostat as a way to make one zone accept more than three sensors: it controls a separate zone.

## Add a sensor to a zone

To add a Dormouse Room Sensor, use the device setup in the app or web dashboard:

1. Open Settings > Home > Add a device.
2. Follow the setup steps and select the zone the sensor is intended to join.
3. Confirm that the sensor has been added to the correct zone.
4. Repeat for any additional sensors, checking the zone's count each time.

A Room Sensor uses one CR2032 coin cell, which lasts about a year. The sensor's battery type and expected life differ from the two AA batteries used by a Dormouse Radiator Valve. Do not count a valve as a Room Sensor when checking the three-sensor limit.

## Radio and connectivity

Room Sensors use a low-power 868 MHz radio link to communicate with their zone's thermostat. The thermostat is the device that connects to Wi-Fi. A sensor does not need its own Wi-Fi connection.

When planning placement, keep the sensor associated with the thermostat for the zone it serves. The sensor measures its local temperature and humidity, and communicates those readings to that zone's thermostat over the radio link.

The product information specifies the radio link but does not set a maximum distance or provide a placement rule based on building materials. Do not assume that a particular range is guaranteed from the information in this guide.

## Check the deployment

After setup, review the home's device assignments and confirm that each sensor is in the intended zone. Check that no zone has more than three Room Sensors and that each sensor is located in the room whose conditions you want to measure.

If you are planning several zones, make a simple device list before installation:

| Zone | Thermostat | Planned Room Sensors | Sensor count |
|---|---|---|---:|
| Zone 1 | Thermostat 1 | List the rooms to measure | Up to 3 |
| Zone 2 | Thermostat 2 | List the rooms to measure | Up to 3 |

Use a separate row for each zone. This makes it easier to spot an over-limit plan and avoids assigning a sensor to the wrong thermostat.

## Product information

The Dormouse Room Sensor measures temperature and humidity. It is powered by one CR2032 coin cell, which lasts about a year, and supports up to three sensors per zone.

For adding or managing devices, go to Settings > Home > Add a device. If you need help with installation or device setup, contact support in the app under Help > Contact support.
