---
title: Firmware Update Observability and Retry Rollout Plan
product: all
type: internal
audience: internal
firmware: 4.1
updated: 2026-10-01
---

# Firmware Update Observability and Retry Rollout Plan

## Purpose and scope

This internal plan describes how to observe a firmware release as it moves from the initial 1% of thermostats to 10% and then to all thermostats over a week. It also covers checks for failed updates and the next-night retry behaviour.

The thermostat installs updates automatically between 02:00 and 04:00 local time. Updates cannot be postponed. During installation, the display shows UPDATING, the thermostat restarts, and heating pauses for about two minutes. If an update fails, the display shows E-510. The thermostat keeps its current firmware and tries again the next night.

The rollout process must account for those user-visible behaviours. Monitoring and support guidance should distinguish an update in progress from an update failure, and should not imply that heating continues during installation.

## Release readiness

Before rollout starts, confirm the release has been tested against the manual test-script library. Check that the release notes, support guidance and monitoring views describe the same expected behaviour and error codes.

Use the following readiness checks:

- Confirm the release identifier and the target firmware version.
- Verify that the thermostat displays UPDATING during installation and restarts when installation completes.
- Verify that heating pauses during installation and resumes after a successful update.
- Verify that an unsuccessful update leaves the thermostat on its current firmware and displays E-510.
- Verify that an E-510 thermostat retries the update on the next night.
- Confirm that support guidance directs users with update failures to the retry behaviour, without advising a manual postponement or an unsupported recovery procedure.

Do not begin the staged rollout until the checks are complete and the team can identify update progress, completion and E-510 outcomes.

## Rollout stages

Roll out each release in three stages: 1% of thermostats, then 10%, then every thermostat over a week. The stages provide checkpoints to review update outcomes before expanding the rollout.

| Stage | Target | Gate |
|---|---:|---|
| Initial | 1% of thermostats | Review installation, completion and failure signals before proceeding. |
| Expanded | 10% of thermostats | Review the same signals across the larger group before proceeding. |
| Broad rollout | Every thermostat over a week | Continue monitoring throughout the rollout and check next-night retries for failures. |

Treat each stage as a review point, not as an automatic transition. Confirm that the observed results are understood and that any E-510 cases have been accounted for before moving to the next stage. The broad rollout takes place over a week; retain visibility throughout that period rather than relying only on the first night.

## Monitoring during installation

Observe the update window of 02:00 to 04:00 local time. Monitor whether thermostats enter the expected installation state, show UPDATING, restart and report a completed update. A thermostat may be unavailable for about two minutes while it restarts; this is expected during installation.

Track outcomes by release and rollout stage. At a minimum, separate:

- updates that have not yet reached their scheduled installation window;
- installations in progress;
- successful completions;
- failures reported as E-510; and
- devices whose outcome is not yet known.

Do not count an installation in progress as a failure solely because the thermostat is temporarily restarting. Likewise, do not infer successful installation from the start of an update alone. Record the outcome after the restart.

## Stage review and expansion

At the end of each stage's observation period, review the available outcomes before increasing exposure. Confirm that successful completions are being reported, that failures are identified as E-510, and that unknown outcomes have been investigated or remain clearly tracked.

For the 1% and 10% stages, use the review to decide whether to proceed to the next stage. For the week-long broad rollout, continue to review progress as exposure expands and ensure that the rollout remains visible across the full period.

If results are unclear, hold at the current stage while the team checks the evidence. Do not treat missing outcome data as proof of success. Record the review decision and the outstanding items so engineering, QA and support use consistent status information.

## E-510 and next-night retry checks

E-510 means the firmware update failed. The thermostat keeps its current firmware and tries again the next night. No action is needed from the user to trigger that retry.

For each E-510 observation:

1. Record the release, rollout stage and affected thermostat.
2. Confirm that the thermostat remained on its current firmware after the failed attempt.
3. Check the following night's 02:00 to 04:00 local-time window for another update attempt.
4. Record whether the retry completed successfully or displayed E-510 again.
5. Keep unresolved cases visible for the next review.

Do not report the failed attempt as a completed update. A retry is an expected part of the documented behaviour, but it is not evidence of success until the outcome is observed. If another failure occurs, retain the case for engineering review and keep support messaging aligned with the thermostat's displayed code.

## Support and user-visible guidance

Support teams should describe the behaviour in the product's terms. During installation, the display shows UPDATING, the thermostat restarts, and heating pauses for about two minutes. If an update fails, the display shows E-510; the thermostat keeps its current firmware and tries again the next night.

Do not tell users that updates can be postponed. Do not describe E-510 as a loss of the current firmware: the thermostat retains its current firmware after a failed update. If a user reports E-510, support should capture the displayed code and the time observed, then check whether the next-night retry has taken place before treating the case as unresolved.

Escalate observations that do not match the documented behaviour for engineering review. Keep support notes factual: distinguish a reported display state from a confirmed update outcome.

## QA and rollout record

Maintain a release record that connects readiness, rollout exposure and observed outcomes. Include the release identifier, test-script completion, stage dates, update-window observations, completion and E-510 outcomes, next-night retry results, and the decision to expand or hold.

QA should use the manual test-script library before rollout and retain the results with the release record. Engineering and support should use the same release and stage identifiers when discussing an issue. This makes it possible to distinguish a test finding, a rollout observation and a user-reported symptom without conflating them.

Close the rollout record only after the week-long broad rollout has been reviewed and known E-510 cases have a recorded retry outcome or remain explicitly tracked.
