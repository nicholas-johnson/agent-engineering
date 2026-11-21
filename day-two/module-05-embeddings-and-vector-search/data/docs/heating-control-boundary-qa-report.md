---
title: Heating Control Boundary QA Report
product: thermostat
type: internal
audience: internal
firmware: 4.1
updated: 2026-01-24
---

# Heating Control Boundary QA Report

## Purpose and scope

This report records QA checks for the Dormouse Thermostat heating controls: the 5 to 30 degree target range, half-degree increments, how long a manual change lasts, boost operation and frost protection. It is an internal verification document for firmware 4.1.

The report distinguishes expected behaviour from checks that require an observed test result. No execution results are supplied here, so the cases below define expected outcomes and pass criteria rather than claiming that testing has passed.

## Product behaviour under test

The thermostat target temperature can be set from 5 to 30 degrees, in half-degree steps. A change made by hand lasts until the next schedule period starts.

Pressing the boost button starts heating at the configured boost temperature for one hour. The default boost temperature is 21 degrees; it can be changed in Settings > Heating > Boost temperature. An upward arrow appears while a boost is running. Pressing the boost button again cancels it.

Frost protection is always on and cannot be turned off. If the room falls below 5 degrees, the thermostat turns the heating on, including when heating is off or Away mode is on. A snowflake appears while frost protection is heating.

## Test setup and evidence

Use a thermostat running firmware 4.1. Confirm firmware from Menu > About. Use a functioning heating installation and a schedule with a clearly identifiable next period. Record the displayed room and target temperatures, relevant symbols, control actions and times.

For boundary tests, allow the thermostat to settle after each change. Verify temperature values at the endpoints and immediately inside them. Do not infer pass status from the expected behaviour alone: attach the test run's observations and outcome to this report.

## Target range and increment checks

| Test | Action | Expected result / pass criterion |
|---|---|---|
| Minimum boundary | Set target to 5 degrees | Target is accepted and displayed as 5 degrees. |
| Below minimum | Attempt to set a value below 5 degrees | No target below 5 degrees is accepted. |
| Maximum boundary | Set target to 30 degrees | Target is accepted and displayed as 30 degrees. |
| Above maximum | Attempt to set a value above 30 degrees | No target above 30 degrees is accepted. |
| Increment | Change the target through the available settings | Each selectable target is separated by 0.5 degrees; no other increment is offered. |
| Endpoint increments | Check the values next to each endpoint | The available values include 5, 5.5 and the final step to 30 degrees; no value exceeds the range. |

Repeat the checks using the thermostat dial and the app. The product guide states that either can be used to change the target.

## Manual-change duration

Set a schedule with a known upcoming period and change the target by hand before that period starts. Confirm that the thermostat uses the manually selected target until the next schedule period begins. At the period transition, confirm that the scheduled period takes effect.

Repeat with a manual change made near the transition, recording the change time and scheduled start time. The expected boundary is the start of the next period, not an assumed fixed duration. Do not report a manual change as lasting indefinitely or for a fixed number of hours.

On the thermostat, Menu > Schedule shows today's periods, but schedule changes are made in the app or web dashboard. Keep the test schedule unchanged during the run so the transition point is unambiguous.

## Boost operation

Use the configured boost temperature recorded before the test; it is 21 degrees unless changed in Settings > Heating > Boost temperature.

1. Press the boost button.
2. Confirm that a boost starts at the boost temperature and that the upward arrow appears.
3. Leave the boost running and record its start time and end time.
4. Confirm that it runs for one hour, then ends.
5. In a separate run, press the boost button again while the boost is active. Confirm that the boost is cancelled and the upward arrow no longer indicates a running boost.

Record whether a schedule transition occurs during the boost run. The guide specifies the boost duration and cancellation control, but does not state how a schedule transition interacts with an active boost; do not mark that interaction as a documented expectation without a separately approved requirement.

## Frost-protection checks

Test frost protection at the below-5-degrees boundary using a controlled, safe test setup. Confirm that when the room falls below 5 degrees, the thermostat turns the heating on and shows the snowflake while frost protection is heating.

Repeat with heating off and with Away mode on. In both cases, frost protection is expected to heat when the room falls below 5 degrees. Confirm that the protection remains available and that no control path turns it off: frost protection is always on and cannot be disabled.

Do not treat behaviour at exactly 5 degrees as a documented trigger. The guide specifies activation when the room falls below 5 degrees. Record the measured room temperature and observed heating request so boundary conclusions do not rely on rounded display values alone.

## Results recording and investigation

For each case, record:

- Thermostat serial prefix and hardware revision, if available.
- Firmware version, test date and control method.
- Initial schedule, target, heating state and Away state.
- Action and timestamp, displayed temperature and symbols.
- Expected result, observed result, pass/fail status and evidence.

If the thermostat does not meet a stated expectation, preserve the observations and contact support in the app under Help > Contact support. For an undocumented interaction, record the behaviour as an observation rather than a product requirement.

## QA release note

This report defines acceptance criteria from the firmware 4.1 user guide. It does not provide measured results or certify a particular device or build. A release or support decision should be based on completed test evidence for the cases above.
