---
title: Thermostat Dial and Menu Interaction Engineering Notes
product: thermostat
type: internal
audience: internal
firmware: 4.1
updated: 2025-04-07
---

# Thermostat Dial and Menu Interaction Engineering Notes

## Scope

These notes describe dial input, menu navigation, target-temperature adjustment and display dimming on the Dormouse Thermostat with firmware 4.1. They are intended for engineering, support and QA use.

Confirm the installed firmware before investigating behaviour: press the dial to open the menu, then choose Menu > About. The thermostat's menu has four items: Schedule, Away, Settings and About.

The thermostat works with the Dormouse app and web dashboard. Temperature changes can be made using the dial or the app; schedule periods can only be changed in the app or web dashboard.

## Display states and dial input

When showing the room temperature, the display presents that reading in large numbers and the target temperature underneath. Turning the dial changes the target temperature. While the target is being changed, the target-temperature digits become larger.

Pressing the dial has two documented functions:

- When the display shows the room temperature, pressing the dial opens the menu.
- When changing the target temperature, pressing the dial confirms the change.

Turn the dial to move between menu items. Press it to choose the selected item. The guide does not specify menu wraparound, the direction associated with each item, or a separate timeout for confirming a target-temperature change.

## Menu navigation

The menu contains Schedule, Away, Settings and About. The operator turns the dial to move through these items and presses it to select one.

On the thermostat, Menu > Schedule displays today's schedule periods. Schedule changes are made in the app or web dashboard, not on the thermostat. Menu > Away provides access to away mode. The display returns to its room-temperature presentation after interaction; after 20 seconds without a touch, it dims.

Do not infer additional menu items or dial shortcuts from these notes. For firmware identification, use Menu > About.

## Target-temperature adjustment

The target temperature can be set from 5 to 30 degrees in half-degree steps. The operator can adjust it by turning the dial or by using the app.

A manual change made by hand lasts until the next schedule period starts. This is distinct from changing a schedule: the thermostat itself shows today's periods but does not allow them to be edited.

During dial adjustment, the target temperature becomes larger on the display. Press the dial to confirm. The guide does not document a cancellation gesture, a confirmation prompt, or the behaviour of an unconfirmed adjustment after inactivity. Do not describe any of these as guaranteed firmware 4.1 behaviour without separate verification.

## Display dimming behaviour

After 20 seconds without a touch, the display dims. The guide does not specify whether dial rotation resets this timer, whether the display turns fully off, or the brightness level after dimming. Avoid treating those details as established behaviour.

For QA, verify the documented condition and timing: leave the display untouched for 20 seconds and check that it dims. Record the test conditions and observed timing. Do not confuse dimming with loss of power or an error state.

## Support investigation

When a user reports unexpected dial or menu behaviour:

1. Confirm firmware 4.1 in Menu > About.
2. Establish whether the display was showing room temperature, a target-temperature adjustment or a menu item.
3. Reproduce the reported dial turn or press and record the displayed state before and after input.
4. For a temperature change, check the requested value against the 5 to 30 degrees range and half-degree steps.
5. Check whether a schedule period started after the manual change; the manual setting lasts only until the next period starts.
6. For dimming reports, record the period without touch and whether the display dims after 20 seconds.

If the report concerns an error code, use the error-code guidance in the user guide. Do not attribute a dial or display symptom to a particular fault unless the evidence supports it.

## QA coverage

A firmware 4.1 interaction check should cover these documented behaviours:

| Test | Expected result |
|---|---|
| Turn the dial while room temperature is displayed | The target temperature changes and appears larger. |
| Set target-temperature values | Values are available from 5 to 30 degrees in half-degree steps. |
| Press the dial during adjustment | The change is confirmed. |
| Press the dial while room temperature is displayed | The menu opens. |
| Turn the dial in the menu | Selection moves between Schedule, Away, Settings and About. |
| Press a menu selection | The selected item opens. |
| Open Menu > Schedule | Today's schedule periods are shown; they are not editable there. |
| Leave the display untouched for 20 seconds | The display dims. |

Capture the firmware version, initial display state, input sequence and observed result for each test. The guide does not define exact dial sensitivity, input increments per rotation, menu ordering mechanics beyond the four listed items, or a precise tolerance around the 20-second dimming interval. Flag those observations for engineering review rather than treating them as documented requirements.

## Release and support references

Firmware 4.1 was released on 2026-08-17. Its documented changes include adjustable boost temperature at Settings > Heating > Boost temperature and password reset links that work for 30 minutes. Neither change alters the dial and menu behaviours described here.

For support escalation, contact support in the app under Help > Contact support. Internal support has three levels: level 1 app chat agents, level 2 product specialists and level 3 engineering. Firmware rollout proceeds to 1%, then 10%, then every thermostat over a week. Every release is tested against the manual test-script library before rollout.
