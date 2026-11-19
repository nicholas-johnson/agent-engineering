---
title: Warm Wake Known Issue Register
product: thermostat
type: internal
audience: internal
firmware: 4.1
updated: 2026-06-19
---

# Warm Wake Known Issue Register

## Purpose and scope

This internal register provides a place to record and review reports involving the Warm Wake name or the sunrise display symbol. It does not define undocumented product behaviour or infer a cause from a report alone.

Warm Wake is a feature of firmware 4.1. The user guide states that the sunrise symbol appears while Warm Wake is heating ahead of the next schedule period. Use that statement as the limit of confirmed behaviour when documenting or assessing reports.

## Confirmed reference

| Item | Confirmed information |
|---|---|
| Feature name | Warm Wake |
| Display indicator | Sunrise symbol |
| Documented meaning | Warm Wake is heating ahead of the next schedule period |
| Firmware reference | The user guide covers firmware 4.1 |
| Firmware introduction | Warm Wake was introduced in firmware 4.0 |

Do not add assumptions about timing, configuration, eligibility, duration, or expected heating in other circumstances. If a report depends on any such detail, record it as unverified and seek engineering review.

## Register entries

Add one entry for each distinct report or group of reports that can reasonably be tracked together. Keep observations separate from interpretations. Do not label a report a defect unless the evidence and review support that classification.

| Field | Record |
|---|---|
| Register ID | Unique internal identifier |
| Date recorded | Date the report was added |
| Source | Internal team or support case reference; do not include customer contact details |
| Firmware | Version shown at Menu > About, if known |
| Hardware revision | A, B or C, if known |
| Serial prefix | DMA, DMB or DMC, if relevant |
| Reported item | Warm Wake name, sunrise symbol, or both |
| Observed behaviour | What was reported or directly observed, without interpretation |
| Context supplied | Relevant schedule or operating context, as reported |
| Evidence | Display description, app information, logs or other available evidence |
| Status | New, investigating, monitoring, resolved, or closed |
| Owner and review date | Responsible internal team and next review date |

## Recording reports

Capture the reporter's description as accurately as possible. Note whether the report concerns the feature name, the sunrise symbol, or both. If the symbol was observed, record what the display showed and any surrounding information available at the time.

Record firmware only when verified. The thermostat shows its firmware version at Menu > About. If the version is unknown, mark it unknown rather than inferring it from the report date. Record hardware revision or serial prefix only when available and relevant.

Keep the reported observation distinct from the confirmed reference above. For example, document "sunrise symbol reported on display" as an observation; do not turn it into a claim about why the symbol appeared.

## Triage and evidence

Triage establishes what is known, not what the product ought to do beyond documented behaviour. Check the report for enough detail to identify the firmware version, the item involved, and the observed circumstances. Request or collect further evidence through the applicable internal process where needed.

When comparing reports, group them only when their documented observations are materially similar. Note differences in firmware, hardware revision, or supplied context. Do not treat a missing sunrise symbol, a reported unexpected symbol, or a question about timing as proof of a defect: the available guide does not specify those expected cases.

If the report includes a thermostat error code, record it separately and use the relevant error-code guidance. Do not attribute an error to Warm Wake without evidence.

## Support handling

Support records should acknowledge the reported experience without promising undocumented behaviour or diagnosing a cause from the Warm Wake name or sunrise symbol alone. Use the confirmed reference in this register when describing what the symbol means.

If more information is needed, ask for observable details relevant to the report, including the firmware version and what appeared on the display. Do not tell a user that Warm Wake starts at a particular time, follows a particular setting, or should behave in a particular unlisted circumstance.

For product assistance, support is contacted in the app under Help > Contact support. Internal case references may be linked in the register; keep personal contact details out of the register.

## QA and engineering review

QA and engineering should assess reports against the documented reference and the available evidence. A test or investigation may explore an unverified condition, but its outcome must not be presented as documented product behaviour unless it is approved and reflected in the applicable product documentation.

Record reproduction steps and results without adding assumptions. If a report cannot be reproduced, retain the reported observation and mark the outcome accordingly. If evidence supports a product issue, document the evidence, affected versions if established, and the review decision.

Internal verification procedures may be used where applicable. Do not include internal rollout or test-process details in customer-facing replies.

## Status and closure

Use **New** for an unreviewed entry, **Investigating** while evidence is being assessed, **Monitoring** when further reports or observation are needed, **Resolved** when an agreed action is complete, and **Closed** when no further tracking is planned.

Before closing an entry, record the disposition and the basis for it. If the report remains unexplained, state that clearly rather than implying normal behaviour. Keep the entry available for trend review and link related reports by register ID.

## Change control

Review this register when the user guide, firmware reference, or approved engineering findings change. Update the confirmed reference only when supported by authoritative product documentation or an approved internal decision. Date each change and record its source.

Until such a change is made, the confirmed description remains limited to this: Warm Wake heats ahead of the next schedule period, and the sunrise symbol is shown while it is doing so.
