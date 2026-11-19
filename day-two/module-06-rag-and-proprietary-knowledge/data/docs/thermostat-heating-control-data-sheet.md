---
title: Thermostat Heating Control Data Sheet
product: thermostat
type: specification
audience: customer
firmware: 4.1
updated: 2025-05-12
---

# Thermostat Heating Control Data Sheet

## Product

The Dormouse Thermostat controls a gas boiler and lets users set a target temperature from the thermostat, the Dormouse app or the web dashboard. Each thermostat controls its own zone, with its own schedule.

The thermostat must be wired to the boiler by a qualified installer. It is designed for indoor use between 0 and 40 degrees.

## Target temperature range

The target temperature can be set from 5 to 30 degrees, in half-degree steps. For example, a target can be set to 18.5 degrees.

To change the target at the thermostat, turn the dial. The display enlarges the target temperature while it is being changed. Press the dial to confirm. The target can also be changed in the app or web dashboard.

A manual temperature change lasts until the next schedule period starts. A schedule period has a start time and target temperature, and lasts until the next period begins.

## Display and heating indication

The round display shows the room temperature in large numbers and the target temperature underneath. After 20 seconds without a touch, the display dims.

The flame symbol indicates that the thermostat is asking the boiler for heat. Frost protection has its own snowflake symbol, shown while it is heating. The upward arrow indicates that a boost is running.

## Boost operation

Press the boost button below the dial to heat the home at the boost temperature for one hour. The display shows an upward arrow while the boost is running. Press the boost button again to cancel it.

The boost temperature is 21 degrees by default. It can be changed in Settings > Heating > Boost temperature.

## Frost protection

Frost protection helps prevent pipes from freezing. It is always on and cannot be turned off.

If the room temperature falls below 5 degrees, the thermostat turns the heating on, even if the heating is off or away mode is on. The display shows a snowflake while frost protection is heating.

## Operating with schedules and away mode

Schedules set target temperatures for periods throughout the day. Each day can have up to six periods. The thermostat follows the current schedule unless a manual temperature change or another heating mode applies.

Away mode keeps the home at the away temperature until it is turned off. The default away temperature is 16 degrees and can be changed in Settings > Away > Away temperature. Frost protection can still turn the heating on while away mode is active.

## Heating system compatibility

The Dormouse Thermostat is for use with a gas boiler: combi, system or conventional. A qualified installer must wire the thermostat to the boiler.

The thermostat connects to a 2.4 GHz Wi-Fi network. Dormouse Radiator Valves and Dormouse Room Sensors communicate with their zone's thermostat over a low-power 868 MHz radio link; they do not use Wi-Fi.

## Power and service conditions

The thermostat is powered by mains through its wall plate. Two AA backup batteries keep the clock and schedules during a power cut for up to 48 hours. While mains power is off, the thermostat cannot switch the heating on.

Replace the backup batteries once a year, or when the display shows E-401. When E-402 appears, the thermostat is running on backup batteries and cannot switch the heating on.

## Errors affecting heating

| Code | Meaning | Heating behaviour or action |
|---|---|---|
| E-217 | Temperature sensor disconnected | The thermostat turns the heating off to be safe. Contact Dormouse support through Help > Contact support in the app. |
| E-305 | Boiler not responding | Check that the boiler is switched on and its pressure is between 1 and 1.5 bar. Check the boiler's own display for a fault. |
| E-312 | Boiler reports a fault | Check the boiler's manual or contact a registered gas engineer. |
| E-402 | Mains power interrupted | The thermostat cannot switch the heating on while running on backup batteries. |
| E-510 | Firmware update failed | The thermostat keeps its current firmware and tries again the next night. |

## Specification summary

| Function | Specification |
|---|---|
| Target temperature range | 5 to 30 degrees |
| Temperature increments | Half-degree steps |
| Manual change duration | Until the next schedule period starts |
| Boost duration | One hour |
| Default boost temperature | 21 degrees; adjustable |
| Frost protection threshold | Below 5 degrees |
| Frost protection availability | Always on; cannot be turned off |
| Heating system | Gas boiler: combi, system or conventional |
| Thermostat power | Mains through wall plate |
| Backup power | Two AA batteries; clock and schedules maintained for up to 48 hours |
