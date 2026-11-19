---
title: Frost Protection Safety Behaviour QA Report
product: thermostat
type: internal
audience: internal
firmware: 4.1
updated: 2025-11-15
---

# Frost Protection Safety Behaviour QA Report

## Purpose

This report defines the expected behaviour and verification coverage for frost protection on the Dormouse Thermostat with firmware 4.1.

Frost protection is intended to help stop pipes freezing. It must activate the heating when the room temperature falls below 5 degrees, including when the heating is off or Away mode is on. Frost protection is always on and cannot be turned off.

## Scope

Verify the thermostat's response to room temperature in these states:

| Heating state | Away mode | Expected frost protection behaviour below 5 degrees |
|---|---|---|
| On | Off | Heating activates |
| Off | Off | Heating activates |
| On | On | Heating activates |
| Off | On | Heating activates |

The thermostat may also be paired with Dormouse Room Sensors or Dormouse Radiator Valves. This report covers the thermostat's frost protection behaviour; it does not define separate frost thresholds for those devices.

## Expected behaviour

When the room falls below 5 degrees, the thermostat turns the heating on even if the heating is off or Away mode is enabled. While frost protection is heating, the display shows the snowflake symbol.

Frost protection does not provide a user setting to disable it. A manual target temperature change lasts until the next schedule period starts, but must not prevent frost protection from activating below 5 degrees.

## Test setup

Use a correctly installed thermostat connected to a compatible gas boiler, with mains power available. Confirm that the thermostat is running firmware 4.1 using Menu > About.

For repeatable temperature testing, use a controlled environment and a calibrated reference thermometer positioned to represent the thermostat's room measurement. Allow the thermostat and reference thermometer to stabilise before recording results. Record the thermostat-reported temperature, the heating state, Away mode state, and display symbols for each test.

Keep the boiler available to respond to a heating demand. If the thermostat reports a boiler or sensor fault, resolve or record that condition before interpreting the frost protection result.

## Test procedure

Run the procedure for each combination of heating state and Away mode in the scope table.

1. Set the heating to the required on or off state.
2. Set Away mode to the required state.
3. Lower the room temperature in a controlled manner until the thermostat reports a temperature below 5 degrees.
4. Observe whether the thermostat requests heat and whether the display shows the snowflake symbol.
5. Record the result. Repeat each combination to check consistency.

Do not use a temperature reading of exactly 5 degrees as the below-threshold test condition. The documented activation condition is that the room falls below 5 degrees.

## Pass and fail criteria

A test passes when, below 5 degrees, the thermostat turns the heating on and shows the snowflake symbol, regardless of whether the heating was off or Away mode was on.

A test fails if the thermostat does not turn the heating on below 5 degrees in any tested state, if Away mode or heating-off state prevents activation, or if the snowflake symbol is absent while frost protection is heating.

Record the observed temperature and state combination for every failure. Do not infer a failure solely from the boiler not producing heat if the thermostat is requesting heat; check the boiler's status and any displayed error code.

## Fault handling and support notes

If E-217 is displayed, the temperature sensor is disconnected and the thermostat turns the heating off to be safe. Contact Dormouse support to arrange a replacement. This condition invalidates a frost protection activation test.

If E-305 is displayed, check that the boiler is switched on and its pressure is between 1 and 1.5 bar, then check the boiler's own display for a fault. If E-312 is displayed, the boiler reports a fault of its own; consult the boiler manual or contact a registered gas engineer.

For customer support, explain that frost protection is always on and cannot be turned off. Direct customers to Help > Contact support in the app when the thermostat appears not to follow the documented behaviour.

## QA record

For each run, retain:

- Thermostat firmware version and test date
- Heating state and Away mode state
- Thermostat-reported temperature below 5 degrees
- Whether heat was requested
- Whether the snowflake symbol appeared
- Any displayed error code and relevant boiler status
- Pass or fail result, with notes on test conditions

## Internal validation and escalation

Before rollout, every firmware release is tested against the manual test-script library. Frost protection coverage should include all four heating and Away mode combinations, plus confirmation that the snowflake symbol appears while frost protection is heating.

Escalate reproducible failures with the QA record and test conditions. Support has three levels: Level 1 app chat agents, Level 2 product specialists, and Level 3 engineering. Use the established support escalation process for cases that cannot be resolved at the first level.
