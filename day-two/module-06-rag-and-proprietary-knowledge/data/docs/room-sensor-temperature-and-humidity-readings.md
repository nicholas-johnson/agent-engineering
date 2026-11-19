---
title: Room Sensor Temperature and Humidity Readings
product: room sensor
type: installation
audience: customer
firmware: 4.1
updated: 2026-08-18
---

# Room Sensor Temperature and Humidity Readings

## Purpose

The Dormouse Room Sensor measures temperature and humidity in a room. When it joins a zone, its readings become available in the Dormouse app for that zone.

A zone is controlled by a Dormouse Thermostat and can also include Dormouse Radiator Valves. A Room Sensor adds measurements from another room in the same zone. It does not connect directly to Wi-Fi: the sensor communicates with its zone's thermostat over a low-power 868 MHz radio link. The thermostat uses Wi-Fi to connect to the app and web dashboard.

## What the sensor measures

The sensor measures the temperature and humidity around it. Its readings represent the room where the sensor is placed; they are not readings from the thermostat or from every room in the zone.

The Room Sensor is a measurement device. The thermostat controls the zone's heating, using its own schedule and settings. Adding a sensor does not create a separate zone or schedule.

## Before installation

Confirm that the home has a Dormouse Thermostat controlling the zone where the sensor will be used. A Room Sensor must join a zone; it does not operate as a standalone Wi-Fi device.

Each zone can have up to three Dormouse Room Sensors. A home can have up to four Dormouse Thermostats, with each thermostat controlling its own zone and schedule. Check the intended zone and the number of sensors already assigned before adding another.

The Room Sensor is powered by one CR2032 coin cell. The cell lasts about a year. Keep the sensor and battery away from children and follow the product's battery handling instructions.

## Adding the sensor to a zone

Add the Room Sensor from the app or web dashboard:

1. Open Settings > Home > Add a device.
2. Follow the on-screen steps to add the Room Sensor.
3. Select the zone in which the sensor is to be used, if prompted.

The sensor communicates with the thermostat for that zone over its low-power 868 MHz radio link. It does not need to be paired with the home's Wi-Fi network. Only the thermostat uses Wi-Fi.

After it has joined the zone, the sensor's temperature and humidity readings are available in the app for that zone. The web dashboard can also be used for most settings, but the guide specifies readings becoming available in the app.

## Understanding the readings

Temperature and humidity readings come from the sensor's location. When interpreting them, consider whether that location is representative of the room you want to monitor. A sensor in one room does not measure conditions in other rooms, even if they are part of the same zone.

The thermostat continues to control heating for the zone. The sensor provides readings; it does not have its own heating schedule or control a separate zone. Each Dormouse Radiator Valve in a zone heats its radiator to its own temperature.

## Communication and availability

The Room Sensor sends readings to its zone's thermostat over a low-power 868 MHz radio link. The thermostat is the device that connects to Wi-Fi and the Dormouse service. The sensor itself does not join the Wi-Fi network.

When the sensor is connected to the zone, its temperature and humidity readings are available in the app. If readings are not available, check that the sensor has been added to the intended zone and that it is within the setup for that zone. The supplied guide does not specify a radio range, a reading update interval, or a sensor-specific error code; do not assume a particular range or refresh time.

## Battery

The sensor uses one CR2032 coin cell, which lasts about a year. Battery life varies with use and conditions. Replace the cell when needed, following the product's battery handling instructions.

Do not confuse the Room Sensor battery with the thermostat's two AA backup batteries. The thermostat's backup batteries keep its clock and schedules during a power cut; they do not power the Room Sensor.

## System limits

| Item | Limit or detail |
|---|---|
| Room Sensors per zone | Up to three |
| Sensor measurements | Temperature and humidity |
| Sensor power | One CR2032 coin cell |
| Approximate battery life | About one year |
| Sensor-to-thermostat connection | Low-power 868 MHz radio link |
| Wi-Fi connection | Used by the thermostat, not the sensor |

A home can have up to four Dormouse Thermostats. Each thermostat controls its own zone, with its own schedule. A Room Sensor joins one of those zones and adds readings from another room.

## Getting help

For help with a Dormouse product, open the app and go to Help > Contact support. When reporting an issue, identify the zone the sensor is intended to join and describe whether the sensor was added successfully and whether its readings are available in the app.
