---
title: Zone Device Capacity and Membership Notes
product: all
type: internal
audience: internal
firmware: 4.1
updated: 2026-05-03
---

# Zone Device Capacity and Membership Notes

## Purpose and scope

This internal reference records the supported device limits for a Dormouse home and its zones. Use it when reviewing a home configuration, checking a proposed device addition, or investigating reports that a device cannot join a zone.

The limits covered here are:

- Up to four Dormouse Thermostats in a home.
- Up to ten Dormouse Radiator Valves in a zone.
- Up to three Dormouse Room Sensors in a zone.

These limits apply to different levels: the thermostat limit is per home, while the valve and sensor limits are per zone. Do not treat the home-wide thermostat limit as a per-zone limit.

## Zone model

A home can contain multiple zones. Each Dormouse Thermostat controls its own zone, and each thermostat has its own schedule. For example, one zone can control downstairs radiators and another can control upstairs radiators.

A Room Sensor or Radiator Valve joins a zone. It does not create a separate zone. Each valve in a zone heats its own radiator to its own temperature. A Room Sensor measures temperature and humidity in another room of the zone.

## Supported capacity

| Device | Supported limit | Scope |
|---|---:|---|
| Dormouse Thermostat | 4 | Per home |
| Dormouse Radiator Valve | 10 | Per zone |
| Dormouse Room Sensor | 3 | Per zone |

For capacity checks, count thermostats across the whole home. Count valves and sensors separately for each zone. The stated limits do not mean that a zone can have ten devices total: it can support up to ten valves and up to three sensors, subject to the home's overall limit of four thermostats.

## Thermostat role and membership

Each Dormouse Thermostat controls one zone and runs that zone's schedule. A home may have up to four thermostats, so it may have up to four thermostat-controlled zones.

When checking a configuration, verify that each thermostat is associated with its intended zone. Keep zone membership clear when describing a setup: a thermostat controls its own zone; valves and sensors join a zone. Do not describe valves or sensors as controlling a zone.

The user-facing guide directs customers to add a thermostat through Settings > Home > Add a device. Only the home owner can add or remove devices.

## Radiator Valve role and membership

A Dormouse Radiator Valve joins a zone and controls the temperature of its own radiator. A zone supports up to ten valves. Each valve is counted against the limit for the zone it joins, not against a single home-wide valve limit.

The valve uses two AA batteries, which typically last about two years. It communicates with its zone's thermostat over a low-power 868 MHz radio link. It does not use Wi-Fi; only the thermostat uses Wi-Fi.

A valve fits M30 x 1.5 valve bodies. Adapters for other common valves are included in the box. These physical fitting details do not change the zone membership limit.

## Room Sensor role and membership

A Dormouse Room Sensor joins a zone to measure temperature and humidity in another room within that zone. A zone supports up to three Room Sensors. Count each sensor against the limit of the zone it joins.

The sensor is powered by one CR2032 coin cell, which typically lasts about a year. It communicates with its zone's thermostat over a low-power 868 MHz radio link. It does not use Wi-Fi; only the thermostat uses Wi-Fi.

Do not treat a Room Sensor as a separate thermostat or zone. Its documented role is to measure conditions in another room of the zone.

## Adding devices and checking capacity

The supported customer path for adding a thermostat, sensor or valve is Settings > Home > Add a device. Before advising on a configuration, establish which zone each valve and sensor is intended to join, then check the relevant counts.

Use this sequence:

1. Count all thermostats in the home. The supported maximum is four.
2. For each zone, count its valves. The supported maximum is ten per zone.
3. For each zone, count its Room Sensors. The supported maximum is three per zone.
4. Confirm that each device's intended role matches its membership: thermostat controls a zone; valve controls its own radiator; sensor measures temperature and humidity in another room of the zone.

The owner is the only household role that can add or remove devices. Members can change temperatures, schedules and away mode, but cannot manage device membership.

## Capacity triage notes

When a customer reports being unable to add a device, first distinguish a home-wide limit from a per-zone limit. Four thermostats is the maximum for the home. Ten valves and three Room Sensors are separate maximums for each zone.

If a zone is at the relevant limit, adding another device of that type would exceed the documented supported capacity. Check the intended zone before concluding that a home-wide limit has been reached; a valve or sensor count in one zone does not establish the count in another.

Do not infer additional capacity from the low-power radio link, a device's battery life, or its physical compatibility. Those details do not alter the stated membership limits.

## Internal handling boundaries

Use the limits in this note as the supported configuration record. The user guide confirms the home limit of four thermostats and the per-zone limits of ten valves and three Room Sensors. It also identifies the distinct roles of these devices and the owner's device-management permissions.

Do not present the per-zone valve or sensor limits as per-home totals. Do not state that a thermostat limit is per zone. Where a report does not identify the zone or device type involved, clarify those details before assessing whether the supported capacity has been reached.
