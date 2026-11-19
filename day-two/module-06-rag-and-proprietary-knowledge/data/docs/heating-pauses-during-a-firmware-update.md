---
title: Heating Pauses During a Firmware Update
product: thermostat
type: troubleshooting
audience: customer
firmware: 4.1
updated: 2026-05-09
---

# Heating Pauses During a Firmware Update

The Dormouse Thermostat pauses heating while it installs a firmware update. This is expected: the thermostat restarts during the update and resumes heating when installation is finished. The process takes about two minutes.

## Confirm the thermostat is updating

Check the thermostat display. During an update, it shows **UPDATING**. Updates install automatically between 02:00 and 04:00 local time and cannot be postponed.

While **UPDATING** is displayed, the heating is paused. Wait for the installation and restart to finish before checking the heating again.

## Confirm heating resumes

After the update finishes, the thermostat restarts and should resume controlling the heating. Check that the display has returned to its usual temperature view, then allow the thermostat to follow its schedule or current target temperature.

If heating does not resume, check whether an error code appears on the thermostat display. The app shows the same code and can notify you about it.

## If the display shows E-510

E-510 means the firmware update failed. The thermostat keeps its current firmware and tries the update again the next night. Nothing needs to be done for this error.

The thermostat may pause heating again while a later update attempt installs. During installation, **UPDATING** appears on the display and heating resumes when the update finishes.

## If heating remains paused

If the thermostat is no longer showing **UPDATING** but heating has not resumed, check the display for an error code and follow the instructions for that code in the user guide. For example, E-217 means the temperature sensor is disconnected; the thermostat turns heating off to be safe, and Dormouse support should be contacted to arrange a replacement.

Contact support in the app under Help > Contact support if you cannot resolve the problem using the displayed error code.
