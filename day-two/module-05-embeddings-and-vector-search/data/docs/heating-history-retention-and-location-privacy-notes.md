---
title: Heating History Retention and Location Privacy Notes
product: all
type: internal
audience: internal
firmware: 4.1
updated: 2026-01-27
---

# Heating History Retention and Location Privacy Notes

## Purpose and scope

This internal note documents two data-handling behaviours relevant to heating history and geofencing:

- Heating history is kept for two years.
- Phone locations are not stored. The system stores only whether each household member is home or away.

These statements describe retention and location handling. They do not specify the detailed storage architecture, deletion process, access controls or audit procedures. Do not infer or promise details that are not documented here.

## Heating history retention

Heating history is kept for two years. The user guide describes monthly energy reports in the app's Energy tab. Each report shows the number of hours the heating was on each day, compares those figures with the previous month, and estimates gas use in kWh. The estimate depends on the boiler size entered under Settings > Home > Boiler size.

When explaining retention, distinguish heating history from the monthly report's presentation. The documented retention period applies to heating history; it does not define separate retention periods for report summaries, account data or other records.

Do not state that heating history is kept indefinitely, or that it is deleted immediately when a report is viewed, an account changes, or a thermostat is removed. Those behaviours are not specified here.

## Phone location handling

Geofencing uses the location of each household member's phone to determine whether that member is home or away. Phone locations are never stored. Only each member's home-or-away status is stored.

The user guide describes the geofencing rules: away mode turns on when every member who shares their location is more than 1 km from home, and turns off when the first of them comes back within 1 km. Each member chooses whether to share their location in the app. Geofencing for the whole home can be stopped at Settings > Away > Geofencing.

When describing this behaviour, do not say that the system stores a member's location history, coordinates or route. Also do not claim that it stores no location-related information at all: the home-or-away status is stored.

## User-facing wording

Use clear, bounded language:

- "Heating history is kept for two years."
- "Phone locations are not stored. The system stores only whether each member is home or away."

Keep the distinction between a phone's location and a member's status explicit. Avoid substituting "location data" for "phone locations" without explaining that home-or-away status is retained.

Do not describe the two-year period as applying to all account data or all app information. Do not imply that the status is anonymous, aggregated, or retained for a particular duration; none of those details are documented here.

## Geofencing context for support

If a member asks why away mode changed, explain the documented thresholds and sharing controls. Away mode turns on when all members who share their location are more than 1 km from home. It turns off when the first of them returns within 1 km. Members control their own location sharing in the app, and the owner or a member can stop geofencing for the whole home at Settings > Away > Geofencing.

Do not suggest that stored phone locations can be reviewed to reconstruct a journey. The documented stored value is home or away, not the phone's location.

## Energy-report context for support

Monthly energy reports arrive on the 1st of each month in the app's Energy tab. They show daily heating-on hours compared with the month before, plus an estimate of gas used in kWh. The estimate depends on the boiler size entered in Settings > Home > Boiler size.

If a user asks how long heating history is retained, state the documented two-year period. Do not infer from the monthly report format that only two months of history exist, or that reports themselves have a different retention period. The guide does not specify how older history is displayed or accessed.

## Boundaries and escalation

These notes cover only the documented retention and privacy statements. They do not define deletion timing, export options, backup retention, internal access, exact data fields, or the technical method used to determine home-or-away status.

If a case requires one of those details, do not invent an answer or make a broader privacy commitment. Record the question and use the established internal route for confirmation. For user support, contact is available in the app under Help > Contact support.
