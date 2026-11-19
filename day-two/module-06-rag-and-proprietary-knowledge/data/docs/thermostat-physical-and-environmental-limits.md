---
title: Thermostat Physical and Environmental Limits
product: thermostat
type: internal
audience: internal
firmware: 4.1
updated: 2025-03-25
---

# Thermostat Physical and Environmental Limits

## Scope

This internal engineering reference records the Dormouse Thermostat's physical dimensions, display size, temperature accuracy, indoor operating range and mains power arrangement. It applies to the thermostat hardware; it does not describe the operating limits of the Dormouse Radiator Valve or Dormouse Room Sensor.

The thermostat is intended for indoor use. Its stated operating temperature range is 0 to 40 degrees. These limits describe the thermostat itself and should not be treated as a specification for the boiler, heating system or other devices in the home.

## Dimensions

The thermostat is 84 mm across and 24 mm deep.

| Measurement | Specification |
|---|---:|
| Width across the thermostat | 84 mm |
| Depth | 24 mm |

These measurements are the documented physical dimensions of the thermostat. Do not infer additional mounting, clearance or wall-plate measurements from them.

## Display

The thermostat has a 2.4-inch round colour display. It presents room and target temperatures, along with status symbols and messages.

The display is part of the thermostat's front face. It dims after 20 seconds without a touch. Turning the dial enlarges the target temperature on the display while it is being changed.

## Temperature accuracy

The thermostat's temperature accuracy is 0.3 degrees. This is the stated accuracy specification for the thermostat's temperature measurement.

The thermostat controls heating using the room temperature it measures and the target temperature selected by the user or schedule. A temperature sensor disconnection is reported as E-217. In that condition, the thermostat turns the heating off to be safe; support should arrange a replacement.

## Indoor operating range

The thermostat is for indoor use between 0 and 40 degrees.

This documented range is an operating limit, not a recommended room-temperature setting. The user-adjustable target temperature is a separate control range: 5 to 30 degrees, in half-degree steps. Frost protection is also separate from the indoor operating range: it turns heating on if the room falls below 5 degrees and cannot be turned off.

Do not use the thermostat outside its stated indoor operating range. The available product information does not specify an outdoor operating range or a storage-temperature range.

## Mains power arrangement

The thermostat is powered by mains electricity through its wall plate. It cannot switch the heating on while mains power is off.

Two AA backup batteries, located behind the front cover, keep the clock and schedules during a power cut for up to 48 hours. They do not provide heating control while mains power is interrupted. E-402 indicates that the thermostat is running on backup batteries.

Replace the backup batteries once a year, or when E-401 appears. E-401 gives at least a month's warning before the batteries run out. The thermostat's batteries are backup power; they are not its normal operating power supply.

## Hardware identification

Three hardware revisions are documented:

| Revision | Year |
|---|---:|
| A | 2024 |
| B | 2025 |
| C | 2026 |

Thermostat serial numbers begin with DMA, DMB or DMC. These prefixes identify the corresponding hardware revision: DMA for revision A, DMB for revision B and DMC for revision C.

The current firmware is 4.1. Firmware version can be checked on the thermostat by pressing the dial to open the menu and choosing Menu > About. Hardware revision and firmware version are separate identifiers.

## Support and verification notes

Use the stated values in this document when recording thermostat physical or environmental specifications. Do not substitute the target-temperature range for the indoor operating range, or describe the backup batteries as the thermostat's mains supply.

For a product fault, direct the user to Help > Contact support in the app. Relevant display codes include E-217 for a disconnected temperature sensor, E-401 for low backup batteries and E-402 for interrupted mains power. The error-code guidance should be followed alongside the limits recorded here.
