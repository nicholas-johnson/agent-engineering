---
title: See which devices connect to Wi-Fi
product: all
type: support
audience: customer
firmware: 4.1
updated: 2026-10-06
---

# See which devices connect to Wi-Fi

## Which devices use Wi-Fi

Only the Dormouse Thermostat connects to your home Wi-Fi network. It uses Wi-Fi to connect to your Dormouse account and communicate with the app and web dashboard.

Dormouse Radiator Valves and Dormouse Room Sensors do not connect to Wi-Fi. They communicate with the thermostat assigned to their zone over a low-power 868 MHz radio link.

## How devices communicate

Each Dormouse Thermostat controls its own zone. A valve or sensor added to a zone communicates with that zone's thermostat:

| Device | How it communicates |
|---|---|
| Dormouse Thermostat | Connects to your 2.4 GHz Wi-Fi network |
| Dormouse Radiator Valve | Uses a low-power 868 MHz radio link to its zone's thermostat |
| Dormouse Room Sensor | Uses a low-power 868 MHz radio link to its zone's thermostat |

The thermostat is the only device in this group that needs Wi-Fi access. Valves and sensors rely on their zone's thermostat for communication.

## What to check if a valve or sensor is not connecting

If a valve or sensor is not communicating, check that it has been added to the correct zone. In the app or web dashboard, go to Settings > Home > Add a device to add a device or check your home's devices.

Checking your Wi-Fi network is relevant to the thermostat, not to the valve or sensor's radio link. The thermostat requires a 2.4 GHz Wi-Fi network; it cannot join a 5 GHz network.

## Adding a device to a zone

To add a thermostat, Dormouse Radiator Valve or Dormouse Room Sensor, go to Settings > Home > Add a device in the app or web dashboard. A home can have up to four thermostats. Each thermostat controls its own zone, and each zone has its own schedule.
