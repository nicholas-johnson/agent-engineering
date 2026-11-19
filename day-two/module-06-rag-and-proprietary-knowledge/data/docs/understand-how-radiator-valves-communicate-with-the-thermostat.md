---
title: Understand how radiator valves communicate with the thermostat
product: radiator valve
type: support
audience: customer
firmware: 4.1
updated: 2026-09-19
---

# Understand how radiator valves communicate with the thermostat

## How the connection works

A Dormouse Radiator Valve communicates with the thermostat for its zone over a low-power 868 MHz radio link. It does not use Wi-Fi.

The thermostat uses Wi-Fi to connect to the Dormouse app and web dashboard. The valve does not connect to either directly: its communication with the system is through the zone's thermostat.

## What a zone means

Each Dormouse Thermostat controls its own zone, with its own schedule. A Dormouse Radiator Valve joins a zone so that the radiator it is fitted to can heat to its own temperature.

A home can have up to four Dormouse Thermostats. Each valve communicates with the thermostat for the zone it has joined, not with a thermostat in another zone.

## Wi-Fi and the radio link

Wi-Fi and the valve's radio link have different roles:

| Connection | What it connects |
|---|---|
| Wi-Fi | The thermostat to your home network |
| Low-power 868 MHz radio link | A valve to the thermostat for its zone |

Because the valve uses the radio link, it does not need to join your Wi-Fi network. The thermostat is the device in the zone that uses Wi-Fi.

## Adding a valve to a zone

To add a Dormouse Radiator Valve, go to Settings > Home > Add a device. The valve must join a zone to communicate with that zone's thermostat.

Up to ten Dormouse Radiator Valves can join one zone. Each valve can then heat its own radiator to its own temperature.

## If the thermostat is not connected to Wi-Fi

The valve-to-thermostat radio link is separate from Wi-Fi. Wi-Fi connects the thermostat to the network; the 868 MHz link connects the valve to its zone's thermostat.

If the thermostat cannot reach the Dormouse cloud, it keeps running its schedules. Changes made in the app wait until the thermostat reconnects. The thermostat shows E-110 when it cannot reach the cloud.

## Related devices

A Dormouse Room Sensor can also join a zone to measure temperature in another room. It communicates with the zone's thermostat over the same low-power 868 MHz radio link. Only the thermostat uses Wi-Fi.

Each zone has its own thermostat, schedule and connected devices. To add a thermostat, sensor or valve, go to Settings > Home > Add a device.

## Getting help

If you need help with a Dormouse device, contact support in the app under Help > Contact support.
