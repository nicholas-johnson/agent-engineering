---
title: Moving or Recommissioning Dormouse Heating Devices
product: all
type: installation
audience: customer
firmware: 4.1
updated: 2025-07-26
---

# Moving or Recommissioning Dormouse Heating Devices

## Scope

Use this guide when removing Dormouse heating devices from service, moving them to another home, or preparing devices for setup in an intended home and zone. It covers the Dormouse Thermostat, Dormouse Radiator Valve and Dormouse Room Sensor.

The thermostat must be wired to a gas boiler by a qualified installer. This guide does not replace the boiler or wiring instructions supplied by the installer. Do not alter boiler wiring unless you are qualified to do so.

## Before you begin

Confirm which devices are being moved and which zone each device is intended to serve. A home can have up to four Dormouse Thermostats, each controlling its own zone and schedule. A zone can include one Dormouse Room Sensor and up to ten Dormouse Radiator Valves.

Check that the intended home has:

- A gas boiler of a supported type: combi, system or conventional.
- A 2.4 GHz Wi-Fi network for each thermostat. Thermostats cannot join a 5 GHz network.
- A Dormouse account and the Dormouse app on a phone running Android 12 or later, or iOS 17 or later.

Radiator Valves and Room Sensors communicate with their zone's thermostat over a low-power 868 MHz radio link. They do not use Wi-Fi; only the thermostat connects to Wi-Fi.

## Remove the thermostat from service

Before giving a thermostat to someone else or moving house without it, perform a factory reset. The reset removes the Wi-Fi details, schedules and link to the Dormouse account.

1. Ensure you have identified the thermostat being removed.
2. Hold the thermostat dial and boost button down together for 10 seconds.
3. Release them when the display shows RESET.
4. Wait for the thermostat to restart.

After restarting, the thermostat is ready to be paired again. A reset does not change the need for a qualified installer to wire the thermostat to the boiler.

## Prepare the thermostat for the intended home

Check that the thermostat is in the zone it is meant to control and that the boiler installation is complete. The thermostat is powered by mains through its wall plate, so confirm that the wall-plate installation and power supply have been handled appropriately by a qualified installer.

To pair the thermostat with the intended home's Wi-Fi and Dormouse account:

1. Hold the dial down for 5 seconds, until the display shows PAIR.
2. In the app, choose Add thermostat and follow the steps.
3. Keep the phone within 5 metres of the thermostat until the app says setup is finished.

Pairing must finish within 3 minutes of PAIR appearing. If it does not, the display shows E-104. Hold the dial for 5 seconds to start pairing again. Check that the phone remains within 5 metres throughout setup.

## Prepare Radiator Valves and Room Sensors

Assign each device to the intended zone during setup. A Room Sensor measures temperature and humidity in another room of its zone. Up to three Room Sensors can join a zone. Up to ten Radiator Valves can join a zone, with each valve heating its own radiator to its own temperature.

Use Settings > Home > Add a device to add a thermostat, sensor or valve. Make sure each device is added to the correct home and zone. A valve or sensor communicates with its zone's thermostat over the 868 MHz radio link; it does not need Wi-Fi credentials.

The Radiator Valve fits M30 x 1.5 valve bodies. Adapters are supplied for other common valve types. It uses two AA batteries, which last about two years. The Room Sensor uses one CR2032 coin cell, which lasts about a year.

## Check power and batteries

The thermostat has two AA backup batteries behind its front cover. These keep the clock and schedules during a power cut for up to 48 hours, but the thermostat cannot switch the heating on while mains power is off. Replace the batteries once a year, or when E-401 appears. E-401 indicates that the batteries should be replaced within a month.

To reach the thermostat batteries, pull the bottom of the front cover gently towards you. Use the correct battery type and fit batteries as directed by their markings.

If the thermostat displays E-402, mains power has been interrupted and it is running on backup batteries. Restore mains power through the appropriate installation work. Do not treat backup batteries as a way to operate the heating without mains power.

## Verify the commissioned setup

After pairing and adding devices, confirm that the thermostat is connected to the intended home's account and that each valve and sensor is assigned to the intended zone. Check that the thermostat can communicate with the Dormouse cloud and that the app displays the home's devices.

On the thermostat, Menu > Schedule shows today's periods. Schedules can be changed in the app or web dashboard, not on the thermostat. Each day can have up to six periods.

Check the thermostat display for errors. For example:

| Code | Meaning | Action |
|------|---------|--------|
| E-101 | Wi-Fi network not found | Check the router is on and provides a 2.4 GHz network. If the network name or password changed, pair the thermostat again. |
| E-104 | Pairing timed out | Start pairing again and keep the phone within 5 metres. |
| E-110 | Dormouse cloud cannot be reached | Check the router's internet connection. The thermostat continues its schedules; app changes wait until reconnection. |
| E-217 | Temperature sensor disconnected | Heating is turned off to be safe. Contact Dormouse support to arrange a replacement. |
| E-305 | Boiler not responding | Check that the boiler is on and its pressure is between 1 and 1.5 bar, then check the boiler display. |

For other error codes, follow the action listed in the Dormouse Thermostat User Guide.

## Handover and support

Explain to the household which thermostat serves each zone and how to use the app to manage devices and schedules. A home has one owner and up to eight members. Members can change temperatures, schedules and away mode; only the owner can add or remove devices and invite or remove members.

If the thermostat is being transferred to a different owner, make sure it has been factory reset before pairing it with the new account. For assistance, contact Dormouse support in the app under Help > Contact support.
