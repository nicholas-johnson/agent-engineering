---
title: Coordinate Radiator Valves with Smart-Home Routines
product: radiator valve
type: integration
audience: customer
firmware: 4.1
updated: 2026-06-27
---

# Coordinate Radiator Valves with Smart-Home Routines

## How Dormouse zones work

A Dormouse Radiator Valve joins a zone controlled by a Dormouse Thermostat. The valve heats its own radiator to its own temperature, while the thermostat controls the zone's heating schedule. A zone can have up to ten radiator valves.

Valves communicate with their zone's thermostat over a low-power 868 MHz radio link. Only the thermostat uses Wi-Fi. Keep the valve joined to its zone while coordinating it with routines in another smart-home system.

## Prepare the zone

Before creating a routine, check that the thermostat and valve are set up in Dormouse. To add a valve to a zone, use Settings > Home > Add a device. The thermostat, valve and any other devices should be assigned to the intended zone.

The Dormouse app and web dashboard let you manage most settings. Each thermostat controls its own zone and has its own schedule. A routine that refers to a particular valve should therefore be associated with the room or zone that valve serves.

## Include a valve in routines

In the smart-home system you use, select the Dormouse Radiator Valve as a device for the routine, if that system offers it. Choose the routine's trigger and the action you want it to perform using that system's available controls.

Keep the valve joined to its Dormouse zone. Do not remove it from the zone as a way to include it in a routine: the valve communicates with the zone's thermostat over the radio link, and the thermostat remains responsible for the zone's schedule.

The specific routine controls and available actions depend on the smart-home system. This guide does not define those controls.

## Keep the thermostat schedule in view

A Dormouse schedule sets target temperatures for periods throughout the day. Each day can have up to six periods. A period lasts until the next one starts. Make schedule changes in the app or web dashboard under Schedule.

A manual target-temperature change lasts until the next schedule period starts. When planning routines, account for that schedule behaviour so you understand how a temporary change relates to the next scheduled period. You can also use Away mode to keep the home at its configured away temperature until you turn it off.

## Understand device connections

The valve's connection to its zone thermostat uses low-power 868 MHz radio. It does not connect directly to Wi-Fi. The thermostat uses Wi-Fi to connect to Dormouse services and to the app or web dashboard.

If the thermostat cannot reach the Dormouse cloud, it keeps running its schedules. Changes made in the app wait until the thermostat reconnects. A crossed Wi-Fi symbol means the thermostat is not connected to Wi-Fi; error E-110 means it cannot reach the Dormouse cloud. Check that the router is connected to the internet if E-110 appears.

## Check the routine in use

After setting up a routine, check the valve and the thermostat's zone to confirm they are operating as intended. The thermostat display shows the room temperature and target temperature. When you turn its dial, the target temperature appears larger while you change it. The display dims after 20 seconds without a touch.

The thermostat's display symbols can help you understand its state: a flame means it is asking the boiler for heat, an upward arrow means a boost is running, and a house with an arrow means Away mode is on. The sunrise symbol indicates Warm Wake. Do not assume a routine changes the thermostat's schedule or removes the valve from its zone.

## Power and heating limits

Dormouse Radiator Valves run on two AA batteries, which last about two years. The thermostat is powered by mains through its wall plate. Its backup batteries keep the clock and schedules during a power cut for up to 48 hours, but the thermostat cannot switch the heating on while mains power is off.

Frost protection is always on and cannot be turned off. If the room falls below 5 degrees, the thermostat turns the heating on even when heating is off or Away mode is on. A routine should not be treated as a way to disable frost protection.

## Get help

If a routine does not appear to work as expected, first check that the valve remains joined to the intended zone and that the thermostat is connected to the network. Error codes are shown on the thermostat and in the app. For example, E-217 means the thermostat's temperature sensor is disconnected; the thermostat turns the heating off to be safe.

Contact Dormouse support in the app under Help > Contact support.
