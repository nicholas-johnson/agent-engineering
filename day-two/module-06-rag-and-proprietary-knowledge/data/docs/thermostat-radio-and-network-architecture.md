---
title: Thermostat Radio and Network Architecture
product: thermostat
type: specification
audience: customer
firmware: 4.1
updated: 2026-01-10
---

# Thermostat Radio and Network Architecture

## Scope

This specification describes how the Dormouse Thermostat, Dormouse Radiator Valve and Dormouse Room Sensor connect within a home. It covers the thermostat's Wi-Fi connection and the low-power radio link used by valves and sensors.

Each Dormouse Thermostat controls its own zone. A home can have up to four thermostats, each with its own schedule. A Room Sensor or Radiator Valve joins a zone and communicates with that zone's thermostat.

## Product roles

| Product | Network role |
|---|---|
| Dormouse Thermostat | Connects to the home's Wi-Fi network and controls its own zone. |
| Dormouse Radiator Valve | Communicates with its zone's thermostat over low-power 868 MHz radio. |
| Dormouse Room Sensor | Communicates with its zone's thermostat over low-power 868 MHz radio. |

Only the thermostat uses Wi-Fi. Radiator Valves and Room Sensors do not join the home Wi-Fi network.

## Thermostat Wi-Fi connection

The thermostat connects to a 2.4 GHz Wi-Fi network. It cannot join a 5 GHz network. Pairing connects the thermostat to both the Wi-Fi network and the Dormouse account.

To pair a thermostat:

1. Hold the dial down for 5 seconds, until the display shows PAIR.
2. In the Dormouse app, choose Add thermostat and follow the steps.
3. Keep the phone within 5 metres of the thermostat until the app confirms that pairing is complete.

Pairing must finish within 3 minutes of PAIR appearing. If it does not, the thermostat shows E-104 and pairing must be started again.

If the thermostat cannot reach the Dormouse cloud, it shows E-110. It continues to run its schedules, but changes made in the app wait until the thermostat reconnects.

## Zone radio link

Dormouse Radiator Valves and Room Sensors communicate with their zone's thermostat over a low-power 868 MHz radio link. They do not use Wi-Fi to communicate with the thermostat.

A zone can include up to ten Dormouse Radiator Valves and up to three Dormouse Room Sensors. Each Radiator Valve controls its own radiator temperature. A Room Sensor measures temperature and humidity in another room in the same zone.

To add a thermostat, sensor or valve, go to Settings > Home > Add a device.

## Product data

| Product | Connection | Power and battery information |
|---|---|---|
| Dormouse Thermostat | 2.4 GHz Wi-Fi; low-power 868 MHz radio for zone devices | Powered by mains through its wall plate. Two AA backup batteries keep the clock and schedules during a power cut for up to 48 hours. |
| Dormouse Radiator Valve | Low-power 868 MHz radio to its zone's thermostat | Two AA batteries, which last about two years. Fits M30 x 1.5 valve bodies; adapters for other common valves are included. |
| Dormouse Room Sensor | Low-power 868 MHz radio to its zone's thermostat | One CR2032 coin cell, which lasts about a year. Measures temperature and humidity. |

The thermostat cannot switch the heating on while mains power is off, even when its backup batteries are installed.

## Thermostat specifications

| Property | Specification |
|---|---|
| Dimensions | 84 mm across and 24 mm deep |
| Display | 2.4-inch round colour display |
| Temperature accuracy | 0.3 degrees |
| Operating environment | Indoors, between 0 and 40 degrees |
| Current firmware | 4.1 |

Thermostat hardware revisions are A (2024), B (2025) and C (2026). Serial numbers start with DMA, DMB or DMC, corresponding to revisions A, B or C.

To check the installed firmware version, press the dial to open the menu and choose Menu > About.

## Connectivity and operating behaviour

The thermostat's Wi-Fi connection supports pairing with a Dormouse account and communication with the Dormouse cloud. If the cloud is unreachable, the thermostat keeps running its schedules; app changes wait until the connection is restored.

Zone devices use the thermostat's 868 MHz radio link rather than Wi-Fi. A home may have up to four thermostats, and each controls its own zone. Devices added to one zone communicate with that zone's thermostat.

The thermostat requires a 2.4 GHz Wi-Fi network during setup. If the network name or password changes, pair the thermostat again.

## Power, installation and care

The thermostat must be wired to a gas boiler by a qualified installer. It is intended for indoor use between 0 and 40 degrees and is powered by mains through its wall plate.

Two AA backup batteries are fitted behind the thermostat's front cover. They preserve the clock and schedules during a power cut for up to 48 hours; they do not enable the thermostat to operate the heating without mains power. Replace them once a year, or when the display shows E-401.

The Radiator Valve uses two AA batteries, and the Room Sensor uses one CR2032 coin cell. Replace each device's batteries as required for that device.

Wipe the thermostat with a soft, dry cloth. Do not use sprays or cleaning products, and do not paint over it.
