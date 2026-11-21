---
title: Automatic Firmware Update Window Support Playbook
product: thermostat
type: internal
audience: internal
firmware: 4.1
updated: 2025-08-22
---

# Automatic Firmware Update Window Support Playbook

## Purpose and scope

This internal playbook explains the Dormouse Thermostat's automatic firmware update window and what users can expect while an update installs. It covers the local-time schedule, heating pause, display indication, restart duration and handling of a failed update.

The thermostat installs updates automatically between 02:00 and 04:00 local time. Updates cannot be postponed. The installation itself takes about two minutes; the wider window is when an update may be installed, not a guarantee that it will begin at 02:00.

## What users see during an update

While an update installs, the thermostat display shows `UPDATING`. The thermostat then restarts. The display indication and restart are expected parts of the update process.

The installation takes about two minutes. During this time, heating pauses until the update has finished. Once installation and restart are complete, the thermostat resumes operation.

## Support handling

When a user reports that the thermostat is updating during the scheduled window, explain that updates install automatically between 02:00 and 04:00 local time and cannot be postponed. Confirm that `UPDATING` is the expected display indication and that heating pauses temporarily during installation.

Set expectations clearly: the update takes about two minutes, after which the thermostat restarts. Avoid describing the whole 02:00 to 04:00 window as the duration of the heating pause.

If the user reports that the display shows `E-510`, follow the failed-update guidance below. For other error codes, use the applicable entry in the thermostat error-code guidance.

## Failed updates: E-510

`E-510` means the firmware update failed. The thermostat keeps its current firmware and tries the update again the next night. The documented action is to wait for the retry; no user action is required.

When responding, explain that the thermostat has not switched to the failed update and will retry automatically. Do not suggest that the user postpone an update or manually install firmware.

## Escalation and response boundaries

For general product support, users can contact Dormouse in the app under Help > Contact support. When handling a firmware-window report, first distinguish an expected update from a reported error:

| Report | Guidance |
|---|---|
| `UPDATING` during installation | Explain the temporary heating pause, restart and approximate two-minute duration. |
| `E-510` | Explain that current firmware remains in place and the thermostat retries the next night. |
| Another displayed error code | Use the guidance for that specific code. |

Do not infer that an update has failed solely because the thermostat is in its automatic update window. Use the displayed code and the thermostat's documented behaviour to guide the response.

## QA and rollout notes

Firmware rollout proceeds in stages: 1% of thermostats, then 10%, then every thermostat over a week. Every release is tested against the manual test-script library before rollout.

These rollout stages are separate from the automatic installation window. The window remains 02:00 to 04:00 local time; it does not indicate which rollout stage a thermostat is in, nor does it change the user's ability to postpone an update.
