---
title: Firmware Release Test Gate
product: thermostat
type: internal
audience: internal
firmware: 4.1
updated: 2026-07-31
---

# Firmware Release Test Gate

## Purpose

This internal gate records the requirement that every Dormouse Thermostat firmware release passes the manual test-script library before rollout. A release must not enter rollout until its manual test results have been reviewed and recorded.

The gate applies to firmware releases for the Dormouse Thermostat. It covers pre-rollout verification and the rollout sequence. It does not replace the user guide or establish new product behaviour.

## Release under test

Record the release identifier and the firmware version being tested. The current firmware version is 4.1.

| Record | Value |
|---|---|
| Release identifier | |
| Firmware version | |
| Test start date | |
| Test completion date | |
| Test record owner | |
| Test result reviewer | |

Keep this information with the manual test results so the release decision can be traced to the firmware version tested.

## Test-script library requirement

Run the manual test-script library against each release before rollout. The library is the required test basis for the gate; passing a subset is not sufficient to satisfy the requirement.

Record the result for every script. Include the script identifier or title, the observed result, and whether it passed. For any failed or incomplete test, record the issue and its disposition. Do not record the release as having passed the gate while required manual tests remain unrun or unresolved.

## Recording test results

Use a result record that makes the outcome clear and reviewable.

| Script identifier or title | Result | Notes or issue reference |
|---|---|---|
| | Pass / Fail / Not run | |
| | Pass / Fail / Not run | |
| | Pass / Fail / Not run | |

Use concise notes to identify unexpected behaviour or relevant evidence. If a result is not a pass, explain what remains outstanding. A "Not run" result is not a pass.

## Gate decision

The release passes this gate only when the manual test-script library has been run and the results have been reviewed. Record the decision and its basis.

| Decision record | Value |
|---|---|
| Manual test library completed | Yes / No |
| Results reviewed | Yes / No |
| Open failures or incomplete tests | |
| Gate decision | Pass / Do not pass |
| Reviewer and date | |

A "Do not pass" decision means the release has not met the documented pre-rollout requirement. Keep the release out of rollout until the gate has been satisfied and the decision updated.

## Rollout sequence

After the release passes the manual test gate, firmware rollout proceeds in stages: 1%, then 10%, then every thermostat over a week. The test gate is a precondition to this rollout sequence; it does not replace or alter the stages.

Record the gate decision before rollout begins. Keep the release identifier and firmware version consistent across the test record and rollout record.

## Release record and traceability

Retain the test results and gate decision with the release record. The record should show which firmware version was tested, whether the full manual test-script library was completed, who reviewed the results, and whether the release passed.

If a release is updated or changed after testing, ensure the gate record identifies the version to which the test results apply. Do not use a pass decision for one version as evidence that a different version passed.

## Completion checklist

Before marking the gate complete, confirm:

- The release identifier and firmware version are recorded.
- The manual test-script library has been run for that release.
- Every script has a recorded result.
- Failures and incomplete tests are visible in the record.
- Results have been reviewed.
- The gate decision is explicit and dated.
- Rollout has not begun before a pass decision is recorded.
