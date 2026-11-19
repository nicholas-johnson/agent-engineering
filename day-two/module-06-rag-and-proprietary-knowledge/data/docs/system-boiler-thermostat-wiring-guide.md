---
title: System Boiler Thermostat Wiring Guide
product: thermostat
type: installation
audience: customer
firmware: 4.1
updated: 2026-06-05
---

# System Boiler Thermostat Wiring Guide

## Scope and compatibility

This guide describes installer checks and the wiring approach for connecting a Dormouse Thermostat to a system boiler. The thermostat is compatible with gas boilers of combi, system or conventional types. It must be wired to the boiler by a qualified installer.

This guide does not provide terminal numbers, wiring diagrams or boiler-specific connection instructions. Boiler terminal layouts vary. Use the boiler manufacturer's documentation to identify the correct thermostat-control connections, and have a qualified installer make and check the wiring.

The thermostat controls its own heating zone. A home can have up to four Dormouse Thermostats, each with its own zone and schedule. Check that the thermostat is intended to control the system boiler's relevant zone before installation.

## Checks before installation

Confirm that the boiler is a supported gas boiler and that its documentation identifies the connections for a thermostat. Check the boiler's own instructions for any requirements or restrictions on control wiring. Do not assume that terminals with similar names or positions have the same function across different boilers.

The thermostat is powered by mains through its wall plate. The boiler connection and thermostat power supply are separate installation considerations; follow the equipment instructions and applicable electrical requirements for both. Do not connect the thermostat until the qualified installer has identified the appropriate boiler control connections.

The thermostat is intended for indoor use between 0 and 40 degrees. Choose an installation position that is within this range and suitable for measuring the temperature of the zone it controls. The thermostat measures temperature to an accuracy of 0.3 degrees.

## Wiring approach

Use the boiler manufacturer's instructions to identify the boiler's thermostat-control input and the required method of connection. The qualified installer should verify that the boiler and thermostat are compatible at those connections before wiring.

Connect the thermostat to the boiler using the wiring arrangement specified for the identified control input. Do not infer connections from another boiler model or from the thermostat's appearance. If the boiler documentation does not clearly identify the correct connection, pause the installation and obtain guidance from the boiler manufacturer or a qualified heating professional.

The thermostat must be wired to the boiler by a qualified installer. Keep the boiler and thermostat installation instructions available during the work, and check the completed installation against both sets of instructions before restoring power or operating the heating.

## Wall plate and thermostat

The thermostat is 84 mm across and 24 mm deep. It has a 2.4-inch round colour display and is powered from the mains through its wall plate. Install the wall plate and connect the thermostat power supply according to the product installation instructions and applicable requirements.

The display shows the room temperature and the target temperature. The dial changes the target temperature; pressing it confirms a change or opens the menu when the display shows the room temperature. A manual temperature change lasts until the next schedule period starts.

The thermostat's backup batteries do not power the heating. Two AA batteries behind the front cover keep the clock and schedules during a power cut for up to 48 hours, but the thermostat cannot switch the heating on while mains power is off.

## Initial power-on and pairing

After wiring and completing the required installation checks, power the thermostat as directed by its installation instructions. To connect it to Wi-Fi and a Dormouse account, pair it with the Dormouse app:

1. Hold the dial down for 5 seconds, until the display shows PAIR.
2. In the app, choose Add thermostat and follow the steps.
3. Keep the phone within 5 metres of the thermostat until the app says pairing has finished.

Pairing must finish within 3 minutes of PAIR appearing. If it does not, the display shows E-104; start pairing again by holding the dial for 5 seconds.

The thermostat needs a 2.4 GHz Wi-Fi network. It cannot join a 5 GHz network. Valves and Room Sensors communicate with their zone's thermostat over a low-power 868 MHz radio link; only the thermostat uses Wi-Fi.

## Heating operation and checks

Turn the dial to set the target temperature, or change it in the app. The target range is 5 to 30 degrees in half-degree steps. The flame symbol means the thermostat is asking the boiler for heat. The snowflake means frost protection is heating the home.

Frost protection is always on and cannot be turned off. If the room falls below 5 degrees, the thermostat turns the heating on even if heating is off or away mode is on.

To check boiler operation, use the boiler's own indicators and instructions as well as the thermostat display. If the boiler does not respond, check that it is switched on and that its pressure is between 1 and 1.5 bar. Then check the boiler's own display for a fault.

## Errors and troubleshooting

The thermostat display and app show the same error code. Use the following guidance for common installation and operation issues:

| Code | Meaning | Action |
|---|---|---|
| E-101 | Wi-Fi network not found | Check that the router is on and offers a 2.4 GHz network. If the network name or password changed, pair the thermostat again. |
| E-104 | Pairing timed out | Start pairing again and keep the phone within 5 metres of the thermostat. |
| E-110 | Cannot reach the Dormouse cloud | Check the router's internet connection. The thermostat continues running schedules; app changes wait until it reconnects. |
| E-217 | Temperature sensor disconnected | The thermostat turns heating off to be safe. Contact Dormouse support to arrange a replacement. |
| E-305 | Boiler not responding | Check that the boiler is on, pressure is between 1 and 1.5 bar, and its display does not show a fault. |
| E-312 | Boiler reports a fault | Consult the boiler manual or call a registered gas engineer. |
| E-402 | Mains power interrupted | The thermostat runs on backup batteries and cannot switch the heating on. |

Contact Dormouse support in the app under Help > Contact support. For a boiler fault, follow the boiler manufacturer's instructions or contact a registered gas engineer.

## Installation handover

Before handing over the system, confirm that the thermostat is powered, paired and connected to the intended zone. Check that the boiler responds to a heating demand and that the thermostat display indicates when it is requesting heat. Explain that schedules are set in the app or web dashboard; Menu > Schedule on the thermostat shows today's periods but does not allow them to be changed.

Tell the household that E-401 means the two AA backup batteries should be replaced within a month. The batteries preserve the clock and schedules during a power cut, but do not enable heating without mains power.

For the thermostat's firmware version, press the dial to open the menu and choose Menu > About. The current firmware is 4.1.
