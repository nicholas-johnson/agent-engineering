---
title: Wired Thermostat and Wireless Zone Devices
product: all
type: installation
audience: customer
firmware: 4.1
updated: 2026-01-06
---

# Wired Thermostat and Wireless Zone Devices

## System overview

The Dormouse Thermostat is wired to the boiler by a qualified installer and connects to Wi-Fi. Dormouse Radiator Valves and Dormouse Room Sensors communicate with the thermostat in their zone over a low-power 868 MHz radio link. They do not use Wi-Fi.

A home can have up to four thermostats. Each thermostat controls its own zone and has its own schedule. A Room Sensor can join a zone to measure temperature and humidity in another room. Up to ten Radiator Valves can join a zone; each valve heats its radiator to its own temperature.

## Before installation

Confirm that the heating system uses a gas boiler: combi, system or conventional. The thermostat must be wired to the boiler by a qualified installer.

For Wi-Fi setup, the home needs a 2.4 GHz network. The thermostat cannot join a 5 GHz network. Pairing also requires the Dormouse app on a phone running Android 12 or later, or iOS 17 or later, and a Dormouse account.

Check that each device is suitable for its planned position. The thermostat is for indoor use between 0 and 40 degrees. Its dimensions are 84 mm across and 24 mm deep.

## Thermostat and boiler wiring

The thermostat is powered from mains through its wall plate and is wired to the boiler. Have a qualified installer complete the boiler wiring. The thermostat cannot switch the heating on if mains power is off, even though its backup batteries can keep the clock and schedules.

The thermostat display shows the room temperature and target temperature. It is accurate to 0.3 degrees. Turn the dial to change the target temperature, then press it to confirm. A manual temperature change lasts until the next schedule period starts.

## Wi-Fi and pairing

Pairing connects the thermostat to the home Wi-Fi network and the Dormouse account. Complete pairing within 3 minutes of the display showing PAIR.

1. Hold the thermostat dial down for 5 seconds, until the display shows PAIR.
2. In the Dormouse app, choose Add thermostat and follow the steps.
3. Keep the phone within 5 metres of the thermostat until the app says pairing has finished.

If pairing takes longer than 3 minutes, the display shows E-104. Hold the dial for 5 seconds to start pairing again.

## Wireless zone devices

Radiator Valves and Room Sensors communicate with their zone thermostat using a low-power 868 MHz radio link. Only the thermostat connects to Wi-Fi. Add a thermostat, sensor or valve in Settings > Home > Add a device.

A Radiator Valve fits M30 x 1.5 valve bodies. Adapters for other common valves are supplied in the box. Each valve uses two AA batteries, which last about two years.

A Room Sensor measures temperature and humidity. It uses one CR2032 coin cell, which lasts about a year. Up to three Room Sensors can join a zone.

## Zone planning and schedules

Plan each thermostat around the area it will control. Each zone has its own thermostat and schedule. For example, separate thermostats can control downstairs and upstairs heating.

Radiator Valves can be added to a zone so that each radiator in it heats to its own temperature. Room Sensors can be added to measure conditions in another room of the same zone. A zone supports up to ten Radiator Valves and up to three Room Sensors.

Set schedules in the Schedule tab of the app or web dashboard. Each day can have up to six periods, each with a start time and target temperature. On the thermostat, Menu > Schedule shows today's periods, but schedules can only be changed in the app or web dashboard.

## Power and backup batteries

The thermostat's two AA backup batteries are behind the front cover. They keep the clock and schedules during a power cut for up to 48 hours, but do not power the heating. Replace them once a year, or when the display shows E-401. To reach them, gently pull the bottom of the front cover towards you.

The thermostat shows E-402 when mains power is interrupted. It then runs on backup batteries and cannot switch the heating on. Radiator Valves and Room Sensors use their own batteries, separate from the thermostat's backup batteries.

## Checks and error codes

After installation, confirm that the thermostat is paired and connected to Wi-Fi, and that the zone devices have been added to the intended thermostat. Check the display and app for errors.

| Code | Meaning | Installer or user action |
|------|---------|--------------------------|
| E-101 | Wi-Fi network not found | Check the router is on and offers a 2.4 GHz network. If the network name or password changed, pair the thermostat again. |
| E-104 | Pairing timed out | Start pairing again and keep the phone within 5 metres. |
| E-110 | Cannot reach the Dormouse cloud | Check the router's internet connection. Schedules continue to run; app changes wait until the thermostat reconnects. |
| E-217 | Temperature sensor disconnected | The thermostat turns heating off to be safe. Contact Dormouse support to arrange a replacement. |
| E-305 | Boiler not responding | Check that the boiler is on and its pressure is between 1 and 1.5 bar. Check the boiler display for a fault. |
| E-401 | Backup batteries low | Replace the two AA batteries behind the thermostat's front cover within a month. |
| E-402 | Mains power interrupted | The thermostat keeps the clock and schedules for up to 48 hours, but cannot switch heating on. |

For support, use Help > Contact support in the app.
