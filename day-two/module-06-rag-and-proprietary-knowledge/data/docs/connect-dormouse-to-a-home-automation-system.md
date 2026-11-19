---
title: Connect Dormouse to a Home Automation System
product: all
type: integration
audience: customer
firmware: 4.1
updated: 2025-04-07
---

# Connect Dormouse to a Home Automation System

## Overview

Dormouse Thermostats connect to your Wi-Fi network and Dormouse account. Dormouse Radiator Valves and Dormouse Room Sensors communicate with the thermostat for their zone over a low-power 868 MHz radio link; they do not use Wi-Fi.

This guide explains what to check before linking Dormouse devices with a home automation system, and how to prepare for setup. The Dormouse user guide does not specify a supported integration method or connection steps for third-party home automation systems. Check the instructions provided by your home automation system before starting. Do not assume that a device can be linked directly or that every Dormouse setting or device will be available.

## Check your Dormouse setup

Make sure your thermostat is paired with your Dormouse account and connected to your home Wi-Fi. Pairing requires a 2.4 GHz Wi-Fi network; the thermostat cannot join a 5 GHz network.

To check the thermostat's firmware, press the dial to open the menu, then choose Menu > About. This guide covers firmware 4.1. If the thermostat shows a different version, consult the instructions for that version before proceeding.

If you have more than one thermostat, note which zone each one controls. A home can have up to four thermostats, each with its own zone and schedule. Room Sensors and Radiator Valves join a zone and communicate with that zone's thermostat.

## Information to have ready

Before you begin, gather the following:

- The Dormouse account sign-in details used with the thermostat.
- The name and password of your 2.4 GHz Wi-Fi network.
- The home automation system's setup instructions and any account details it requires.
- The identity of each Dormouse thermostat and the zone it controls.
- The devices associated with each zone, such as Room Sensors and Radiator Valves.
- Access to the Dormouse app or web dashboard, if you need to check or change Dormouse settings.

If two-step verification is enabled for your Dormouse account, a 6-digit code may be requested when signing in on a new phone or browser. The code arrives by email, or through an authenticator app if you have set one up.

## Know how Dormouse devices connect

Only the Dormouse Thermostat uses Wi-Fi. A Radiator Valve or Room Sensor communicates with its zone's thermostat using a low-power 868 MHz radio link. Do not try to join these accessories directly to your Wi-Fi network.

A Dormouse Room Sensor measures temperature and humidity in another room of its zone. Up to three Room Sensors can join a zone. Up to ten Radiator Valves can join a zone; each valve heats its own radiator to its own temperature.

To add a thermostat, sensor or valve to your Dormouse home, use Settings > Home > Add a device in the app or web dashboard. Adding a device to Dormouse is separate from linking Dormouse with a home automation system.

## Prepare the home automation system

Use the home automation system's own instructions to check whether it supports Dormouse and what information it needs. The Dormouse user guide does not define a connection method, compatibility list, permissions, or the controls that another system can provide.

If the setup asks you to choose a Dormouse device, use the thermostat's zone and device details to identify the right one. If it asks for Dormouse account access, make sure you are using the account associated with the correct home. Do not share your password or verification code unless the system's instructions clearly require those details and you trust the system.

If the system cannot find Dormouse, check its instructions for network and account requirements. Do not change the thermostat's Wi-Fi details or reset it unless the relevant instructions tell you to do so.

## Check normal thermostat operation

Before linking systems, confirm that the thermostat displays the room temperature and target temperature, and that the heating responds to normal controls. You can change the target temperature by turning the dial or using the Dormouse app. A manual change lasts until the next schedule period starts.

Schedules are managed in the app or web dashboard. On the thermostat, Menu > Schedule shows today's periods, but schedules cannot be changed there. Away mode can be turned on in the app or by choosing Menu > Away on the thermostat.

These checks help distinguish an integration setup issue from a problem with the thermostat or the home's heating.

## If the connection does not work

Check the thermostat's display and the app for an error code:

| Code | Meaning | What to check |
|---|---|---|
| E-101 | Wi-Fi network not found | Check that the router is on and offers a 2.4 GHz network. If the network name or password changed, pair the thermostat again. |
| E-110 | Cannot reach the Dormouse cloud | Check that the router is connected to the internet. Schedules continue to run; app changes wait until the thermostat reconnects. |
| E-104 | Pairing timed out | Pairing must finish within 3 minutes. Hold the dial for 5 seconds to start again and keep your phone within 5 metres. |

If the thermostat is connected and working but the home automation system still cannot find it, follow that system's troubleshooting instructions. The Dormouse guide does not specify additional integration troubleshooting steps.

## Keep control of your Dormouse home

Household members can change the temperature, schedules and away mode. Only the home owner can add or remove devices, invite members or remove them. If the connection requires changes to the Dormouse home or its devices, make sure the person setting it up has the required access.

A factory reset removes Wi-Fi details, schedules and the link to your Dormouse account. It is not a routine connection step. Only reset the thermostat when you intend to remove its existing setup; hold the dial and boost button together for 10 seconds, until the display shows RESET.

For help with Dormouse devices, use Help > Contact support in the app.
