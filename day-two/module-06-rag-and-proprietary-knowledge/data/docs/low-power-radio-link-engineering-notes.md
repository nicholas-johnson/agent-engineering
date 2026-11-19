---
title: Low-Power Radio Link Engineering Notes
product: all
type: internal
audience: internal
firmware: 4.1
updated: 2025-10-29
---

# Low-Power Radio Link Engineering Notes

## Scope

These internal engineering notes describe the Dormouse Radiator Valve and Dormouse Room Sensor radio connection to a zone's Dormouse Thermostat. They distinguish that local connection from the thermostat's Wi-Fi connection and record the supported device limits and power details.

This document does not specify radio protocols, pairing procedures, signal ranges, channel plans, security mechanisms, retry behaviour or diagnostics. Those details are not defined in the available product information and must not be inferred from the radio frequency alone.

## System overview

A Dormouse Thermostat controls its own zone. A Dormouse Radiator Valve or Dormouse Room Sensor can join a zone and communicate with that zone's thermostat over a low-power 868 MHz radio link.

Only the thermostat uses Wi-Fi. Valves and sensors do not use Wi-Fi to communicate with the thermostat. The thermostat's Wi-Fi connection is used to connect it to the network and Dormouse services; it is separate from the local 868 MHz device link.

| Device | Connection to zone thermostat | Uses Wi-Fi |
|---|---|---|
| Dormouse Thermostat | Connects to the network over Wi-Fi | Yes |
| Dormouse Radiator Valve | Low-power 868 MHz radio link | No |
| Dormouse Room Sensor | Low-power 868 MHz radio link | No |

## Zone topology and device limits

A home can have up to four Dormouse Thermostats. Each thermostat controls its own zone, with its own schedule. Valves and sensors join a zone; they do not replace the thermostat that controls it.

A zone supports up to ten Dormouse Radiator Valves and up to three Dormouse Room Sensors. A Room Sensor measures temperature and humidity in another room of the zone. Each Radiator Valve heats its own radiator to its own temperature.

The thermostat's user guide describes adding a thermostat, sensor or valve through Settings > Home > Add a device. The zone assignment matters: the radio link is between an accessory and its zone's thermostat.

## Dormouse Radiator Valve

The Dormouse Radiator Valve runs on two AA batteries, which last about two years. It fits M30 x 1.5 valve bodies. Adapters for other common valve types are included in the box.

The valve communicates with its zone thermostat over the low-power 868 MHz radio link. It does not use Wi-Fi. A zone can contain up to ten valves.

Do not interpret the valve's battery life as a service interval guaranteed under every usage condition; the available product information states an approximate life of about two years. No radio range, battery reporting threshold, or battery replacement procedure is specified here.

## Dormouse Room Sensor

The Dormouse Room Sensor measures temperature and humidity. It runs on one CR2032 coin cell, which lasts about a year. Up to three sensors can join a zone.

The sensor communicates with its zone thermostat over the low-power 868 MHz radio link. It does not use Wi-Fi. Sensor readings are associated with the zone the sensor has joined.

The thermostat error-code guidance distinguishes a disconnected temperature sensor from a humidity sensor fault. For a temperature sensor disconnection, the thermostat turns the heating off to be safe and the user should contact Dormouse support. For a humidity sensor fault, heating keeps working, but humidity readings disappear from the app; the user should contact support if the code remains for more than a day.

## Thermostat connectivity boundary

The thermostat is the only device in this accessory system that uses Wi-Fi. Its Wi-Fi connection is to a 2.4 GHz network; it cannot join a 5 GHz network. The thermostat guide's Wi-Fi errors concern that network connection, not the 868 MHz accessory link.

In particular, E-101 means the Wi-Fi network was not found, and E-110 means the thermostat cannot reach the Dormouse cloud. E-110 guidance says the thermostat keeps running its schedules while app changes wait until it reconnects. These errors should not be described as proof of a valve or sensor radio-link failure.

The available documentation does not define how an accessory radio-link fault is displayed, what happens to valve control during such a fault, or how link quality is measured. Do not promise specific behaviour without confirmed engineering information.

## Support and troubleshooting boundaries

When investigating a report, first establish which device or connection is involved: thermostat-to-Wi-Fi, or accessory-to-zone-thermostat over 868 MHz. Confirm the accessory type and the zone it is intended to join. Do not ask users to troubleshoot a valve or sensor by changing Wi-Fi network settings.

Use only documented user guidance when advising customers. To add a device, direct them to Settings > Home > Add a device. For a thermostat error code, use the error-code instructions in the user guide. The guide does not provide a customer-facing checklist for 868 MHz radio-link faults.

Support is contacted in the app under Help > Contact support. Escalation levels and internal diagnostic procedures are not specified in this document.

## Engineering and QA limits

The confirmed radio-link facts are limited to its frequency band, low-power description, endpoints and zone relationship: Dormouse Radiator Valves and Dormouse Room Sensors communicate with their zone thermostat over a low-power 868 MHz radio link.

No modulation, transmit power, antenna design, link budget, range, coexistence, interference tolerance, protocol, message timing, encryption, pairing handshake, regulatory test result or recovery strategy is specified here. QA and engineering documents must not present any such value or behaviour as a product fact unless it is verified in an approved technical source.

Keep the connectivity distinction explicit in reviews and support material: accessories use the local 868 MHz link; only thermostats use Wi-Fi.
