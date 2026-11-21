---
title: Household Notification Preferences Support Notes
product: app
type: internal
audience: internal
firmware: 4.1
updated: 2026-06-30
---

# Household Notification Preferences Support Notes

## Purpose and scope

This note explains the notifications available in the Dormouse app and how each household member manages their own choices. Notification preferences belong to individual members: changing your choices does not change what other members receive.

Members can choose notifications in Settings > Notifications. The available types are listed below. Notifications can also appear when the thermostat shows an error code; the app shows the same code as the thermostat.

## Available notification types

The app can notify a member when:

| Notification | What it reports |
|---|---|
| Thermostat error | The thermostat shows an error code. The app shows the same code. |
| Low backup batteries | The thermostat's backup batteries are low. |
| Heating while everyone is away | The heating has been on for 2 hours while everyone is away. |
| Firmware update installed | A firmware update has been installed. |
| Monthly energy report | The member's monthly energy report is ready. |

These notifications report product events or information. For example, an error notification does not replace the error code's troubleshooting instructions. Use the code shown in the app or on the thermostat to identify the issue and follow the relevant guidance in the user guide.

## Managing personal choices

Each household member chooses their own notifications in the app:

1. Sign in to the Dormouse app.
2. Open Settings > Notifications.
3. Choose the notifications you want to receive.

These choices apply to the signed-in member. Household sharing allows members to change temperature, schedules and away mode, but notification choices are managed separately by each member.

If a member wants to change which alerts they receive, they should update their own settings. Another member should not be expected to change them on their behalf.

## Household membership and access

A home has one owner and up to eight members. The owner can invite or remove members; members can manage their own notification choices. Invitations are sent from Settings > Household > Invite and work for 7 days.

If a person is no longer a member of the home, they should no longer be treated as an active household recipient. Only the owner can remove members. For a current member who cannot access the app, first direct them to sign in with their own account and open Settings > Notifications.

Two-step verification may ask for a 6-digit code when signing in on a new phone or browser. The code is sent by email or supplied by an authenticator app if one has been set up. It is configured at Settings > Account > Two-step verification.

## Error notifications

When the thermostat has an error, its display shows a code and the app shows the same code. The app can notify members about the error. Use the code to guide support and troubleshooting; do not infer a different fault from the notification alone.

Examples include E-401 for low backup batteries, E-110 when the thermostat cannot reach the Dormouse cloud, and E-510 when a firmware update fails. The appropriate action depends on the code. For instance, E-401 means the two AA backup batteries should be replaced within a month. E-510 requires no immediate action: the thermostat keeps its current firmware and tries again the next night.

If an error notification is received, ask the member to check the code in the app or on the thermostat and follow the user guide's instructions for that code. Contact support in the app under Help > Contact support when further assistance is needed.

## Away and heating notifications

The app can notify a member when the heating has been on for 2 hours while everyone is away. This notification describes that condition; it does not itself change the household's notification choices or replace away-mode controls.

Away mode can be turned on in the app or from the thermostat. Geofencing can turn away mode on and off based on the location of household members who share their location. Each member chooses whether to share their location in the app. Phone locations are never stored; only whether each member is home or away is stored.

Keep these functions distinct when helping members: notification preferences are set under Settings > Notifications, while geofencing is managed at Settings > Away > Geofencing.

## Firmware and energy notifications

A firmware notification reports that an update has been installed. Updates install automatically between 02:00 and 04:00 local time and cannot be postponed. During installation, the thermostat displays UPDATING, restarts and pauses heating until the update finishes, which takes about two minutes.

A monthly energy-report notification reports that the member's report is ready. Reports arrive on the 1st of each month in the app's Energy tab. They show daily heating hours compared with the previous month and an estimate of gas used in kWh. The estimate depends on the boiler size entered at Settings > Home > Boiler size.

## Support handling

When a member says they are not receiving a notification, confirm that they are signed in to their own account and have reviewed Settings > Notifications. Do not assume another member's selections apply to them. Identify the notification type and the event it covers before advising further.

For thermostat errors, ask for the displayed code and use the user guide's error-code instructions. For firmware questions, distinguish an installed-update notification from E-510, which indicates a failed update and an automatic retry the next night. For energy reports, check that the member is looking in the Energy tab and understands that the report arrives on the 1st.

If the issue remains unresolved, the member can contact Dormouse support in the app under Help > Contact support.
