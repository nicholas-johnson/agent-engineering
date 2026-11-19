---
title: Thermostat, Valve and Sensor Zone Planning
product: all
type: installation
audience: customer
firmware: 4.1
updated: 2025-11-13
---

# Thermostat, Valve and Sensor Zone Planning

## Purpose and scope

This guide helps installers and confident customers plan a home with up to four Dormouse Thermostats. Each thermostat controls its own zone and has its own schedule. Dormouse Radiator Valves and Dormouse Room Sensors are assigned to a zone and communicate with that zone's thermostat.

Plan the zones and device assignments before adding equipment in the app or web dashboard. This makes it easier to check that each thermostat controls the intended area and that every valve and sensor is associated with the correct zone.

The thermostat must be wired to a compatible gas boiler by a qualified installer. This guide covers zone planning and device relationships; it does not provide boiler wiring instructions.

## Choose the zones

A zone is the area controlled by one Dormouse Thermostat. A home can have up to four thermostats, each controlling its own zone with its own schedule. For example, one zone may serve the downstairs radiators and another the upstairs radiators.

Decide which areas should have independent schedules and temperature control. Use a separate thermostat for each zone you want to control independently. Do not plan more than four thermostat-controlled zones in one home.

Before installation, record the intended area for each thermostat. Use clear names in your own installation notes so that the thermostat, valves and sensors can be checked against the plan.

| Planned zone | Thermostat location or area | Devices assigned to the zone |
|---|---|---|
| Zone 1 |  |  |
| Zone 2 |  |  |
| Zone 3 |  |  |
| Zone 4 |  |  |

## Plan thermostat locations and connections

Each thermostat controls its own zone and is powered by mains through its wall plate. It connects to the home's 2.4 GHz Wi-Fi network. The thermostat cannot join a 5 GHz network.

The thermostat is for indoor use between 0 and 40 degrees. Its temperature accuracy is 0.3 degrees. It measures 84 mm across and 24 mm deep, with a 2.4-inch round colour display.

The thermostat must be wired to a gas boiler by a qualified installer. Confirm that the boiler is a combi, system or conventional gas boiler. The thermostat cannot switch the heating on while mains power is off; its backup batteries preserve the clock and schedules for up to 48 hours during a power cut.

Plan access to the thermostat for operation and maintenance. The front cover needs to be accessible so the two AA backup batteries can be replaced.

## Assign radiator valves

A Dormouse Radiator Valve joins a zone and controls its own radiator to its own temperature. Plan each valve as part of the zone served by the corresponding thermostat. A zone can have up to ten Dormouse Radiator Valves.

The valve fits M30 x 1.5 valve bodies. Adapters for other common valve types are supplied in the box. Each valve runs on two AA batteries, which last about two years.

Valves communicate with their zone thermostat over a low-power 868 MHz radio link. They do not connect directly to Wi-Fi. When planning assignments, list each radiator and its intended zone so that valves are not associated with the wrong thermostat.

| Zone | Radiator or room | Valve planned | Valve body or adapter note |
|---|---|---|---|
|  |  |  |  |

Check the valve count for each zone before adding devices. Do not exceed ten valves in a zone.

## Assign room sensors

A Dormouse Room Sensor measures temperature and humidity in another room of a zone. Assign each sensor to the thermostat controlling that zone. A zone can have up to three Dormouse Room Sensors.

Each sensor uses one CR2032 coin cell, which lasts about a year. Sensors communicate with their zone thermostat over the same low-power 868 MHz radio link used by the Radiator Valve. Only the thermostat uses Wi-Fi.

Plan sensor locations according to the rooms whose temperature and humidity you want measured. Record the intended room and zone before installation, then check the assignment when adding the sensor.

| Zone | Sensor location | Intended measurement |
|---|---|---|
|  |  | Temperature and humidity |
|  |  | Temperature and humidity |
|  |  | Temperature and humidity |

Keep the sensor count to three or fewer per zone.

## Check radio and Wi-Fi requirements

The thermostat uses Wi-Fi to connect to the Dormouse service and requires a 2.4 GHz network. During pairing, keep the phone within 5 metres of the thermostat and complete pairing within 3 minutes of the display showing PAIR.

Radiator Valves and Room Sensors do not use Wi-Fi. They communicate with their assigned zone thermostat over a low-power 868 MHz radio link. Plan their assignments around the thermostat for the zone they serve, not around the home Wi-Fi network.

Before commissioning, confirm that the household Wi-Fi network offers 2.4 GHz. If the thermostat cannot find the network, the display may show E-101. Check that the router is on and offers a 2.4 GHz network. If the network name or password has changed, pair the thermostat again.

## Add and verify devices

Add thermostats, valves and sensors in the app or web dashboard under Settings > Home > Add a device. Follow the app's steps and use the zone plan to assign each device to the intended thermostat.

On the thermostat, Menu > Schedule shows today's periods, but schedules can only be changed in the app or web dashboard. Each thermostat has its own schedule for its zone.

After adding devices, compare the installed equipment with the plan:

1. Confirm that each thermostat represents the intended zone.
2. Confirm that every valve is assigned to the thermostat for its zone.
3. Confirm that every sensor is assigned to the thermostat for its zone.
4. Check that no zone has more than ten valves or three sensors.
5. Confirm that the home has no more than four thermostats.

If a thermostat shows E-110, it cannot reach the Dormouse cloud. Check that the router is connected to the internet. The thermostat continues to run its schedules; changes made in the app wait until it reconnects.

## Commissioning and handover

Record the final zone assignments and device counts for the household. Explain which thermostat controls each zone and where its valves and sensors are installed. Members of the home can change temperatures, schedules and away mode; only the owner can add or remove devices, invite members or remove them.

Remind the household that thermostat backup batteries preserve the clock and schedules for up to 48 hours during a power cut, but the thermostat cannot switch the heating on without mains power. Replace the thermostat's two AA backup batteries once a year, or when E-401 appears. Replace them within a month after that code appears.

For product support, use Help > Contact support in the app.
