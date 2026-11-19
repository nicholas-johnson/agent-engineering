---
title: Energy Report Data QA Report
product: app
type: internal
audience: internal
firmware: 4.1
updated: 2025-01-23
---

# Energy Report Data QA Report

## Scope

This report records quality checks for the Dormouse monthly energy report. The report appears in the app's Energy tab on the 1st of each month. It contains daily heating hours, comparisons with the previous month and an estimate of gas used in kWh.

The estimate depends on the boiler size entered for the home. The input is managed at Settings > Home > Boiler size. The user guide does not define the calculation method, report-generation time, data correction policy or validation ranges for this input. Those details must not be inferred from the displayed estimate alone.

This document covers timing, daily heating-hour comparisons, gas-use estimates and boiler-size input. It is an internal QA reference; it does not add product behaviour beyond the documented features.

## Monthly report timing

Verify that a report is available in the app's Energy tab on the 1st of each month. Check the date boundary in the app rather than assuming a specific generation hour: the documented delivery date is the 1st, but no time of day is specified.

For each monthly cycle, record:

- The month the report describes.
- The date the report becomes available.
- Whether the report is visible in the Energy tab.
- Whether the report presents daily heating hours, a comparison with the month before and an estimated gas-use figure in kWh.

Do not treat a report generated or displayed later on the 1st as a failure solely because it was not present earlier that day. The documented requirement specifies the calendar date, not an availability time.

## Daily heating-hour comparisons

Check that the report presents heating hours for each day and compares those figures with the month before. Validate the daily values and their comparison against the underlying heating records available to the QA process.

Take care when comparing months of different lengths. A month may have fewer calendar days than the month before; do not report absent dates as missing data without confirming that the date belongs to the report period.

The guide does not specify rounding, display precision, treatment of partial days or how comparisons are expressed. Record the observed presentation and raise discrepancies for review rather than applying an undocumented expected format. Confirm that the report's month and the comparison month are labelled clearly enough to distinguish the two periods.

## Gas-use estimate

The report shows an estimate of gas used in kWh. The estimate depends on the size of the home's boiler. Treat it as an estimate, not a direct gas-meter reading.

For QA, check that:

- The report includes a gas-use estimate in kWh.
- The value is associated with the correct report period.
- Changing the boiler-size input is reflected in the estimate according to the implemented calculation.
- A missing or unrecognised input does not produce a value that is presented as a measured gas reading.

The user guide does not specify the estimation formula, its precision, expected ranges or how missing boiler-size data is handled. Do not define pass/fail thresholds for these items from the guide alone. Record the input and output used in a test, and refer any calculation-level expectation to the approved implementation specification.

## Boiler-size input

The boiler-size input is managed at Settings > Home > Boiler size. Confirm that the setting can be reached and that the saved value is available to the energy-report estimate.

The guide does not document supported units, allowed values, input validation, default values or behaviour when the boiler is replaced. QA must therefore verify these against the approved product requirements or implementation specification, not invent limits based on typical boilers.

When investigating a suspected mismatch, capture:

1. The boiler-size value shown in Settings > Home > Boiler size.
2. The report month and the gas-use estimate shown.
3. Whether the input was changed before the report was produced.
4. The relevant account and home context, following internal data-handling procedures.

Avoid concluding that an estimate is wrong solely because it differs from a household's metered usage: the report is explicitly an estimate and depends on boiler size.

## Data and period checks

For a report under test, verify that daily heating-hour figures belong to the intended month and that the comparison uses the month immediately before it. Check the start and end dates of both periods against the report labels and the underlying test data.

Heating history is kept for 2 years. When testing reports near the edge of that retention period, confirm that the source data required for the report remains available. Do not assume that data older than the documented retention period can be used to reproduce a report.

Keep test evidence sufficient to distinguish a report-period error from an input or estimate issue. At minimum, record the report month, comparison month, daily values reviewed, boiler-size input and displayed gas-use estimate. Follow internal data-handling procedures when storing account or home identifiers.

## Defect triage and reporting

Classify a report issue by the observable failure:

| Area | Example observation | Initial QA check |
|---|---|---|
| Timing | Report not visible on the 1st | Confirm the local calendar date and Energy tab. No availability hour is specified. |
| Daily hours | A day appears inconsistent | Compare the day and report period with the underlying heating records. |
| Comparison | Previous-month figures appear misaligned | Confirm both month labels and period boundaries. |
| Estimate | Gas-use value appears inconsistent | Record the boiler-size input, period and estimate; check the approved calculation specification. |
| Input | Boiler-size value is not retained or applied | Recheck the saved setting and reproduce with controlled test data. |

Include screenshots or other approved evidence where useful. Do not label an undocumented calculation rule or display precision as a product defect until the applicable requirement has been confirmed.

## Release and verification notes

Repeat the timing, daily comparison, estimate and boiler-size checks when changes affect energy reporting, heating-history processing or home settings. Use controlled test data where possible so that a report-period issue can be separated from a change in heating activity or boiler-size input.

The published user guide is the source of truth for documented user-facing behaviour: monthly reports arrive on the 1st in the Energy tab, show daily heating hours compared with the month before, and include an estimated gas-use figure in kWh that depends on boiler size. Any additional acceptance criteria must come from approved internal requirements.
