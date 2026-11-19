---
title: Thermostat Temperature Measurement Specification
product: thermostat
type: specification
audience: customer
firmware: 4.1
updated: 2025-07-17
---

# Thermostat Temperature Measurement Specification

## Scope

This specification describes the temperature measurement accuracy and indoor operating range of the Dormouse Thermostat. It applies to the thermostat hardware running firmware 4.1.

The thermostat measures room temperature and displays it in large numbers. Its target temperature is shown underneath. This document covers the stated measurement accuracy and the conditions for indoor use; it does not specify temperature resolution, response time, calibration procedures or performance outside the operating range.

## Measurement accuracy

The thermostat's temperature measurement accuracy is 0.3 degrees.

This is the stated accuracy for the thermostat's room-temperature measurement. The guide does not define a separate accuracy specification for target temperature, or specify how accuracy varies across the operating range.

## Indoor operating range

The thermostat is for indoor use between 0 and 40 degrees. Use it within this range for its stated operating conditions.

This range describes the indoor temperatures for which the thermostat is intended. It is not a heating target range. The target temperature can be set from 5 to 30 degrees, in half-degree steps.

## Temperature display

The round display shows the measured room temperature in large numbers and the target temperature underneath. When the dial is turned, the target temperature becomes larger while it is being changed. The display dims after 20 seconds without a touch.

The room-temperature display presents the thermostat's measurement. The target temperature is the requested temperature, not a second measurement.

## Temperature control

Turn the dial, or use the app, to change the target temperature. A manual change lasts until the next schedule period starts. The thermostat can also heat at the boost temperature for one hour when a boost is started.

Frost protection is always on. If the room falls below 5 degrees, the thermostat turns the heating on, including when heating is off or away mode is on. The display shows a snowflake while frost protection is heating.

## Installation and operating context

The thermostat is powered by mains through its wall plate and must be wired to a gas boiler by a qualified installer. It is intended for indoor use within the specified 0 to 40 degree operating range.

The thermostat connects to Wi-Fi on a 2.4 GHz network. Wi-Fi is used for connectivity; the thermostat's stated temperature accuracy and indoor operating range are measurement and operating specifications.

## Specification summary

| Item | Specification |
|---|---|
| Product | Dormouse Thermostat |
| Temperature measurement accuracy | 0.3 degrees |
| Indoor operating range | 0 to 40 degrees |
| Room-temperature display | Large numbers on the round display |
| Target temperature range | 5 to 30 degrees |
| Target temperature increments | Half-degree steps |
| Power | Mains through the wall plate |

## Specification limits

This specification states the accuracy and indoor operating range provided for the Dormouse Thermostat. It does not provide additional limits or test conditions for measurement accuracy, nor does it describe behaviour outside the stated indoor operating range.
