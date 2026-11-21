---
title: Understand how the Room Sensor communicates
product: room sensor
type: support
audience: customer
firmware: 4.1
updated: 2025-06-02
---

# Understand how the Room Sensor communicates

## The communication link

The Dormouse Room Sensor communicates with the thermostat for its zone using a low-power 868 MHz radio link. It does not use Wi-Fi.

Only the thermostat connects to Wi-Fi. The sensor sends its readings to its zone's thermostat over the radio link; it does not connect directly to your Wi-Fi network or account.

## What this means for setup

Add the Room Sensor to a zone through the thermostat system. In the app or web dashboard, go to Settings > Home > Add a device.

A home can have up to four Dormouse Thermostats. Each thermostat controls its own zone, and a Room Sensor joins one zone to measure temperature and humidity in another room in that zone. A Room Sensor communicates with that zone's thermostat, not with a thermostat in a different zone.

## What the sensor measures

The Room Sensor measures temperature and humidity. Its readings are used by the zone it has joined. The sensor is powered by one CR2032 coin cell, which lasts about a year.

## Wi-Fi and the thermostat

Because the Room Sensor uses radio to communicate with its zone's thermostat, it does not need its own Wi-Fi connection. The thermostat is the device that uses Wi-Fi to connect to your home network and Dormouse services.

If the thermostat is not connected to Wi-Fi, the Room Sensor still communicates with its zone's thermostat over the radio link. For thermostat Wi-Fi or cloud error codes, check the thermostat's display and the Error codes section of the user guide.
