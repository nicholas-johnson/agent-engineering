---
title: Use Thermostat Status in Home Automations
product: thermostat
type: integration
audience: customer
firmware: 4.1
updated: 2025-07-25
---

# Use Thermostat Status in Home Automations

## Overview

Compatible home automation systems can use the Dormouse Thermostat's room temperature, target temperature and heating state as inputs. This lets you build automations that respond to the conditions reported by the thermostat.

The thermostat controls its own heating according to its schedule, manual temperature changes, away mode and other settings. An automation that reads thermostat status does not replace those controls. The thermostat remains responsible for operating the heating.

The thermostat connects to Wi-Fi. A compatible system must be able to access thermostat status through its own Dormouse integration or connection method. Setup and available automation features depend on that system.

## Choose the status input

Use the status that matches what you want an automation to respond to:

| Input | What it represents |
|---|---|
| Room temperature | The temperature the thermostat reports for the room. |
| Target temperature | The temperature the thermostat is currently set to reach. |
| Heating state | Whether the thermostat is asking the boiler for heat. |

Room temperature and target temperature are different values. For example, the room may be cooler than the target while the thermostat is heating. The target can also change when you turn the dial, use the app, or when a new schedule period starts.

Heating state indicates a request for heat from the thermostat. It is not a measurement of the room temperature and does not indicate how warm the boiler or radiators are.

## Prepare your thermostat

Before creating an automation, check that the thermostat is paired and connected to Wi-Fi. If the display shows the Wi-Fi symbol with a cross, the thermostat is not connected to Wi-Fi.

You can check the firmware version on the thermostat: press the dial to open the menu, then choose Menu > About. This guide covers firmware 4.1.

If the thermostat cannot reach the Dormouse cloud, it shows E-110. The thermostat keeps running its schedules, but changes made in the app wait until it reconnects. Check that your router is connected to the internet. Automation availability may depend on the connection used by your compatible system.

## Connect a compatible system

Use the connection or integration instructions provided by your home automation system. The setup process and the status fields it supports are determined by that system.

When selecting thermostat information, choose the specific status input your automation needs: room temperature, target temperature or heating state. Do not assume that a system's general "temperature" field means the target temperature; check how that system identifies each value.

Some systems may refresh status periodically rather than immediately. Check the system's own documentation for its update timing and for how it handles a lost connection.

## Create an automation

In your compatible system, select the Dormouse Thermostat as a status source, then build a rule around one or more available inputs. For example, an automation could use room temperature as a condition, or use heating state to decide whether to run another compatible device.

Set clear conditions and actions in the automation system. If you use a temperature threshold, consider what should happen when the reported temperature moves back across that threshold. Where supported, configure separate start and stop conditions to avoid repeated switching near a single threshold.

Test the automation after saving it. Check that it responds to the intended status input and does not interfere with the thermostat's own heating controls.

## Understand changes in status

The target temperature can be set from 5 to 30 degrees in half-degree steps. A change made by hand lasts until the next schedule period starts. The target may therefore change when you adjust it manually or when the schedule advances.

The heating state can change as the thermostat responds to its target, schedule and other modes. Frost protection is always on: if the room falls below 5 degrees, the thermostat turns the heating on even when heating is off or away mode is on. The display shows a snowflake while frost protection is heating.

A boost heats at the boost temperature for one hour, unless cancelled sooner. Away mode maintains the away temperature until it is turned off. These thermostat functions can affect the status values available to automations.

## Keep heating controls clear

Use status-based automations as inputs for other compatible systems, not as a substitute for the thermostat's heating controls. Avoid actions that repeatedly override the target temperature or conflict with schedules, away mode or frost protection.

The thermostat can control its own heating only when mains power is available. Its backup batteries keep the clock and schedules for up to 48 hours during a power cut, but the thermostat cannot switch the heating on while mains power is off.

If the thermostat reports E-217, its temperature sensor is disconnected and it turns the heating off to be safe. Contact Dormouse support through the app at Help > Contact support.

## Check and maintain your setup

After changing a schedule, target temperature or away setting, confirm that your automation still uses the intended status and conditions. If it stops responding, check the thermostat's Wi-Fi connection, the compatible system's connection and the status field selected in the automation.

A thermostat restart can occur during a firmware update. Updates install automatically between 02:00 and 04:00 local time. While an update installs, the display shows UPDATING, the thermostat restarts and heating pauses until the update has finished. If an update fails, the display shows E-510 and the thermostat tries again the next night.

Keep automation rules simple and review them if you change how you use schedules, manual temperature settings or away mode.
