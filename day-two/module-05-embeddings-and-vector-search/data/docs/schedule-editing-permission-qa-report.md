---
title: Schedule Editing Permission QA Report
product: thermostat
type: internal
audience: internal
firmware: 4.1
updated: 2026-04-02
---

# Schedule Editing Permission QA Report

## Report scope

This report records QA coverage for schedule viewing and editing in Dormouse Thermostat firmware 4.1. It verifies two product rules:

- Schedules can be viewed on the thermostat.
- Schedule changes can be made in the Dormouse app or web dashboard, but not on the thermostat.

It also verifies that a day's schedule supports up to six periods. Each period has a start time and target temperature, and lasts until the next period starts.

## Test environment

Run the checks with a thermostat paired to a Dormouse account and connected to a home. Use the app and web dashboard associated with that account. Confirm the thermostat is running firmware 4.1 by opening Menu > About.

Use a test day with fewer than six periods for the viewing and editing checks. For the period-limit checks, use a separate schedule or restore the test schedule after each case. Record the platform, firmware version and observed result for each run.

## Test cases

| ID | Test | Expected result |
|---|---|---|
| SCH-01 | Open Menu > Schedule on the thermostat. | The thermostat shows today's periods. |
| SCH-02 | Attempt to change a period on the thermostat. | The thermostat does not provide a way to change schedule periods. |
| SCH-03 | Open the Schedule tab in the app and choose a day. | The chosen day's periods can be edited. |
| SCH-04 | Open the Schedule tab in the web dashboard and choose a day. | The chosen day's periods can be edited. |
| SCH-05 | Create or retain six periods for a day. | The schedule supports six periods for that day. |
| SCH-06 | Attempt to add a seventh period to the same day. | No more than six periods are accepted for that day. |
| SCH-07 | Choose Copy day for a schedule. | The periods can be copied to other days. |

## Procedure: thermostat viewing and editing permission

1. Press the thermostat dial to open the menu.
2. Turn the dial to Schedule and press to choose it.
3. Check that today's schedule periods are displayed.
4. Try the available dial actions and inspect whether any action edits a period's start time or target temperature.
5. Record whether schedule information is viewable and whether schedule editing is unavailable on the thermostat.

**Pass criteria:** Today's periods are visible. The thermostat does not allow the user to change them. Do not count a manual target-temperature adjustment as schedule editing: a hand-made temperature change lasts until the next schedule period starts.

## Procedure: app and web dashboard editing

For each interface, open the Schedule tab and choose a day. Edit a period's start time or target temperature, then save or complete the interface's normal edit flow. Reopen the selected day and verify that the change is reflected there.

If the thermostat is available for observation, check its Menu > Schedule view after the change. It should show today's periods as applicable, but remain view-only. The ability to view periods on the thermostat does not grant schedule-editing permission there.

**Pass criteria:** Schedule changes can be made in both the app and web dashboard. The thermostat remains unable to change schedule periods.

## Procedure: period limit and schedule structure

On a selected day, configure periods with distinct start times and target temperatures. Verify that each period has a start time and a target temperature, and that its temperature applies until the next period starts.

Add periods until the day has six. Confirm all six are available in the schedule. Then attempt to add another period. Record the interface response and verify that the resulting schedule does not contain more than six periods for that day. Repeat as needed in the other editing interface.

**Pass criteria:** A day can have up to six periods, and no more than six are present after the seventh-period attempt. The test must not infer a minimum number of periods or a particular spacing between start times from this limit.

## Results and evidence

Record each test ID as Pass, Fail or Blocked. Attach evidence that identifies the platform and firmware version, such as a test log or screenshots of the relevant schedule view. For SCH-02, record the interaction used to confirm that the thermostat offers no schedule-editing control; do not treat the presence of the displayed periods as evidence of edit permission.

For a failure, capture the affected day and period count, the interface used, and the action that produced the result. Avoid including account credentials or personal household information in evidence.

## Known boundaries

This report covers schedule viewing and editing permission and the daily period limit. It does not define schedule time increments, validation rules for start times, schedule conflict handling, or behaviour during connectivity loss. Do not report those behaviours as requirements based on these tests alone.

On the thermostat, Menu > Schedule shows today's periods. Schedule changes are made in the app or web dashboard. Copy day is available when setting a schedule and applies the same periods to other days.

## Triage and release record

If schedule editing appears on the thermostat, or if a day can hold more than six periods, preserve the test evidence and report the issue through the internal QA process. If a schedule cannot be edited in the app or web dashboard, first record which interface and day were used and whether the change persists when the day is reopened.

For an external customer case, support can be contacted in the app under Help > Contact support. Do not use internal escalation details in customer-facing guidance.

Firmware rollout is staged: first 1%, then 10%, then every thermostat over a week. Every release is tested against the manual test-script library before rollout. Include this report's test results with the relevant release QA record.
