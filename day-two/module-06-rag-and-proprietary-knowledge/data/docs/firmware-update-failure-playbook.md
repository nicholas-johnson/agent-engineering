---
title: Firmware Update Failure Playbook
product: thermostat
type: internal
audience: internal
firmware: 4.1
updated: 2026-10-03
---

# Firmware Update Failure Playbook

## Purpose and scope

This internal playbook covers E-510, the display code shown when a firmware update fails. It records what the thermostat does after a failure and the guidance for support and engineering teams.

The playbook applies to the Dormouse Thermostat on firmware 4.1. Its update process installs firmware automatically between 02:00 and 04:00 local time. The update cannot be postponed.

## Customer-visible behaviour

When an update fails, the thermostat displays E-510. The thermostat keeps running its current firmware; the failed update does not replace it. It automatically tries the update again the following night.

The app displays the same error code and can notify the member about it, depending on their notification settings. The thermostat may also show UPDATING and restart while an update is being installed. Installation takes about two minutes, during which heating pauses.

## Support handling

Tell the customer that E-510 means the firmware update failed, that their thermostat is still using its current firmware, and that it will try again the following night. The documented action is to wait for the automatic retry; no customer action is needed.

Do not advise a customer to factory-reset the thermostat or start pairing again for E-510. Those actions are not the documented response to this code.

If the customer needs further help, direct them to Help > Contact support in the app. Keep the case focused on the displayed code and whether it appears again after the next scheduled attempt.

## Diagnostic record

For each reported case, record:

- The displayed code: E-510.
- Whether the customer reports seeing UPDATING or a restart.
- Whether heating paused during installation.
- Whether E-510 appeared again after the following night's retry.
- Any other error code shown by the thermostat or app.

Do not infer a cause from E-510 alone. The documented meaning is that the firmware update failed; the thermostat retains its current firmware and retries the following night.

## Retry and follow-up

The retry is automatic and takes place the following night. Updates are installed between 02:00 and 04:00 local time and cannot be postponed. There is no documented manual retry control or alternate update window.

If E-510 remains after the next attempt, record that outcome and refer the case through the normal support process. The available product guidance does not specify further customer troubleshooting steps or a guaranteed resolution time.

## QA and release notes

Use the documented behaviour as the acceptance criterion for E-510:

1. A failed firmware update results in E-510 being shown.
2. The thermostat retains and continues to use its current firmware.
3. The thermostat attempts the update again the following night.
4. The customer-facing response does not claim that the update installed or that a specific cause has been identified.

Firmware 3.5 introduced the next-night retry for failed updates and changed E-401 so it appears a month before the backup batteries run out. These are separate behaviours: E-401 concerns low backup batteries, while E-510 concerns a failed firmware update.
