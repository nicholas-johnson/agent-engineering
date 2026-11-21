---
title: Away Mode and Geofencing QA Report
product: app
type: internal
audience: internal
firmware: 4.1
updated: 2025-05-27
---

# Away Mode and Geofencing QA Report

## Purpose and scope

This report validates the documented behaviour of away temperature configuration, household members' location-sharing choices, and geofencing's 1 km home and away thresholds.

Away mode keeps the home at the configured away temperature until it is turned off. The default away temperature is 16 degrees. Geofencing can turn away mode on or off automatically using the location of household members who share their location.

This report is limited to these behaviours. It does not define location-processing implementation, timing tolerances, or behaviour outside the documented conditions.

## Configuration validation

Verify the away temperature can be changed at Settings > Away > Away temperature. Confirm that the configured value is used while away mode is on, and that the default is 16 degrees before it is changed.

Verify that away mode can also be turned on manually by tapping Away in the app or by choosing Menu > Away on the thermostat. It remains on until turned off. Do not treat a manually enabled away mode as proof that geofencing has activated.

Record the selected away temperature and the control path used for each test. The guide does not specify a valid temperature range, input increments, or whether an already active away mode immediately adopts a changed temperature. Do not pass or fail those details against this report.

## Location-sharing choices

Each household member chooses whether to share their location in the app. Geofencing uses the location of members who share it.

Verify that a member can make their own sharing choice and that the choice is respected when evaluating geofencing. Do not assume that a member who has not chosen to share location counts as sharing, or infer additional behaviour for members who do not share.

To stop geofencing for the whole home, use Settings > Away > Geofencing. Validate this control separately from individual sharing choices. The guide does not specify the resulting away-mode state when geofencing is stopped; do not infer that disabling geofencing automatically turns away mode on or off.

## Threshold behaviour

The documented distance threshold is 1 km from home:

- Away mode turns on when every member who shares their location is more than 1 km from home.
- Away mode turns off when the first of those members comes back within 1 km of home.

Validate each condition using location cases clearly on either side of the threshold. The guide does not define a distance tolerance, treatment of a location exactly 1 km away, location-update frequency, or delay before a state change. Record those observations without treating unspecified timing or boundary behaviour as a documented requirement.

## Test procedure

1. Set a known away temperature at Settings > Away > Away temperature. Record the selected value.
2. Confirm that away mode can be enabled manually through the app and the thermostat menu.
3. In the app, set up test household members with their location-sharing choices recorded.
4. With every sharing member more than 1 km from home, check whether geofencing turns away mode on.
5. With away mode on, bring one sharing member within 1 km of home. Check whether geofencing turns away mode off.
6. Repeat with multiple sharing members. Confirm that one member returning within 1 km is sufficient to turn away mode off, and that the away condition requires every sharing member to be more than 1 km away.
7. Repeat relevant cases with a member not sharing location. Record the result; the guide does not specify all interactions involving non-sharing members.
8. Disable geofencing at Settings > Away > Geofencing and verify that the control is available. Record the resulting state without applying an undocumented expectation.

## Expected results and evidence

A pass requires the documented conditions to be observed:

| Check | Expected result |
|---|---|
| Default away temperature | 16 degrees |
| Away temperature configuration | Can be changed at Settings > Away > Away temperature |
| All sharing members more than 1 km away | Geofencing turns away mode on |
| First sharing member returns within 1 km | Geofencing turns away mode off |
| Individual location sharing | Each member chooses whether to share in the app |
| Whole-home geofencing control | Available at Settings > Away > Geofencing |

For each run, retain the configured away temperature, member sharing choices, relevant distances, observed away-mode state, test time, and control path. Keep results for boundary and timing cases separate from pass/fail findings for documented behaviour.

## Known limits and escalation

The user guide does not specify the exact behaviour at precisely 1 km, location precision, update intervals, transition delays, or every combination of sharing choices. These are unspecified, not confirmed defects. Avoid promising a particular result in support guidance unless it is covered by the documented conditions.

If a test contradicts a documented expected result, capture the test evidence and contact support in the app under Help > Contact support. Include the thermostat firmware version, available in Menu > About, along with the recorded sharing choices, distances, and away-mode state.
