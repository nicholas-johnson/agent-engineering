---
title: Thermostat Zone Capacity and Device Compatibility
product: thermostat
type: specification
audience: customer
firmware: 4.1
updated: 2026-06-04
---

# Thermostat Zone Capacity and Device Compatibility

## Product overview

A Dormouse home can contain up to four Dormouse Thermostats. Each thermostat controls its own zone, with its own schedule. A zone can use its thermostat alone or include compatible Dormouse devices to measure or control conditions in other rooms.

The Dormouse Radiator Valve lets a radiator in a zone heat to its own temperature. A Dormouse Room Sensor measures temperature and humidity in another room of the zone. The thermostat is the Wi-Fi-connected device; valves and sensors communicate with their zone's thermostat over a low-power 868 MHz radio link.

## Capacity at a glance

| Device or capacity | Supported quantity |
|---|---:|
| Dormouse Thermostats per home | Up to 4 |
| Dormouse Radiator Valves per zone | Up to 10 |
| Dormouse Room Sensors per zone | Up to 3 |

Each thermostat controls one zone. The capacity for valves and sensors applies to each zone, not to the home as a whole.

## Dormouse Thermostat

The thermostat measures and controls the temperature in its zone. It connects to Wi-Fi and the Dormouse app and web dashboard. Schedules are set for each thermostat's zone.

The thermostat is powered from mains through its wall plate. Two AA backup batteries behind the front cover keep the clock and schedules during a power cut for up to 48 hours. The thermostat cannot switch the heating on while mains power is off.

The thermostat is 84 mm across and 24 mm deep, with a 2.4-inch round colour display. Its temperature accuracy is 0.3 degrees. It is intended for indoor use between 0 and 40 degrees.

## Dormouse Radiator Valve

Up to ten Dormouse Radiator Valves can join a zone. Each valve lets its radiator heat to its own temperature, while remaining part of that zone.

The valve fits M30 x 1.5 valve bodies. Adapters are included for other common valve types. It runs on two AA batteries, which typically last about two years.

A valve communicates with the thermostat for its zone over the low-power 868 MHz radio link. It does not use Wi-Fi.

## Dormouse Room Sensor

Up to three Dormouse Room Sensors can join a zone. A sensor measures temperature and humidity in another room of that zone.

Each sensor uses one CR2032 coin cell, which typically lasts about a year. It communicates with the zone's thermostat over the low-power 868 MHz radio link and does not use Wi-Fi.

A sensor adds measurements from another room to its zone. It does not create a separate zone or schedule.

## Zone configuration

A zone is controlled by one thermostat and can include up to ten radiator valves and up to three room sensors. Adding a device to a zone does not increase the number of zones; a home can have up to four zones when it has four thermostats.

For example, one thermostat can control the downstairs radiators and another can control the upstairs radiators. Valves can then be assigned to their respective zones, and sensors can measure conditions in other rooms within those zones.

To add a thermostat, sensor or valve, go to Settings > Home > Add a device.

## Compatibility and connectivity

The Dormouse Thermostat requires a 2.4 GHz Wi-Fi network. It cannot join a 5 GHz network. Wi-Fi connects the thermostat to the Dormouse service; radiator valves and room sensors use the 868 MHz radio link to communicate with their zone's thermostat.

A compatible setup therefore requires a thermostat for each zone, suitable Wi-Fi for the thermostat, and compatible Dormouse valves or sensors where needed. The thermostat must be wired to a gas boiler by a qualified installer. Supported boiler types are combi, system and conventional.

## Firmware and identification

This specification applies to the Dormouse Thermostat with firmware 4.1. To check the installed firmware, press the dial to open the menu and choose Menu > About.

Thermostat hardware revisions are A (2024), B (2025) and C (2026). Serial numbers begin DMA, DMB or DMC, corresponding to revisions A, B or C. Hardware revision does not change the stated home, zone or device capacities.

## Capacity planning

Plan the home by counting thermostats first: each thermostat controls one zone, and a home supports up to four thermostats. Then count the devices needed in each zone, observing the per-zone limits of ten valves and three sensors.

| Planning item | Limit |
|---|---:|
| Zones in a home | 4 |
| Valves in one zone | 10 |
| Sensors in one zone | 3 |

Devices must be added to the intended zone. A valve or sensor communicates with that zone's thermostat, so placement should be planned around the zone it will serve.
