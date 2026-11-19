---
title: Firmware 4.1 Rollout Plan
product: thermostat
type: internal
audience: internal
firmware: 4.1
updated: 2025-12-12
---

# Firmware 4.1 Rollout Plan

## Purpose and scope

This internal plan documents the staged rollout of Dormouse Thermostat firmware 4.1. The rollout sequence is 1 percent of thermostats, then 10 percent, then every thermostat over a week.

Firmware updates install automatically between 02:00 and 04:00 local time and cannot be postponed by users. During installation, the display shows UPDATING, the thermostat restarts and heating pauses. Installation takes about two minutes.

Firmware 4.1 adds the option to change the boost temperature in Settings > Heating > Boost temperature. It also changes password reset links: they now work for 30 minutes and can only be used once.

## Rollout sequence

Progress through the rollout in three stages:

| Stage | Audience | Progression |
|---|---|---|
| Initial | 1 percent of thermostats | Begin the rollout and assess the initial cohort. |
| Expanded | 10 percent of thermostats | Expand after reviewing the initial cohort. |
| Complete | All thermostats | Roll out to every thermostat over a week. |

The rollout is staged by the proportion of thermostats receiving the update. Installation happens automatically during the local update window. Do not describe this process to users as an update they can schedule or postpone.

## Release content

Firmware 4.1 includes two changes relevant to this release:

- **Boost temperature:** The default remains 21 degrees unless the user changes it. Users can now change it in Settings > Heating > Boost temperature.
- **Password reset links:** A reset link works for 30 minutes and can be used once. If it expires, the user must request a new link.

The product guide is the source of truth for user-facing behaviour. Use its terminology and instructions when preparing support or release communications.

## User-visible update behaviour

During installation, the thermostat displays UPDATING, restarts and pauses heating until the update finishes. The process takes about two minutes. Updates install automatically between 02:00 and 04:00 local time and cannot be postponed.

If an update fails, the display shows E-510. The thermostat retains its current firmware and tries again the next night. Support should not advise users to reset the thermostat or take other recovery steps for E-510; the documented action is to let the thermostat retry.

## Monitoring and release checks

Review the available rollout information at each stage before expanding to the next audience. Use the following checks to structure the review:

1. Confirm the rollout has reached the intended stage: 1 percent, 10 percent or all thermostats.
2. Check reported update failures and E-510 cases.
3. Review user reports concerning the boost temperature setting and password reset links.
4. Confirm that reported behaviour matches the firmware 4.1 release content and the product guide.
5. Record findings and any decision about proceeding to the next stage.

This plan defines the staged sequence and product behaviour. It does not set numerical acceptance thresholds or specify a separate rollback procedure.

## Support playbook

For questions about changing the boost temperature, direct users to Settings > Heating > Boost temperature. Explain that the boost temperature is 21 degrees unless they change it, and that a boost runs for one hour when started with the boost button.

For an expired password reset link, ask the user to request a new one from Forgot password? on the sign-in screen. The link works for 30 minutes and can only be used once.

For E-510, explain that the thermostat keeps its current firmware and tries again the next night. For questions that need further investigation, users can contact support in the app under Help > Contact support.

Do not promise a particular installation time beyond the documented local window, or imply that users can postpone an update.

## QA and product references

Firmware releases are tested against the manual test-script library before rollout. Use that library for release testing; this plan does not reproduce its test cases.

For user-facing details, refer to the Dormouse Thermostat User Guide for firmware 4.1. In particular, use its descriptions of boost operation, password reset, update installation and E-510. Keep internal rollout mechanics separate from user instructions.

## Rollout completion

The rollout is complete when firmware 4.1 has been offered to all thermostats over the one-week rollout. Installation remains automatic and takes place during each thermostat's local update window.

Record the stage reached, the observations from each stage, and the completion status. User-facing documentation should describe the product's behaviour, not the internal 1 percent, 10 percent and all-thermostat sequence.
