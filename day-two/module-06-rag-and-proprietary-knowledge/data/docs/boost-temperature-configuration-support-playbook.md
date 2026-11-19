---
title: Boost Temperature Configuration Support Playbook
product: thermostat
type: internal
audience: internal
firmware: 4.1
updated: 2025-07-18
---

# Boost Temperature Configuration Support Playbook

## Purpose and scope

Use this playbook to help support staff explain how boost works on the Dormouse Thermostat with firmware 4.1, and guide customers through changing or cancelling a boost.

A boost heats the home at the configured boost temperature for one hour. The default boost temperature is 21 degrees. Customers can change it in the app, the web dashboard or on the thermostat settings where available. The menu path is Settings > Heating > Boost temperature.

This playbook covers expected behaviour and support checks. It does not cover general heating schedules, boiler faults or installation. If a customer reports an error code or a problem beyond the checks here, follow the relevant user-guide instructions and contact route.

## Explain boost operation

The boost button is below the thermostat dial. Pressing it starts a boost. While a boost is running, the display shows an upward arrow.

Explain that boost uses the boost temperature setting, not a separate temperature entered when starting the boost. Unless the customer has changed the setting, that temperature is 21 degrees.

A boost is temporary: it runs for one hour. It does not permanently change the customer's schedule or the configured boost temperature. A manual change to the target temperature has different behaviour: it lasts until the next schedule period starts.

Use clear wording such as: "Press the boost button to heat at your configured boost temperature for one hour. The upward arrow shows that boost is running."

Do not promise that the room will reach the boost temperature within the hour. The guide describes the target temperature and duration, not a guaranteed warm-up time.

## Start and confirm a boost

To start a boost, press the boost button below the dial. Check the display for the upward arrow, which indicates that a boost is running.

Customers can also use the Dormouse app or web dashboard for most settings, but the documented start action is pressing the thermostat's boost button. Do not give an unverified app or dashboard path for starting a boost.

If the customer says the boost did not start:

1. Ask them to check whether the upward arrow is visible.
2. If it is not visible, ask them to press the boost button once.
3. If an error code is shown, use the error-code guidance for that code rather than treating the issue as a boost configuration problem.
4. If the arrow is visible but the home is not heating, check whether the customer has a boiler-related error or other heating issue. Boost requests heat at its target; it does not override a boiler fault.

Do not ask the customer to change their schedule as a routine boost check. Boost is a separate, time-limited operation.

## Explain the one-hour duration

A boost runs for one hour. Set this expectation before troubleshooting: it is not an all-day setting and does not remain active until the customer manually turns it off.

The upward arrow indicates that the boost is running. The customer can use that symbol to distinguish an active boost from ordinary scheduled heating.

Avoid implying that the one-hour duration can be configured. The guide provides a configurable boost temperature, but it does not provide a setting to change the boost duration.

If the customer wants the home held at a temperature beyond the boost period, explain that a boost is temporary. They can set a target temperature by turning the dial or using the app; a hand-made target temperature change lasts until the next schedule period starts. For longer-term changes, schedules can be changed in the app or web dashboard.

## Cancel a boost

To cancel a running boost, press the boost button again. The upward arrow should no longer indicate that a boost is running.

If the customer is unsure whether the boost has been cancelled, have them check the display for the upward arrow. Do not tell them to factory reset, change the schedule or switch off frost protection to stop a boost. Frost protection is always on and cannot be turned off, but it is separate from boost.

If pressing the button again does not appear to cancel the boost:

1. Check whether the upward arrow is still displayed.
2. Ask the customer to try pressing the boost button once more, then check the display again.
3. Record any displayed error code and follow its troubleshooting instructions.
4. If the issue persists without an error code, contact support through the app under Help > Contact support.

Do not claim that cancelling a boost changes the configured boost temperature or the schedule.

## Change the boost temperature

The boost temperature is 21 degrees unless the customer changes it. It can be set in Settings > Heating > Boost temperature. The setting is available in the app, web dashboard and thermostat settings.

Guide the customer through the path using the interface they are using. Confirm that they are changing **Boost temperature**, rather than the general target temperature or away temperature.

The thermostat's target temperature can be set from 5 to 30 degrees in half-degree steps. Do not assume that the customer wants the boost temperature set to a particular value; let them choose their preferred setting in the available controls.

After changing the setting, explain that the new boost temperature is the temperature used for a boost. The one-hour duration remains unchanged. A boost that is already running is described in the guide as using the boost temperature, but it does not specify whether a temperature change takes effect immediately during an active boost. Do not promise when a change made mid-boost will take effect. If timing matters, have the customer cancel the current boost and start a new one after changing the setting.

## Distinguish boost from other heating behaviour

Use these distinctions when a customer describes heating that seems unexpected:

| Behaviour | What it means |
|---|---|
| Upward arrow | A boost is running. |
| Sunrise symbol | Warm Wake is heating ahead of a schedule period. |
| Flame | The thermostat is asking the boiler for heat. |
| Snowflake | Frost protection is heating because the room is below 5 degrees. |
| House with an arrow | Away mode is on. |

A flame means the thermostat is asking the boiler for heat; it does not by itself mean that a boost is active. Similarly, frost protection can heat even when heating is off or away mode is on. Do not diagnose either behaviour as a boost solely from seeing that the heating is on.

Do not explain how Warm Wake works, how early it starts or where its setting is. If a customer asks about Warm Wake, use approved Warm Wake guidance without adding those details.

## Escalation and internal handling

If the customer cannot change the setting, start a boost or cancel it after the checks above, direct them to Help > Contact support in the app. Include the firmware version, the interface used, what action was taken, whether the upward arrow appeared, and any error code shown. The firmware version can be checked on the thermostat at Menu > About.

For internal triage, support has three levels:

1. Level 1: app chat agents handle routine guidance and documented checks.
2. Level 2: product specialists investigate cases that remain unresolved after those checks.
3. Level 3: engineering handles issues requiring engineering investigation.

Escalate with the customer's observed behaviour and steps already tried. Do not represent internal triage levels as customer-facing product features.

## QA verification notes

When checking boost behaviour against the guide, verify that staff explanations state all of the following accurately:

- Pressing the boost button starts a boost.
- A running boost lasts one hour and uses the configured boost temperature.
- The default boost temperature is 21 degrees.
- The upward arrow indicates that a boost is running.
- Pressing the boost button again cancels it.
- Boost temperature is changed at Settings > Heating > Boost temperature.

Do not mark an explanation incorrect for omitting undocumented details such as the exact response time to a setting change during an active boost. Do not add claims about boost duration controls, app start controls, or guaranteed heating results.

Every release is tested against the manual test-script library before rollout. Internal firmware rollout proceeds to 1%, then 10%, then every thermostat over a week. These rollout details are for internal use and should not be included in customer-facing explanations.
